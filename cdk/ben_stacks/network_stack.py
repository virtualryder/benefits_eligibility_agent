"""NetworkStack (Gate-B B1) — private networking with ZERO public egress for the governed pipeline.

Benefits has NO external data dependency: the eligibility engine runs on public HHS Federal Poverty
Guidelines baked in as configuration (no lookup call), and the only AWS services the governed tools
touch are Comprehend (masking) and Bedrock (drafting) plus DynamoDB/S3/Step Functions/Secrets/KMS —
all reachable privately. So `network_mode=private` gives the strongest posture of the portfolio:

  * every governed tool Lambda runs in PRIVATE_ISOLATED subnets with **no route to the internet** —
    no NAT gateway, no Internet Gateway, no egress firewall to configure, because there is no egress
    path to allow or deny in the first place. Exfiltration to an arbitrary host is impossible by
    construction, not by allowlist.
  * AWS-service traffic never leaves the AWS network: gateway endpoints (S3, DynamoDB) + interface
    endpoints (Secrets Manager, Step Functions, Comprehend, Bedrock runtime, CloudWatch Logs, KMS,
    STS) serve it privately.

Contrast with the housing/EDU/PV agents, which DO reach one sanctioned external API (HUD / College
Scorecard / openFDA) and therefore ship a Network Firewall egress allowlist. Benefits needs none.
"""
import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2, aws_iam as iam
from constructs import Construct

# Benefits reaches NO external domain — the allowlist is empty by design (docs/DATA-SOURCE-POLICY.md).
ALLOWED_DOMAINS = []


