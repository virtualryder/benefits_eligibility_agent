# Case trace — `OBS-SPA-B993F` (tenant `sp-a`)

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
| sessions | ['aegis-sp-a-acb2cd74e392462bb803e851d209ef44'] |
| single_tenant | True |
| tenants_seen | ['sp-a'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 02:05:32.251 | lambda | call | ingest_application -> ingested=True | trace_id=6aa2106b3f69767908 request_id=816ffcfc-bc68-4ae8 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:32.722 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa2106c6c2ed32f79 span_id=da6c0679962533c7 session_id=aegis-sp-a-acb2cd7 |
| 02:05:33.321 | runtime-span | runtime-http | POST /invocations | trace_id=6aa2106c6c2ed32f79 span_id=0a3b551f11f47fd1 session_id=aegis-sp-a-acb2cd7 |
| 02:05:33.413 | runtime-span | span | SSM.GetParameter | trace_id=6aa2106c6c2ed32f79 span_id=f6892888dd4a301c session_id=aegis-sp-a-acb2cd7 |
| 02:05:33.456 | runtime-span | span | SSM.GetParameter | trace_id=6aa2106c6c2ed32f79 span_id=9fc6a998eb3ba100 session_id=aegis-sp-a-acb2cd7 |
| 02:05:33.528 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa2106c6c2ed32f79 span_id=e4fc55b468c811bd session_id=aegis-sp-a-acb2cd7 |
| 02:05:33.578 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa2106c6c2ed32f79 span_id=4ce920191b11dcb2 session_id=aegis-sp-a-acb2cd7 |
| 02:05:33.673 | runtime-span | span | mcp.session | trace_id=6aa2106c6c2ed32f79 span_id=8fd60b338b6b405e session_id=aegis-sp-a-acb2cd7 |
| 02:05:33.807 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa2106c6c2ed32f79 span_id=78e257c195791b0e session_id=aegis-sp-a-acb2cd7 |
| 02:05:34.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5339 out=136 masked_before_model=True | request_id=ba8aa39e-9083-48ff session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:34.062 | runtime-span | lambda-segment | ben-fp8-tenant-interceptor/LambdaService | trace_id=6aa2106c6c2ed32f79 span_id=1ed1a7bb3b5673dd |
| 02:05:34.069 | runtime-span | lambda-segment | ben-fp8-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=2efc71465db5a965 |
| 02:05:34.089 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=e88614ebed4ba132 |
| 02:05:34.093 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005934093,"body":{"isError":false,"lo | session_id=aegis-sp-a-acb2cd7 trace_id=6aa2106c6c2ed32f79 |
| 02:05:34.097 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005934097,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:05:34.187 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005934187,"body":{"isError":false,"re | trace_id=6aa2106c6c2ed32f79 |
| 02:05:34.195 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=46564 out=2115 | trace_id=6aa2106c6c2ed32f79 span_id=af719eb46b7941ff session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:34.196 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2106c6c2ed32f79 span_id=17d8789822ce28a1 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:34.205 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5339 out=136 | trace_id=6aa2106c6c2ed32f79 span_id=85615d99a4cd4514 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:34.208 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2106c6c2ed32f79 span_id=2f3de802d4ec9916 session_id=aegis-sp-a-acb2cd7 |
| 02:05:34.208 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5339 out=136 | trace_id=6aa2106c6c2ed32f79 span_id=8986325227ad48e0 session_id=aegis-sp-a-acb2cd7 request_id=ba8aa39e-9083-48ff |
| 02:05:37.495 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2106c6c2ed32f79 span_id=05dc8404b48382ad session_id=aegis-sp-a-acb2cd7 |
| 02:05:37.511 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2106c6c2ed32f79 span_id=fe071c4518e94154 session_id=aegis-sp-a-acb2cd7 |
| 02:05:37.538 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa2106c6c2ed32f79 span_id=371e67662bd206fd session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:37.540 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa2106c6c2ed32f79 span_id=db814a487c5e23ec session_id=aegis-sp-a-acb2cd7 |
| 02:05:37.592 | runtime-span | lambda-segment | ben-fp8-tenant-interceptor/LambdaService | trace_id=6aa2106c6c2ed32f79 span_id=56ec6fc2dc70648f |
| 02:05:37.598 | runtime-span | lambda-segment | ben-fp8-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=5d636ab4bb1bc2fe |
| 02:05:37.982 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=b6e6d215437599db |
| 02:05:37.986 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005937986,"body":{"isError":false,"lo | session_id=aegis-sp-a-acb2cd7 trace_id=6aa2106c6c2ed32f79 |
| 02:05:37.988 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005937988,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:05:38.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5553 out=118 masked_before_model=True | request_id=1630a459-51ed-43e7 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:38.083 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005938083,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:05:38.112 | runtime-span | lambda-segment | ben-fp8-intake-application/LambdaService | trace_id=6aa2106c6c2ed32f79 span_id=0e89546289034479 |
| 02:05:38.117 | runtime-span | lambda-segment | ben-fp8-intake-application/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=83fc85a323a1c758 |
| 02:05:38.300 | lambda | call | intake_application -> ok | trace_id=6aa2106c6c2ed32f79 session_id=aegis-sp-a-acb2cd7 request_id=f705fda8-4d99-49ce tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:38.300 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=533d27e8a3140085 |
| 02:05:38.306 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005938306,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:05:38.306 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005938306,"body":{"isError":false,"re | trace_id=6aa2106c6c2ed32f79 |
| 02:05:38.312 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2106c6c2ed32f79 span_id=6436e8ffaef72f93 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:38.313 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5553 out=118 | trace_id=6aa2106c6c2ed32f79 span_id=56b665a46fd12881 session_id=aegis-sp-a-acb2cd7 request_id=1630a459-51ed-43e7 |
| 02:05:38.313 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5553 out=118 | trace_id=6aa2106c6c2ed32f79 span_id=86db2d1787650b43 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:38.314 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2106c6c2ed32f79 span_id=1f102d38eded8037 session_id=aegis-sp-a-acb2cd7 |
| 02:05:41.130 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2106c6c2ed32f79 span_id=9205d846d73b3a9c session_id=aegis-sp-a-acb2cd7 |
| 02:05:41.136 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2106c6c2ed32f79 span_id=390c38ce3b503778 session_id=aegis-sp-a-acb2cd7 |
| 02:05:41.145 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa2106c6c2ed32f79 span_id=de4b43c6da51dfec session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:41.146 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa2106c6c2ed32f79 span_id=5eda7a871f5839d2 session_id=aegis-sp-a-acb2cd7 |
| 02:05:41.262 | runtime-span | lambda-segment | ben-fp8-tenant-interceptor/LambdaService | trace_id=6aa2106c6c2ed32f79 span_id=0c246f259c65fc36 |
| 02:05:41.266 | runtime-span | lambda-segment | ben-fp8-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=0a8778956d68f4f3 |
| 02:05:41.408 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=773a975f9decbdea |
| 02:05:41.411 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005941411,"body":{"isError":false,"lo | session_id=aegis-sp-a-acb2cd7 trace_id=6aa2106c6c2ed32f79 |
| 02:05:41.416 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005941416,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:05:41.500 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005941500,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:05:41.520 | runtime-span | lambda-segment | ben-fp8-mask-pii/LambdaService | trace_id=6aa2106c6c2ed32f79 span_id=2bfe4085b7c4d86d |
| 02:05:41.526 | runtime-span | lambda-segment | ben-fp8-mask-pii/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=553e88d388e2558e |
| 02:05:42.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5978 out=397 masked_before_model=True | request_id=d112ba99-73d2-4dc6 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:42.016 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa2106c6c2ed32f79 session_id=aegis-sp-a-acb2cd7 request_id=f8c2b32b-98b4-4ca7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:42.016 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=8818136d9d380785 |
| 02:05:42.021 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005942021,"body":{"isError":false,"re | trace_id=6aa2106c6c2ed32f79 |
| 02:05:42.021 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005942021,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:05:42.027 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2106c6c2ed32f79 span_id=be732645fc3618d9 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:42.028 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5978 out=397 | trace_id=6aa2106c6c2ed32f79 span_id=70180e805f03e364 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:42.029 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2106c6c2ed32f79 span_id=2dd59ea8235092e3 session_id=aegis-sp-a-acb2cd7 |
| 02:05:42.029 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5978 out=397 | trace_id=6aa2106c6c2ed32f79 span_id=778ad8145bb145eb session_id=aegis-sp-a-acb2cd7 request_id=d112ba99-73d2-4dc6 |
| 02:05:46.566 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2106c6c2ed32f79 span_id=31dea9c12e4dd223 session_id=aegis-sp-a-acb2cd7 |
| 02:05:46.572 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2106c6c2ed32f79 span_id=18875fa51af53788 session_id=aegis-sp-a-acb2cd7 |
| 02:05:46.586 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa2106c6c2ed32f79 span_id=7324f8a44ac76f23 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:46.587 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa2106c6c2ed32f79 span_id=a2c4d2113c4bfefe session_id=aegis-sp-a-acb2cd7 |
| 02:05:46.677 | runtime-span | lambda-segment | ben-fp8-tenant-interceptor/LambdaService | trace_id=6aa2106c6c2ed32f79 span_id=67eabb080a9d3fb6 |
| 02:05:46.684 | runtime-span | lambda-segment | ben-fp8-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=8cabf710c4925117 |
| 02:05:46.846 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=d12cee0cc46ec7b8 |
| 02:05:46.850 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005946850,"body":{"isError":false,"lo | session_id=aegis-sp-a-acb2cd7 trace_id=6aa2106c6c2ed32f79 |
| 02:05:46.853 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005946853,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:05:46.933 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005946933,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:05:46.963 | runtime-span | lambda-segment | ben-fp8-assess-eligibility/LambdaService | trace_id=6aa2106c6c2ed32f79 span_id=301d254855143484 |
| 02:05:46.968 | runtime-span | lambda-segment | ben-fp8-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=3ea5a8a20bfc35f7 |
| 02:05:46.992 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=dc31eee4143aa51d |
| 02:05:46.993 | lambda | call | assess_eligibility -> ok | trace_id=6aa2106c6c2ed32f79 session_id=aegis-sp-a-acb2cd7 request_id=2c4b9cdb-42fa-4d4c tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:46.998 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005946998,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:05:46.998 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005946998,"body":{"isError":false,"re | trace_id=6aa2106c6c2ed32f79 |
| 02:05:47.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6606 out=566 masked_before_model=True | request_id=4776175c-a9a6-49b4 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:47.004 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2106c6c2ed32f79 span_id=30c5a839a3ad2218 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:47.005 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6606 out=566 | trace_id=6aa2106c6c2ed32f79 span_id=dacc164d7fdd3716 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:47.006 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2106c6c2ed32f79 span_id=f8e9bade3499c423 session_id=aegis-sp-a-acb2cd7 |
| 02:05:47.006 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6606 out=566 | trace_id=6aa2106c6c2ed32f79 span_id=1c38d60fe4deb518 session_id=aegis-sp-a-acb2cd7 request_id=4776175c-a9a6-49b4 |
| 02:05:53.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7220 out=334 masked_before_model=True | request_id=3aac0771-f3cc-46f4 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:53.194 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2106c6c2ed32f79 span_id=9c37dc5dca74bf96 session_id=aegis-sp-a-acb2cd7 |
| 02:05:53.200 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2106c6c2ed32f79 span_id=893afe1332287d97 session_id=aegis-sp-a-acb2cd7 |
| 02:05:53.232 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa2106c6c2ed32f79 span_id=ca7842a09252a8a1 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:53.233 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa2106c6c2ed32f79 span_id=13001966dd7a6943 session_id=aegis-sp-a-acb2cd7 |
| 02:05:53.360 | runtime-span | lambda-segment | ben-fp8-tenant-interceptor/LambdaService | trace_id=6aa2106c6c2ed32f79 span_id=7296db3e4ce1f96c |
| 02:05:53.364 | runtime-span | lambda-segment | ben-fp8-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=c6f1feecbb67759a |
| 02:05:53.540 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=b59ce1f29395ccb1 |
| 02:05:53.544 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005953544,"body":{"isError":false,"lo | session_id=aegis-sp-a-acb2cd7 trace_id=6aa2106c6c2ed32f79 |
| 02:05:53.547 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005953547,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:05:53.615 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005953615,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:05:53.644 | runtime-span | lambda-segment | ben-fp8-core-tools/LambdaService | trace_id=6aa2106c6c2ed32f79 span_id=6e4569b743e2202b |
| 02:05:53.650 | runtime-span | lambda-segment | ben-fp8-core-tools/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=4cf4dd8488ed9604 |
| 02:05:53.674 | lambda | call | benefits_core -> committed=False | trace_id=6aa2106c6c2ed32f79 session_id=aegis-sp-a-acb2cd7 request_id=cf4d1bbb-c3f9-45da tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:53.675 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=0bcf68905d104509 |
| 02:05:53.679 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005953679,"body":{"isError":false,"re | trace_id=6aa2106c6c2ed32f79 |
| 02:05:53.679 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005953679,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:05:53.685 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2106c6c2ed32f79 span_id=8be832e730f6e188 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:53.686 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7220 out=334 | trace_id=6aa2106c6c2ed32f79 span_id=df9ca24da5a879bb session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:53.687 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7220 out=334 | trace_id=6aa2106c6c2ed32f79 span_id=f01df80a8702cfab session_id=aegis-sp-a-acb2cd7 request_id=3aac0771-f3cc-46f4 |
| 02:05:53.694 | runtime-span | span | SSM.GetParameter | trace_id=6aa2106c6c2ed32f79 span_id=bdfd9e625e09a238 session_id=aegis-sp-a-acb2cd7 |
| 02:05:53.729 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2106c6c2ed32f79 span_id=b0f7e08da4332877 session_id=aegis-sp-a-acb2cd7 |
| 02:05:59.348 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2106c6c2ed32f79 span_id=f06d07fa3a3559c9 session_id=aegis-sp-a-acb2cd7 |
| 02:05:59.354 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2106c6c2ed32f79 span_id=00ed8d3627c9246c session_id=aegis-sp-a-acb2cd7 |
| 02:05:59.384 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa2106c6c2ed32f79 span_id=f222ef2cc9b60a41 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:05:59.385 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa2106c6c2ed32f79 span_id=f60f4473765d5e3b session_id=aegis-sp-a-acb2cd7 |
| 02:05:59.520 | runtime-span | lambda-segment | ben-fp8-tenant-interceptor/LambdaService | trace_id=6aa2106c6c2ed32f79 span_id=7d0342527f750bfb |
| 02:05:59.525 | runtime-span | lambda-segment | ben-fp8-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=c64bad55087cec44 |
| 02:05:59.531 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=a604f1474b78a6ee |
| 02:05:59.533 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005959533,"body":{"isError":false,"lo | session_id=aegis-sp-a-acb2cd7 trace_id=6aa2106c6c2ed32f79 |
| 02:05:59.537 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005959537,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:05:59.617 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005959617,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:05:59.648 | runtime-span | lambda-segment | ben-fp8-write-audit/LambdaService | trace_id=6aa2106c6c2ed32f79 span_id=3d23c2c871bfb057 |
| 02:05:59.653 | runtime-span | lambda-segment | ben-fp8-write-audit/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=70568981e3dd31ba |
| 02:06:00.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7853 out=111 masked_before_model=True | request_id=d5d7bbdb-f0ff-444f session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:06:00.000 | worm | evidence | INTENT benefits-determination seq=0 chain=99e56ad34a86… | trace_id=6aa2106c6c2ed32f79 session_id=aegis-sp-a-acb2cd7 request_id=b493c0e3-9fc1-4cfb tenant=sp-a |
| 02:06:00.450 | lambda | call | write_audit -> stored=True | trace_id=6aa2106c6c2ed32f79 session_id=aegis-sp-a-acb2cd7 request_id=b493c0e3-9fc1-4cfb tenant=sp-a case_id=OBS-SPA-B993F |
| 02:06:00.457 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=85c8e671a17031c2 |
| 02:06:00.463 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005960463,"body":{"isError":false,"re | trace_id=6aa2106c6c2ed32f79 |
| 02:06:00.463 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005960463,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:06:00.469 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2106c6c2ed32f79 span_id=cfce311a34c3f25b session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:06:00.471 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7853 out=111 | trace_id=6aa2106c6c2ed32f79 span_id=ebab65ca8efc51aa session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:06:00.472 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7853 out=111 | trace_id=6aa2106c6c2ed32f79 span_id=e4f12fe722f782e6 session_id=aegis-sp-a-acb2cd7 request_id=d5d7bbdb-f0ff-444f |
| 02:06:00.473 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2106c6c2ed32f79 span_id=273424d2cbd39216 session_id=aegis-sp-a-acb2cd7 |
| 02:06:02.955 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2106c6c2ed32f79 span_id=9c41808b43b849e4 session_id=aegis-sp-a-acb2cd7 |
| 02:06:02.961 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2106c6c2ed32f79 span_id=3460246f62bd73a0 session_id=aegis-sp-a-acb2cd7 |
| 02:06:02.972 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa2106c6c2ed32f79 span_id=457b50f5a4b9c0d7 session_id=aegis-sp-a-acb2cd7 |
| 02:06:02.972 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa2106c6c2ed32f79 span_id=464a0bad1da76945 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:06:03.081 | runtime-span | lambda-segment | ben-fp8-tenant-interceptor/LambdaService | trace_id=6aa2106c6c2ed32f79 span_id=614edfddb1448e38 |
| 02:06:03.085 | runtime-span | lambda-segment | ben-fp8-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=fef66cca10f25adc |
| 02:06:03.249 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=7bab384502bca2d9 |
| 02:06:03.253 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005963253,"body":{"isError":false,"lo | session_id=aegis-sp-a-acb2cd7 trace_id=6aa2106c6c2ed32f79 |
| 02:06:03.257 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005963257,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:06:03.361 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005963361,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:06:03.397 | runtime-span | lambda-segment | ben-fp8-request-signoff/LambdaService | trace_id=6aa2106c6c2ed32f79 span_id=1297ae8e0e5ff11b |
| 02:06:03.558 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=483044cd21dfc7b8 |
| 02:06:03.894 | runtime-span | lambda-segment | ben-fp8-request-signoff/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=4b0337e31ff6907d |
| 02:06:05.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8015 out=453 masked_before_model=True | request_id=9ba0b353-5d6e-4d55 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:06:05.320 | lambda | call | request_signoff -> requested=False | trace_id=6aa2106c6c2ed32f79 session_id=aegis-sp-a-acb2cd7 request_id=5d447d37-a3b5-4e12 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:06:05.320 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2106c6c2ed32f79 span_id=6fe68a7880832751 |
| 02:06:05.325 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005965325,"body":{"isError":false,"lo | trace_id=6aa2106c6c2ed32f79 |
| 02:06:05.325 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp8-ben-gw-lvdzwlytyd","event_timestamp":1789005965325,"body":{"isError":false,"re | trace_id=6aa2106c6c2ed32f79 |
| 02:06:05.330 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2106c6c2ed32f79 span_id=dbfe20269230eec8 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:06:05.332 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8015 out=453 | trace_id=6aa2106c6c2ed32f79 span_id=66bfb28a6a7a23b4 session_id=aegis-sp-a-acb2cd7 tenant=sp-a case_id=OBS-SPA-B993F |
| 02:06:05.333 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8015 out=453 | trace_id=6aa2106c6c2ed32f79 span_id=d496c39bba6eff79 session_id=aegis-sp-a-acb2cd7 request_id=9ba0b353-5d6e-4d55 |
| 02:06:05.334 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa2106c6c2ed32f79 span_id=002ec023c602a83f session_id=aegis-sp-a-acb2cd7 |
| 02:06:05.338 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2106c6c2ed32f79 span_id=292a00b151d35691 session_id=aegis-sp-a-acb2cd7 |
| 02:06:14.130 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2106c6c2ed32f79 span_id=53582199b49587c4 session_id=aegis-sp-a-acb2cd7 |
| 02:06:14.136 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2106c6c2ed32f79 span_id=69520239bb9b0858 session_id=aegis-sp-a-acb2cd7 |
