# #170 — VPC + WAF on the runtime path (2026-09-05) — VPC **PASS** · WAF ACL built, association **BLOCKED live**

**What this is.** A from-zero deploy (`ben-nw`, `-c network_mode=private -c waf=1`) exercising the
network/edge perimeter of the runtime path, with `scripts/network_waf_proof.py`. Account ids redacted
to `111122223333`. This is an **honest split result**: the VPC control is live-proven; the WAF Web ACL
is provisioned as IaC but its **association to the Cognito user pool could not be completed live** in
this environment, for AWS-side reasons documented below.

## VPC isolation of the governed compute path — **PASS**

| check | result | detail |
|---|---|---|
| governed Lambdas in VPC | **PASS** | all **16** governed tool Lambdas run in the VPC, across **2 isolated subnets** (`subnet-…423`, `subnet-…5b1`) with the single tools security group (`sg-…063`) |
| zero public egress | **PASS** | the VPC (`vpc-…da6`) has **0 NAT gateways** and **0 internet gateways** — the governed pipeline has no route to the internet by construction, not by allowlist |

This is the substantive perimeter control for the compute path and it is enforced and proven live
(`-c network_mode=private`, `NetworkStack`: S3/DynamoDB gateway endpoints + Comprehend/Bedrock/Secrets/
StepFunctions/Logs/KMS/STS interface endpoints; SG egress 443 to AWS endpoints only).

## WAF on the auth front door — Web ACL built as IaC; association blocked live

The `-c waf=1` deploy creates a **REGIONAL WAFv2 Web ACL** (`ben-nw-auth-waf`) with the AWS managed
**Common Rule Set** + a **per-IP rate-based** block rule (verified created). The Web ACL is the correct,
attachable control for the runtime/auth path, because the AgentCore Gateway and Runtime are **managed
endpoints and are not WAF-associable resource types** (WAFv2 associates only with ALB / API Gateway /
CloudFront / AppSync / **Cognito user pool** / App Runner); the user pool is the associable surface.

**The association could not be completed live.** Three distinct AWS-side obstacles were hit and are
recorded here so the finding is not lost:

1. The native `AWS::WAFv2::WebACLAssociation` targeting a Cognito user pool **hangs indefinitely** in
   CloudFormation (CREATE_IN_PROGRESS for >8 min with no progress; `get-web-acl-for-resource` still
   null) — its stabilization waiter misbehaves for Cognito targets.
2. A direct `AssociateWebACL` API call (and an `AwsCustomResource` doing the same) returns
   **`WAFUnavailableEntityException`: "AWS WAF couldn't retrieve the resource that you requested"** —
   persistently, across 12 retries over ~60 s and again after several more minutes.
3. Adding a Cognito **hosted domain** (Managed Login v1) to the pool did **not** clear it either.

AWS documents WAF web ACLs as available on all Cognito feature plans, and `get-web-acl-for-resource`
accepts the pool ARN as a valid associable resource (returns null, not an error), so the pool ARN and
tier are not the blocker. The remaining likely cause is a longer readiness lag and/or a **Managed Login
(branding v2)** requirement for the association to bind — not resolved within this session.

## Honest status

- **VPC: done and live-proven.**
- **WAF: the Web ACL is provisioned as IaC and correctly configured**, but WAF is **not live-enforcing**
  because the association did not complete. This is tracked as a follow-up: fold the association into a
  **retrying Lambda-backed custom resource** and confirm the Managed Login v2 prerequisite, then
  re-run the association proof.
- **AgentCore Runtime / Gateway VPC (reference).** Both support customer-VPC connectivity, set at
  create time via `networkConfiguration = { networkMode: "VPC", networkModeConfig: { subnets, securityGroups } }`
  (requires ECR dkr+api, S3, and CloudWatch Logs VPC endpoints; PrivateLink inbound for the control APIs).
  The Runtime here is toolkit-launched (`agentcore configure`/`launch`), so this is wired at launch,
  not in the CDK app; the confirmed shape is recorded for the adopter.

## Teardown

`cdk destroy --all` (env `nw`) removed all four stacks; the out-of-band test domain was deleted first so
the pool could delete; the WAF Web ACL is deleted with the identity stack. Account model-invocation
logging was never touched (observability stack not deployed).

Raw redacted record: `evidence/AGENTCORE-NETWORK-WAF-2026-09-05.json` (verdict shows the VPC checks true
and the WAF association error verbatim).
