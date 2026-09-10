# Case trace — `OBS-SPB-C845D` (tenant `sp-b`)

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
| sessions | ['aegis-sp-b-ca11745e866143a3979c23c05b3a23fc'] |
| single_tenant | True |
| tenants_seen | ['sp-b'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 22:10:27.184 | lambda | call | ingest_application -> ingested=True | trace_id=6aa32ad23381c38633 request_id=8216464a-95e5-4e5f tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:27.837 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa32ad342eb3f9f4f span_id=64663180425a3f49 session_id=aegis-sp-b-ca11745 |
| 22:10:28.311 | runtime-span | runtime-http | POST /invocations | trace_id=6aa32ad342eb3f9f4f span_id=03a73ab80732920d session_id=aegis-sp-b-ca11745 |
| 22:10:28.380 | runtime-span | span | SSM.GetParameter | trace_id=6aa32ad342eb3f9f4f span_id=d4d65b9ef45f36f2 session_id=aegis-sp-b-ca11745 |
| 22:10:28.420 | runtime-span | span | SSM.GetParameter | trace_id=6aa32ad342eb3f9f4f span_id=b094e36eee2d988e session_id=aegis-sp-b-ca11745 |
| 22:10:28.467 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa32ad342eb3f9f4f span_id=ddc7b3d77e069b71 session_id=aegis-sp-b-ca11745 |
| 22:10:28.516 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa32ad342eb3f9f4f span_id=843091d25bc1fbbb session_id=aegis-sp-b-ca11745 |
| 22:10:28.596 | runtime-span | span | mcp.session | trace_id=6aa32ad342eb3f9f4f span_id=e633338ada2dc7a4 session_id=aegis-sp-b-ca11745 |
| 22:10:28.717 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa32ad342eb3f9f4f span_id=34036c0af949840c session_id=aegis-sp-b-ca11745 |
| 22:10:28.940 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaService | trace_id=6aa32ad342eb3f9f4f span_id=396308687c6398b3 |
| 22:10:28.944 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=36fa4244841e917a |
| 22:10:28.964 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=b98e6a09555b5f26 |
| 22:10:28.967 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078228967,"body":{"isError":false,"lo | session_id=aegis-sp-b-ca11745 trace_id=6aa32ad342eb3f9f4f |
| 22:10:28.970 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078228970,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:10:29.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5339 out=136 masked_before_model=True | request_id=77913e4f-102c-44e0 session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:29.061 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078229061,"body":{"isError":false,"re | trace_id=6aa32ad342eb3f9f4f |
| 22:10:29.068 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=46538 out=2115 | trace_id=6aa32ad342eb3f9f4f span_id=bf902de208ca1612 session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:29.069 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa32ad342eb3f9f4f span_id=1211524b0009c3cd session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:29.070 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5339 out=136 | trace_id=6aa32ad342eb3f9f4f span_id=bd84a8d07f291ccb session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:29.072 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5339 out=136 | trace_id=6aa32ad342eb3f9f4f span_id=57c3e57e858c2486 session_id=aegis-sp-b-ca11745 request_id=77913e4f-102c-44e0 |
| 22:10:29.073 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32ad342eb3f9f4f span_id=e3045e2e1f46113c session_id=aegis-sp-b-ca11745 |
| 22:10:33.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5553 out=118 masked_before_model=True | request_id=b2b4bd5c-b015-4f5d session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:33.139 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32ad342eb3f9f4f span_id=6c54205b2e3028c9 session_id=aegis-sp-b-ca11745 |
| 22:10:33.154 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa32ad342eb3f9f4f span_id=a5be1dbf2153818b session_id=aegis-sp-b-ca11745 |
| 22:10:33.187 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa32ad342eb3f9f4f span_id=b228539b10cb2fb6 session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:33.188 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa32ad342eb3f9f4f span_id=7f5969c7294b4a9d session_id=aegis-sp-b-ca11745 |
| 22:10:33.280 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaService | trace_id=6aa32ad342eb3f9f4f span_id=452a3e14826be1dc |
| 22:10:33.285 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=d1d16b5990d17170 |
| 22:10:33.456 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=e47561f580b93053 |
| 22:10:33.460 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078233460,"body":{"isError":false,"lo | session_id=aegis-sp-b-ca11745 trace_id=6aa32ad342eb3f9f4f |
| 22:10:33.463 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078233463,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:10:33.541 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078233541,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:10:33.563 | runtime-span | lambda-segment | ben-fpg-intake-application/LambdaService | trace_id=6aa32ad342eb3f9f4f span_id=3b3112cd8aaf905e |
| 22:10:33.568 | runtime-span | lambda-segment | ben-fpg-intake-application/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=123e27baa61692b5 |
| 22:10:33.731 | lambda | call | intake_application -> ok | trace_id=6aa32ad342eb3f9f4f session_id=aegis-sp-b-ca11745 request_id=2b6dbeef-d37f-4102 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:33.732 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=ab15dd518351dbde |
| 22:10:33.735 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078233735,"body":{"isError":false,"re | trace_id=6aa32ad342eb3f9f4f |
| 22:10:33.735 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078233735,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:10:33.740 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa32ad342eb3f9f4f span_id=93806c2b1adc872c session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:33.741 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5553 out=118 | trace_id=6aa32ad342eb3f9f4f span_id=cf352f0b8c90e8c7 session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:33.742 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32ad342eb3f9f4f span_id=b35290c83e91934e session_id=aegis-sp-b-ca11745 |
| 22:10:33.742 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5553 out=118 | trace_id=6aa32ad342eb3f9f4f span_id=3adb73e92be781e6 session_id=aegis-sp-b-ca11745 request_id=b2b4bd5c-b015-4f5d |
| 22:10:37.455 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32ad342eb3f9f4f span_id=ad634a468669582f session_id=aegis-sp-b-ca11745 |
| 22:10:37.462 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa32ad342eb3f9f4f span_id=f54c3e0d9dbb8ea2 session_id=aegis-sp-b-ca11745 |
| 22:10:37.471 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa32ad342eb3f9f4f span_id=e84b463c68334cdb session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:37.472 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa32ad342eb3f9f4f span_id=e17a6c9edf68dcc1 session_id=aegis-sp-b-ca11745 |
| 22:10:37.573 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaService | trace_id=6aa32ad342eb3f9f4f span_id=41c9c260b5b64422 |
| 22:10:37.578 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=43896e59d38c2f41 |
| 22:10:37.720 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=9365dc5d68ae9af9 |
| 22:10:37.723 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078237723,"body":{"isError":false,"lo | session_id=aegis-sp-b-ca11745 trace_id=6aa32ad342eb3f9f4f |
| 22:10:37.727 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078237727,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:10:37.800 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078237800,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:10:37.828 | runtime-span | lambda-segment | ben-fpg-mask-pii/LambdaService | trace_id=6aa32ad342eb3f9f4f span_id=3ef48ad7895ffac0 |
| 22:10:37.832 | runtime-span | lambda-segment | ben-fpg-mask-pii/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=aa8d6738258e378f |
| 22:10:38.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5974 out=393 masked_before_model=True | request_id=86265114-4ddc-42ac session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:38.310 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa32ad342eb3f9f4f session_id=aegis-sp-b-ca11745 request_id=d6286d4c-cabb-4079 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:38.311 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=8f12375f00bf256c |
| 22:10:38.316 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078238316,"body":{"isError":false,"re | trace_id=6aa32ad342eb3f9f4f |
| 22:10:38.316 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078238316,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:10:38.321 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa32ad342eb3f9f4f span_id=e574b84debf7be9d session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:38.322 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5974 out=393 | trace_id=6aa32ad342eb3f9f4f span_id=7eeebb8de4c7b30c session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:38.323 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32ad342eb3f9f4f span_id=dd5b854d1ec9223d session_id=aegis-sp-b-ca11745 |
| 22:10:38.323 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5974 out=393 | trace_id=6aa32ad342eb3f9f4f span_id=eb3a6cfeb7423eda session_id=aegis-sp-b-ca11745 request_id=86265114-4ddc-42ac |
| 22:10:42.900 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32ad342eb3f9f4f span_id=7f4f38982675f65c session_id=aegis-sp-b-ca11745 |
| 22:10:42.907 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa32ad342eb3f9f4f span_id=0eaf1df014c901b6 session_id=aegis-sp-b-ca11745 |
| 22:10:42.917 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa32ad342eb3f9f4f span_id=4381e0063a179e73 session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:42.917 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa32ad342eb3f9f4f span_id=4ec7db602face04a session_id=aegis-sp-b-ca11745 |
| 22:10:43.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6598 out=562 masked_before_model=True | request_id=c0c27b69-757a-4b90 session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:43.022 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaService | trace_id=6aa32ad342eb3f9f4f span_id=38b2ad7d8d6690fc |
| 22:10:43.032 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=ef1d0c3ebaf7b681 |
| 22:10:43.204 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=5ba7ea23638e7593 |
| 22:10:43.209 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078243209,"body":{"isError":false,"lo | session_id=aegis-sp-b-ca11745 trace_id=6aa32ad342eb3f9f4f |
| 22:10:43.213 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078243213,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:10:43.292 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078243292,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:10:43.311 | runtime-span | lambda-segment | ben-fpg-assess-eligibility/LambdaService | trace_id=6aa32ad342eb3f9f4f span_id=3ca33c1e92d19c36 |
| 22:10:43.316 | runtime-span | lambda-segment | ben-fpg-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=29ed3d4bf5086fb7 |
| 22:10:43.359 | lambda | call | assess_eligibility -> ok | trace_id=6aa32ad342eb3f9f4f session_id=aegis-sp-b-ca11745 request_id=986ea345-0419-45a1 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:43.360 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=87a53db922a7d83b |
| 22:10:43.364 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078243364,"body":{"isError":false,"re | trace_id=6aa32ad342eb3f9f4f |
| 22:10:43.364 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078243364,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:10:43.370 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa32ad342eb3f9f4f span_id=10c06df149544751 session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:43.371 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6598 out=562 | trace_id=6aa32ad342eb3f9f4f span_id=9ec3dc6fa6ff1781 session_id=aegis-sp-b-ca11745 request_id=c0c27b69-757a-4b90 |
| 22:10:43.371 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6598 out=562 | trace_id=6aa32ad342eb3f9f4f span_id=ebda0ffdd081a689 session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:43.377 | runtime-span | span | SSM.GetParameter | trace_id=6aa32ad342eb3f9f4f span_id=07d1340ce8b6523b session_id=aegis-sp-b-ca11745 |
| 22:10:43.416 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32ad342eb3f9f4f span_id=4d45f51187a79f28 session_id=aegis-sp-b-ca11745 |
| 22:10:49.713 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32ad342eb3f9f4f span_id=101449b4bcb796cb session_id=aegis-sp-b-ca11745 |
| 22:10:49.720 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa32ad342eb3f9f4f span_id=dd2295d8fb11ebd3 session_id=aegis-sp-b-ca11745 |
| 22:10:49.750 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa32ad342eb3f9f4f span_id=e3f19bbe7b7696d6 session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:49.751 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa32ad342eb3f9f4f span_id=e7a7ca61a8c7587d session_id=aegis-sp-b-ca11745 |
| 22:10:49.864 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaService | trace_id=6aa32ad342eb3f9f4f span_id=797cf211614a8fa1 |
| 22:10:49.869 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=c4dfdbc8a58de6a2 |
| 22:10:50.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7208 out=355 masked_before_model=True | request_id=83a78e81-0240-4af4 session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:50.038 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=e618775c2b67622b |
| 22:10:50.041 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078250041,"body":{"isError":false,"lo | session_id=aegis-sp-b-ca11745 trace_id=6aa32ad342eb3f9f4f |
| 22:10:50.046 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078250046,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:10:50.123 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078250123,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:10:50.152 | runtime-span | lambda-segment | ben-fpg-core-tools/LambdaService | trace_id=6aa32ad342eb3f9f4f span_id=0b44e6cc1fc22983 |
| 22:10:50.164 | runtime-span | lambda-segment | ben-fpg-core-tools/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=be03612549332b3f |
| 22:10:50.188 | lambda | call | benefits_core -> committed=False | trace_id=6aa32ad342eb3f9f4f session_id=aegis-sp-b-ca11745 request_id=d16bf265-8b82-490e tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:50.188 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=2e74d5770da38f87 |
| 22:10:50.193 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078250193,"body":{"isError":false,"re | trace_id=6aa32ad342eb3f9f4f |
| 22:10:50.193 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078250193,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:10:50.199 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa32ad342eb3f9f4f span_id=4c94246ac317efbd session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:50.200 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7208 out=355 | trace_id=6aa32ad342eb3f9f4f span_id=b41e009296cb61c0 session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:50.201 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32ad342eb3f9f4f span_id=9c5c11bdc8be33f1 session_id=aegis-sp-b-ca11745 |
| 22:10:50.201 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7208 out=355 | trace_id=6aa32ad342eb3f9f4f span_id=c336749c570c0bf8 session_id=aegis-sp-b-ca11745 request_id=83a78e81-0240-4af4 |
| 22:10:57.000 | worm | evidence | INTENT benefits-determination seq=0 chain=4ea213880e11… | trace_id=6aa32ad342eb3f9f4f session_id=aegis-sp-b-ca11745 request_id=96b309e7-c6af-4178 tenant=sp-b |
| 22:10:57.184 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32ad342eb3f9f4f span_id=dc1f63c1e1e1b93f session_id=aegis-sp-b-ca11745 |
| 22:10:57.191 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa32ad342eb3f9f4f span_id=5d8580b33659a5fe session_id=aegis-sp-b-ca11745 |
| 22:10:57.229 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa32ad342eb3f9f4f span_id=c4c538c1fcfa9163 session_id=aegis-sp-b-ca11745 |
| 22:10:57.229 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa32ad342eb3f9f4f span_id=0d7133fcad37e804 session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:57.338 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaService | trace_id=6aa32ad342eb3f9f4f span_id=146df5f8fbcc7dac |
| 22:10:57.343 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=43e8498b85f0add7 |
| 22:10:57.495 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=f5d6ba430eedd468 |
| 22:10:57.498 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078257498,"body":{"isError":false,"lo | session_id=aegis-sp-b-ca11745 trace_id=6aa32ad342eb3f9f4f |
| 22:10:57.502 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078257502,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:10:57.589 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078257589,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:10:57.612 | runtime-span | lambda-segment | ben-fpg-write-audit/LambdaService | trace_id=6aa32ad342eb3f9f4f span_id=08a74e15e8f6a1f4 |
| 22:10:57.618 | runtime-span | lambda-segment | ben-fpg-write-audit/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=039f11cc3432cc7b |
| 22:10:58.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7852 out=111 masked_before_model=True | request_id=ca0bc0b5-0ace-44b7 session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:58.103 | lambda | call | write_audit -> stored=True | trace_id=6aa32ad342eb3f9f4f session_id=aegis-sp-b-ca11745 request_id=96b309e7-c6af-4178 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:58.104 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=a90ddd56a70987e7 |
| 22:10:58.111 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078258111,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:10:58.111 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078258111,"body":{"isError":false,"re | trace_id=6aa32ad342eb3f9f4f |
| 22:10:58.116 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa32ad342eb3f9f4f span_id=4163261b5e724f09 session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:58.117 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7852 out=111 | trace_id=6aa32ad342eb3f9f4f span_id=7bae05007894a386 session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:10:58.118 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7852 out=111 | trace_id=6aa32ad342eb3f9f4f span_id=10cf589ff311fcac session_id=aegis-sp-b-ca11745 request_id=ca0bc0b5-0ace-44b7 |
| 22:10:58.119 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32ad342eb3f9f4f span_id=e135e79b49cbb414 session_id=aegis-sp-b-ca11745 |
| 22:11:00.711 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32ad342eb3f9f4f span_id=79249ad8109e354e session_id=aegis-sp-b-ca11745 |
| 22:11:00.718 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa32ad342eb3f9f4f span_id=b3c00c75407b4ce1 session_id=aegis-sp-b-ca11745 |
| 22:11:00.723 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa32ad342eb3f9f4f span_id=296cac2f10b016ec session_id=aegis-sp-b-ca11745 |
| 22:11:00.732 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa32ad342eb3f9f4f span_id=2a56657f87f0879e session_id=aegis-sp-b-ca11745 |
| 22:11:00.732 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa32ad342eb3f9f4f span_id=b2d28e6fa98cb127 session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:11:00.845 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaService | trace_id=6aa32ad342eb3f9f4f span_id=5b6f3039b0c88236 |
| 22:11:00.850 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=22faa0aa8285e3c6 |
| 22:11:01.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8014 out=440 masked_before_model=True | request_id=b1e98d7e-c03b-4f1d session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:11:01.003 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=41339f3f0d7064c7 |
| 22:11:01.006 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078261006,"body":{"isError":false,"lo | session_id=aegis-sp-b-ca11745 trace_id=6aa32ad342eb3f9f4f |
| 22:11:01.011 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078261011,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:11:01.097 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078261097,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:11:01.120 | runtime-span | lambda-segment | ben-fpg-request-signoff/LambdaService | trace_id=6aa32ad342eb3f9f4f span_id=35c17a6499ceade1 |
| 22:11:01.125 | runtime-span | lambda-segment | ben-fpg-request-signoff/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=611ffcb4318884e1 |
| 22:11:01.148 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32ad342eb3f9f4f span_id=da9755cbb67d8751 |
| 22:11:01.149 | lambda | call | request_signoff -> requested=False | trace_id=6aa32ad342eb3f9f4f session_id=aegis-sp-b-ca11745 request_id=4514f12a-fa0d-42b7 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:11:01.154 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078261154,"body":{"isError":false,"re | trace_id=6aa32ad342eb3f9f4f |
| 22:11:01.154 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078261154,"body":{"isError":false,"lo | trace_id=6aa32ad342eb3f9f4f |
| 22:11:01.159 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa32ad342eb3f9f4f span_id=3b3d305a607b7918 session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:11:01.161 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8014 out=440 | trace_id=6aa32ad342eb3f9f4f span_id=efa558ac12fc186d session_id=aegis-sp-b-ca11745 tenant=sp-b case_id=OBS-SPB-C845D |
| 22:11:01.161 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8014 out=440 | trace_id=6aa32ad342eb3f9f4f span_id=1f15572c4a172cbc session_id=aegis-sp-b-ca11745 request_id=b1e98d7e-c03b-4f1d |
| 22:11:01.165 | runtime-span | span | SSM.GetParameter | trace_id=6aa32ad342eb3f9f4f span_id=1e6a047c055fc3eb session_id=aegis-sp-b-ca11745 |
| 22:11:01.203 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32ad342eb3f9f4f span_id=faaae4d37ada0070 session_id=aegis-sp-b-ca11745 |
| 22:11:10.331 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32ad342eb3f9f4f span_id=057cbb0ce8e04c1b session_id=aegis-sp-b-ca11745 |
| 22:11:10.338 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa32ad342eb3f9f4f span_id=570ae470674e7eb2 session_id=aegis-sp-b-ca11745 |
