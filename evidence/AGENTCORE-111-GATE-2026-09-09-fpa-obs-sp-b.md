# Case trace — `OBS-SPB-50AB0` (tenant `sp-b`)

| metric | value |
|---|---|
| agent_spans | 1 |
| gateway_requests | 33 |
| lambda_calls | 7 |
| lambda_calls_joined_to_evidence | 6 |
| masked_before_model_all | True |
| model_invocations | 6 |
| model_invocations_joined_to_spans | 6 |
| model_invocations_tagged_tenant | 6 |
| model_spans | 12 |
| sessions | ['aegis-sp-b-434b204f26464583bb2404d75fa59c74'] |
| single_tenant | True |
| tenants_seen | ['sp-b'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 07:11:27.199 | lambda | call | ingest_application -> ingested=True | trace_id=6aa2581e282f40254b request_id=4d4d74bf-658d-43cb tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:27.751 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa2581f34368ebf52 span_id=14421fc7c6ee0286 session_id=aegis-sp-b-434b204 |
| 07:11:28.382 | runtime-span | runtime-http | POST /invocations | trace_id=6aa2581f34368ebf52 span_id=204537fc4d27d6fe session_id=aegis-sp-b-434b204 |
| 07:11:28.476 | runtime-span | span | SSM.GetParameter | trace_id=6aa2581f34368ebf52 span_id=6022be9843054450 session_id=aegis-sp-b-434b204 |
| 07:11:28.522 | runtime-span | span | SSM.GetParameter | trace_id=6aa2581f34368ebf52 span_id=54fac97c577a7df2 session_id=aegis-sp-b-434b204 |
| 07:11:28.577 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa2581f34368ebf52 span_id=e7f862c3e45d4367 session_id=aegis-sp-b-434b204 |
| 07:11:28.629 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa2581f34368ebf52 span_id=9cdd073e23824767 session_id=aegis-sp-b-434b204 |
| 07:11:28.728 | runtime-span | span | mcp.session | trace_id=6aa2581f34368ebf52 span_id=572af7928f1f4ba3 session_id=aegis-sp-b-434b204 |
| 07:11:28.868 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa2581f34368ebf52 span_id=f0b42252062abd03 session_id=aegis-sp-b-434b204 |
| 07:11:29.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5345 out=128 masked_before_model=True | request_id=6d44d00c-9b9d-4a3a session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:29.089 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaService | trace_id=6aa2581f34368ebf52 span_id=14ce6a715eeb9a2a |
| 07:11:29.122 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024289122,"body":{"isError":false,"lo | session_id=aegis-sp-b-434b204 trace_id=6aa2581f34368ebf52 |
| 07:11:29.125 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024289125,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:29.204 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024289204,"body":{"isError":false,"re | trace_id=6aa2581f34368ebf52 |
| 07:11:29.212 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2581f34368ebf52 span_id=37eb3eaa794ee7b0 session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:29.212 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=38744 out=2096 | trace_id=6aa2581f34368ebf52 span_id=17712e7ad910dd6a session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:29.214 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5345 out=128 | trace_id=6aa2581f34368ebf52 span_id=401aee60661c4f60 session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:29.225 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2581f34368ebf52 span_id=e4f381a5acb74e6a session_id=aegis-sp-b-434b204 |
| 07:11:29.225 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5345 out=128 | trace_id=6aa2581f34368ebf52 span_id=1670cb55814dde9b session_id=aegis-sp-b-434b204 request_id=6d44d00c-9b9d-4a3a |
| 07:11:32.664 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2581f34368ebf52 span_id=e58c2f57bf55aefc session_id=aegis-sp-b-434b204 |
| 07:11:32.680 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2581f34368ebf52 span_id=0623f5242cb9a7af session_id=aegis-sp-b-434b204 |
| 07:11:32.709 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa2581f34368ebf52 span_id=e81c5769a3aeba99 session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:32.710 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa2581f34368ebf52 span_id=72afcf7b0f44634e session_id=aegis-sp-b-434b204 |
| 07:11:32.808 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaService | trace_id=6aa2581f34368ebf52 span_id=2b4417cc69d46374 |
| 07:11:33.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5551 out=122 masked_before_model=True | request_id=ee9f6a53-a233-4113 session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:33.000 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024293000,"body":{"isError":false,"lo | session_id=aegis-sp-b-434b204 trace_id=6aa2581f34368ebf52 |
| 07:11:33.004 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024293004,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:33.078 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024293078,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:33.108 | runtime-span | lambda-segment | ben-fpa-intake-application/LambdaService | trace_id=6aa2581f34368ebf52 span_id=22fc574f8110e6f5 |
| 07:11:33.113 | runtime-span | lambda-segment | ben-fpa-intake-application/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=b2b5c5f1ed4f16bc |
| 07:11:33.289 | lambda | call | intake_application -> ok | trace_id=6aa2581f34368ebf52 session_id=aegis-sp-b-434b204 request_id=29cb3351-315a-484e tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:33.289 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=ea92b9e253f1dec1 |
| 07:11:33.293 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024293293,"body":{"isError":false,"re | trace_id=6aa2581f34368ebf52 |
| 07:11:33.294 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024293294,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:33.299 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2581f34368ebf52 span_id=be43d7d31a214689 session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:33.300 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5551 out=122 | trace_id=6aa2581f34368ebf52 span_id=52ef19066f40f71c session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:33.301 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2581f34368ebf52 span_id=06ad5135095ddf6b session_id=aegis-sp-b-434b204 |
| 07:11:33.301 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5551 out=122 | trace_id=6aa2581f34368ebf52 span_id=450d29bd6ff6ded3 session_id=aegis-sp-b-434b204 request_id=ee9f6a53-a233-4113 |
| 07:11:36.194 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2581f34368ebf52 span_id=a8f210d4052baba5 session_id=aegis-sp-b-434b204 |
| 07:11:36.200 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2581f34368ebf52 span_id=7d460626dca125c9 session_id=aegis-sp-b-434b204 |
| 07:11:36.208 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa2581f34368ebf52 span_id=9dd7e9402462280e session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:36.209 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa2581f34368ebf52 span_id=d59fe853aa616e5d session_id=aegis-sp-b-434b204 |
| 07:11:36.305 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaService | trace_id=6aa2581f34368ebf52 span_id=7d1ade3ee56b3926 |
| 07:11:36.310 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=3ecfdd55c7d912ef |
| 07:11:36.479 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=fe9987792a46fdbb |
| 07:11:36.482 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024296482,"body":{"isError":false,"lo | session_id=aegis-sp-b-434b204 trace_id=6aa2581f34368ebf52 |
| 07:11:36.485 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024296485,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:36.558 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024296558,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:36.586 | runtime-span | lambda-segment | ben-fpa-mask-pii/LambdaService | trace_id=6aa2581f34368ebf52 span_id=749eaa5af92b9a94 |
| 07:11:36.592 | runtime-span | lambda-segment | ben-fpa-mask-pii/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=7c3fd4be07282279 |
| 07:11:37.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5978 out=399 masked_before_model=True | request_id=81b30f77-21c7-42e6 session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:37.073 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa2581f34368ebf52 session_id=aegis-sp-b-434b204 request_id=a68276c2-f6b1-4940 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:37.073 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=65678610929ddbf9 |
| 07:11:37.078 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024297078,"body":{"isError":false,"re | trace_id=6aa2581f34368ebf52 |
| 07:11:37.078 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024297078,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:37.083 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2581f34368ebf52 span_id=8602366fd1e63874 session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:37.084 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5978 out=399 | trace_id=6aa2581f34368ebf52 span_id=d8fc889956edc0d5 session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:37.085 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2581f34368ebf52 span_id=76b701dfbdc2dbc9 session_id=aegis-sp-b-434b204 |
| 07:11:37.085 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5978 out=399 | trace_id=6aa2581f34368ebf52 span_id=b7277fd60ebdec3d session_id=aegis-sp-b-434b204 request_id=81b30f77-21c7-42e6 |
| 07:11:43.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6608 out=567 masked_before_model=True | request_id=cb19ffab-b112-49f9 session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:43.193 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2581f34368ebf52 span_id=02f873e76036416b session_id=aegis-sp-b-434b204 |
| 07:11:43.199 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2581f34368ebf52 span_id=fa5e179187ec66d3 session_id=aegis-sp-b-434b204 |
| 07:11:43.234 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa2581f34368ebf52 span_id=976c37ec47f35939 session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:43.235 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa2581f34368ebf52 span_id=78b8164a371cc3b1 session_id=aegis-sp-b-434b204 |
| 07:11:43.335 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaService | trace_id=6aa2581f34368ebf52 span_id=637f71ad45d538c6 |
| 07:11:43.342 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=ad2301b25433ff20 |
| 07:11:43.518 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=776bf80c82b2b713 |
| 07:11:43.521 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024303521,"body":{"isError":false,"lo | session_id=aegis-sp-b-434b204 trace_id=6aa2581f34368ebf52 |
| 07:11:43.524 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024303524,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:43.598 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024303598,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:43.619 | runtime-span | lambda-segment | ben-fpa-assess-eligibility/LambdaService | trace_id=6aa2581f34368ebf52 span_id=0b553111c7927711 |
| 07:11:43.624 | runtime-span | lambda-segment | ben-fpa-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=43fac21ca4184d42 |
| 07:11:43.658 | lambda | call | assess_eligibility -> ok | trace_id=6aa2581f34368ebf52 session_id=aegis-sp-b-434b204 request_id=a714bb1e-70d0-4ea1 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:43.659 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=57e65b3eb553c917 |
| 07:11:43.662 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024303662,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:43.662 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024303662,"body":{"isError":false,"re | trace_id=6aa2581f34368ebf52 |
| 07:11:43.668 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2581f34368ebf52 span_id=b7c8fc22f1a6f758 session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:43.669 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6608 out=567 | trace_id=6aa2581f34368ebf52 span_id=74a2f8d06b79c788 session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:43.670 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6608 out=567 | trace_id=6aa2581f34368ebf52 span_id=e929f87a57b24566 session_id=aegis-sp-b-434b204 request_id=cb19ffab-b112-49f9 |
| 07:11:43.677 | runtime-span | span | SSM.GetParameter | trace_id=6aa2581f34368ebf52 span_id=eb292a3dceb0cc61 session_id=aegis-sp-b-434b204 |
| 07:11:43.712 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2581f34368ebf52 span_id=a6bda06cdfea6e54 session_id=aegis-sp-b-434b204 |
| 07:11:50.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7223 out=419 masked_before_model=True | request_id=01b63b50-5ec0-46cc session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:50.026 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2581f34368ebf52 span_id=d8f0110b1c579c6b session_id=aegis-sp-b-434b204 |
| 07:11:50.032 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2581f34368ebf52 span_id=3bf0bc1c5eed8519 session_id=aegis-sp-b-434b204 |
| 07:11:50.056 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa2581f34368ebf52 span_id=9665c68e5c4ed23e session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:50.057 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa2581f34368ebf52 span_id=08b13416cb89d0f7 session_id=aegis-sp-b-434b204 |
| 07:11:50.160 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaService | trace_id=6aa2581f34368ebf52 span_id=332f0d91ddc7049c |
| 07:11:50.166 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=dbbafadd05457e18 |
| 07:11:50.339 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=868dc69f296664b2 |
| 07:11:50.342 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024310342,"body":{"isError":false,"lo | session_id=aegis-sp-b-434b204 trace_id=6aa2581f34368ebf52 |
| 07:11:50.346 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024310346,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:50.423 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024310423,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:50.443 | runtime-span | lambda-segment | ben-fpa-core-tools/LambdaService | trace_id=6aa2581f34368ebf52 span_id=2ed5ffa821f0a487 |
| 07:11:50.449 | runtime-span | lambda-segment | ben-fpa-core-tools/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=c9fcee7e9208c482 |
| 07:11:50.469 | lambda | call | benefits_core -> committed=False | trace_id=6aa2581f34368ebf52 session_id=aegis-sp-b-434b204 request_id=bad9dcec-3b5c-4e49 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:50.470 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=c5358d7c46cf0937 |
| 07:11:50.474 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024310474,"body":{"isError":false,"re | trace_id=6aa2581f34368ebf52 |
| 07:11:50.474 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024310474,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:50.479 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2581f34368ebf52 span_id=ab2d8d4443b61cc9 session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:50.481 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7223 out=419 | trace_id=6aa2581f34368ebf52 span_id=f548102ae04c353d session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:50.482 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7223 out=419 | trace_id=6aa2581f34368ebf52 span_id=634d12da1952cba2 session_id=aegis-sp-b-434b204 request_id=01b63b50-5ec0-46cc |
| 07:11:50.483 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2581f34368ebf52 span_id=ae588b7e710f5e07 session_id=aegis-sp-b-434b204 |
| 07:11:56.000 | worm | evidence | INTENT benefits-determination seq=0 chain=87cc06e84c44… | trace_id=6aa2581f34368ebf52 session_id=aegis-sp-b-434b204 request_id=c185062b-9418-4d72 tenant=sp-b |
| 07:11:56.169 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2581f34368ebf52 span_id=ac128aff008e26db session_id=aegis-sp-b-434b204 |
| 07:11:56.174 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2581f34368ebf52 span_id=423dce6d35f19c46 session_id=aegis-sp-b-434b204 |
| 07:11:56.204 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa2581f34368ebf52 span_id=8173b7c889dd4906 session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:56.205 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa2581f34368ebf52 span_id=96c1287930cc371b session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:56.205 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa2581f34368ebf52 span_id=dfd6f168c4d1ddf2 session_id=aegis-sp-b-434b204 |
| 07:11:56.206 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa2581f34368ebf52 span_id=da458c543ca73f11 session_id=aegis-sp-b-434b204 |
| 07:11:56.309 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaService | trace_id=6aa2581f34368ebf52 span_id=17926ccd24d4c594 |
| 07:11:56.315 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=1c9ae87219b82906 |
| 07:11:56.334 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaService | trace_id=6aa2581f34368ebf52 span_id=6624ebd1e72ed5dc |
| 07:11:56.484 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=14611056fa3882e5 |
| 07:11:56.488 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024316488,"body":{"isError":false,"lo | session_id=aegis-sp-b-434b204 trace_id=6aa2581f34368ebf52 |
| 07:11:56.491 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024316491,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:56.503 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=a5562b5a677921f3 |
| 07:11:56.559 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024316559,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:56.586 | runtime-span | lambda-segment | ben-fpa-write-audit/LambdaService | trace_id=6aa2581f34368ebf52 span_id=51985a033a568349 |
| 07:11:56.591 | runtime-span | lambda-segment | ben-fpa-write-audit/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=f4e262f9536cb5ac |
| 07:11:56.664 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=64ccdaf34394a9ff |
| 07:11:56.667 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024316667,"body":{"isError":false,"lo | session_id=aegis-sp-b-434b204 trace_id=6aa2581f34368ebf52 |
| 07:11:56.670 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024316670,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:56.741 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024316741,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:56.765 | runtime-span | lambda-segment | ben-fpa-request-signoff/LambdaService | trace_id=6aa2581f34368ebf52 span_id=3a128c923aa75219 |
| 07:11:56.775 | runtime-span | lambda-segment | ben-fpa-request-signoff/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=8ea98c4d08e49306 |
| 07:11:56.795 | lambda | call | request_signoff -> requested=False | trace_id=6aa2581f34368ebf52 session_id=aegis-sp-b-434b204 request_id=109dd296-bd9b-4af9 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:56.796 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=e9cdf20835ca992b |
| 07:11:56.799 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024316799,"body":{"isError":false,"re | trace_id=6aa2581f34368ebf52 |
| 07:11:56.800 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024316800,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:57.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8039 out=461 masked_before_model=True | request_id=f4ac1483-f58f-4f9d session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:57.097 | lambda | call | write_audit -> stored=True | trace_id=6aa2581f34368ebf52 session_id=aegis-sp-b-434b204 request_id=c185062b-9418-4d72 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:57.102 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2581f34368ebf52 span_id=98816801dcad1073 |
| 07:11:57.106 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024317106,"body":{"isError":false,"lo | trace_id=6aa2581f34368ebf52 |
| 07:11:57.106 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024317106,"body":{"isError":false,"re | trace_id=6aa2581f34368ebf52 |
| 07:11:57.112 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2581f34368ebf52 span_id=bc12485b52e41b25 session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:57.113 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8039 out=461 | trace_id=6aa2581f34368ebf52 span_id=5e41356474184dbe session_id=aegis-sp-b-434b204 tenant=sp-b case_id=OBS-SPB-50AB0 |
| 07:11:57.114 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8039 out=461 | trace_id=6aa2581f34368ebf52 span_id=e6c35d11c0943566 session_id=aegis-sp-b-434b204 request_id=f4ac1483-f58f-4f9d |
| 07:11:57.115 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2581f34368ebf52 span_id=106b34ff3dfd5148 session_id=aegis-sp-b-434b204 |
| 07:12:06.642 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2581f34368ebf52 span_id=b3504e4f61fccf92 session_id=aegis-sp-b-434b204 |
| 07:12:06.648 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa2581f34368ebf52 span_id=9183c2daa141bdbb session_id=aegis-sp-b-434b204 |
| 07:12:06.652 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2581f34368ebf52 span_id=d50253a4946fb305 session_id=aegis-sp-b-434b204 |
