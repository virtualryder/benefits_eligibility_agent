"""WorkflowStack (Benefits) — the DETERMINISTIC workflow controller (P0-2) + the human sign-off gate.

The regulated pipeline is a Step Functions STANDARD state machine — the model no longer decides the
compliance sequence. Every transition is gated on machine-verifiable evidence via the workflow_guards
Lambda; a failed guard routes to ManualReview (NEEDS_REVIEW), never onward:

  RECEIVED → Extract → [extracted?] → Mask → [deidentified?] → AssessEligibility → [rules_executed?]
    → CheckAdverseNotice → [adverse change carries advance notice?] → (hold → AdverseNoticeHold)
    → DraftNotice → AuditIntent → HumanSignoff (waitForTaskToken, SoD) → COMMITTED

AdverseNoticeHold is a TERMINAL DUE-PROCESS state, not an error: an adverse redetermination (a
reduction or termination of benefits) that lacks the required timely advance notice HOLDS — Goldberg v.
Kelly is enforced by the platform, not the model. A non-adverse change (a new application, a favorable
change) passes the gate. The redetermination classification is supplied to the execution as
`$.redetermination` (the `redetermine` tool's output; a new application passes `{"change_type":"NEW"}`).

R3-2 ZERO-PII STATE: the execution is started with {case_id, requester, case_ref, redetermination} — the
raw application NEVER enters Step Functions state (it lives in the encrypted case store; the intake API
/ scripts call the ingest-application Lambda first). The drafter returns an opaque notice_ref, so the
drafted notice text never enters state either. The strict canary holds the controller to zero content
in execution history.
"""
import aws_cdk as cdk
from aws_cdk import (aws_kms as kms, aws_logs as logs, aws_stepfunctions as sfn,
                     aws_stepfunctions_tasks as tasks)
from constructs import Construct