class NetworkStack(cdk.Stack):
    # AZs every interface endpoint this VPC needs is offered in (us-east-1, checked 2026-09-05 with
    # `aws ec2 describe-vpc-endpoint-services`): cognito-idp is offered ONLY in us-east-1b/1c/1d, while
    # comprehend / bedrock-runtime / states / secretsmanager / logs / kms / sts are in every AZ. The
    # previous pin (1a + 1b) failed the Tier-1 live gate on the cognito-idp endpoint ("does not support
    # the availability zone of the subnet") - the endpoint had only ever been unit-synthesized. Override
    # per account/region with -c vpc_azs=<az>,<az>; AZ-name-to-physical mapping differs per account, so
    # re-check the cognito-idp AZ list when deploying elsewhere.
    DEFAULT_AZS = ("us-east-1b", "us-east-1c")

    def __init__(self, scope: Construct, cid: str, *, prefix: str, bedrock_principals=(), azs=(), **kw):
        super().__init__(scope, cid, **kw)
        self.azs = [a for a in (azs or self.DEFAULT_AZS) if a]

        # Isolated-only VPC: no public subnets, no NAT, no IGW. The app subnets have no default route
        # to 0.0.0.0/0 at all. AZs pinned to ones every required interface endpoint is offered in.
        self.vpc = ec2.Vpc(
            self, "Vpc", vpc_name=f"{prefix}-net",
            availability_zones=list(self.azs), nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="app", subnet_type=ec2.SubnetType.PRIVATE_ISOLATED, cidr_mask=24),
            ])
        app_sel = ec2.SubnetSelection(subnet_group_name="app")
        self.endpoints = {}

        # ── AWS traffic stays on the AWS network (the ONLY reachable destinations) ────
        self.vpc.add_gateway_endpoint("S3Ep", service=ec2.GatewayVpcEndpointAwsService.S3, subnets=[app_sel])
        self.vpc.add_gateway_endpoint("DdbEp", service=ec2.GatewayVpcEndpointAwsService.DYNAMODB, subnets=[app_sel])
        for name, svc in (("SecretsEp", ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER),
                          ("SfnEp", ec2.InterfaceVpcEndpointAwsService.STEP_FUNCTIONS),
                          ("ComprehendEp", ec2.InterfaceVpcEndpointAwsService.COMPREHEND),
                          ("BedrockEp", ec2.InterfaceVpcEndpointAwsService.BEDROCK_RUNTIME),
                          ("LogsEp", ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH_LOGS),
                          ("KmsEp", ec2.InterfaceVpcEndpointAwsService.KMS),
                          ("StsEp", ec2.InterfaceVpcEndpointAwsService.STS),
                          # Live-found L9 (Tier-1 gate attempt 8, 2026-09-06): EVERY governed tool reads the
                          # kill switch from Parameter Store before doing anything else, and the budget
                          # meter publishes to CloudWatch metrics. Neither ssm nor monitoring had an
                          # endpoint, so in private mode every tool hung on the SSM read until the 30s
                          # Lambda timeout and the gateway surfaced it as a 500 (not even a Cedar deny
                          # could be observed). tests/test_cdk_stacks.py now derives the required endpoint
                          # set from the boto3 clients in the deployed Lambda bundle.
                          ("SsmEp", ec2.InterfaceVpcEndpointAwsService.SSM),
                          ("MonitoringEp", ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH_MONITORING),
                          # deep-dive #5: the approval/requester verifier fetches the Cognito JWKS
                          # (https://cognito-idp.<region>.amazonaws.com/<pool>/.well-known/jwks.json) at
                          # cold start to verify RS256 access tokens. In a zero-egress VPC there is no
                          # internet route, so WITHOUT this cognito-idp interface endpoint the JWKS fetch
                          # fails on a cold start and identity verification breaks. private_dns_enabled
                          # makes the public cognito-idp hostname resolve to the endpoint inside the VPC.
                          ("CognitoIdpEp", ec2.InterfaceVpcEndpointAwsService("cognito-idp"))):
            self.endpoints[name] = self.vpc.add_interface_endpoint(
                name, service=svc, subnets=app_sel, private_dns_enabled=True)

        # ── Bedrock runtime endpoint POLICY (enforcement-perimeter review, 2026-09-05) ─────────
        # Network-layer half of the perimeter INSIDE the pack's own VPC: the bedrock-runtime interface
        # endpoint accepts inference calls ONLY from the governed drafter role (the compute stack's
        # core-tools Lambda, whose IAM allow additionally requires a guardrail on every call) and any
        # -c approved_bedrock_principals. Anything else in these subnets that obtains Bedrock
        # credentials is refused at the endpoint - the in-VPC counterpart of the org SCP under org/.
        # aws:PrincipalArn resolves to the ROLE arn for a role session, so a caller-chosen session name
        # cannot satisfy it. Converse / ConverseStream authorize as InvokeModel / ...WithResponseStream.
        # L12: the EXACT pinned drafter role (see compute_stack.drafter_role_name) - no wildcard, no case guess.
        from .compute_stack import drafter_role_name
        drafter_role_pattern = f"arn:aws:iam::{self.account}:role/{drafter_role_name(prefix)}"
        self.bedrock_endpoint_principals = [drafter_role_pattern] + [p for p in bedrock_principals if p]
        self.endpoints["BedrockEp"].add_to_policy(iam.PolicyStatement(
            sid="GovernedDrafterOnly", effect=iam.Effect.ALLOW,
            principals=[iam.AnyPrincipal()],
            actions=["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream", "bedrock:ApplyGuardrail"],
            resources=["*"],
            conditions={"ArnLike": {"aws:PrincipalArn": self.bedrock_endpoint_principals},
                        "StringEquals": {"aws:PrincipalAccount": self.account}}))

        # ── the governed Lambdas' security group: egress 443 only ────────────────────
        # allow_all_outbound=False keeps the intent explicit. Egress is TLS-443 to any IPv4 — but this
        # can ONLY reach (a) the in-VPC interface endpoints (Comprehend/Bedrock/Secrets/SFN/Logs/KMS/STS/SSM/Monitoring/Cognito)
        # and (b) the S3 + DynamoDB GATEWAY endpoints, whose traffic is routed to the AWS service
        # prefix-lists (NOT the VPC CIDR — a VPC-CIDR-only rule silently blocks DynamoDB/S3). There is no
        # NAT/IGW, so no arbitrary internet host is reachable regardless of this rule.
        self.lambda_sg = ec2.SecurityGroup(
            self, "LambdaSg", vpc=self.vpc, allow_all_outbound=False,
            security_group_name=f"{prefix}-tools",
            description="Governed tool Lambdas - egress 443 only; reachable set = in-VPC AWS endpoints + S3/DDB gateway prefix-lists; no internet route exists")
        # Interface endpoints (Comprehend/Bedrock/Secrets/SFN/Logs/KMS/STS/SSM/Monitoring/Cognito) live in the VPC CIDR; the
        # S3 + DynamoDB GATEWAY endpoints route to the AWS service prefix-lists (NOT the VPC CIDR — a
        # VPC-CIDR-only rule silently blocks DynamoDB/S3). Allowing 443 to any IPv4 covers both, and with
        # no NAT/IGW there is no route to any arbitrary internet host regardless.
        self.lambda_sg.add_egress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(443),
                                       "TLS 443; reachable set = AWS interface endpoints + S3/DDB gateway prefix-lists (no NAT/IGW route out)")

        cdk.CfnOutput(self, "VpcId", value=self.vpc.vpc_id)
        cdk.CfnOutput(self, "EgressPosture",
                      value="zero-public-egress (isolated subnets; AWS private endpoints only; no NAT/IGW)")
        cdk.CfnOutput(self, "AllowedEgressDomains", value="(none)")
