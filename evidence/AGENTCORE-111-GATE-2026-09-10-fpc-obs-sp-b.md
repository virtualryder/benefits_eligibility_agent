# Case trace — `OBS-SPB-EE891` (tenant `sp-b`)

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
| sessions | ['aegis-sp-b-2105ea519b034396809e7e105932922c'] |
| single_tenant | True |
| tenants_seen | ['sp-b'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 16:09:39.980 | lambda | call | ingest_application -> ingested=True | trace_id=6aa2d643196e98fc09 request_id=1ea9b949-1a55-4936 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:40.652 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa2d64411da81733e span_id=bed61542978c7c33 session_id=aegis-sp-b-2105ea5 |
| 16:09:41.691 | runtime-span | runtime-http | POST /invocations | trace_id=6aa2d64411da81733e span_id=cf7914c991a25b59 session_id=aegis-sp-b-2105ea5 |
| 16:09:41.781 | runtime-span | span | SSM.GetParameter | trace_id=6aa2d64411da81733e span_id=433bdf29815e7938 session_id=aegis-sp-b-2105ea5 |
| 16:09:41.830 | runtime-span | span | SSM.GetParameter | trace_id=6aa2d64411da81733e span_id=ef2a1585658cff83 session_id=aegis-sp-b-2105ea5 |
| 16:09:41.890 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa2d64411da81733e span_id=ba1d230742865fba session_id=aegis-sp-b-2105ea5 |
| 16:09:41.943 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa2d64411da81733e span_id=d3d0c6160a4a31f0 session_id=aegis-sp-b-2105ea5 |
| 16:09:42.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5339 out=210 masked_before_model=True | request_id=d30db6f4-4dc0-48d8 session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:42.038 | runtime-span | span | mcp.session | trace_id=6aa2d64411da81733e span_id=1bdf4a3c74329c7d session_id=aegis-sp-b-2105ea5 |
| 16:09:42.114 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa2d64411da81733e span_id=07443c46c1484eb2 session_id=aegis-sp-b-2105ea5 |
| 16:09:42.326 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaService | trace_id=6aa2d64411da81733e span_id=2785cc8e10f583f5 |
| 16:09:42.332 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=c61aea32f30b19ee |
| 16:09:42.332 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=4cb0512f8b7d4e63 |
| 16:09:42.336 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056582336,"body":{"isError":false,"lo | session_id=aegis-sp-b-2105ea5 trace_id=6aa2d64411da81733e |
| 16:09:42.341 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056582341,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:09:42.422 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056582422,"body":{"isError":false,"re | trace_id=6aa2d64411da81733e |
| 16:09:42.431 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=33155 out=2130 | trace_id=6aa2d64411da81733e span_id=9a4a1b667c66c0db session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:42.432 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2d64411da81733e span_id=60119399a05bfcb0 session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:42.433 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5339 out=210 | trace_id=6aa2d64411da81733e span_id=c948345b8ba50bdb session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:42.443 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d64411da81733e span_id=c3863579c134c334 session_id=aegis-sp-b-2105ea5 |
| 16:09:42.443 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5339 out=210 | trace_id=6aa2d64411da81733e span_id=221873d4a18b796f session_id=aegis-sp-b-2105ea5 request_id=d30db6f4-4dc0-48d8 |
| 16:09:46.170 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d64411da81733e span_id=ab1f2c2c02a6b60b session_id=aegis-sp-b-2105ea5 |
| 16:09:46.205 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2d64411da81733e span_id=f4ac3bbfce24323f session_id=aegis-sp-b-2105ea5 |
| 16:09:46.288 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa2d64411da81733e span_id=1a95bcd12e80661c session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:46.289 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa2d64411da81733e span_id=a6fd33e1bcdc2409 session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:46.290 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa2d64411da81733e span_id=9194d8d6189f6fe7 session_id=aegis-sp-b-2105ea5 |
| 16:09:46.290 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa2d64411da81733e span_id=33aff1019844e942 session_id=aegis-sp-b-2105ea5 |
| 16:09:46.426 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaService | trace_id=6aa2d64411da81733e span_id=476f7e1d758d7c9c |
| 16:09:46.432 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaService | trace_id=6aa2d64411da81733e span_id=7c3ba9d04c8735e6 |
| 16:09:46.435 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=83837c96393ed839 |
| 16:09:46.440 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=c7647e6fc6b7107f |
| 16:09:46.640 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=e0e76f10b82c094b |
| 16:09:46.643 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056586643,"body":{"isError":false,"lo | session_id=aegis-sp-b-2105ea5 trace_id=6aa2d64411da81733e |
| 16:09:46.646 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056586646,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:09:46.720 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056586720,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:09:46.747 | runtime-span | lambda-segment | ben-fpc-mask-pii/LambdaService | trace_id=6aa2d64411da81733e span_id=2ba7a19bda3cef6f |
| 16:09:46.751 | runtime-span | lambda-segment | ben-fpc-mask-pii/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=8669137290fefa77 |
| 16:09:46.849 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=7d0e2904e56bf8a6 |
| 16:09:46.853 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056586853,"body":{"isError":false,"lo | session_id=aegis-sp-b-2105ea5 trace_id=6aa2d64411da81733e |
| 16:09:46.859 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056586859,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:09:46.944 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056586944,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:09:46.973 | runtime-span | lambda-segment | ben-fpc-intake-application/LambdaService | trace_id=6aa2d64411da81733e span_id=6e99b2ca95004ee3 |
| 16:09:46.978 | runtime-span | lambda-segment | ben-fpc-intake-application/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=e4a77b0ad33a60ae |
| 16:09:47.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5976 out=394 masked_before_model=True | request_id=caf81141-00ea-4918 session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:47.159 | lambda | call | intake_application -> ok | trace_id=6aa2d64411da81733e session_id=aegis-sp-b-2105ea5 request_id=0aa396ed-702e-4e3d tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:47.159 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=a429ea17f4b35be0 |
| 16:09:47.164 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056587164,"body":{"isError":false,"re | trace_id=6aa2d64411da81733e |
| 16:09:47.165 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056587165,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:09:47.231 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa2d64411da81733e session_id=aegis-sp-b-2105ea5 request_id=445e8a8f-1613-42da tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:47.232 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=131436c76b570bed |
| 16:09:47.237 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056587237,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:09:47.237 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056587237,"body":{"isError":false,"re | trace_id=6aa2d64411da81733e |
| 16:09:47.242 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2d64411da81733e span_id=c9a42f0ce2c8b6c0 session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:47.243 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5976 out=394 | trace_id=6aa2d64411da81733e span_id=e1107eddaccfff97 session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:47.244 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d64411da81733e span_id=61da6ea15f9fd769 session_id=aegis-sp-b-2105ea5 |
| 16:09:47.244 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5976 out=394 | trace_id=6aa2d64411da81733e span_id=8ddddf0e45b9b2a5 session_id=aegis-sp-b-2105ea5 request_id=caf81141-00ea-4918 |
| 16:09:52.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6601 out=562 masked_before_model=True | request_id=ed6bfc4c-1b59-4719 session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:52.128 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d64411da81733e span_id=15f43c756ca9a53b session_id=aegis-sp-b-2105ea5 |
| 16:09:52.134 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2d64411da81733e span_id=477c2ebd47257829 session_id=aegis-sp-b-2105ea5 |
| 16:09:52.144 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa2d64411da81733e span_id=63642bb7f015c1fd session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:52.145 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa2d64411da81733e span_id=4599e2135bf46a2c session_id=aegis-sp-b-2105ea5 |
| 16:09:52.237 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaService | trace_id=6aa2d64411da81733e span_id=4e740909e1afa837 |
| 16:09:52.241 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=a8d063ae68b45620 |
| 16:09:52.411 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=20a7975d6284cc6c |
| 16:09:52.415 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056592415,"body":{"isError":false,"lo | session_id=aegis-sp-b-2105ea5 trace_id=6aa2d64411da81733e |
| 16:09:52.422 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056592422,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:09:52.499 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056592499,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:09:52.529 | runtime-span | lambda-segment | ben-fpc-assess-eligibility/LambdaService | trace_id=6aa2d64411da81733e span_id=44ce1b77849e21ef |
| 16:09:52.535 | runtime-span | lambda-segment | ben-fpc-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=d3d33f3207e40b56 |
| 16:09:52.565 | lambda | call | assess_eligibility -> ok | trace_id=6aa2d64411da81733e session_id=aegis-sp-b-2105ea5 request_id=6db488c6-db35-4afa tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:52.566 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=bd9c31c5aa04dbaa |
| 16:09:52.571 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056592571,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:09:52.571 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056592571,"body":{"isError":false,"re | trace_id=6aa2d64411da81733e |
| 16:09:52.577 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2d64411da81733e span_id=0505665d9c3417cd session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:52.579 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6601 out=562 | trace_id=6aa2d64411da81733e span_id=45c324738e0394e9 session_id=aegis-sp-b-2105ea5 request_id=ed6bfc4c-1b59-4719 |
| 16:09:52.579 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6601 out=562 | trace_id=6aa2d64411da81733e span_id=884ded50e4187b36 session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:52.580 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d64411da81733e span_id=81646a36724773d8 session_id=aegis-sp-b-2105ea5 |
| 16:09:59.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7211 out=426 masked_before_model=True | request_id=ba725cca-089b-4df8 session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:59.298 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d64411da81733e span_id=8ecca35b994cd30d session_id=aegis-sp-b-2105ea5 |
| 16:09:59.304 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2d64411da81733e span_id=77a9e117279c96a4 session_id=aegis-sp-b-2105ea5 |
| 16:09:59.337 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa2d64411da81733e span_id=ee3cae922e127ded session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:59.338 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa2d64411da81733e span_id=acd115088314a585 session_id=aegis-sp-b-2105ea5 |
| 16:09:59.443 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaService | trace_id=6aa2d64411da81733e span_id=3c6a2625c6ff5a35 |
| 16:09:59.447 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=f76f1c7331945234 |
| 16:09:59.644 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=a24b3dbdca6ceae9 |
| 16:09:59.647 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056599647,"body":{"isError":false,"lo | session_id=aegis-sp-b-2105ea5 trace_id=6aa2d64411da81733e |
| 16:09:59.650 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056599650,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:09:59.718 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056599718,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:09:59.733 | runtime-span | lambda-segment | ben-fpc-core-tools/LambdaService | trace_id=6aa2d64411da81733e span_id=2329297f32128290 |
| 16:09:59.739 | runtime-span | lambda-segment | ben-fpc-core-tools/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=2469bdc0cee5e6cf |
| 16:09:59.764 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=958b822dd46c8b05 |
| 16:09:59.765 | lambda | call | benefits_core -> committed=False | trace_id=6aa2d64411da81733e session_id=aegis-sp-b-2105ea5 request_id=3ddb9071-fdd1-4e05 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:59.769 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056599769,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:09:59.769 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056599769,"body":{"isError":false,"re | trace_id=6aa2d64411da81733e |
| 16:09:59.774 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2d64411da81733e span_id=9f2072013f30f50f session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:59.776 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7211 out=426 | trace_id=6aa2d64411da81733e span_id=4225c8a55c89f76f session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:09:59.777 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7211 out=426 | trace_id=6aa2d64411da81733e span_id=4ec92e1eef4ae560 session_id=aegis-sp-b-2105ea5 request_id=ba725cca-089b-4df8 |
| 16:09:59.783 | runtime-span | span | SSM.GetParameter | trace_id=6aa2d64411da81733e span_id=a351c66547c98db0 session_id=aegis-sp-b-2105ea5 |
| 16:09:59.824 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d64411da81733e span_id=659efed962c61539 session_id=aegis-sp-b-2105ea5 |
| 16:10:06.000 | worm | evidence | INTENT benefits-determination seq=0 chain=23c38bd3958c… | trace_id=6aa2d64411da81733e session_id=aegis-sp-b-2105ea5 request_id=4fe3b0d8-ef6d-405b tenant=sp-b |
| 16:10:06.133 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d64411da81733e span_id=8c0e010fbf8fec30 session_id=aegis-sp-b-2105ea5 |
| 16:10:06.138 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2d64411da81733e span_id=201eb2e8aaecb9e2 session_id=aegis-sp-b-2105ea5 |
| 16:10:06.169 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa2d64411da81733e span_id=4464c3de08ebdd0c session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:10:06.170 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa2d64411da81733e span_id=c080805d1eb2c951 session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:10:06.171 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa2d64411da81733e span_id=383bf7fb742aa9a7 session_id=aegis-sp-b-2105ea5 |
| 16:10:06.171 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa2d64411da81733e span_id=23648776acf53917 session_id=aegis-sp-b-2105ea5 |
| 16:10:06.278 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaService | trace_id=6aa2d64411da81733e span_id=45ea2528e75bab39 |
| 16:10:06.282 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=4b17d2894db1a2d2 |
| 16:10:06.282 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaService | trace_id=6aa2d64411da81733e span_id=1a91be3034f89def |
| 16:10:06.288 | runtime-span | lambda-segment | ben-fpc-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=e4df1290372bd691 |
| 16:10:06.452 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=37b94b46c5d68039 |
| 16:10:06.455 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056606455,"body":{"isError":false,"lo | session_id=aegis-sp-b-2105ea5 trace_id=6aa2d64411da81733e |
| 16:10:06.456 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=f266792d4ec8e431 |
| 16:10:06.459 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056606459,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:10:06.460 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056606460,"body":{"isError":false,"lo | session_id=aegis-sp-b-2105ea5 trace_id=6aa2d64411da81733e |
| 16:10:06.465 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056606465,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:10:06.532 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056606532,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:10:06.547 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056606547,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:10:06.559 | runtime-span | lambda-segment | ben-fpc-request-signoff/LambdaService | trace_id=6aa2d64411da81733e span_id=57f77406ff7a495c |
| 16:10:06.562 | runtime-span | lambda-segment | ben-fpc-request-signoff/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=07c12fd0cc9ec187 |
| 16:10:06.563 | runtime-span | lambda-segment | ben-fpc-write-audit/LambdaService | trace_id=6aa2d64411da81733e span_id=6aaf2d564a8e7a86 |
| 16:10:06.567 | runtime-span | lambda-segment | ben-fpc-write-audit/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=8fcc3a00ee116230 |
| 16:10:06.583 | lambda | call | request_signoff -> requested=False | trace_id=6aa2d64411da81733e session_id=aegis-sp-b-2105ea5 request_id=780bc21c-9d88-4ace tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:10:06.584 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=68f7c6a361c22943 |
| 16:10:06.587 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056606587,"body":{"isError":false,"re | trace_id=6aa2d64411da81733e |
| 16:10:06.587 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056606587,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:10:07.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8028 out=538 masked_before_model=True | request_id=9d21da63-a40b-488c session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:10:07.071 | lambda | call | write_audit -> stored=True | trace_id=6aa2d64411da81733e session_id=aegis-sp-b-2105ea5 request_id=4fe3b0d8-ef6d-405b tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:10:07.072 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2d64411da81733e span_id=bfb97aa3a951a2f2 |
| 16:10:07.077 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056607077,"body":{"isError":false,"re | trace_id=6aa2d64411da81733e |
| 16:10:07.077 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpc-ben-gw-xweky2wdti","event_timestamp":1789056607077,"body":{"isError":false,"lo | trace_id=6aa2d64411da81733e |
| 16:10:07.083 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2d64411da81733e span_id=9e4f0ccc2a319cc8 session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:10:07.085 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8028 out=538 | trace_id=6aa2d64411da81733e span_id=19501f0bc0f05ada session_id=aegis-sp-b-2105ea5 tenant=sp-b case_id=OBS-SPB-EE891 |
| 16:10:07.086 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d64411da81733e span_id=afe08a8a28413885 session_id=aegis-sp-b-2105ea5 |
| 16:10:07.086 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8028 out=538 | trace_id=6aa2d64411da81733e span_id=66407e3ae19b00cd session_id=aegis-sp-b-2105ea5 request_id=9d21da63-a40b-488c |
| 16:10:16.670 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2d64411da81733e span_id=a5961be641652701 session_id=aegis-sp-b-2105ea5 |
| 16:10:16.676 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa2d64411da81733e span_id=096adae9e607b7ba session_id=aegis-sp-b-2105ea5 |
| 16:10:16.679 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2d64411da81733e span_id=43a09aea7575e66a session_id=aegis-sp-b-2105ea5 |
