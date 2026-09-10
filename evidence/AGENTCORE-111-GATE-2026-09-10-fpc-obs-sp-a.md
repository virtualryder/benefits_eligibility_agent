# Case trace — `OBS-SPA-67A67` (tenant `sp-a`)

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
| sessions | ['aegis-sp-a-8e3e41a0f6a342819e9c7d5cadfb8c4f'] |
| single_tenant | True |
| tenants_seen | ['sp-a'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 16:08:52.640 | lambda | call | ingest_application -> ingested=True | trace_id=6aa2d61459c27a7c2b request_id=ef6a9ccd-cac5-475d tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:08:53.210 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa2d61511b1849122 span_id=f283a645bbdffb0e session_id=aegis-sp-a-8e3e41a |
| 16:08:53.861 | runtime-span | runtime-http | POST /invocations | trace_id=6aa2d61511b1849122 span_id=481bbaa74249c08b session_id=aegis-sp-a-8e3e41a |
| 16:08:53.957 | runtime-span | span | SSM.GetParameter | trace_id=6aa2d61511b1849122 span_id=a73fa224f4209188 session_id=aegis-sp-a-8e3e41a |
| 16:08:54.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5337 out=120 masked_before_model=True | request_id=23aa30af-2787-4c13 session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:08:54.008 | runtime-span | span | SSM.GetParameter | trace_id=6aa2d61511b1849122 span_id=a2592012f03fa34e session_id=aegis-sp-a-8e3e41a |
| 16:08:54.080 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa2d61511b1849122 span_id=f3866afc1d8c1a08 session_id=aegis-sp-a-8e3e41a |
| 16:08:54.129 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa2d61511b1849122 span_id=d866d13d2dc92da7 session_id=aegis-sp-a-8e3e41a |
| 16:08:54.227 | runtime-span | span | mcp.session | trace_id=6aa2d61511b1849122 span_id=8d4e7fbbb5e64cdb session_id=aegis-sp-a-8e3e41a |
| 16:08:54.363 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa2d61511b1849122 span_id=2564cffc9cf72a28 session_id=aegis-sp-a-8e3e41a |
| 16:08:54.576 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaService | trace_id=6aa2d61511b1849122 span_id=27778bc10eec238d |
| 16:08:54.583 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=06fe161e5021a1de |
| 16:08:54.606 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=e6bac38e22e1eea8 |
| 16:08:54.608 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056534608,"body":{"isError":false,"lo | session_id=aegis-sp-a-8e3e41a trace_id=6aa2d61511b1849122 |
| 16:08:54.612 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056534612,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:08:54.712 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056534712,"body":{"isError":false,"re | trace_id=6aa2d61511b1849122 |
| 16:08:54.720 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=38609 out=2089 | trace_id=6aa2d61511b1849122 span_id=a81a5362fb209fc6 session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:08:54.721 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2d61511b1849122 span_id=0482f6c4ebb081bc session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:08:54.723 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5337 out=120 | trace_id=6aa2d61511b1849122 span_id=6f0d580cc79e2341 session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:08:54.734 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d61511b1849122 span_id=20757ffdd71e1701 session_id=aegis-sp-a-8e3e41a |
| 16:08:54.734 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5337 out=120 | trace_id=6aa2d61511b1849122 span_id=05dc91f620833a90 session_id=aegis-sp-a-8e3e41a request_id=23aa30af-2787-4c13 |
| 16:08:59.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5535 out=120 masked_before_model=True | request_id=1dcae3f8-fc56-426a session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:08:59.039 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d61511b1849122 span_id=5dd52439fdba93fd session_id=aegis-sp-a-8e3e41a |
| 16:08:59.054 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2d61511b1849122 span_id=b10e6f289b6ca0de session_id=aegis-sp-a-8e3e41a |
| 16:08:59.085 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa2d61511b1849122 span_id=b5f1718655e4340d session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:08:59.086 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa2d61511b1849122 span_id=ab50576d9761c31a session_id=aegis-sp-a-8e3e41a |
| 16:08:59.198 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaService | trace_id=6aa2d61511b1849122 span_id=535bb9e1d200d808 |
| 16:08:59.207 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=3b9043bbbdc82262 |
| 16:08:59.583 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=58df6f17f7bde71e |
| 16:08:59.585 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056539585,"body":{"isError":false,"lo | session_id=aegis-sp-a-8e3e41a trace_id=6aa2d61511b1849122 |
| 16:08:59.589 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056539589,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:08:59.659 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056539659,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:08:59.683 | runtime-span | lambda-segment | ben-fpc-intake-application/LambdaService | trace_id=6aa2d61511b1849122 span_id=23c719dfa314533e |
| 16:08:59.688 | runtime-span | lambda-segment | ben-fpc-intake-application/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=1372effcacf7f0c0 |
| 16:08:59.875 | lambda | call | intake_application -> ok | trace_id=6aa2d61511b1849122 session_id=aegis-sp-a-8e3e41a request_id=3259df4b-2740-4784 tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:08:59.876 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=3db26991feac093e |
| 16:08:59.880 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056539880,"body":{"isError":false,"re | trace_id=6aa2d61511b1849122 |
| 16:08:59.880 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056539880,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:08:59.886 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2d61511b1849122 span_id=ec3e143c8d2dfb32 session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:08:59.887 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5535 out=120 | trace_id=6aa2d61511b1849122 span_id=0658517b920b85f7 session_id=aegis-sp-a-8e3e41a request_id=1dcae3f8-fc56-426a |
| 16:08:59.887 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5535 out=120 | trace_id=6aa2d61511b1849122 span_id=f25107a6924c2d3a session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:08:59.888 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d61511b1849122 span_id=cd744f4ccbd7b9c0 session_id=aegis-sp-a-8e3e41a |
| 16:09:03.530 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d61511b1849122 span_id=b90896bb2d89bdea session_id=aegis-sp-a-8e3e41a |
| 16:09:03.536 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2d61511b1849122 span_id=75570626e0cfae3c session_id=aegis-sp-a-8e3e41a |
| 16:09:03.546 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa2d61511b1849122 span_id=772c9f77b815d1e7 session_id=aegis-sp-a-8e3e41a |
| 16:09:03.546 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa2d61511b1849122 span_id=6bdac7ea5e95ad3c session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:03.641 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaService | trace_id=6aa2d61511b1849122 span_id=55bc55b5c45a66ff |
| 16:09:03.648 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=f5b8caba548d65be |
| 16:09:03.800 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=58f612a6b7c9b694 |
| 16:09:03.804 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056543804,"body":{"isError":false,"lo | session_id=aegis-sp-a-8e3e41a trace_id=6aa2d61511b1849122 |
| 16:09:03.825 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056543825,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:09:03.906 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056543906,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:09:03.934 | runtime-span | lambda-segment | ben-fpc-mask-pii/LambdaService | trace_id=6aa2d61511b1849122 span_id=55453d931e152db3 |
| 16:09:03.944 | runtime-span | lambda-segment | ben-fpc-mask-pii/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=bb3e96870f4ab1cd |
| 16:09:04.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5953 out=404 masked_before_model=True | request_id=125df441-1d8e-4668 session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:04.442 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa2d61511b1849122 session_id=aegis-sp-a-8e3e41a request_id=8c9428d0-13f2-4b2b tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:04.443 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=6ef10060c40f71db |
| 16:09:04.446 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056544446,"body":{"isError":false,"re | trace_id=6aa2d61511b1849122 |
| 16:09:04.446 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056544446,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:09:04.452 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2d61511b1849122 span_id=c7322ba9f674f950 session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:04.453 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5953 out=404 | trace_id=6aa2d61511b1849122 span_id=9da18eadacdbbe22 session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:04.454 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d61511b1849122 span_id=2b8a5be60086320b session_id=aegis-sp-a-8e3e41a |
| 16:09:04.454 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5953 out=404 | trace_id=6aa2d61511b1849122 span_id=9b052007c1126edd session_id=aegis-sp-a-8e3e41a request_id=125df441-1d8e-4668 |
| 16:09:09.557 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d61511b1849122 span_id=f7bd81852fed35bd session_id=aegis-sp-a-8e3e41a |
| 16:09:09.563 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2d61511b1849122 span_id=9552512a9e2a5c23 session_id=aegis-sp-a-8e3e41a |
| 16:09:09.595 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa2d61511b1849122 span_id=eb05a2438dbf2f94 session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:09.596 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa2d61511b1849122 span_id=106d8bef011704bf session_id=aegis-sp-a-8e3e41a |
| 16:09:09.708 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaService | trace_id=6aa2d61511b1849122 span_id=653ebd57466c4442 |
| 16:09:09.713 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=749b4513c933f2f2 |
| 16:09:09.876 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=91e4a086291f268c |
| 16:09:09.880 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056549880,"body":{"isError":false,"lo | session_id=aegis-sp-a-8e3e41a trace_id=6aa2d61511b1849122 |
| 16:09:09.884 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056549884,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:09:09.962 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056549962,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:09:09.987 | runtime-span | lambda-segment | ben-fpc-assess-eligibility/LambdaService | trace_id=6aa2d61511b1849122 span_id=30c458e5b9fb3f17 |
| 16:09:09.992 | runtime-span | lambda-segment | ben-fpc-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=bcc67a2add656088 |
| 16:09:10.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6588 out=577 masked_before_model=True | request_id=73a92a1f-6f33-4b0f session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:10.012 | lambda | call | assess_eligibility -> ok | trace_id=6aa2d61511b1849122 session_id=aegis-sp-a-8e3e41a request_id=305a840e-e1b7-4af9 tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:10.012 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=72953eabdca2c716 |
| 16:09:10.017 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056550017,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:09:10.017 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056550017,"body":{"isError":false,"re | trace_id=6aa2d61511b1849122 |
| 16:09:10.022 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2d61511b1849122 span_id=19c638eb4c912579 session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:10.023 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6588 out=577 | trace_id=6aa2d61511b1849122 span_id=06968c7ea6648fb4 session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:10.024 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6588 out=577 | trace_id=6aa2d61511b1849122 span_id=2f55f0d0c7adbb42 session_id=aegis-sp-a-8e3e41a request_id=73a92a1f-6f33-4b0f |
| 16:09:10.031 | runtime-span | span | SSM.GetParameter | trace_id=6aa2d61511b1849122 span_id=d587f77062c62e02 session_id=aegis-sp-a-8e3e41a |
| 16:09:10.068 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d61511b1849122 span_id=0936985f7d96c049 session_id=aegis-sp-a-8e3e41a |
| 16:09:17.950 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d61511b1849122 span_id=b0a2ecd14f2c70d3 session_id=aegis-sp-a-8e3e41a |
| 16:09:17.956 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2d61511b1849122 span_id=5bff705355facfbd session_id=aegis-sp-a-8e3e41a |
| 16:09:17.981 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa2d61511b1849122 span_id=05963a3342ee20a3 session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:17.982 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa2d61511b1849122 span_id=e1caca31986ced4b session_id=aegis-sp-a-8e3e41a |
| 16:09:18.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7213 out=377 masked_before_model=True | request_id=3881c2d6-e2ff-4bca session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:18.081 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaService | trace_id=6aa2d61511b1849122 span_id=11bcb96dc7883c9d |
| 16:09:18.086 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=fd0c477b9105dc38 |
| 16:09:18.260 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=7610e1adb6bcb3cc |
| 16:09:18.263 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056558263,"body":{"isError":false,"lo | session_id=aegis-sp-a-8e3e41a trace_id=6aa2d61511b1849122 |
| 16:09:18.267 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056558267,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:09:18.349 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056558349,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:09:18.380 | runtime-span | lambda-segment | ben-fpc-core-tools/LambdaService | trace_id=6aa2d61511b1849122 span_id=748cf0810eeef919 |
| 16:09:18.384 | runtime-span | lambda-segment | ben-fpc-core-tools/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=9e1bdc4ed7104c82 |
| 16:09:18.415 | lambda | call | benefits_core -> committed=False | trace_id=6aa2d61511b1849122 session_id=aegis-sp-a-8e3e41a request_id=06d85a4c-109e-4a83 tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:18.415 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=f3f1407e09455c5d |
| 16:09:18.420 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056558420,"body":{"isError":false,"re | trace_id=6aa2d61511b1849122 |
| 16:09:18.421 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056558421,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:09:18.426 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2d61511b1849122 span_id=d084faf329ff7884 session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:18.427 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7213 out=377 | trace_id=6aa2d61511b1849122 span_id=1c7d10ac71083606 session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:18.428 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7213 out=377 | trace_id=6aa2d61511b1849122 span_id=56a923c8d040b374 session_id=aegis-sp-a-8e3e41a request_id=3881c2d6-e2ff-4bca |
| 16:09:18.429 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d61511b1849122 span_id=cf67c1021d8c9655 session_id=aegis-sp-a-8e3e41a |
| 16:09:24.238 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d61511b1849122 span_id=e6f89fea81dd4c5b session_id=aegis-sp-a-8e3e41a |
| 16:09:24.244 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa2d61511b1849122 span_id=6ca2b7bbbd7cec57 session_id=aegis-sp-a-8e3e41a |
| 16:09:24.250 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2d61511b1849122 span_id=54c34f9981852718 session_id=aegis-sp-a-8e3e41a |
| 16:09:24.281 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa2d61511b1849122 span_id=c57ce1c369eeb50d session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:24.281 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa2d61511b1849122 span_id=8f7d77056427192a session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:24.282 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa2d61511b1849122 span_id=18328a1a5f75d146 session_id=aegis-sp-a-8e3e41a |
| 16:09:24.283 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa2d61511b1849122 span_id=bf499a28b57578e5 session_id=aegis-sp-a-8e3e41a |
| 16:09:24.392 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaService | trace_id=6aa2d61511b1849122 span_id=4a32ba4dfc56bbcc |
| 16:09:24.398 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=e1cb44e91a056d0d |
| 16:09:24.400 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaService | trace_id=6aa2d61511b1849122 span_id=332a650d10d0917b |
| 16:09:24.529 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=81342ef52f7a1f90 |
| 16:09:24.563 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=435b4e656bbf9d8c |
| 16:09:24.565 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056564565,"body":{"isError":false,"lo | session_id=aegis-sp-a-8e3e41a trace_id=6aa2d61511b1849122 |
| 16:09:24.569 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056564569,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:09:24.642 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056564642,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:09:24.661 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=c3146c5ac3c89230 |
| 16:09:24.671 | runtime-span | lambda-segment | ben-fpc-request-signoff/LambdaService | trace_id=6aa2d61511b1849122 span_id=52050b56f124960d |
| 16:09:24.803 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=5ade419f96b2bb7b |
| 16:09:25.192 | runtime-span | lambda-segment | ben-fpc-request-signoff/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=c197ab07b8ad9c2e |
| 16:09:26.727 | lambda | call | request_signoff -> requested=False | trace_id=6aa2d61511b1849122 session_id=aegis-sp-a-8e3e41a request_id=d93e57aa-5348-48d8 tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:26.728 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=16db3230e3f6fcaa |
| 16:09:26.733 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056566733,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:09:26.733 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056566733,"body":{"isError":false,"re | trace_id=6aa2d61511b1849122 |
| 16:09:28.000 | worm | evidence | INTENT benefits-determination seq=0 chain=7bddae984cd2… | trace_id=6aa2d61511b1849122 session_id=aegis-sp-a-8e3e41a request_id=b5073f31-0b32-4704 tenant=sp-a |
| 16:09:28.139 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=fac32c2f2d666292 |
| 16:09:28.143 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056568143,"body":{"isError":false,"lo | session_id=aegis-sp-a-8e3e41a trace_id=6aa2d61511b1849122 |
| 16:09:28.146 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056568146,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:09:28.219 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056568219,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:09:28.243 | runtime-span | lambda-segment | ben-fpc-write-audit/LambdaService | trace_id=6aa2d61511b1849122 span_id=715fc7bedbd7b5c8 |
| 16:09:28.247 | runtime-span | lambda-segment | ben-fpc-write-audit/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=e0d3d2e15081abca |
| 16:09:29.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7983 out=491 masked_before_model=True | request_id=de96436a-cef1-4e61 session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:29.131 | lambda | call | write_audit -> stored=True | trace_id=6aa2d61511b1849122 session_id=aegis-sp-a-8e3e41a request_id=b5073f31-0b32-4704 tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:29.132 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d61511b1849122 span_id=8ed057aecb37df68 |
| 16:09:29.137 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056569137,"body":{"isError":false,"lo | trace_id=6aa2d61511b1849122 |
| 16:09:29.137 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056569137,"body":{"isError":false,"re | trace_id=6aa2d61511b1849122 |
| 16:09:29.142 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2d61511b1849122 span_id=6c39393d3144605f session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:29.143 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7983 out=491 | trace_id=6aa2d61511b1849122 span_id=e108593db26fea36 session_id=aegis-sp-a-8e3e41a tenant=sp-a case_id=OBS-SPA-67A67 |
| 16:09:29.144 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7983 out=491 | trace_id=6aa2d61511b1849122 span_id=0764e2f6fc8a8863 session_id=aegis-sp-a-8e3e41a request_id=de96436a-cef1-4e61 |
| 16:09:29.149 | runtime-span | span | SSM.GetParameter | trace_id=6aa2d61511b1849122 span_id=ff28dfc2d71f7f7a session_id=aegis-sp-a-8e3e41a |
| 16:09:29.184 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d61511b1849122 span_id=659658c82799e0ac session_id=aegis-sp-a-8e3e41a |
| 16:09:39.439 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d61511b1849122 span_id=ee2994ac0d6aafe8 session_id=aegis-sp-a-8e3e41a |
| 16:09:39.446 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2d61511b1849122 span_id=584fae4ec16d4e04 session_id=aegis-sp-a-8e3e41a |
