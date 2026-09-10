# Case trace — `OBS-SPA-01254` (tenant `sp-a`)

| metric | value |
|---|---|
| agent_spans | 1 |
| gateway_requests | 33 |
| lambda_calls | 7 |
| lambda_calls_joined_to_evidence | 6 |
| masked_before_model_all | True |
| model_invocations | 7 |
| model_invocations_joined_to_spans | 7 |
| model_invocations_tagged_tenant | 7 |
| model_spans | 14 |
| sessions | ['aegis-sp-a-4b6595170adf492897056938b535cc91'] |
| single_tenant | True |
| tenants_seen | ['sp-a'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 07:10:40.516 | lambda | call | ingest_application -> ingested=True | trace_id=6aa257f0615b35011a request_id=721c06d9-10bd-45a6 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:41.064 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa257f0586abaa663 span_id=f84062370ef98ae4 session_id=aegis-sp-a-4b65951 |
| 07:10:41.587 | runtime-span | runtime-http | POST /invocations | trace_id=6aa257f0586abaa663 span_id=fcd76c7cddd8b3ae session_id=aegis-sp-a-4b65951 |
| 07:10:41.656 | runtime-span | span | SSM.GetParameter | trace_id=6aa257f0586abaa663 span_id=04bfe87fb99c1c3a session_id=aegis-sp-a-4b65951 |
| 07:10:41.698 | runtime-span | span | SSM.GetParameter | trace_id=6aa257f0586abaa663 span_id=b1b26ac1de9de93b session_id=aegis-sp-a-4b65951 |
| 07:10:41.756 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa257f0586abaa663 span_id=dfd739860f027f02 session_id=aegis-sp-a-4b65951 |
| 07:10:41.804 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa257f0586abaa663 span_id=6b02b6c2fffe6ced session_id=aegis-sp-a-4b65951 |
| 07:10:41.887 | runtime-span | span | mcp.session | trace_id=6aa257f0586abaa663 span_id=3dedfcd1c95b5830 session_id=aegis-sp-a-4b65951 |
| 07:10:42.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5340 out=138 masked_before_model=True | request_id=b23ec72b-a622-40c4 session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:42.063 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa257f0586abaa663 span_id=9634a681fa2b1b4e session_id=aegis-sp-a-4b65951 |
| 07:10:42.313 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaService | trace_id=6aa257f0586abaa663 span_id=4ed6fe8fd264af82 |
| 07:10:42.321 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=c7bce4f7cd41812a |
| 07:10:42.340 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=ef84a0cad644244d |
| 07:10:42.344 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024242344,"body":{"isError":false,"lo | session_id=aegis-sp-a-4b65951 trace_id=6aa257f0586abaa663 |
| 07:10:42.349 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024242349,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:10:42.434 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024242434,"body":{"isError":false,"re | trace_id=6aa257f0586abaa663 |
| 07:10:42.442 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=46607 out=2116 | trace_id=6aa257f0586abaa663 span_id=6fefb854762c0b0f session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:42.443 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa257f0586abaa663 span_id=8564d6cdb708f0dc session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:42.444 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5340 out=138 | trace_id=6aa257f0586abaa663 span_id=e512a44e88ec91ca session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:42.446 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5340 out=138 | trace_id=6aa257f0586abaa663 span_id=8fc07ac9417dc3b4 session_id=aegis-sp-a-4b65951 request_id=b23ec72b-a622-40c4 |
| 07:10:42.447 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa257f0586abaa663 span_id=f086148b2c9ba7b2 session_id=aegis-sp-a-4b65951 |
| 07:10:47.338 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa257f0586abaa663 span_id=abab0e9a654e87a2 session_id=aegis-sp-a-4b65951 |
| 07:10:47.352 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa257f0586abaa663 span_id=bb1713ce118a3fbe session_id=aegis-sp-a-4b65951 |
| 07:10:47.394 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa257f0586abaa663 span_id=f93d9cb903afd03e session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:47.395 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa257f0586abaa663 span_id=336b95dfb84b0caa session_id=aegis-sp-a-4b65951 |
| 07:10:47.492 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaService | trace_id=6aa257f0586abaa663 span_id=4069bce955760737 |
| 07:10:47.506 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=7eff041fd7f20332 |
| 07:10:47.897 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=933985287add7fe2 |
| 07:10:47.902 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024247902,"body":{"isError":false,"lo | session_id=aegis-sp-a-4b65951 trace_id=6aa257f0586abaa663 |
| 07:10:47.905 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024247905,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:10:47.978 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024247978,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:10:48.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5556 out=120 masked_before_model=True | request_id=2b743746-0380-42cf session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:48.009 | runtime-span | lambda-segment | ben-fpa-intake-application/LambdaService | trace_id=6aa257f0586abaa663 span_id=73c2a57c38113841 |
| 07:10:48.220 | lambda | call | intake_application -> ok | trace_id=6aa257f0586abaa663 session_id=aegis-sp-a-4b65951 request_id=5b30f85d-dfa6-48e9 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:48.226 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024248226,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:10:48.226 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024248226,"body":{"isError":false,"re | trace_id=6aa257f0586abaa663 |
| 07:10:48.231 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa257f0586abaa663 span_id=696521e07766dad6 session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:48.232 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5556 out=120 | trace_id=6aa257f0586abaa663 span_id=064f167aa59cc32b session_id=aegis-sp-a-4b65951 request_id=2b743746-0380-42cf |
| 07:10:48.232 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5556 out=120 | trace_id=6aa257f0586abaa663 span_id=e3679c66b56d9748 session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:48.233 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa257f0586abaa663 span_id=8e9953689867e2a7 session_id=aegis-sp-a-4b65951 |
| 07:10:51.078 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa257f0586abaa663 span_id=558bbbb208508eb5 session_id=aegis-sp-a-4b65951 |
| 07:10:51.085 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa257f0586abaa663 span_id=f42679740dc52a01 session_id=aegis-sp-a-4b65951 |
| 07:10:51.094 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa257f0586abaa663 span_id=f96da9198352c2dc session_id=aegis-sp-a-4b65951 |
| 07:10:51.094 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa257f0586abaa663 span_id=9f13fdf3c2da846e session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:51.188 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaService | trace_id=6aa257f0586abaa663 span_id=26c980b206cbae70 |
| 07:10:51.199 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=ffee349b93467edc |
| 07:10:51.380 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=173dd958f1d70e4b |
| 07:10:51.383 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024251383,"body":{"isError":false,"lo | session_id=aegis-sp-a-4b65951 trace_id=6aa257f0586abaa663 |
| 07:10:51.386 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024251386,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:10:51.461 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024251461,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:10:51.483 | runtime-span | lambda-segment | ben-fpa-mask-pii/LambdaService | trace_id=6aa257f0586abaa663 span_id=36d2f18d557934e7 |
| 07:10:51.985 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa257f0586abaa663 session_id=aegis-sp-a-4b65951 request_id=b2f1b37b-7061-4fc9 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:51.990 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024251990,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:10:51.990 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024251990,"body":{"isError":false,"re | trace_id=6aa257f0586abaa663 |
| 07:10:51.995 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5986 out=399 | trace_id=6aa257f0586abaa663 span_id=94d24a5d88f87b6b session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:51.995 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa257f0586abaa663 span_id=b815a52453a5895a session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:51.996 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa257f0586abaa663 span_id=0afebad811472fad session_id=aegis-sp-a-4b65951 |
| 07:10:51.996 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5986 out=399 | trace_id=6aa257f0586abaa663 span_id=d7eba5eedf65eef9 session_id=aegis-sp-a-4b65951 request_id=3d8cd7a2-6d88-4542 |
| 07:10:52.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5986 out=399 masked_before_model=True | request_id=3d8cd7a2-6d88-4542 session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:56.844 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa257f0586abaa663 span_id=42a2530e4f623234 session_id=aegis-sp-a-4b65951 |
| 07:10:56.851 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa257f0586abaa663 span_id=ea3ac80e3d9b3a7c session_id=aegis-sp-a-4b65951 |
| 07:10:56.860 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa257f0586abaa663 span_id=8fa8f62fc614f1a7 session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:56.861 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa257f0586abaa663 span_id=a2640367dd0183e5 session_id=aegis-sp-a-4b65951 |
| 07:10:56.953 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaService | trace_id=6aa257f0586abaa663 span_id=4bab707f19b4097e |
| 07:10:56.958 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=655a538eb8a89dbb |
| 07:10:57.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6616 out=568 masked_before_model=True | request_id=3a405c33-3df8-4a3a session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:57.132 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=54cf1d31e893bb9e |
| 07:10:57.135 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024257135,"body":{"isError":false,"lo | session_id=aegis-sp-a-4b65951 trace_id=6aa257f0586abaa663 |
| 07:10:57.138 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024257138,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:10:57.214 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024257214,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:10:57.247 | runtime-span | lambda-segment | ben-fpa-assess-eligibility/LambdaService | trace_id=6aa257f0586abaa663 span_id=5b5fc2a2990034d4 |
| 07:10:57.259 | runtime-span | lambda-segment | ben-fpa-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=2a38505c6b11e745 |
| 07:10:57.283 | lambda | call | assess_eligibility -> ok | trace_id=6aa257f0586abaa663 session_id=aegis-sp-a-4b65951 request_id=a1ec9442-03e6-42d2 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:57.283 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=d41497bd3614f13e |
| 07:10:57.288 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024257288,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:10:57.288 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024257288,"body":{"isError":false,"re | trace_id=6aa257f0586abaa663 |
| 07:10:57.293 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa257f0586abaa663 span_id=2e413b1f52af41ae session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:57.294 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6616 out=568 | trace_id=6aa257f0586abaa663 span_id=29aa7f92f8f4a69c session_id=aegis-sp-a-4b65951 request_id=3a405c33-3df8-4a3a |
| 07:10:57.294 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6616 out=568 | trace_id=6aa257f0586abaa663 span_id=5ce9916eb62d7dc3 session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:10:57.300 | runtime-span | span | SSM.GetParameter | trace_id=6aa257f0586abaa663 span_id=43df605fd762a107 session_id=aegis-sp-a-4b65951 |
| 07:10:57.343 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa257f0586abaa663 span_id=da7bf09818a7160b session_id=aegis-sp-a-4b65951 |
| 07:11:04.977 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa257f0586abaa663 span_id=7e54d9e942925eb3 session_id=aegis-sp-a-4b65951 |
| 07:11:04.983 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa257f0586abaa663 span_id=4460edaa3770faf0 session_id=aegis-sp-a-4b65951 |
| 07:11:05.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7231 out=340 masked_before_model=True | request_id=e9febad1-2ced-4d8d session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:11:05.013 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa257f0586abaa663 span_id=a0bb5ba77cb287ba session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:11:05.014 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa257f0586abaa663 span_id=3062be67e29216ee session_id=aegis-sp-a-4b65951 |
| 07:11:05.115 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaService | trace_id=6aa257f0586abaa663 span_id=470917aaa6e8ea92 |
| 07:11:05.322 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024265322,"body":{"isError":false,"lo | session_id=aegis-sp-a-4b65951 trace_id=6aa257f0586abaa663 |
| 07:11:05.328 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024265328,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:11:05.409 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024265409,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:11:05.430 | runtime-span | lambda-segment | ben-fpa-core-tools/LambdaService | trace_id=6aa257f0586abaa663 span_id=68626b07dab416cf |
| 07:11:05.436 | runtime-span | lambda-segment | ben-fpa-core-tools/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=30968905aea947be |
| 07:11:05.459 | lambda | call | benefits_core -> committed=False | trace_id=6aa257f0586abaa663 session_id=aegis-sp-a-4b65951 request_id=3126d744-773a-416c tenant=sp-a case_id=OBS-SPA-01254 |
| 07:11:05.460 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=3a4a8019759acd0c |
| 07:11:05.464 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024265464,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:11:05.464 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024265464,"body":{"isError":false,"re | trace_id=6aa257f0586abaa663 |
| 07:11:05.470 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa257f0586abaa663 span_id=0fa50da136509fe6 session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:11:05.471 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7231 out=340 | trace_id=6aa257f0586abaa663 span_id=8387cac3beb8c913 session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:11:05.472 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa257f0586abaa663 span_id=44a61ead5a08c4ca session_id=aegis-sp-a-4b65951 |
| 07:11:05.472 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7231 out=340 | trace_id=6aa257f0586abaa663 span_id=25d21d457e56b867 session_id=aegis-sp-a-4b65951 request_id=e9febad1-2ced-4d8d |
| 07:11:10.925 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa257f0586abaa663 span_id=013a431dbdc0ce82 session_id=aegis-sp-a-4b65951 |
| 07:11:10.931 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa257f0586abaa663 span_id=7469ccc10fafee3a session_id=aegis-sp-a-4b65951 |
| 07:11:10.941 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa257f0586abaa663 span_id=7cfe9b2223db52fd session_id=aegis-sp-a-4b65951 |
| 07:11:10.941 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa257f0586abaa663 span_id=d9d51a07afa5960f session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:11:10.992 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaService | trace_id=6aa257f0586abaa663 span_id=3f548833c592fedb |
| 07:11:10.998 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=6ec1a86655cdda49 |
| 07:11:11.000 | worm | evidence | INTENT benefits-determination seq=0 chain=286d983fbbbd… | trace_id=6aa257f0586abaa663 session_id=aegis-sp-a-4b65951 request_id=b0f2ae61-e487-4ccc tenant=sp-a |
| 07:11:11.163 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=1ebb526bdb86812a |
| 07:11:11.165 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024271165,"body":{"isError":false,"lo | session_id=aegis-sp-a-4b65951 trace_id=6aa257f0586abaa663 |
| 07:11:11.169 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024271169,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:11:11.242 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024271242,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:11:11.269 | runtime-span | lambda-segment | ben-fpa-write-audit/LambdaService | trace_id=6aa257f0586abaa663 span_id=083b32a6afe9128f |
| 07:11:11.275 | runtime-span | lambda-segment | ben-fpa-write-audit/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=3b9e2ade4e96e411 |
| 07:11:12.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7859 out=109 masked_before_model=True | request_id=71246699-4e9d-4fe5 session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:11:12.076 | lambda | call | write_audit -> stored=True | trace_id=6aa257f0586abaa663 session_id=aegis-sp-a-4b65951 request_id=b0f2ae61-e487-4ccc tenant=sp-a case_id=OBS-SPA-01254 |
| 07:11:12.078 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=67029431fdf4b961 |
| 07:11:12.082 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024272082,"body":{"isError":false,"re | trace_id=6aa257f0586abaa663 |
| 07:11:12.082 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024272082,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:11:12.087 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa257f0586abaa663 span_id=880571e88a031c72 session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:11:12.088 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7859 out=109 | trace_id=6aa257f0586abaa663 span_id=e3117236bcaba8a1 session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:11:12.089 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7859 out=109 | trace_id=6aa257f0586abaa663 span_id=a2a5ad5310298ba4 session_id=aegis-sp-a-4b65951 request_id=71246699-4e9d-4fe5 |
| 07:11:12.090 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa257f0586abaa663 span_id=4ce8b65a93069ffd session_id=aegis-sp-a-4b65951 |
| 07:11:12.095 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa257f0586abaa663 span_id=92cfaa5c4cc8d1d8 session_id=aegis-sp-a-4b65951 |
| 07:11:15.008 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa257f0586abaa663 span_id=e42a7e83b4701dc4 session_id=aegis-sp-a-4b65951 |
| 07:11:15.014 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa257f0586abaa663 span_id=4e8e862c087f6d58 session_id=aegis-sp-a-4b65951 |
| 07:11:15.022 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa257f0586abaa663 span_id=ca6b2467944bbd94 session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:11:15.023 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa257f0586abaa663 span_id=a7b2d788c262d36e session_id=aegis-sp-a-4b65951 |
| 07:11:15.124 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaService | trace_id=6aa257f0586abaa663 span_id=026edf6b8f6b9a3d |
| 07:11:15.131 | runtime-span | lambda-segment | ben-fpa-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=1e760234e11743d6 |
| 07:11:15.278 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=e517e74d0dfd1411 |
| 07:11:15.282 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024275282,"body":{"isError":false,"lo | session_id=aegis-sp-a-4b65951 trace_id=6aa257f0586abaa663 |
| 07:11:15.286 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024275286,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:11:15.366 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024275366,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:11:15.398 | runtime-span | lambda-segment | ben-fpa-request-signoff/LambdaService | trace_id=6aa257f0586abaa663 span_id=29c952d84503df6f |
| 07:11:15.556 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=54c8df290a604061 |
| 07:11:15.906 | runtime-span | lambda-segment | ben-fpa-request-signoff/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=9699d74af401d12e |
| 07:11:17.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8019 out=442 masked_before_model=True | request_id=8cbe5487-418e-4351 session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:11:17.355 | lambda | call | request_signoff -> requested=False | trace_id=6aa257f0586abaa663 session_id=aegis-sp-a-4b65951 request_id=727343ae-1a9c-4550 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:11:17.356 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa257f0586abaa663 span_id=9b7d1f05ec06690c |
| 07:11:17.360 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024277360,"body":{"isError":false,"lo | trace_id=6aa257f0586abaa663 |
| 07:11:17.360 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpa-ben-gw-ny0fwotz9q","event_timestamp":1789024277360,"body":{"isError":false,"re | trace_id=6aa257f0586abaa663 |
| 07:11:17.365 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa257f0586abaa663 span_id=d3180bec74852a70 session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:11:17.366 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8019 out=442 | trace_id=6aa257f0586abaa663 span_id=de1dcb420346eff8 session_id=aegis-sp-a-4b65951 tenant=sp-a case_id=OBS-SPA-01254 |
| 07:11:17.367 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8019 out=442 | trace_id=6aa257f0586abaa663 span_id=d857b665446bba3e session_id=aegis-sp-a-4b65951 request_id=8cbe5487-418e-4351 |
| 07:11:17.371 | runtime-span | span | SSM.GetParameter | trace_id=6aa257f0586abaa663 span_id=4fc0e27b30346743 session_id=aegis-sp-a-4b65951 |
| 07:11:17.413 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa257f0586abaa663 span_id=31abfc25788b1d17 session_id=aegis-sp-a-4b65951 |
| 07:11:26.671 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa257f0586abaa663 span_id=8d8c33261f946a8d session_id=aegis-sp-a-4b65951 |
| 07:11:26.677 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa257f0586abaa663 span_id=5da9b801f52ae382 session_id=aegis-sp-a-4b65951 |
