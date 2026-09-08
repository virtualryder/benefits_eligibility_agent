"""#234: account-level guardrail enforcement needs no Organization - and the claim that said it did.

The register recorded from 2026-09-05 that account-wide enforcement is "detective only until an
Organization exists" (PERIM-1b / R4-1). For SCPs that is still true. For GUARDRAILS it is not:

  "The account-enforced guardrail should automatically apply to both inputs and outputs" - set with
  "the PutEnforcedGuardrailConfiguration API in every region where you want to enforce the
  guardrail".
  https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-enforcements.html

That is PREVENTIVE, account-wide, and available on a standalone account. It does not stop a
principal from calling Bedrock - that is the SCP's job and still needs an Organization - but it does
mean any call that happens is guardrailed, including one from a caller who never went through the
gateway. The #168 capture trail detects those; this makes them safe as well as visible.

These tests pin the blast-radius refusal and the two documented traps, because the tool changes
EVERY Bedrock invocation in the account and is one typo from doing it by accident.
"""
import importlib.util
import os
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "aeg", os.path.join(ROOT, "scripts", "account_enforced_guardrail.py"))
aeg = importlib.util.module_from_spec(_spec)
sys.modules["aeg"] = aeg
_spec.loader.exec_module(aeg)


def test_apply_refuses_without_the_blast_radius_confirmation(capsys):
    rc = aeg.main(["--apply", "--guardrail-id", "gr-1", "--guardrail-version", "1"])
    assert rc == 2
    out = capsys.readouterr().out
    assert "REFUSED" in out
    assert "EVERY Bedrock model invocation in this AWS account" in out


def test_remove_refuses_without_the_blast_radius_confirmation(capsys):
    rc = aeg.main(["--remove", "--config-id", "cfg-1"])
    assert rc == 2
    assert "REFUSED" in capsys.readouterr().out


def test_a_draft_guardrail_version_is_refused(capsys):
    """AWS requires a numeric version; DRAFT is not an enforcement target."""
    rc = aeg.main(["--apply", "--guardrail-id", "gr-1", "--guardrail-version", "DRAFT",
                   "--i-understand-this-affects-every-bedrock-call-in-the-account"])
    assert rc == 2
    assert "DRAFT" in capsys.readouterr().out


def test_apply_requires_both_identifier_and_version(capsys):
    rc = aeg.main(["--apply", "--guardrail-id", "gr-1",
                   "--i-understand-this-affects-every-bedrock-call-in-the-account"])
    assert rc == 2
    assert "--guardrail-version" in capsys.readouterr().out


def test_apply_and_remove_are_mutually_exclusive(capsys):
    assert aeg.main(["--apply", "--remove"]) == 2


def test_the_boto3_operation_name_is_the_odd_one_aws_actually_ships():
    """Both obvious spellings do not exist; this pins the one that does.

    `list_enforced_guardrail_configurations` and `get_enforced_guardrail_configuration` were both
    tried against the live API first and both returned "operation does not exist". The real name is
    `list_enforced_guardrails_configuration` - guardrailS plural, configuration singular.
    """
    src = (ROOT / "scripts" / "account_enforced_guardrail.py").read_text(encoding="utf-8")
    assert "list_enforced_guardrails_configuration()" in src
    assert "put_enforced_guardrail_configuration(" in src
    assert "delete_enforced_guardrail_configuration(" in src
