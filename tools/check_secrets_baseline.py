#!/usr/bin/env python3
"""Compare a re-scanned secrets baseline against the committed one, ignoring the timestamp.

WHY THIS EXISTS
---------------
The Security workflow did:

    detect-secrets scan --baseline .secrets.baseline
    git diff --exit-code .secrets.baseline \
      || { echo "::error::new potential secret(s) not in .secrets.baseline"; exit 1; }

`detect-secrets scan` rewrites `generated_at` with the current UTC time on every run, so
`git diff --exit-code` ALWAYS reported a change and the step ALWAYS failed - with a message
accusing the developer of adding a secret. The gate could not pass even on an untouched tree.

A control that cries wolf on every run is worse than no control: it teaches people to skip the
step. This compares what the baseline is FOR - the findings - and says precisely what is new.

    python tools/check_secrets_baseline.py <committed.json> <rescanned.json>
"""
import io
import json
import sys

IGNORED_TOP_LEVEL = {"generated_at"}


def _findings(doc):
    """{(filename, type, hashed_secret)} - line numbers move when a file is edited above the
    finding, and a moved line is not a new secret."""
    out = set()
    for filename, entries in (doc.get("results") or {}).items():
        for e in entries:
            out.add((filename.replace("\\", "/"), e.get("type"), e.get("hashed_secret")))
    return out


def main(argv):
    if len(argv) != 3:
        print(__doc__.strip())
        return 2
    committed = json.load(io.open(argv[1], encoding="utf-8"))
    rescanned = json.load(io.open(argv[2], encoding="utf-8"))

    new = _findings(rescanned) - _findings(committed)
    gone = _findings(committed) - _findings(rescanned)

    for key in sorted(set(committed) | set(rescanned)):
        if key in IGNORED_TOP_LEVEL or key == "results":
            continue
        if committed.get(key) != rescanned.get(key):
            print("::error::secrets baseline config changed (%s) - re-baseline deliberately" % key)
            return 1

    if new:
        print("::error::%d potential secret(s) not in .secrets.baseline:" % len(new))
        for filename, kind, h in sorted(new):
            print("  %s  [%s]  %s" % (filename, kind, h))
        print("Review each one. If they are fixtures rather than credentials, re-baseline with")
        print("`detect-secrets scan --baseline .secrets.baseline` and say WHY in the commit.")
        return 1

    if gone:
        print("note: %d baseline entry/entries no longer found (file deleted or secret removed)."
              % len(gone))
    print("secrets baseline: no new findings (%d tracked)" % len(_findings(committed)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
