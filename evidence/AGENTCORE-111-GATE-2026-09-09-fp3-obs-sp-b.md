# Case trace — `OBS-SPB-1C78F` (tenant `sp-b`)

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
| sessions | ['aegis-sp-b-d6cd8f1399da487da684158d037fac0b'] |
| single_tenant | True |
| tenants_seen | ['sp-b'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 18:29:14.313 | lambda | call | ingest_application -> ingested=True | trace_id=6aa1a5794652d2a549 request_id=9b705118-0f85-4249 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:14.769 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa1a57a58e1543e19 span_id=bedfcac2922d2f96 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:15.273 | runtime-span | runtime-http | POST /invocations | trace_id=6aa1a57a58e1543e19 span_id=2187ca88dfc0b7eb session_id=aegis-sp-b-d6cd8f1 |
| 18:29:15.341 | runtime-span | span | SSM.GetParameter | trace_id=6aa1a57a58e1543e19 span_id=d6e2c40443c30c9f session_id=aegis-sp-b-d6cd8f1 |
| 18:29:15.381 | runtime-span | span | SSM.GetParameter | trace_id=6aa1a57a58e1543e19 span_id=04fb4d5b05ed298d session_id=aegis-sp-b-d6cd8f1 |
| 18:29:15.426 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa1a57a58e1543e19 span_id=fce48297f37a26f2 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:15.472 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa1a57a58e1543e19 span_id=4f2b155ecb103982 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:15.550 | runtime-span | span | mcp.session | trace_id=6aa1a57a58e1543e19 span_id=6b2c904e43a71fa5 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:15.675 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa1a57a58e1543e19 span_id=4b4d1f1f742b5169 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:15.900 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaService | trace_id=6aa1a57a58e1543e19 span_id=0f78a85a303a0d1f |
| 18:29:15.905 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=02beeb1abb10bf45 |
| 18:29:15.905 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=9c8aba52da98a26a |
| 18:29:15.909 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978555909,"body":{"isError":false,"lo | session_id=aegis-sp-b-d6cd8f1 trace_id=6aa1a57a58e1543e19 |
| 18:29:15.912 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978555912,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:15.991 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978555991,"body":{"isError":false,"re | trace_id=6aa1a57a58e1543e19 |
| 18:29:15.997 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=33241 out=2134 | trace_id=6aa1a57a58e1543e19 span_id=37a03bd762fa66da session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:15.998 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1a57a58e1543e19 span_id=fabd0974f97117c0 session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:15.999 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5344 out=218 | trace_id=6aa1a57a58e1543e19 span_id=fc67f298e649ad85 session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:16.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5344 out=218 masked_before_model=True | request_id=15f3ee5c-20f0-4ff2 session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:16.001 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5344 out=218 | trace_id=6aa1a57a58e1543e19 span_id=db013dc5ade554d5 session_id=aegis-sp-b-d6cd8f1 request_id=15f3ee5c-20f0-4ff2 |
| 18:29:16.002 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a57a58e1543e19 span_id=0380fba2754bd157 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:19.645 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a57a58e1543e19 span_id=57c02ebed6c39969 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:19.659 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1a57a58e1543e19 span_id=f05fb947f6c9a874 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:19.686 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa1a57a58e1543e19 span_id=f89d8170b69fdc0a session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:19.686 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa1a57a58e1543e19 span_id=3a86d0fa58089ade session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:19.687 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa1a57a58e1543e19 span_id=fa7beae83032edb9 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:19.688 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa1a57a58e1543e19 span_id=bb2b9f8a5bc1d154 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:19.796 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaService | trace_id=6aa1a57a58e1543e19 span_id=1f7dd646a0f9ba78 |
| 18:29:19.802 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=72d3964b1c5e6804 |
| 18:29:19.806 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaService | trace_id=6aa1a57a58e1543e19 span_id=52ece0cf3b343140 |
| 18:29:19.817 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=70c9b2d319d9b69f |
| 18:29:19.979 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=183438629d7eeb2e |
| 18:29:19.982 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978559982,"body":{"isError":false,"lo | session_id=aegis-sp-b-d6cd8f1 trace_id=6aa1a57a58e1543e19 |
| 18:29:19.985 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978559985,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:20.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5989 out=395 masked_before_model=True | request_id=ba5a0409-8e14-4f04 session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:20.001 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=773c08dad9a6e1bd |
| 18:29:20.005 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978560005,"body":{"isError":false,"lo | session_id=aegis-sp-b-d6cd8f1 trace_id=6aa1a57a58e1543e19 |
| 18:29:20.009 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978560009,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:20.059 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978560059,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:20.088 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978560088,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:20.089 | runtime-span | lambda-segment | ben-fp3-intake-application/LambdaService | trace_id=6aa1a57a58e1543e19 span_id=6bf62a17be1536d4 |
| 18:29:20.096 | runtime-span | lambda-segment | ben-fp3-intake-application/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=6b0a9bfa35507971 |
| 18:29:20.112 | runtime-span | lambda-segment | ben-fp3-mask-pii/LambdaService | trace_id=6aa1a57a58e1543e19 span_id=19b628d9e75445d9 |
| 18:29:20.116 | runtime-span | lambda-segment | ben-fp3-mask-pii/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=36871fc4cb47ec40 |
| 18:29:20.267 | lambda | call | intake_application -> ok | trace_id=6aa1a57a58e1543e19 session_id=aegis-sp-b-d6cd8f1 request_id=40c62668-e09b-4de3 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:20.267 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=80891b7b7054c6a8 |
| 18:29:20.272 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978560272,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:20.272 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978560272,"body":{"isError":false,"re | trace_id=6aa1a57a58e1543e19 |
| 18:29:20.561 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa1a57a58e1543e19 session_id=aegis-sp-b-d6cd8f1 request_id=647b6a5b-3e2a-4326 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:20.561 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=bbbcba5a4e119b12 |
| 18:29:20.565 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978560565,"body":{"isError":false,"re | trace_id=6aa1a57a58e1543e19 |
| 18:29:20.565 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978560565,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:20.570 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1a57a58e1543e19 span_id=507204b0823dacd2 session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:20.571 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5989 out=395 | trace_id=6aa1a57a58e1543e19 span_id=2355c31e25b3af9b session_id=aegis-sp-b-d6cd8f1 request_id=ba5a0409-8e14-4f04 |
| 18:29:20.571 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5989 out=395 | trace_id=6aa1a57a58e1543e19 span_id=133640bd7075d5e6 session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:20.572 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a57a58e1543e19 span_id=dcc97624e43534c1 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:25.516 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a57a58e1543e19 span_id=d5297008282eef0a session_id=aegis-sp-b-d6cd8f1 |
| 18:29:25.522 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1a57a58e1543e19 span_id=ea8b739260acf9da session_id=aegis-sp-b-d6cd8f1 |
| 18:29:25.529 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa1a57a58e1543e19 span_id=a1366a56e8e1a01a session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:25.530 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa1a57a58e1543e19 span_id=9a93f35527eb44ea session_id=aegis-sp-b-d6cd8f1 |
| 18:29:25.624 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaService | trace_id=6aa1a57a58e1543e19 span_id=50d3ee1998e28d73 |
| 18:29:25.633 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=ffdbade575fb6443 |
| 18:29:25.788 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=a8c73667cad9a9b4 |
| 18:29:25.791 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978565791,"body":{"isError":false,"lo | session_id=aegis-sp-b-d6cd8f1 trace_id=6aa1a57a58e1543e19 |
| 18:29:25.796 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978565796,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:25.876 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978565876,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:25.934 | runtime-span | lambda-segment | ben-fp3-assess-eligibility/LambdaService | trace_id=6aa1a57a58e1543e19 span_id=5fbc6c5448649248 |
| 18:29:25.946 | runtime-span | lambda-segment | ben-fp3-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=d86cfd8cde780bb6 |
| 18:29:25.984 | lambda | call | assess_eligibility -> ok | trace_id=6aa1a57a58e1543e19 session_id=aegis-sp-b-d6cd8f1 request_id=eaa29afa-f99e-4ebe tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:25.984 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=fe47d048137e510f |
| 18:29:25.990 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978565990,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:25.990 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978565990,"body":{"isError":false,"re | trace_id=6aa1a57a58e1543e19 |
| 18:29:25.995 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1a57a58e1543e19 span_id=ab347502c5f243aa session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:25.996 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6615 out=569 | trace_id=6aa1a57a58e1543e19 span_id=93222c266f154dd4 session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:25.997 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a57a58e1543e19 span_id=7a868593efafce63 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:25.997 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6615 out=569 | trace_id=6aa1a57a58e1543e19 span_id=631e3fb7e7ff0c5e session_id=aegis-sp-b-d6cd8f1 request_id=3f436a6d-f59c-4876 |
| 18:29:26.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6615 out=569 masked_before_model=True | request_id=3f436a6d-f59c-4876 session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:32.484 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a57a58e1543e19 span_id=19613208943b639b session_id=aegis-sp-b-d6cd8f1 |
| 18:29:32.492 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1a57a58e1543e19 span_id=5f79a263abed8ef4 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:32.522 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa1a57a58e1543e19 span_id=14cc7d3b6c1902d6 session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:32.523 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa1a57a58e1543e19 span_id=5c6fb9b3b55f0447 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:32.663 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaService | trace_id=6aa1a57a58e1543e19 span_id=2d654564ef20a6a8 |
| 18:29:32.667 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=8038a340f1e588a1 |
| 18:29:32.841 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=4a1571dd9ec836a5 |
| 18:29:32.845 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978572845,"body":{"isError":false,"lo | session_id=aegis-sp-b-d6cd8f1 trace_id=6aa1a57a58e1543e19 |
| 18:29:32.849 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978572849,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:32.931 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978572931,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:32.963 | runtime-span | lambda-segment | ben-fp3-core-tools/LambdaService | trace_id=6aa1a57a58e1543e19 span_id=3647dfd880be595d |
| 18:29:32.969 | runtime-span | lambda-segment | ben-fp3-core-tools/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=855035e44778f0a8 |
| 18:29:33.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7233 out=433 masked_before_model=True | request_id=aa7fe93b-3924-478e session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:33.011 | lambda | call | benefits_core -> committed=False | trace_id=6aa1a57a58e1543e19 session_id=aegis-sp-b-d6cd8f1 request_id=f078df86-4554-4f6a tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:33.012 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=7ccb3f6c57894b13 |
| 18:29:33.017 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978573017,"body":{"isError":false,"re | trace_id=6aa1a57a58e1543e19 |
| 18:29:33.017 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978573017,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:33.023 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1a57a58e1543e19 span_id=1d1e295f80766f88 session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:33.024 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7233 out=433 | trace_id=6aa1a57a58e1543e19 span_id=d92ba48c6c48d189 session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:33.025 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7233 out=433 | trace_id=6aa1a57a58e1543e19 span_id=5b5af8e9494b499a session_id=aegis-sp-b-d6cd8f1 request_id=aa7fe93b-3924-478e |
| 18:29:33.030 | runtime-span | span | SSM.GetParameter | trace_id=6aa1a57a58e1543e19 span_id=23e9060861485d5b session_id=aegis-sp-b-d6cd8f1 |
| 18:29:33.056 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a57a58e1543e19 span_id=4b9caddf0fe5614f session_id=aegis-sp-b-d6cd8f1 |
| 18:29:39.000 | worm | evidence | INTENT benefits-determination seq=0 chain=fd7ba067fbd6… | trace_id=6aa1a57a58e1543e19 session_id=aegis-sp-b-d6cd8f1 request_id=b2c250a7-62f6-4aec tenant=sp-b |
| 18:29:39.188 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a57a58e1543e19 span_id=7c779f0d5f88ab85 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:39.195 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1a57a58e1543e19 span_id=02a5da059068e043 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:39.224 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa1a57a58e1543e19 span_id=6452ba43ddef5044 session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:39.225 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa1a57a58e1543e19 span_id=a73a912a6abb4669 session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:39.226 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa1a57a58e1543e19 span_id=0d6ca751cdb8d146 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:39.226 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa1a57a58e1543e19 span_id=71a61376c08a95e4 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:39.326 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaService | trace_id=6aa1a57a58e1543e19 span_id=173c4217e5b33a0e |
| 18:29:39.331 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=e20fc47da0b71cb3 |
| 18:29:39.338 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaService | trace_id=6aa1a57a58e1543e19 span_id=6751bd992cd096fa |
| 18:29:39.343 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=8dd84761c55e257e |
| 18:29:39.500 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=f17f627f7ce0da92 |
| 18:29:39.503 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978579503,"body":{"isError":false,"lo | session_id=aegis-sp-b-d6cd8f1 trace_id=6aa1a57a58e1543e19 |
| 18:29:39.503 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=db3d25e43ba1932e |
| 18:29:39.506 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978579506,"body":{"isError":false,"lo | session_id=aegis-sp-b-d6cd8f1 trace_id=6aa1a57a58e1543e19 |
| 18:29:39.509 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978579509,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:39.511 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978579511,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:39.595 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978579595,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:39.602 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978579602,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:39.618 | runtime-span | lambda-segment | ben-fp3-write-audit/LambdaService | trace_id=6aa1a57a58e1543e19 span_id=4f4ea4e03430ecb3 |
| 18:29:39.624 | runtime-span | lambda-segment | ben-fp3-write-audit/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=34660ebbfbed3101 |
| 18:29:39.625 | runtime-span | lambda-segment | ben-fp3-request-signoff/LambdaService | trace_id=6aa1a57a58e1543e19 span_id=4a57cf2078a0e94e |
| 18:29:39.632 | runtime-span | lambda-segment | ben-fp3-request-signoff/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=0ff3129b247506be |
| 18:29:39.657 | lambda | call | request_signoff -> requested=False | trace_id=6aa1a57a58e1543e19 session_id=aegis-sp-b-d6cd8f1 request_id=8a308b32-e4b1-49b5 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:39.657 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=e148614e7169ee3e |
| 18:29:39.662 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978579662,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:39.662 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978579662,"body":{"isError":false,"re | trace_id=6aa1a57a58e1543e19 |
| 18:29:40.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8060 out=519 masked_before_model=True | request_id=6d39c056-11b9-4134 session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:40.099 | lambda | call | write_audit -> stored=True | trace_id=6aa1a57a58e1543e19 session_id=aegis-sp-b-d6cd8f1 request_id=b2c250a7-62f6-4aec tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:40.100 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a57a58e1543e19 span_id=cba8bcaee4b3ed1c |
| 18:29:40.105 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978580105,"body":{"isError":false,"re | trace_id=6aa1a57a58e1543e19 |
| 18:29:40.106 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978580106,"body":{"isError":false,"lo | trace_id=6aa1a57a58e1543e19 |
| 18:29:40.111 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1a57a58e1543e19 span_id=35a5e323519bc79c session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:40.113 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8060 out=519 | trace_id=6aa1a57a58e1543e19 span_id=d910ad4080537e39 session_id=aegis-sp-b-d6cd8f1 request_id=6d39c056-11b9-4134 |
| 18:29:40.113 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8060 out=519 | trace_id=6aa1a57a58e1543e19 span_id=1cacbdf16f6f81ae session_id=aegis-sp-b-d6cd8f1 tenant=sp-b case_id=OBS-SPB-1C78F |
| 18:29:40.114 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a57a58e1543e19 span_id=dc99f6d24281e721 session_id=aegis-sp-b-d6cd8f1 |
| 18:29:50.284 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a57a58e1543e19 span_id=467e91fd24db464a session_id=aegis-sp-b-d6cd8f1 |
| 18:29:50.290 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa1a57a58e1543e19 span_id=3ce693fee90f97be session_id=aegis-sp-b-d6cd8f1 |
| 18:29:50.295 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1a57a58e1543e19 span_id=a96533a84fdcf5b7 session_id=aegis-sp-b-d6cd8f1 |