class WorkflowStack(cdk.Stack):
    def __init__(self, scope: Construct, cid: str, *, prefix: str, compute, data,
                 multitenant: bool = False, **kw):
        super().__init__(scope, cid, **kw)

        # Hybrid multi-tenant (governed-core 1.6.0): the Step Functions hop has NO gateway interceptor,
        # so the acting tenant travels in the execution input as the HMAC-SIGNED pair
        # (tenancy.TENANT_FIELD / TENANT_SIG_FIELD, minted by the tenanted caller that started the
        # execution) and is threaded into EVERY Lambda payload; each Lambda re-verifies the signature
        # before routing to that tenant's ledger / vault / approvals register. In multi-tenant mode an
        # execution started WITHOUT the pair fails at the first state (States.Runtime on the missing
        # path) — fail-closed, never a silent write to the base stores. Silo: nothing is threaded.
        tenant_fields = ({"__aegis_tenant.$": "$.__aegis_tenant",
                          "__aegis_tenant_sig.$": "$.__aegis_tenant_sig"} if multitenant else {})

        def invoke(name, fn, payload, result_path):
            return tasks.LambdaInvoke(self, name, lambda_function=fn,
                                      payload=sfn.TaskInput.from_object({**payload, **tenant_fields}),
                                      result_selector={"out.$": "$.Payload"},
                                      result_path=result_path)

        def guard(name, guard_name, payload):
            return tasks.LambdaInvoke(self, name, lambda_function=compute.guards,
                                      payload=sfn.TaskInput.from_object(
                                          {"guard": guard_name, **payload, **tenant_fields}),
                                      result_selector={"ok.$": "$.Payload.ok",
                                                       "reason.$": "$.Payload.reason"},
                                      result_path=f"$.guards.{guard_name}")

        manual_review = sfn.Succeed(self, "ManualReview",
                                    comment="Fail-closed: evidence missing/unverified -> NEEDS_REVIEW "
                                            "for a caseworker; no automated outcome.")

        # R3-2: extract runs off an opaque case_ref (raw application never in execution state).
        extract = invoke("Extract", compute.intake, {"case_ref.$": "$.case_ref"}, "$.extract")
        g_extracted = guard("GuardExtracted", "extracted", {"fields.$": "$.extract.out.fields"})

        mask = invoke("MaskPii", compute.mask, {"case_ref.$": "$.case_ref"}, "$.mask")
        g_deid = guard("GuardDeidentified", "deidentified",
                       {"sanitized_ref.$": "$.mask.out.sanitized_ref"})

        assess = invoke("AssessEligibility", compute.assess,
                        {"household_size.$": "$.extract.out.fields.household_size",
                         "monthly_income.$": "$.extract.out.fields.monthly_income",
                         "liquid_resources.$": "$.extract.out.fields.liquid_resources",
                         "categorical_eligibility.$": "$.extract.out.fields.categorical_eligibility",
                         "deidentified": True, "sanitized_ref.$": "$.mask.out.sanitized_ref"},
                        "$.assessment")
        g_rules = guard("GuardRulesExecuted", "rules_executed", {"assessment.$": "$.assessment.out"})

        # DUE PROCESS gate (Goldberg v. Kelly): an adverse redetermination without advance notice HOLDS.
        g_adverse = guard("CheckAdverseNotice", "adverse_notice",
                          {"redetermination.$": "$.redetermination"})
        adverse_hold = sfn.Succeed(
            self, "AdverseNoticeHold",
            comment="TERMINAL DUE-PROCESS HOLD (not an error): an adverse redetermination (benefit "
                    "reduced/terminated) lacks the required timely advance notice; the caseworker issues "
                    "notice with fair-hearing rights before any adverse action (Goldberg v. Kelly).")

        # R3-2: no content in the payload — the drafter loads the masked text SERVER-SIDE from the
        # sanitized-artifact store via the signed ref, and returns notice_ref (not the notice text).
        draft = invoke("DraftNotice", compute.core,
                       {"deidentified": True, "sanitized_ref.$": "$.mask.out.sanitized_ref"},
                       "$.draft")
        audit_intent = invoke("AuditIntent", compute.write_audit,
                              {"icsr_id.$": "$.case_id", "action": "benefits-determination",
                               "phase": "INTENT", "actor": "workflow-controller",
                               "payload.$": "States.JsonToString($.assessment.out)"},
                              "$.audit")

        signoff = tasks.LambdaInvoke(
            self, "HumanSignoff", lambda_function=compute.signoff_register,
            integration_pattern=sfn.IntegrationPattern.WAIT_FOR_TASK_TOKEN,
            payload=sfn.TaskInput.from_object(
                {"icsr_id.$": "$.case_id", "requester.$": "$.requester",
                 # bind the approval to the EXACT determination the approver saw
                 "content_hash.$": "States.Hash(States.JsonToString($.assessment.out), 'SHA-256')",
                 "taskToken": sfn.JsonPath.task_token, **tenant_fields}),
            timeout=cdk.Duration.hours(24), result_path="$.approval")
        finalize = invoke("Finalize", compute.finalize,
                          {"icsr_id.$": "$.case_id", "requester.$": "$.requester",
                           "approver.$": "$.approval.approver"}, "$.commit")
        committed = sfn.Succeed(self, "Committed")

        c1 = sfn.Choice(self, "ExtractedOk").when(
            sfn.Condition.boolean_equals("$.guards.extracted.ok", True), mask).otherwise(manual_review)
        c2 = sfn.Choice(self, "DeidentifiedOk").when(
            sfn.Condition.boolean_equals("$.guards.deidentified.ok", True), assess).otherwise(manual_review)
        c3 = sfn.Choice(self, "RulesOk").when(
            sfn.Condition.boolean_equals("$.guards.rules_executed.ok", True), g_adverse).otherwise(manual_review)
        c4 = sfn.Choice(self, "AdverseNoticeOk").when(
            sfn.Condition.boolean_equals("$.guards.adverse_notice.ok", True), draft).otherwise(adverse_hold)
        # G1 hardening (2026-08-29, proven live): a guardrail-BLOCKED or errored draft must never
        # reach the sign-off gate — an approver should not be asked to sign a case whose notice the
        # guardrail refused to generate. A successful draft carries notice_ref (or inline notice in
        # storeless sandboxes); anything else routes to ManualReview (NEEDS_REVIEW).
        c5 = sfn.Choice(self, "DraftOk").when(
            sfn.Condition.or_(sfn.Condition.is_present("$.draft.out.notice_ref"),
                              sfn.Condition.is_present("$.draft.out.notice")),
            audit_intent).otherwise(manual_review)
        # G2 (2026-08-29): finalize now VERIFIES the approval path and refuses a token released
        # around approve_signoff (or a self-approval). A refused finalize must not land on the
        # Committed state — it routes to ManualReview (NEEDS_REVIEW), and the refusal is already a
        # DENIED event in the hash-chained ledger.
        c6 = sfn.Choice(self, "FinalizeOk").when(
            sfn.Condition.boolean_equals("$.commit.out.committed", True),
            committed).otherwise(manual_review)

        definition = extract.next(g_extracted).next(c1)
        mask.next(g_deid).next(c2)
        assess.next(g_rules).next(c3)
        g_adverse.next(c4)
        draft.next(c5)
        audit_intent.next(signoff).next(finalize).next(c6)

        # Observability review 2026-08-29: retained (1y) execution logging + X-Ray tracing.
        # include_execution_data=False keeps case payloads out of the log stream — state carries
        # references only (R3-2), and the log record matches that discipline. CMK applies when present.
        wf_cmk = None
        if getattr(data, "cmk", None) is not None:
            wf_cmk = kms.Key.from_key_arn(self, "WfCmk", data.cmk.key_arn)
        wf_logs = logs.LogGroup(
            self, "ControllerLogs", log_group_name=f"/aws/states/{prefix}-determination-workflow",
            encryption_key=wf_cmk, retention=logs.RetentionDays.ONE_YEAR,
            removal_policy=cdk.RemovalPolicy.DESTROY)
        self.controller = sfn.StateMachine(
            self, "Controller", state_machine_name=f"{prefix}-determination-workflow",
            definition_body=sfn.DefinitionBody.from_chainable(definition),
            state_machine_type=sfn.StateMachineType.STANDARD,
            timeout=cdk.Duration.hours(25),
            tracing_enabled=True,
            logs=sfn.LogOptions(destination=wf_logs, level=sfn.LogLevel.ALL,
                                include_execution_data=False),
        )
        cdk.CfnOutput(self, "ControllerArn", value=self.controller.state_machine_arn)
