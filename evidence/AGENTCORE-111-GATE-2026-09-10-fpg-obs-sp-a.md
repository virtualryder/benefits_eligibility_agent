# Case trace — `OBS-SPA-B8337` (tenant `sp-a`)

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
| sessions | ['aegis-sp-a-3dc5f7615de14780b7f6894670c31832'] |
| single_tenant | True |
| tenants_seen | ['sp-a'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 22:09:43.092 | lambda | call | ingest_application -> ingested=True | trace_id=6aa32aa65092160956 request_id=34d05de3-06eb-4075 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:43.647 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa32aa77f31e4163e span_id=9a8f002b49a61b59 session_id=aegis-sp-a-3dc5f76 |
| 22:09:44.247 | runtime-span | runtime-http | POST /invocations | trace_id=6aa32aa77f31e4163e span_id=c9589b7e189bb1da session_id=aegis-sp-a-3dc5f76 |
| 22:09:44.316 | runtime-span | span | SSM.GetParameter | trace_id=6aa32aa77f31e4163e span_id=89919e2b63642e7a session_id=aegis-sp-a-3dc5f76 |
| 22:09:44.357 | runtime-span | span | SSM.GetParameter | trace_id=6aa32aa77f31e4163e span_id=ca3d13a7d6a0ec50 session_id=aegis-sp-a-3dc5f76 |
| 22:09:44.419 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa32aa77f31e4163e span_id=faee25fdece5e4a7 session_id=aegis-sp-a-3dc5f76 |
| 22:09:44.473 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa32aa77f31e4163e span_id=7beb815c02cd5c26 session_id=aegis-sp-a-3dc5f76 |
| 22:09:44.553 | runtime-span | span | mcp.session | trace_id=6aa32aa77f31e4163e span_id=4a8174c9cdc8a13d session_id=aegis-sp-a-3dc5f76 |
| 22:09:44.710 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa32aa77f31e4163e span_id=a83b03dc13fea36f session_id=aegis-sp-a-3dc5f76 |
| 22:09:44.934 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaService | trace_id=6aa32aa77f31e4163e span_id=7ecbb3234aad6d41 |
| 22:09:44.940 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=09da2fce704cc93b |
| 22:09:44.961 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=0d69843835aa8832 |
| 22:09:44.965 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078184965,"body":{"isError":false,"lo | session_id=aegis-sp-a-3dc5f76 trace_id=6aa32aa77f31e4163e |
| 22:09:44.968 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078184968,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:09:45.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5341 out=139 masked_before_model=True | request_id=02dbf27b-1043-456a session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:45.058 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078185058,"body":{"isError":false,"re | trace_id=6aa32aa77f31e4163e |
| 22:09:45.065 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=46551 out=2155 | trace_id=6aa32aa77f31e4163e span_id=774125de19089e68 session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:45.066 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa32aa77f31e4163e span_id=d1e0c4e31aaf3ac4 session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:45.067 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5341 out=139 | trace_id=6aa32aa77f31e4163e span_id=ad2eb5d82d9ee2b4 session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:45.070 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32aa77f31e4163e span_id=67ed8836d0b7c73f session_id=aegis-sp-a-3dc5f76 |
| 22:09:45.070 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5341 out=139 | trace_id=6aa32aa77f31e4163e span_id=618c640b056596f1 session_id=aegis-sp-a-3dc5f76 request_id=02dbf27b-1043-456a |
| 22:09:48.401 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32aa77f31e4163e span_id=2226af3ed3787c01 session_id=aegis-sp-a-3dc5f76 |
| 22:09:48.416 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa32aa77f31e4163e span_id=a7c13c041267aaa5 session_id=aegis-sp-a-3dc5f76 |
| 22:09:48.445 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa32aa77f31e4163e span_id=f940c6d1881ab8f8 session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:48.446 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa32aa77f31e4163e span_id=0698adc5ce5daec4 session_id=aegis-sp-a-3dc5f76 |
| 22:09:48.488 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaService | trace_id=6aa32aa77f31e4163e span_id=2d4b17dac1258d1c |
| 22:09:48.495 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=585a9b461b54a2e1 |
| 22:09:48.859 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=11bd18c7eadb0ec4 |
| 22:09:48.862 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078188862,"body":{"isError":false,"lo | session_id=aegis-sp-a-3dc5f76 trace_id=6aa32aa77f31e4163e |
| 22:09:48.866 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078188866,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:09:48.948 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078188948,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:09:48.972 | runtime-span | lambda-segment | ben-fpg-intake-application/LambdaService | trace_id=6aa32aa77f31e4163e span_id=3b9e5df6cee2e9cd |
| 22:09:48.977 | runtime-span | lambda-segment | ben-fpg-intake-application/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=c30d4fb2f476f372 |
| 22:09:49.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5558 out=123 masked_before_model=True | request_id=9e6f5cb8-1e55-4b7f session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:49.164 | lambda | call | intake_application -> ok | trace_id=6aa32aa77f31e4163e session_id=aegis-sp-a-3dc5f76 request_id=f758c1e3-a6f4-4b05 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:49.164 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=0f829dad86948316 |
| 22:09:49.169 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078189169,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:09:49.169 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078189169,"body":{"isError":false,"re | trace_id=6aa32aa77f31e4163e |
| 22:09:49.174 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa32aa77f31e4163e span_id=3097cb3c62413ab7 session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:49.175 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5558 out=123 | trace_id=6aa32aa77f31e4163e span_id=0dc8577d9fbdbc90 session_id=aegis-sp-a-3dc5f76 request_id=9e6f5cb8-1e55-4b7f |
| 22:09:49.175 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5558 out=123 | trace_id=6aa32aa77f31e4163e span_id=77dd51f1f7e2ab86 session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:49.176 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32aa77f31e4163e span_id=a72b184d9708a101 session_id=aegis-sp-a-3dc5f76 |
| 22:09:51.933 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32aa77f31e4163e span_id=75a01b073cdb611c session_id=aegis-sp-a-3dc5f76 |
| 22:09:51.941 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa32aa77f31e4163e span_id=c7206b945fe9c5d5 session_id=aegis-sp-a-3dc5f76 |
| 22:09:51.952 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa32aa77f31e4163e span_id=52b761b693ea7a53 session_id=aegis-sp-a-3dc5f76 |
| 22:09:51.952 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa32aa77f31e4163e span_id=ea7b456dfdb642df session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:52.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5983 out=430 masked_before_model=True | request_id=1e882fa8-2fb3-46ca session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:52.051 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaService | trace_id=6aa32aa77f31e4163e span_id=5d70817524983fec |
| 22:09:52.055 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=cb12b269a9617aa4 |
| 22:09:52.204 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=e9b1fc2ce9f7178b |
| 22:09:52.208 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078192208,"body":{"isError":false,"lo | session_id=aegis-sp-a-3dc5f76 trace_id=6aa32aa77f31e4163e |
| 22:09:52.212 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078192212,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:09:52.312 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078192312,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:09:52.331 | runtime-span | lambda-segment | ben-fpg-mask-pii/LambdaService | trace_id=6aa32aa77f31e4163e span_id=2a13d8d5d73e5ae9 |
| 22:09:52.336 | runtime-span | lambda-segment | ben-fpg-mask-pii/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=c7e64f75bf9beb2a |
| 22:09:52.807 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa32aa77f31e4163e session_id=aegis-sp-a-3dc5f76 request_id=3ac9ee87-b0e8-46ea tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:52.808 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=42d6d9ed6d6ecac8 |
| 22:09:52.812 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078192812,"body":{"isError":false,"re | trace_id=6aa32aa77f31e4163e |
| 22:09:52.812 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078192812,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:09:52.817 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5983 out=430 | trace_id=6aa32aa77f31e4163e span_id=4ef020e446e50281 session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:52.817 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa32aa77f31e4163e span_id=48a940e0b0a6cb1c session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:52.818 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32aa77f31e4163e span_id=00512391303445a2 session_id=aegis-sp-a-3dc5f76 |
| 22:09:52.818 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5983 out=430 | trace_id=6aa32aa77f31e4163e span_id=e4eedf43b9058dea session_id=aegis-sp-a-3dc5f76 request_id=1e882fa8-2fb3-46ca |
| 22:09:57.892 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32aa77f31e4163e span_id=ae8fb0ff404abdd4 session_id=aegis-sp-a-3dc5f76 |
| 22:09:57.900 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa32aa77f31e4163e span_id=788b748865909b1e session_id=aegis-sp-a-3dc5f76 |
| 22:09:57.909 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa32aa77f31e4163e span_id=9e7742e11168c4ec session_id=aegis-sp-a-3dc5f76 |
| 22:09:57.909 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa32aa77f31e4163e span_id=482ab92101b57e1e session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:58.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6606 out=561 masked_before_model=True | request_id=e1f09dea-7261-4300 session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:58.008 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaService | trace_id=6aa32aa77f31e4163e span_id=62e0ab3460972f27 |
| 22:09:58.012 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=e3c10e536c564ac6 |
| 22:09:58.156 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=35722be295372c7d |
| 22:09:58.159 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078198159,"body":{"isError":false,"lo | session_id=aegis-sp-a-3dc5f76 trace_id=6aa32aa77f31e4163e |
| 22:09:58.165 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078198165,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:09:58.234 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078198234,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:09:58.260 | runtime-span | lambda-segment | ben-fpg-assess-eligibility/LambdaService | trace_id=6aa32aa77f31e4163e span_id=38983a0c91f675a0 |
| 22:09:58.264 | runtime-span | lambda-segment | ben-fpg-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=62c895ffe4d7e741 |
| 22:09:58.287 | lambda | call | assess_eligibility -> ok | trace_id=6aa32aa77f31e4163e session_id=aegis-sp-a-3dc5f76 request_id=2ae23ba5-ad63-44cc tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:58.288 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=ecaa7552265c18e9 |
| 22:09:58.292 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078198292,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:09:58.292 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078198292,"body":{"isError":false,"re | trace_id=6aa32aa77f31e4163e |
| 22:09:58.297 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa32aa77f31e4163e span_id=12eb681c25d079ab session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:58.298 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6606 out=561 | trace_id=6aa32aa77f31e4163e span_id=f516fcc647a8ddc5 session_id=aegis-sp-a-3dc5f76 request_id=e1f09dea-7261-4300 |
| 22:09:58.298 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6606 out=561 | trace_id=6aa32aa77f31e4163e span_id=5a19e77485c4f400 session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:09:58.299 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32aa77f31e4163e span_id=7e64d1e6edca009f session_id=aegis-sp-a-3dc5f76 |
| 22:10:04.549 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32aa77f31e4163e span_id=7a8d54b4a078732e session_id=aegis-sp-a-3dc5f76 |
| 22:10:04.556 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa32aa77f31e4163e span_id=427e155711e1d1b7 session_id=aegis-sp-a-3dc5f76 |
| 22:10:04.580 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa32aa77f31e4163e span_id=ab446bb723b10ed9 session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:10:04.581 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa32aa77f31e4163e span_id=e39d35d879e5db2d session_id=aegis-sp-a-3dc5f76 |
| 22:10:04.717 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaService | trace_id=6aa32aa77f31e4163e span_id=3662c963bfda9e45 |
| 22:10:04.723 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=bcbb6b38452db55f |
| 22:10:04.896 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=5663bb64c0daaae5 |
| 22:10:04.901 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078204901,"body":{"isError":false,"lo | session_id=aegis-sp-a-3dc5f76 trace_id=6aa32aa77f31e4163e |
| 22:10:04.905 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078204905,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:10:05.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7215 out=335 masked_before_model=True | request_id=625c39df-f515-49c4 session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:10:05.013 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078205013,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:10:05.043 | runtime-span | lambda-segment | ben-fpg-core-tools/LambdaService | trace_id=6aa32aa77f31e4163e span_id=7b97a53d938a5c84 |
| 22:10:05.047 | runtime-span | lambda-segment | ben-fpg-core-tools/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=747c80a9e9837ffc |
| 22:10:05.072 | lambda | call | benefits_core -> committed=False | trace_id=6aa32aa77f31e4163e session_id=aegis-sp-a-3dc5f76 request_id=e14c017d-d1cc-43bd tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:10:05.072 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=f4f517c0b5cf37b1 |
| 22:10:05.077 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078205077,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:10:05.077 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078205077,"body":{"isError":false,"re | trace_id=6aa32aa77f31e4163e |
| 22:10:05.082 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa32aa77f31e4163e span_id=9df56b2e75b5c0e2 session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:10:05.084 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7215 out=335 | trace_id=6aa32aa77f31e4163e span_id=f607b20b2f3c7a80 session_id=aegis-sp-a-3dc5f76 request_id=625c39df-f515-49c4 |
| 22:10:05.084 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7215 out=335 | trace_id=6aa32aa77f31e4163e span_id=f1ac38ab3484b4cc session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:10:05.089 | runtime-span | span | SSM.GetParameter | trace_id=6aa32aa77f31e4163e span_id=b0051e19ec72affa session_id=aegis-sp-a-3dc5f76 |
| 22:10:05.125 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32aa77f31e4163e span_id=1234c5279957b43d session_id=aegis-sp-a-3dc5f76 |
| 22:10:10.911 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32aa77f31e4163e span_id=fb7805c98dd4ca71 session_id=aegis-sp-a-3dc5f76 |
| 22:10:10.919 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa32aa77f31e4163e span_id=896ebd68787b576a session_id=aegis-sp-a-3dc5f76 |
| 22:10:10.946 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa32aa77f31e4163e span_id=af3aeee2aebb003e session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:10:10.947 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa32aa77f31e4163e span_id=04ffee096c660f8f session_id=aegis-sp-a-3dc5f76 |
| 22:10:11.000 | worm | evidence | INTENT benefits-determination seq=0 chain=caa44726357d… | trace_id=6aa32aa77f31e4163e session_id=aegis-sp-a-3dc5f76 request_id=5fe4229a-69e1-4806 tenant=sp-a |
| 22:10:11.064 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaService | trace_id=6aa32aa77f31e4163e span_id=23789a26293aa06b |
| 22:10:11.068 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=33aaf5c20dfccfbf |
| 22:10:11.220 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=e1de9ac33916a115 |
| 22:10:11.224 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078211224,"body":{"isError":false,"lo | session_id=aegis-sp-a-3dc5f76 trace_id=6aa32aa77f31e4163e |
| 22:10:11.227 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078211227,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:10:11.302 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078211302,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:10:11.329 | runtime-span | lambda-segment | ben-fpg-write-audit/LambdaService | trace_id=6aa32aa77f31e4163e span_id=6851d9a3b74a418c |
| 22:10:11.340 | runtime-span | lambda-segment | ben-fpg-write-audit/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=b092d04b4bb0db1d |
| 22:10:12.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7843 out=111 masked_before_model=True | request_id=44ba231b-02e9-4693 session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:10:12.104 | lambda | call | write_audit -> stored=True | trace_id=6aa32aa77f31e4163e session_id=aegis-sp-a-3dc5f76 request_id=5fe4229a-69e1-4806 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:10:12.104 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=0f817e489e1018c0 |
| 22:10:12.108 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078212108,"body":{"isError":false,"re | trace_id=6aa32aa77f31e4163e |
| 22:10:12.109 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078212109,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:10:12.114 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa32aa77f31e4163e span_id=fc2218ed6ba068b1 session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:10:12.115 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7843 out=111 | trace_id=6aa32aa77f31e4163e span_id=8e4ea48ac563c3f5 session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:10:12.116 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7843 out=111 | trace_id=6aa32aa77f31e4163e span_id=c10db284d6d4c912 session_id=aegis-sp-a-3dc5f76 request_id=44ba231b-02e9-4693 |
| 22:10:12.117 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32aa77f31e4163e span_id=c0ba378eed41cd6e session_id=aegis-sp-a-3dc5f76 |
| 22:10:15.192 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32aa77f31e4163e span_id=a2ea1783eb11cd7b session_id=aegis-sp-a-3dc5f76 |
| 22:10:15.199 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa32aa77f31e4163e span_id=746f1654b6e21e86 session_id=aegis-sp-a-3dc5f76 |
| 22:10:15.205 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa32aa77f31e4163e span_id=85efe58388e6d986 session_id=aegis-sp-a-3dc5f76 |
| 22:10:15.213 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa32aa77f31e4163e span_id=81e68dd987b790dc session_id=aegis-sp-a-3dc5f76 |
| 22:10:15.213 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa32aa77f31e4163e span_id=5e560dd042129b07 session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:10:15.305 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaService | trace_id=6aa32aa77f31e4163e span_id=260d8024b8da330c |
| 22:10:15.319 | runtime-span | lambda-segment | ben-fpg-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=2b3937a4f4710456 |
| 22:10:15.463 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=0cf20e6aea05439c |
| 22:10:15.466 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078215466,"body":{"isError":false,"lo | session_id=aegis-sp-a-3dc5f76 trace_id=6aa32aa77f31e4163e |
| 22:10:15.472 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078215472,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:10:15.548 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078215548,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:10:15.575 | runtime-span | lambda-segment | ben-fpg-request-signoff/LambdaService | trace_id=6aa32aa77f31e4163e span_id=05ae1fb3d9db8991 |
| 22:10:15.727 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=9170604f0d869aee |
| 22:10:16.079 | runtime-span | lambda-segment | ben-fpg-request-signoff/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=0f90924fb325fbdb |
| 22:10:17.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8005 out=456 masked_before_model=True | request_id=9300578c-414e-44cd session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:10:17.501 | lambda | call | request_signoff -> requested=False | trace_id=6aa32aa77f31e4163e session_id=aegis-sp-a-3dc5f76 request_id=133e7777-66a7-4dcc tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:10:17.502 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa32aa77f31e4163e span_id=15f1df0718dea1b9 |
| 22:10:17.506 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078217506,"body":{"isError":false,"lo | trace_id=6aa32aa77f31e4163e |
| 22:10:17.506 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpg-ben-gw-x61kuvgtqs","event_timestamp":1789078217506,"body":{"isError":false,"re | trace_id=6aa32aa77f31e4163e |
| 22:10:17.511 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa32aa77f31e4163e span_id=984fac2cb3dfca25 session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:10:17.513 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8005 out=456 | trace_id=6aa32aa77f31e4163e span_id=3bde723d9fbfcdc4 session_id=aegis-sp-a-3dc5f76 request_id=9300578c-414e-44cd |
| 22:10:17.513 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8005 out=456 | trace_id=6aa32aa77f31e4163e span_id=6f3b18eb3377c2f3 session_id=aegis-sp-a-3dc5f76 tenant=sp-a case_id=OBS-SPA-B8337 |
| 22:10:17.514 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32aa77f31e4163e span_id=b8bdebd630493dda session_id=aegis-sp-a-3dc5f76 |
| 22:10:26.675 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa32aa77f31e4163e span_id=fc0489cffcadc80c session_id=aegis-sp-a-3dc5f76 |
| 22:10:26.682 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa32aa77f31e4163e span_id=f29b0fceeabfb152 session_id=aegis-sp-a-3dc5f76 |
