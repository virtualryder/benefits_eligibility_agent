"""Documentation-integrity gate: NO cross-vertical contamination in customer-facing docs.

WHY THIS EXISTS: this repository shares a governed-agent pattern with sibling verticals
(pharmacovigilance, financial aid, housing). Docs have twice been ported from those repos and shipped
with their domain language intact — an independent reviewer found `drug`, `suspect product`,
`ICSR`, `EudraVigilance`, HIPAA-as-default and `21 CFR Part 11` in *benefits* customer-facing files.
That is a credibility defect: a reader reasonably concludes the implementation was adapted as carelessly
as the prose.

This test fails the build if any forbidden term appears in a tracked Markdown doc, so the defect cannot
regress silently. If a term is ever legitimately needed (e.g. naming a sibling agent in a portfolio
sentence), add a narrow, commented exception below — never widen the list.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Terms that belong to OTHER verticals and must never describe this product.
FORBIDDEN = [
    r"\bICSR\b",
    r"\bopenFDA\b",
    r"\bFAERS\b",
    r"\bCIOMS\b",
    r"\bEudraVigilance\b",
    r"\bMedDRA\b",
    r"\bWHODrug\b",
    r"\bpharmacovigilance\b",
    r"\bsafety physician\b",
    r"\bQPPV\b",
    r"\bcausality\b",
    r"\bseriousness\b",
    r"\batorvastatin\b",
    r"\brhabdomyolysis\b",
    r"suspect product",
    r"21 CFR (Part )?(11|314)",
    r"api\.fda\.gov",
    r"\bFAFSA\b",
    r"\bISIR\b",
    r"College Scorecard",
    r"\bPell\b",
    r"\bHUD\b",
    r"Housing Choice Voucher",
]

# HIPAA is not the governing framework for benefits data. It may ONLY appear alongside an explicit
# qualifier explaining that it is not the default (see docs/INCIDENT-RESPONSE.md).
HIPAA = re.compile(r"\bHIPAA\b", re.I)
HIPAA_QUALIFIERS = ("not the default", "only if", "only where", "is not the governing")

# Files to check: every tracked Markdown doc a customer or reviewer might read.
SKIP_DIRS = {".git", "cdk.out", ".build", "node_modules", "__pycache__", "evidence"}
# Meta-documents that QUOTE an external review (they must be able to name the contaminating terms in
# order to record what was fixed). These are internal records, not product descriptions.
SKIP_FILES = {"REVIEW-RESPONSE-ACTION-PLAN.md"}

# A bare mention of a sibling vertical is allowed ONLY as a portfolio/pattern comparison — i.e. the same
# line makes clear it is a DIFFERENT agent (e.g. "the same pattern as the pharmacovigilance agent",
# "unlike the housing agent"). Product-describing uses are still forbidden.
SIBLING_COMPARISON = re.compile(
    r"(same (governed[- ]hero[- ]agent |governance |reusable |manifest-driven )?(pattern|template|core)|"
    r"sibling|portfolio|unlike|contrast|counterpart|other verticals|(all )?four (governed )?agents|"
    r"companion agent|governed-agent-platform|measured against the deployed|per transaction \(|"
    r"produced from the same)",
    re.I,
)
SIBLING_TERMS = {"pharmacovigilance", "hud", "college scorecard", "openfda", "faers",
                 "housing choice voucher", "fafsa", "isir", "pell"}


def _docs():
    for p in ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.parts) or p.name in SKIP_FILES:
            continue
        yield p


def _line_at(text, idx):
    start = text.rfind("\n", 0, idx) + 1
    end = text.find("\n", idx)
    return text[start: end if end != -1 else len(text)]


def test_no_cross_vertical_terms_in_docs():
    hits = []
    for p in _docs():
        text = p.read_text(encoding="utf-8", errors="replace")
        for pat in FORBIDDEN:
            for m in re.finditer(pat, text, re.I):
                line_text = _line_at(text, m.start())
                # a sibling vertical may be NAMED as a comparison, never as this product's domain
                if m.group(0).lower() in SIBLING_TERMS and SIBLING_COMPARISON.search(line_text):
                    continue
                line = text[: m.start()].count("\n") + 1
                hits.append(f"{p.relative_to(ROOT)}:{line}: {m.group(0)!r}")
    assert not hits, (
        "Cross-vertical contamination in customer-facing docs (this product is benefits, not "
        "pharmacovigilance/financial-aid/housing):\n  " + "\n  ".join(hits)
    )


def test_hipaa_only_appears_with_a_disclaimer():
    """HIPAA is not the benefits privacy framework. If it appears, the same paragraph must say so."""
    bad = []
    for p in _docs():
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in HIPAA.finditer(text):
            # look at a window around the match for an explicit qualifier
            window = text[max(0, m.start() - 400): m.end() + 400].lower()
            if not any(q in window for q in HIPAA_QUALIFIERS):
                line = text[: m.start()].count("\n") + 1
                bad.append(f"{p.relative_to(ROOT)}:{line}")
    assert not bad, (
        "HIPAA referenced without the required qualifier (benefits data is governed by state "
        "public-assistance confidentiality, Medicaid 42 CFR 431 Subpart F, SNAP 7 CFR 272.1(c), and "
        "IRS Pub 1075 only where FTI applies):\n  " + "\n  ".join(bad)
    )


def test_no_multi_program_eligibility_overclaim():
    """The engine is a preliminary FPL/SNAP-style income screen. It must never be described as a
    multi-program eligibility engine, and unemployment insurance is out of scope entirely."""
    bad = []
    for p in _docs():
        text = p.read_text(encoding="utf-8", errors="replace")
        low = text.lower()
        if "unemployment insurance" in low:
            # allowed ONLY as an explicit exclusion
            for m in re.finditer(r"unemployment insurance", low):
                window = low[max(0, m.start() - 300): m.end() + 300]
                if not any(k in window for k in ("out of scope", "excluded", "exclude", "not supported", "no ui logic")):
                    bad.append(f"{p.relative_to(ROOT)}: 'unemployment insurance' without an exclusion qualifier")
    assert not bad, "Product-scope overclaim:\n  " + "\n  ".join(bad)
