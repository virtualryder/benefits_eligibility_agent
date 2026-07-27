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
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

# Benefits reaches NO external domain — the allowlist is empty by design (docs/DATA-SOURCE-POLICY.md).
ALLOWED_DOMAINS = []


class NetworkStack(cdk.Stack):
    def __init__(self, scope: Construct, cid: str, *, prefix: str, **kw):
        super().__init__(scope, cid, **kw)

        # Isolated-only VPC: no public subnets, no NAT, no IGW. The app subnets have no default route
        # to 0.0.0.0/0 at all. AZs pinned to the us-east-1 deployment path (parity with the siblings).
        self.vpc = ec2.Vpc(
            self, "Vpc", vpc_name=f"{prefix}-net",
            availability_zones=["us-east-1a", "us-east-1b"], nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="app", subnet_type=ec2.SubnetType.PRIVATE_ISOLATED, cidr_mask=24),
            ])
        app_sel = ec2.SubnetSelection(subnet_group_name="app")

        # ── AWS traffic stays on the AWS network (the ONLY reachable destinations) ────
        self.vpc.add_gateway_endpoint("S3Ep", service=ec2.GatewayVpcEndpointAwsService.S3, subnets=[app_sel])
        self.vpc.add_gateway_endpoint("DdbEp", service=ec2.GatewayVpcEndpointAwsService.DYNAMODB, subnets=[app_sel])
        for name, svc in (("SecretsEp", ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER),
                          ("SfnEp", ec2.InterfaceVpcEndpointAwsService.STEP_FUNCTIONS),
                          ("ComprehendEp", ec2.InterfaceVpcEndpointAwsService.COMPREHEND),
                          ("BedrockEp", ec2.InterfaceVpcEndpointAwsService.BEDROCK_RUNTIME),
                          ("LogsEp", ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH_LOGS),
                          ("KmsEp", ec2.InterfaceVpcEndpointAwsService.KMS),
                          ("StsEp", ec2.InterfaceVpcEndpointAwsService.STS)):
            self.vpc.add_interface_endpoint(name, service=svc, subnets=app_sel, private_dns_enabled=True)

        # ── the governed Lambdas' security group: egress 443 only ────────────────────
        # allow_all_outbound=False keeps the intent explicit. Egress is TLS-443 to any IPv4 — but this
        # can ONLY reach (a) the in-VPC interface endpoints (Comprehend/Bedrock/Secrets/SFN/Logs/KMS/STS)
        # and (b) the S3 + DynamoDB GATEWAY endpoints, whose traffic is routed to the AWS service
        # prefix-lists (NOT the VPC CIDR — a VPC-CIDR-only rule silently blocks DynamoDB/S3). There is no
        # NAT/IGW, so no arbitrary internet host is reachable regardless of this rule.
        self.lambda_sg = ec2.SecurityGroup(
            self, "LambdaSg", vpc=self.vpc, allow_all_outbound=False,
            security_group_name=f"{prefix}-tools",
            description="Governed tool Lambdas - egress 443 only; reachable set = in-VPC AWS endpoints + S3/DDB gateway prefix-lists; no internet route exists")
        # Interface endpoints (Comprehend/Bedrock/Secrets/SFN/Logs/KMS/STS) live in the VPC CIDR; the
        # S3 + DynamoDB GATEWAY endpoints route to the AWS service prefix-lists (NOT the VPC CIDR — a
        # VPC-CIDR-only rule silently blocks DynamoDB/S3). Allowing 443 to any IPv4 covers both, and with
        # no NAT/IGW there is no route to any arbitrary internet host regardless.
        self.lambda_sg.add_egress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(443),
                                       "TLS 443; reachable set = AWS interface endpoints + S3/DDB gateway prefix-lists (no NAT/IGW route out)")

        cdk.CfnOutput(self, "VpcId", value=self.vpc.vpc_id)
        cdk.CfnOutput(self, "EgressPosture",
                      value="zero-public-egress (isolated subnets; AWS private endpoints only; no NAT/IGW)")
        cdk.CfnOutput(self, "AllowedEgressDomains", value="(none)")
