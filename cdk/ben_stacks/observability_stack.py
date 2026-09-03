"""ObservabilityStack (GA-6, Review-2) — minimum production-operations signals as IaC.

Dashboards + alarms an operations team can actually run the pilot with. Sources are service metrics
(no app instrumentation required) plus metric filters staged for the custom security signals. SNS is
the pager seam (subscribe email/PagerDuty at deploy)."""
import aws_cdk as cdk
from aws_cdk import (aws_cloudtrail as cloudtrail, aws_cloudwatch as cw,
                     aws_cloudwatch_actions as cwa, aws_iam as iam, aws_kms as kms, aws_logs as logs,
                     aws_s3 as s3, aws_sns as sns, custom_resources as cr)
from constructs import Construct


class ObservabilityStack(cdk.Stack):
    def __init__(self, scope: Construct, cid: str, *, prefix: str, compute, workflow,
                 data=None, gateway=None, model_logging: bool = False, **kw):
        super().__init__(scope, cid, **kw)
        self._transparency(prefix, gateway, model_logging)
        # Gate-B: ops alarms may carry case ids — under customer-managed KMS the topic is CMK-encrypted.
        # Imported key reference (see compute_stack): cloudwatch.amazonaws.com is pre-authorized in
        # the DataStack key policy so alarms can publish to the encrypted topic.
        cmk = None
        if data is not None and getattr(data, "cmk", None) is not None:
            cmk = kms.Key.from_key_arn(self, "DataCmk", data.cmk.key_arn)
        topic = sns.Topic(self, "Alarms", topic_name=f"{prefix}-ops-alarms", master_key=cmk)

        def alarm(name, metric, threshold=0, eval_periods=1, desc=""):
            a = cw.Alarm(self, name, metric=metric, threshold=threshold,
                         evaluation_periods=eval_periods,
                         comparison_operator=cw.ComparisonOperator.GREATER_THAN_THRESHOLD,
                         treat_missing_data=cw.TreatMissingData.NOT_BREACHING,
                         alarm_description=desc)
            a.add_alarm_action(cwa.SnsAction(topic))
            return a

        sm = workflow.controller
        # ── workflow health ──────────────────────────────────────────────────
        alarm("WorkflowFailed", sm.metric_failed(period=cdk.Duration.minutes(5)),
              desc="Determination workflow execution FAILED — investigate; cases are not being processed.")
        alarm("WorkflowTimedOut", sm.metric_timed_out(period=cdk.Duration.minutes(5)),
              desc="Execution timed out (approval older than the 24h gate?) — approval backlog or stuck state.")
        alarm("WorkflowThrottled", sm.metric_throttled(period=cdk.Duration.minutes(5)),
              desc="Executions throttled — quota pressure.")

        # ── control-plane Lambda health (the governance-critical functions) ──
        for label, fn in (("Mask", compute.mask), ("Guards", compute.guards),
                          ("Finalize", compute.finalize), ("WriteAudit", compute.write_audit),
                          ("Assess", compute.assess)):
            alarm(f"{label}Errors", fn.metric_errors(period=cdk.Duration.minutes(5)),
                  desc=f"{label} Lambda errors — a governance-critical function is failing "
                       f"({'masking' if label == 'Mask' else 'audit trail' if label == 'WriteAudit' else 'pipeline'} impact; fail-closed but investigate).")

        # ── R3-3 security metrics: guard failures ARE security signals ───────
        # workflow_guards emits EMF (Benefits/Governance :: GuardFailed{Guard}) on every evaluation.
        # A nonzero sum means forged/tampered/missing evidence — or an ADVERSE redetermination missing
        # its required advance notice — hit a guard. Page immediately.
        guard_failed = cw.Metric(namespace="Benefits/Governance", metric_name="GuardFailed",
                                 statistic="Sum", period=cdk.Duration.minutes(5))
        alarm("GuardFailures", guard_failed,
              desc="A workflow guard REFUSED a transition (forged sanitized_ref, a spoofed boolean, or "
                   "an adverse benefits action lacking its advance notice). Security / due-process "
                   "signal - triage per THREAT-MODEL.md; repeated failures may indicate an active "
                   "forgery attempt or a due-process gap.")

        # ── dashboard: security · workflow · ops ─────────────────────────────
        dash = cw.Dashboard(self, "Dashboard", dashboard_name=f"{prefix}-operations")
        dash.add_widgets(
            cw.GraphWidget(title="Workflow: started / succeeded / failed / timed-out", width=12,
                           left=[sm.metric_started(), sm.metric_succeeded(),
                                 sm.metric_failed(), sm.metric_timed_out()]),
            cw.GraphWidget(title="Governance Lambdas: errors", width=12,
                           left=[compute.mask.metric_errors(), compute.guards.metric_errors(),
                                 compute.write_audit.metric_errors(), compute.finalize.metric_errors()]),
        )
        dash.add_widgets(
            cw.GraphWidget(title="SECURITY: guard failures (forged/tampered evidence refused)", width=12,
                           left=[guard_failed]),
            cw.GraphWidget(title="Sign-off gate: pending approvals (finalize invocations)", width=12,
                           left=[compute.finalize.metric_invocations(),
                                 compute.signoff_register.metric_invocations()]),
        )
        dash.add_widgets(
            cw.GraphWidget(title="Governance Lambdas: duration p95", width=12,
                           left=[compute.mask.metric_duration(statistic="p95"),
                                 compute.core.metric_duration(statistic="p95"),
                                 compute.assess.metric_duration(statistic="p95")]),
            cw.GraphWidget(title="Eligibility assess: invocations vs errors", width=12,
                           left=[compute.assess.metric_invocations(), compute.assess.metric_errors()]),
        )

        # ---- Evidence-store data events (observability review 2026-08-29) -------------------
        # A data-only trail on the agent's WORM vault: the audit ledger proves what the gateway
        # wrote; these object-level events independently prove nobody ELSE touched the evidence.
        # Management events are NONE (the platform's evidence trail owns those + DynamoDB data
        # events for all tables), so this trail bills only per data event — cents at pilot volume.
        if data is not None and getattr(data, "worm_bucket", None) is not None:
            evidence_trail = cloudtrail.Trail(
                self, "WormDataEvents", trail_name=f"{prefix}-worm-data-events",
                management_events=cloudtrail.ReadWriteType.NONE,
                include_global_service_events=False, is_multi_region_trail=False)
            evidence_trail.add_event_selector(
                cloudtrail.DataResourceType.S3_OBJECT,
                [f"{data.worm_bucket.bucket_arn}/"],
                read_write_type=cloudtrail.ReadWriteType.ALL)
            cdk.CfnOutput(self, "EvidenceTrailArn", value=evidence_trail.trail_arn)

        cdk.CfnOutput(self, "AlarmTopicArn", value=topic.topic_arn,
                      description="Subscribe ops email / PagerDuty here.")
        cdk.CfnOutput(self, "DashboardName", value=f"{prefix}-operations")

    # ── Phase 110: full transparency — every model invocation + every gateway request ────────────
    def _transparency(self, prefix, gateway, model_logging):
        """Bedrock MODEL INVOCATION LOGGING (the exact Converse request/response bodies, tagged by the
        runtime's requestMetadata: tenant / session_id / case_id) + the AgentCore GATEWAY's vended
        request logs (CloudWatch Logs delivery, log type APPLICATION_LOGS). The runtime's spans and
        logs are AgentCore-managed (/aws/bedrock-agentcore/runtimes/<agent>-<endpoint>, aws/spans).
        Sources: Bedrock model-invocation logging + AgentCore observability configuration docs."""
        self.model_log_group = None
        if model_logging:
            lg = logs.LogGroup(self, "ModelInvocationLogs", log_group_name=f"/aws/bedrock/modelinvocations/{prefix}",
                               retention=logs.RetentionDays.ONE_YEAR, removal_policy=cdk.RemovalPolicy.DESTROY)
            big = s3.Bucket(self, "ModelInvocationLargeData", block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                            encryption=s3.BucketEncryption.S3_MANAGED, enforce_ssl=True,
                            removal_policy=cdk.RemovalPolicy.DESTROY, auto_delete_objects=True)
            big.add_to_resource_policy(iam.PolicyStatement(
                actions=["s3:PutObject"], resources=[f"{big.bucket_arn}/*"],
                principals=[iam.ServicePrincipal("bedrock.amazonaws.com")],
                conditions={"StringEquals": {"aws:SourceAccount": self.account}}))
            role = iam.Role(self, "ModelInvocationLogRole", assumed_by=iam.ServicePrincipal(
                "bedrock.amazonaws.com", conditions={"StringEquals": {"aws:SourceAccount": self.account}}))
            role.add_to_policy(iam.PolicyStatement(actions=["logs:CreateLogStream", "logs:PutLogEvents"],
                                                   resources=[lg.log_group_arn, f"{lg.log_group_arn}:log-stream:*"]))
            cfg = {"loggingConfig": {
                "cloudWatchConfig": {"logGroupName": lg.log_group_name, "roleArn": role.role_arn,
                                     "largeDataDeliveryS3Config": {"bucketName": big.bucket_name}},
                "textDataDeliveryEnabled": True, "imageDataDeliveryEnabled": False,
                "embeddingDataDeliveryEnabled": False, "videoDataDeliveryEnabled": False}}
            put = cr.AwsSdkCall(service="bedrock", action="putModelInvocationLoggingConfiguration",
                                parameters=cfg, physical_resource_id=cr.PhysicalResourceId.of(f"{prefix}-model-logging"))
            res = cr.AwsCustomResource(
                self, "ModelInvocationLogging", on_create=put, on_update=put,
                on_delete=cr.AwsSdkCall(service="bedrock", action="deleteModelInvocationLoggingConfiguration"),
                policy=cr.AwsCustomResourcePolicy.from_statements([
                    iam.PolicyStatement(actions=["bedrock:PutModelInvocationLoggingConfiguration",
                                                 "bedrock:DeleteModelInvocationLoggingConfiguration"], resources=["*"]),
                    iam.PolicyStatement(actions=["iam:PassRole"], resources=[role.role_arn])]))
            res.node.add_dependency(role)
            self.model_log_group = lg
            cdk.CfnOutput(self, "ModelInvocationLogGroup", value=lg.log_group_name)
            cdk.CfnOutput(self, "ModelInvocationLargeDataBucket", value=big.bucket_name)

        self.gateway_log_group = None
        if gateway is not None and getattr(gateway, "gateway_arn", None):
            glg = logs.LogGroup(self, "GatewayRequestLogs", log_group_name=f"/aws/vendedlogs/bedrock-agentcore/gateway/{prefix}",
                                retention=logs.RetentionDays.ONE_YEAR, removal_policy=cdk.RemovalPolicy.DESTROY)
            src = logs.CfnDeliverySource(self, "GatewayLogSource", name=f"{prefix}-gateway-logs",
                                         resource_arn=gateway.gateway_arn, log_type="APPLICATION_LOGS")
            dst = logs.CfnDeliveryDestination(self, "GatewayLogDestination", name=f"{prefix}-gateway-logs",
                                              destination_resource_arn=glg.log_group_arn)
            dlv = logs.CfnDelivery(self, "GatewayLogDelivery", delivery_source_name=src.name,
                                   delivery_destination_arn=dst.attr_arn)
            dlv.add_dependency(src)
            dlv.add_dependency(dst)
            self.gateway_log_group = glg
            cdk.CfnOutput(self, "GatewayRequestLogGroup", value=glg.log_group_name)
