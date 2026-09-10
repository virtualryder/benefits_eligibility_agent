# Case trace — `OBS-SPB-E083C` (tenant `sp-b`)

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
| sessions | ['aegis-sp-b-0a498081fb854bbea00c7d801f52f4fe'] |
| single_tenant | True |
| tenants_seen | ['sp-b'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 00:30:59.021 | lambda | call | ingest_application -> ingested=True | trace_id=6aa1fa426f60277b00 request_id=7b9f9c48-f4cf-453a tenant=sp-b case_id=OBS-SPB-E083C |
| 00:30:59.691 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa1fa435b623d036b span_id=57522e73f628e60f session_id=aegis-sp-b-0a49808 |
| 00:31:00.204 | runtime-span | runtime-http | POST /invocations | trace_id=6aa1fa435b623d036b span_id=a903571597e110fa session_id=aegis-sp-b-0a49808 |
| 00:31:00.274 | runtime-span | span | SSM.GetParameter | trace_id=6aa1fa435b623d036b span_id=7964b2c797284c4a session_id=aegis-sp-b-0a49808 |
| 00:31:00.313 | runtime-span | span | SSM.GetParameter | trace_id=6aa1fa435b623d036b span_id=1eef4023d988bffa session_id=aegis-sp-b-0a49808 |
| 00:31:00.366 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa1fa435b623d036b span_id=071cd8a170c9fcf0 session_id=aegis-sp-b-0a49808 |
| 00:31:00.412 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa1fa435b623d036b span_id=a2cad2cec180c356 session_id=aegis-sp-b-0a49808 |
| 00:31:00.488 | runtime-span | span | mcp.session | trace_id=6aa1fa435b623d036b span_id=1469be405fb5437b session_id=aegis-sp-b-0a49808 |
| 00:31:00.636 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa1fa435b623d036b span_id=b841bb458088e657 session_id=aegis-sp-b-0a49808 |
| 00:31:00.868 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaService | trace_id=6aa1fa435b623d036b span_id=5cbd4376f0ff865a |
| 00:31:00.873 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=a0cb99a9aec61bdd |
| 00:31:00.897 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=2f24d7debe186798 |
| 00:31:00.901 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000260901,"body":{"isError":false,"lo | session_id=aegis-sp-b-0a49808 trace_id=6aa1fa435b623d036b |
| 00:31:00.904 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000260904,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:00.984 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000260984,"body":{"isError":false,"re | trace_id=6aa1fa435b623d036b |
| 00:31:00.993 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1fa435b623d036b span_id=dbaa494398d385d2 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:00.993 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=46602 out=2109 | trace_id=6aa1fa435b623d036b span_id=5d60030cd37b2d68 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:00.994 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5343 out=140 | trace_id=6aa1fa435b623d036b span_id=3e6f50aa6a2ff526 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:00.997 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa435b623d036b span_id=8a9b09abbdc897ba session_id=aegis-sp-b-0a49808 |
| 00:31:00.997 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5343 out=140 | trace_id=6aa1fa435b623d036b span_id=011b344d285612d5 session_id=aegis-sp-b-0a49808 request_id=e4aabac1-2d2b-49e9 |
| 00:31:01.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5343 out=140 masked_before_model=True | request_id=e4aabac1-2d2b-49e9 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:04.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5561 out=122 masked_before_model=True | request_id=909ce5ba-1029-4824 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:04.234 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa435b623d036b span_id=481c9ba897feebb9 session_id=aegis-sp-b-0a49808 |
| 00:31:04.248 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1fa435b623d036b span_id=0a25754e2165ec89 session_id=aegis-sp-b-0a49808 |
| 00:31:04.277 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa1fa435b623d036b span_id=a1f8a33df7dbd7c7 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:04.278 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa1fa435b623d036b span_id=c4f06ad310c568c9 session_id=aegis-sp-b-0a49808 |
| 00:31:04.368 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaService | trace_id=6aa1fa435b623d036b span_id=7c7cd7fa124d5acb |
| 00:31:04.372 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=3132c0ec1b0697fe |
| 00:31:04.540 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=a38b8344bc6b8893 |
| 00:31:04.544 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000264544,"body":{"isError":false,"lo | session_id=aegis-sp-b-0a49808 trace_id=6aa1fa435b623d036b |
| 00:31:04.549 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000264549,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:04.633 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000264633,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:04.656 | runtime-span | lambda-segment | ben-fp7-intake-application/LambdaService | trace_id=6aa1fa435b623d036b span_id=5788f891755cce4c |
| 00:31:04.661 | runtime-span | lambda-segment | ben-fp7-intake-application/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=9a3628891e705ddb |
| 00:31:04.836 | lambda | call | intake_application -> ok | trace_id=6aa1fa435b623d036b session_id=aegis-sp-b-0a49808 request_id=4f438750-af93-48c3 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:04.836 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=ce3c0f94be8d943a |
| 00:31:04.839 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000264839,"body":{"isError":false,"re | trace_id=6aa1fa435b623d036b |
| 00:31:04.840 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000264840,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:04.845 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1fa435b623d036b span_id=e82305e72e164eab session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:04.846 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa435b623d036b span_id=f27f1b3840334581 session_id=aegis-sp-b-0a49808 |
| 00:31:04.846 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5561 out=122 | trace_id=6aa1fa435b623d036b span_id=c52086a43fcbd5b3 session_id=aegis-sp-b-0a49808 request_id=909ce5ba-1029-4824 |
| 00:31:04.846 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5561 out=122 | trace_id=6aa1fa435b623d036b span_id=983ec8d19e666262 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:07.518 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa435b623d036b span_id=aecb05fa85ab67fd session_id=aegis-sp-b-0a49808 |
| 00:31:07.524 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1fa435b623d036b span_id=43dcb7de61063d1e session_id=aegis-sp-b-0a49808 |
| 00:31:07.532 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa1fa435b623d036b span_id=e33f7438e8539455 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:07.533 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa1fa435b623d036b span_id=fc93e26f33c5415e session_id=aegis-sp-b-0a49808 |
| 00:31:07.670 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaService | trace_id=6aa1fa435b623d036b span_id=2ebae307dae9b7a5 |
| 00:31:07.680 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=368af1539402a4af |
| 00:31:07.836 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=f610dada91b3ec02 |
| 00:31:07.841 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000267841,"body":{"isError":false,"lo | session_id=aegis-sp-b-0a49808 trace_id=6aa1fa435b623d036b |
| 00:31:07.846 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000267846,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:07.923 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000267923,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:07.944 | runtime-span | lambda-segment | ben-fp7-mask-pii/LambdaService | trace_id=6aa1fa435b623d036b span_id=7c67e9d927a515ae |
| 00:31:07.949 | runtime-span | lambda-segment | ben-fp7-mask-pii/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=4bdc54cd8242dba6 |
| 00:31:08.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5984 out=391 masked_before_model=True | request_id=e3188e84-3091-4baf session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:08.521 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa1fa435b623d036b session_id=aegis-sp-b-0a49808 request_id=3a669ee0-9332-4f1c tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:08.521 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=67c479598e0f2fcd |
| 00:31:08.526 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000268526,"body":{"isError":false,"re | trace_id=6aa1fa435b623d036b |
| 00:31:08.526 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000268526,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:08.531 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1fa435b623d036b span_id=1e4f770f5448e5b9 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:08.532 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5984 out=391 | trace_id=6aa1fa435b623d036b span_id=64ba54ca9e9bdff0 session_id=aegis-sp-b-0a49808 request_id=e3188e84-3091-4baf |
| 00:31:08.532 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5984 out=391 | trace_id=6aa1fa435b623d036b span_id=c59fa5feef4206b1 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:08.533 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa435b623d036b span_id=288f6a3aeb5c1510 session_id=aegis-sp-b-0a49808 |
| 00:31:13.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6606 out=560 masked_before_model=True | request_id=ff268d4b-56ce-4a37 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:13.180 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa435b623d036b span_id=e662913d0eade52e session_id=aegis-sp-b-0a49808 |
| 00:31:13.187 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1fa435b623d036b span_id=c4a9b11595621090 session_id=aegis-sp-b-0a49808 |
| 00:31:13.197 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa1fa435b623d036b span_id=a6961272b4554e48 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:13.198 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa1fa435b623d036b span_id=3e5924284a9e3ef2 session_id=aegis-sp-b-0a49808 |
| 00:31:13.288 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaService | trace_id=6aa1fa435b623d036b span_id=13c8eaa833bf1e40 |
| 00:31:13.294 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=6416e7d013d6ffef |
| 00:31:13.464 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=d675d2606cfb635f |
| 00:31:13.469 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000273469,"body":{"isError":false,"lo | session_id=aegis-sp-b-0a49808 trace_id=6aa1fa435b623d036b |
| 00:31:13.473 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000273473,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:13.557 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000273557,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:13.584 | runtime-span | lambda-segment | ben-fp7-assess-eligibility/LambdaService | trace_id=6aa1fa435b623d036b span_id=2f63549073d5ca3b |
| 00:31:13.591 | runtime-span | lambda-segment | ben-fp7-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=d4c43ae5252c5916 |
| 00:31:13.633 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=4fb45469b0df1189 |
| 00:31:13.634 | lambda | call | assess_eligibility -> ok | trace_id=6aa1fa435b623d036b session_id=aegis-sp-b-0a49808 request_id=dd264f14-d0da-40ab tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:13.643 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000273643,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:13.643 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000273643,"body":{"isError":false,"re | trace_id=6aa1fa435b623d036b |
| 00:31:13.648 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1fa435b623d036b span_id=6ff71720e0f977b6 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:13.649 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6606 out=560 | trace_id=6aa1fa435b623d036b span_id=7c1e4d8b13dc3127 session_id=aegis-sp-b-0a49808 request_id=ff268d4b-56ce-4a37 |
| 00:31:13.649 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6606 out=560 | trace_id=6aa1fa435b623d036b span_id=630f087786f2f40f session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:13.650 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa435b623d036b span_id=f93b489dc6960da4 session_id=aegis-sp-b-0a49808 |
| 00:31:20.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7214 out=344 masked_before_model=True | request_id=7d0dca1f-593b-4900 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:20.120 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa435b623d036b span_id=be8d1b103e4d9833 session_id=aegis-sp-b-0a49808 |
| 00:31:20.127 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1fa435b623d036b span_id=20cb1488d3327f74 session_id=aegis-sp-b-0a49808 |
| 00:31:20.157 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa1fa435b623d036b span_id=0c5a1bdd5dd0ad92 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:20.158 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa1fa435b623d036b span_id=39ade126a4961fd4 session_id=aegis-sp-b-0a49808 |
| 00:31:20.276 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaService | trace_id=6aa1fa435b623d036b span_id=6321f035ca4834c4 |
| 00:31:20.281 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=ed461cc38b31a346 |
| 00:31:20.459 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=b2a0c4d01871a2a1 |
| 00:31:20.463 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000280463,"body":{"isError":false,"lo | session_id=aegis-sp-b-0a49808 trace_id=6aa1fa435b623d036b |
| 00:31:20.469 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000280469,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:20.539 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000280539,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:20.572 | runtime-span | lambda-segment | ben-fp7-core-tools/LambdaService | trace_id=6aa1fa435b623d036b span_id=75a94b6919b662b2 |
| 00:31:20.577 | runtime-span | lambda-segment | ben-fp7-core-tools/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=a467ba6c2760b9ea |
| 00:31:20.603 | lambda | call | benefits_core -> committed=False | trace_id=6aa1fa435b623d036b session_id=aegis-sp-b-0a49808 request_id=c16c119a-a7fe-4aff tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:20.603 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=257c1d6f4cf85613 |
| 00:31:20.607 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000280607,"body":{"isError":false,"re | trace_id=6aa1fa435b623d036b |
| 00:31:20.607 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000280607,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:20.612 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1fa435b623d036b span_id=d56bb5a7736579d9 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:20.613 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7214 out=344 | trace_id=6aa1fa435b623d036b span_id=70aaf6bad7609a51 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:20.614 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7214 out=344 | trace_id=6aa1fa435b623d036b span_id=ca401f8e865bd40a session_id=aegis-sp-b-0a49808 request_id=7d0dca1f-593b-4900 |
| 00:31:20.619 | runtime-span | span | SSM.GetParameter | trace_id=6aa1fa435b623d036b span_id=52e8c27f24a4ccb3 session_id=aegis-sp-b-0a49808 |
| 00:31:20.656 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa435b623d036b span_id=4bb32cd4baa222ea session_id=aegis-sp-b-0a49808 |
| 00:31:26.454 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa435b623d036b span_id=db5717e5ef9df36f session_id=aegis-sp-b-0a49808 |
| 00:31:26.460 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1fa435b623d036b span_id=8e5289e86cf2f47a session_id=aegis-sp-b-0a49808 |
| 00:31:26.488 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa1fa435b623d036b span_id=4d37e41c723a0bf9 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:26.489 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa1fa435b623d036b span_id=f1cc82c7fc2f6206 session_id=aegis-sp-b-0a49808 |
| 00:31:26.608 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaService | trace_id=6aa1fa435b623d036b span_id=0f1cd0893042fc7c |
| 00:31:26.613 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=44a25c06ef155abc |
| 00:31:26.761 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=8c6ca760a1723d70 |
| 00:31:26.765 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000286765,"body":{"isError":false,"lo | session_id=aegis-sp-b-0a49808 trace_id=6aa1fa435b623d036b |
| 00:31:26.768 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000286768,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:26.859 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000286859,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:26.884 | runtime-span | lambda-segment | ben-fp7-write-audit/LambdaService | trace_id=6aa1fa435b623d036b span_id=1a9062389e40908f |
| 00:31:26.889 | runtime-span | lambda-segment | ben-fp7-write-audit/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=5c7ce0d865f3304f |
| 00:31:27.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7866 out=111 masked_before_model=True | request_id=483d8845-ac56-4ad0 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:27.000 | worm | evidence | INTENT benefits-determination seq=0 chain=2abd08a2c7a4… | trace_id=6aa1fa435b623d036b session_id=aegis-sp-b-0a49808 request_id=12670b8d-3d80-48e1 tenant=sp-b |
| 00:31:27.329 | lambda | call | write_audit -> stored=True | trace_id=6aa1fa435b623d036b session_id=aegis-sp-b-0a49808 request_id=12670b8d-3d80-48e1 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:27.343 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=389a926b0a6f74a6 |
| 00:31:27.347 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000287347,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:27.347 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000287347,"body":{"isError":false,"re | trace_id=6aa1fa435b623d036b |
| 00:31:27.352 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1fa435b623d036b span_id=e1c030343fa1fead session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:27.353 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7866 out=111 | trace_id=6aa1fa435b623d036b span_id=e2cb4f1c07af16a4 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:27.354 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7866 out=111 | trace_id=6aa1fa435b623d036b span_id=e0ab040a24822992 session_id=aegis-sp-b-0a49808 request_id=483d8845-ac56-4ad0 |
| 00:31:27.355 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa435b623d036b span_id=a69e45ecef61610e session_id=aegis-sp-b-0a49808 |
| 00:31:29.915 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa435b623d036b span_id=5ed2b28742835eae session_id=aegis-sp-b-0a49808 |
| 00:31:29.921 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1fa435b623d036b span_id=efb471a15ed02408 session_id=aegis-sp-b-0a49808 |
| 00:31:29.929 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa1fa435b623d036b span_id=75bad6b7396c0707 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:29.930 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa1fa435b623d036b span_id=61e79bb8035eaea9 session_id=aegis-sp-b-0a49808 |
| 00:31:30.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8028 out=441 masked_before_model=True | request_id=d1aea1c5-6f5c-45e6 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:30.039 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaService | trace_id=6aa1fa435b623d036b span_id=7966254c7eb1d734 |
| 00:31:30.043 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=5d68cd45eaedf9b6 |
| 00:31:30.190 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=315989a182d116bc |
| 00:31:30.193 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000290193,"body":{"isError":false,"lo | session_id=aegis-sp-b-0a49808 trace_id=6aa1fa435b623d036b |
| 00:31:30.198 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000290198,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:30.277 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000290277,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:30.304 | runtime-span | lambda-segment | ben-fp7-request-signoff/LambdaService | trace_id=6aa1fa435b623d036b span_id=20bd3a6c1b7ca47e |
| 00:31:30.310 | runtime-span | lambda-segment | ben-fp7-request-signoff/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=0d804b998f543843 |
| 00:31:30.329 | lambda | call | request_signoff -> requested=False | trace_id=6aa1fa435b623d036b session_id=aegis-sp-b-0a49808 request_id=8b1a465f-7b03-4882 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:30.329 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa435b623d036b span_id=8f6e0249a1cbed00 |
| 00:31:30.335 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000290335,"body":{"isError":false,"lo | trace_id=6aa1fa435b623d036b |
| 00:31:30.335 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000290335,"body":{"isError":false,"re | trace_id=6aa1fa435b623d036b |
| 00:31:30.339 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1fa435b623d036b span_id=3e1a45bfd42a2ca5 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:30.340 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8028 out=441 | trace_id=6aa1fa435b623d036b span_id=5db07bb38e9e5b95 session_id=aegis-sp-b-0a49808 tenant=sp-b case_id=OBS-SPB-E083C |
| 00:31:30.341 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8028 out=441 | trace_id=6aa1fa435b623d036b span_id=ee5a978884e642f2 session_id=aegis-sp-b-0a49808 request_id=d1aea1c5-6f5c-45e6 |
| 00:31:30.342 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa435b623d036b span_id=50f088d033561657 session_id=aegis-sp-b-0a49808 |
| 00:31:39.230 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa435b623d036b span_id=5686304ae6489224 session_id=aegis-sp-b-0a49808 |
| 00:31:39.236 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa1fa435b623d036b span_id=08756598981228ae session_id=aegis-sp-b-0a49808 |
| 00:31:39.240 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1fa435b623d036b span_id=f9efbe632e5aa4d7 session_id=aegis-sp-b-0a49808 |
