# Case trace — `OBS-SPB-F752B` (tenant `sp-b`)

| metric | value |
|---|---|
| agent_spans | 1 |
| gateway_requests | 33 |
| lambda_calls | 7 |
| lambda_calls_joined_to_evidence | 6 |
| masked_before_model_all | True |
| model_invocations | 5 |
| model_invocations_joined_to_spans | 5 |
| model_invocations_tagged_tenant | 5 |
| model_spans | 10 |
| sessions | ['aegis-sp-b-d20dd3c0327f4165908e85306c7f97fe'] |
| single_tenant | True |
| tenants_seen | ['sp-b'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 17:14:16.251 | lambda | call | ingest_application -> ingested=True | trace_id=6aa2e56728e55ac177 request_id=a36a0469-53fc-4e87 tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:16.884 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa2e5686f44f44a6b span_id=583f377c27d5e12a session_id=aegis-sp-b-d20dd3c |
| 17:14:17.546 | runtime-span | runtime-http | POST /invocations | trace_id=6aa2e5686f44f44a6b span_id=0734f795ad53a18b session_id=aegis-sp-b-d20dd3c |
| 17:14:17.641 | runtime-span | span | SSM.GetParameter | trace_id=6aa2e5686f44f44a6b span_id=bd3e1147abed40a5 session_id=aegis-sp-b-d20dd3c |
| 17:14:17.687 | runtime-span | span | SSM.GetParameter | trace_id=6aa2e5686f44f44a6b span_id=fb92c0ba8dd6b3c3 session_id=aegis-sp-b-d20dd3c |
| 17:14:17.747 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa2e5686f44f44a6b span_id=5c3b2707dd1e21ab session_id=aegis-sp-b-d20dd3c |
| 17:14:17.796 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa2e5686f44f44a6b span_id=0b170c7f204fce38 session_id=aegis-sp-b-d20dd3c |
| 17:14:17.896 | runtime-span | span | mcp.session | trace_id=6aa2e5686f44f44a6b span_id=69e2cd88fdde6e23 session_id=aegis-sp-b-d20dd3c |
| 17:14:18.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5337 out=208 masked_before_model=True | request_id=3aef47bf-0677-412d session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:18.029 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa2e5686f44f44a6b span_id=1a2bd1b2d59b0d9a session_id=aegis-sp-b-d20dd3c |
| 17:14:18.260 | runtime-span | lambda-segment | ben-fpd-tenant-interceptor/LambdaService | trace_id=6aa2e5686f44f44a6b span_id=2d4ca248f80839d9 |
| 17:14:18.270 | runtime-span | lambda-segment | ben-fpd-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=9301e7c9c80c9a43 |
| 17:14:18.300 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=4b02bc5c6910b7ef |
| 17:14:18.302 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060458302,"body":{"isError":false,"lo | session_id=aegis-sp-b-d20dd3c trace_id=6aa2e5686f44f44a6b |
| 17:14:18.308 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060458308,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:18.393 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060458393,"body":{"isError":false,"re | trace_id=6aa2e5686f44f44a6b |
| 17:14:18.401 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=33179 out=2014 | trace_id=6aa2e5686f44f44a6b span_id=03a2486dfb2f5faf session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:18.402 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2e5686f44f44a6b span_id=9d8eee6e27b16a3f session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:18.403 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5337 out=208 | trace_id=6aa2e5686f44f44a6b span_id=8cb5c5f276eea5dd session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:18.415 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2e5686f44f44a6b span_id=a45b6433066b33e6 session_id=aegis-sp-b-d20dd3c |
| 17:14:18.415 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5337 out=208 | trace_id=6aa2e5686f44f44a6b span_id=7b19fd2a5813b386 session_id=aegis-sp-b-d20dd3c request_id=3aef47bf-0677-412d |
| 17:14:21.941 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2e5686f44f44a6b span_id=59b778b2439c75c4 session_id=aegis-sp-b-d20dd3c |
| 17:14:21.958 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2e5686f44f44a6b span_id=12ff2486b308c63a session_id=aegis-sp-b-d20dd3c |
| 17:14:21.991 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa2e5686f44f44a6b span_id=3bc061ff5e92ae5e session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:21.992 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa2e5686f44f44a6b span_id=ccd38bd2914aeb7a session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:21.993 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa2e5686f44f44a6b span_id=92f9b44354005e83 session_id=aegis-sp-b-d20dd3c |
| 17:14:21.993 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa2e5686f44f44a6b span_id=06d0ea388a504566 session_id=aegis-sp-b-d20dd3c |
| 17:14:22.092 | runtime-span | lambda-segment | ben-fpd-tenant-interceptor/LambdaService | trace_id=6aa2e5686f44f44a6b span_id=0b41bb38113de69a |
| 17:14:22.097 | runtime-span | lambda-segment | ben-fpd-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=9fe4edd1e2ecca8b |
| 17:14:22.099 | runtime-span | lambda-segment | ben-fpd-tenant-interceptor/LambdaService | trace_id=6aa2e5686f44f44a6b span_id=1b68a7ce9fb883cd |
| 17:14:22.251 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=50849f6a7105f88f |
| 17:14:22.275 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=e70ea562896d7c45 |
| 17:14:22.279 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060462279,"body":{"isError":false,"lo | session_id=aegis-sp-b-d20dd3c trace_id=6aa2e5686f44f44a6b |
| 17:14:22.282 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060462282,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:22.362 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060462362,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:22.383 | runtime-span | lambda-segment | ben-fpd-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=ca50b29b59b7da85 |
| 17:14:22.388 | runtime-span | lambda-segment | ben-fpd-intake-application/LambdaService | trace_id=6aa2e5686f44f44a6b span_id=0cc9493b94c595a3 |
| 17:14:22.395 | runtime-span | lambda-segment | ben-fpd-intake-application/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=32b5420508373ead |
| 17:14:22.561 | lambda | call | intake_application -> ok | trace_id=6aa2e5686f44f44a6b session_id=aegis-sp-b-d20dd3c request_id=56dc62e2-80e0-4266 tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:22.569 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=97af658e00a3d298 |
| 17:14:22.575 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060462575,"body":{"isError":false,"re | trace_id=6aa2e5686f44f44a6b |
| 17:14:22.575 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060462575,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:26.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5977 out=399 masked_before_model=True | request_id=1fff6e17-0aa8-4e83 session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:26.244 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=67664acd958c2447 |
| 17:14:26.247 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060466247,"body":{"isError":false,"lo | session_id=aegis-sp-b-d20dd3c trace_id=6aa2e5686f44f44a6b |
| 17:14:26.250 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060466250,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:26.331 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060466331,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:26.356 | runtime-span | lambda-segment | ben-fpd-mask-pii/LambdaService | trace_id=6aa2e5686f44f44a6b span_id=7dbbac01345090b5 |
| 17:14:26.360 | runtime-span | lambda-segment | ben-fpd-mask-pii/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=c447664453f4f305 |
| 17:14:26.860 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa2e5686f44f44a6b session_id=aegis-sp-b-d20dd3c request_id=fc1f3d00-45e4-45f2 tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:26.860 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=403210c5a96146b4 |
| 17:14:26.868 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060466868,"body":{"isError":false,"re | trace_id=6aa2e5686f44f44a6b |
| 17:14:26.868 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060466868,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:26.873 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2e5686f44f44a6b span_id=91c2cdfdd4b5c4b1 session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:26.874 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5977 out=399 | trace_id=6aa2e5686f44f44a6b span_id=e7d5c94fd6fb4b0a session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:26.875 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2e5686f44f44a6b span_id=3768e8a40212dd01 session_id=aegis-sp-b-d20dd3c |
| 17:14:26.875 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5977 out=399 | trace_id=6aa2e5686f44f44a6b span_id=7ca291e8b7f635ba session_id=aegis-sp-b-d20dd3c request_id=1fff6e17-0aa8-4e83 |
| 17:14:31.742 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2e5686f44f44a6b span_id=7ade6a8d7e5074a8 session_id=aegis-sp-b-d20dd3c |
| 17:14:31.749 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2e5686f44f44a6b span_id=251c2705d5f4fb99 session_id=aegis-sp-b-d20dd3c |
| 17:14:31.782 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa2e5686f44f44a6b span_id=696c46d9c8b4fb61 session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:31.783 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa2e5686f44f44a6b span_id=8b8ee522c5d32057 session_id=aegis-sp-b-d20dd3c |
| 17:14:31.835 | runtime-span | lambda-segment | ben-fpd-tenant-interceptor/LambdaService | trace_id=6aa2e5686f44f44a6b span_id=606e697ead42f247 |
| 17:14:31.840 | runtime-span | lambda-segment | ben-fpd-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=5b8e8ce608e5241d |
| 17:14:31.992 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=7637d4953060f959 |
| 17:14:31.995 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060471995,"body":{"isError":false,"lo | session_id=aegis-sp-b-d20dd3c trace_id=6aa2e5686f44f44a6b |
| 17:14:31.997 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060471997,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:32.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6607 out=566 masked_before_model=True | request_id=abc7ec67-e38d-4a7f session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:32.058 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060472058,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:32.073 | runtime-span | lambda-segment | ben-fpd-assess-eligibility/LambdaService | trace_id=6aa2e5686f44f44a6b span_id=3df2506adfba341d |
| 17:14:32.078 | runtime-span | lambda-segment | ben-fpd-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=81567643fd740d83 |
| 17:14:32.106 | lambda | call | assess_eligibility -> ok | trace_id=6aa2e5686f44f44a6b session_id=aegis-sp-b-d20dd3c request_id=cb1d37ab-6f29-4bca tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:32.107 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=89e0c27fa9b733d4 |
| 17:14:32.111 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060472111,"body":{"isError":false,"re | trace_id=6aa2e5686f44f44a6b |
| 17:14:32.111 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060472111,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:32.116 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2e5686f44f44a6b span_id=dde889ef36ffef02 session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:32.118 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6607 out=566 | trace_id=6aa2e5686f44f44a6b span_id=5e4b758f8118bd5b session_id=aegis-sp-b-d20dd3c request_id=abc7ec67-e38d-4a7f |
| 17:14:32.118 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6607 out=566 | trace_id=6aa2e5686f44f44a6b span_id=c4bda04b3ebbb6c0 session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:32.119 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2e5686f44f44a6b span_id=bdf6b71d18b190a2 session_id=aegis-sp-b-d20dd3c |
| 17:14:39.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7221 out=419 masked_before_model=True | request_id=9264902f-1856-4d7c session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:39.102 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2e5686f44f44a6b span_id=2b9044518b0b5644 session_id=aegis-sp-b-d20dd3c |
| 17:14:39.116 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2e5686f44f44a6b span_id=db2da9142e5f59c0 session_id=aegis-sp-b-d20dd3c |
| 17:14:39.148 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa2e5686f44f44a6b span_id=0e793524ac859e4a session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:39.149 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa2e5686f44f44a6b span_id=39cf9e722d64ec61 session_id=aegis-sp-b-d20dd3c |
| 17:14:39.272 | runtime-span | lambda-segment | ben-fpd-tenant-interceptor/LambdaService | trace_id=6aa2e5686f44f44a6b span_id=2aef4f02cf71ab8f |
| 17:14:39.277 | runtime-span | lambda-segment | ben-fpd-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=e8b237012b535ebd |
| 17:14:39.424 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=96129d1fb5e514e5 |
| 17:14:39.427 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060479427,"body":{"isError":false,"lo | session_id=aegis-sp-b-d20dd3c trace_id=6aa2e5686f44f44a6b |
| 17:14:39.432 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060479432,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:39.505 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060479505,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:39.536 | runtime-span | lambda-segment | ben-fpd-core-tools/LambdaService | trace_id=6aa2e5686f44f44a6b span_id=556ff7bc54e0eeb9 |
| 17:14:39.543 | runtime-span | lambda-segment | ben-fpd-core-tools/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=89fb031cc2aa280c |
| 17:14:39.571 | lambda | call | benefits_core -> committed=False | trace_id=6aa2e5686f44f44a6b session_id=aegis-sp-b-d20dd3c request_id=1c4ecc3a-e1dc-4854 tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:39.572 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=d0c51ed21d9a5469 |
| 17:14:39.576 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060479576,"body":{"isError":false,"re | trace_id=6aa2e5686f44f44a6b |
| 17:14:39.576 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060479576,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:39.581 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2e5686f44f44a6b span_id=d994db8ed840c6d0 session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:39.582 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7221 out=419 | trace_id=6aa2e5686f44f44a6b span_id=f2471eafb6094040 session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:39.583 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7221 out=419 | trace_id=6aa2e5686f44f44a6b span_id=efe7dac8c78d3615 session_id=aegis-sp-b-d20dd3c request_id=9264902f-1856-4d7c |
| 17:14:39.591 | runtime-span | span | SSM.GetParameter | trace_id=6aa2e5686f44f44a6b span_id=f2d169c65b83031e session_id=aegis-sp-b-d20dd3c |
| 17:14:39.627 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2e5686f44f44a6b span_id=8bf285a14a78ffee session_id=aegis-sp-b-d20dd3c |
| 17:14:45.000 | worm | evidence | INTENT benefits-determination seq=0 chain=881fc0f03a1d… | trace_id=6aa2e5686f44f44a6b session_id=aegis-sp-b-d20dd3c request_id=6a7f646e-08aa-4bb6 tenant=sp-b |
| 17:14:45.075 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2e5686f44f44a6b span_id=1a18bfb7589636b0 session_id=aegis-sp-b-d20dd3c |
| 17:14:45.083 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2e5686f44f44a6b span_id=df5fab977a28d5dd session_id=aegis-sp-b-d20dd3c |
| 17:14:45.091 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa2e5686f44f44a6b span_id=6a90354755a7429f session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:45.092 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa2e5686f44f44a6b span_id=4ff559c446b4615a session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:45.093 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa2e5686f44f44a6b span_id=d5899daaecca8ed0 session_id=aegis-sp-b-d20dd3c |
| 17:14:45.093 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa2e5686f44f44a6b span_id=e815dfafd4c5f99f session_id=aegis-sp-b-d20dd3c |
| 17:14:45.148 | runtime-span | lambda-segment | ben-fpd-tenant-interceptor/LambdaService | trace_id=6aa2e5686f44f44a6b span_id=0e3f67bc1fede1fa |
| 17:14:45.153 | runtime-span | lambda-segment | ben-fpd-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=0f3ef487f9f9684b |
| 17:14:45.204 | runtime-span | lambda-segment | ben-fpd-tenant-interceptor/LambdaService | trace_id=6aa2e5686f44f44a6b span_id=1e39576a15ebeb3f |
| 17:14:45.212 | runtime-span | lambda-segment | ben-fpd-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=20e2758d43e75d23 |
| 17:14:45.336 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=5b6f949ede505756 |
| 17:14:45.339 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060485339,"body":{"isError":false,"lo | session_id=aegis-sp-b-d20dd3c trace_id=6aa2e5686f44f44a6b |
| 17:14:45.344 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060485344,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:45.396 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=25abb5dd19e7fa62 |
| 17:14:45.401 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060485401,"body":{"isError":false,"lo | session_id=aegis-sp-b-d20dd3c trace_id=6aa2e5686f44f44a6b |
| 17:14:45.407 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060485407,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:45.444 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060485444,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:45.459 | runtime-span | lambda-segment | ben-fpd-request-signoff/LambdaService | trace_id=6aa2e5686f44f44a6b span_id=4198a9d3a7736120 |
| 17:14:45.464 | runtime-span | lambda-segment | ben-fpd-request-signoff/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=217646fffff2d727 |
| 17:14:45.480 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060485480,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:45.486 | lambda | call | request_signoff -> requested=False | trace_id=6aa2e5686f44f44a6b session_id=aegis-sp-b-d20dd3c request_id=fa3b0272-fced-4bf8 tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:45.486 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=d34d694d6cb0236e |
| 17:14:45.491 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060485491,"body":{"isError":false,"re | trace_id=6aa2e5686f44f44a6b |
| 17:14:45.491 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060485491,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:45.505 | runtime-span | lambda-segment | ben-fpd-write-audit/LambdaService | trace_id=6aa2e5686f44f44a6b span_id=007e58c00a652ecc |
| 17:14:45.509 | runtime-span | lambda-segment | ben-fpd-write-audit/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=ae3fae1c37355c09 |
| 17:14:45.981 | lambda | call | write_audit -> stored=True | trace_id=6aa2e5686f44f44a6b session_id=aegis-sp-b-d20dd3c request_id=6a7f646e-08aa-4bb6 tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:45.982 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2e5686f44f44a6b span_id=5ab387437460b44a |
| 17:14:45.985 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060485985,"body":{"isError":false,"re | trace_id=6aa2e5686f44f44a6b |
| 17:14:45.986 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpd-ben-gw-ss91naozai","event_timestamp":1789060485986,"body":{"isError":false,"lo | trace_id=6aa2e5686f44f44a6b |
| 17:14:45.991 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2e5686f44f44a6b span_id=ebb9eb9dfe91d83e session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:45.992 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8037 out=422 | trace_id=6aa2e5686f44f44a6b span_id=091da62f76369e83 session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:45.993 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8037 out=422 | trace_id=6aa2e5686f44f44a6b span_id=6f1a3ca7ec4dcba1 session_id=aegis-sp-b-d20dd3c request_id=af3aeb56-ad99-4e35 |
| 17:14:45.994 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2e5686f44f44a6b span_id=6f2803e1da3df740 session_id=aegis-sp-b-d20dd3c |
| 17:14:46.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8037 out=422 masked_before_model=True | request_id=af3aeb56-ad99-4e35 session_id=aegis-sp-b-d20dd3c tenant=sp-b case_id=OBS-SPB-F752B |
| 17:14:54.676 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2e5686f44f44a6b span_id=aa1ab2739d5c1497 session_id=aegis-sp-b-d20dd3c |
| 17:14:54.683 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa2e5686f44f44a6b span_id=12dec2986cd4f934 session_id=aegis-sp-b-d20dd3c |
| 17:14:54.688 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2e5686f44f44a6b span_id=5f658dc66c62df34 session_id=aegis-sp-b-d20dd3c |
