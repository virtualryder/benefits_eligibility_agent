# Case trace — `OBS-SPA-A7E56` (tenant `sp-a`)

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
| sessions | ['aegis-sp-a-09d482f0fb2e4b9eae2cf2fabf7f4b75'] |
| single_tenant | True |
| tenants_seen | ['sp-a'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 19:09:00.386 | lambda | call | ingest_application -> ingested=True | trace_id=6aa3004c0783d3fd4d request_id=d786d961-c176-4796 tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:00.931 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa3004c29788dba2a span_id=76d7350133073638 session_id=aegis-sp-a-09d482f |
| 19:09:01.542 | runtime-span | runtime-http | POST /invocations | trace_id=6aa3004c29788dba2a span_id=7ba0f160fe3eb7fa session_id=aegis-sp-a-09d482f |
| 19:09:01.633 | runtime-span | span | SSM.GetParameter | trace_id=6aa3004c29788dba2a span_id=198d027aa92cd782 session_id=aegis-sp-a-09d482f |
| 19:09:01.683 | runtime-span | span | SSM.GetParameter | trace_id=6aa3004c29788dba2a span_id=feabc36d12291210 session_id=aegis-sp-a-09d482f |
| 19:09:01.761 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa3004c29788dba2a span_id=75638c544927b2b2 session_id=aegis-sp-a-09d482f |
| 19:09:01.812 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa3004c29788dba2a span_id=ca17af6aba529874 session_id=aegis-sp-a-09d482f |
| 19:09:01.907 | runtime-span | span | mcp.session | trace_id=6aa3004c29788dba2a span_id=78af1161fe4080ca session_id=aegis-sp-a-09d482f |
| 19:09:02.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5347 out=141 masked_before_model=True | request_id=59b0b6bf-23b9-441b session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:02.063 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa3004c29788dba2a span_id=532684954a3ca6fa session_id=aegis-sp-a-09d482f |
| 19:09:02.285 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaService | trace_id=6aa3004c29788dba2a span_id=38763a123534488a |
| 19:09:02.290 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=1c29a6beebee51dd |
| 19:09:02.311 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=919993b96633f2aa |
| 19:09:02.314 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067342314,"body":{"isError":false,"lo | session_id=aegis-sp-a-09d482f trace_id=6aa3004c29788dba2a |
| 19:09:02.319 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067342319,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:02.420 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067342420,"body":{"isError":false,"re | trace_id=6aa3004c29788dba2a |
| 19:09:02.427 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=46603 out=2098 | trace_id=6aa3004c29788dba2a span_id=c0f6d2c0fe2de94d session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:02.428 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa3004c29788dba2a span_id=8a0f89a4eaa04d82 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:02.437 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5347 out=141 | trace_id=6aa3004c29788dba2a span_id=160215b8fde89f9a session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:02.440 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5347 out=141 | trace_id=6aa3004c29788dba2a span_id=ff7e77e192cefcc9 session_id=aegis-sp-a-09d482f request_id=59b0b6bf-23b9-441b |
| 19:09:02.441 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa3004c29788dba2a span_id=66cff86c4fde049e session_id=aegis-sp-a-09d482f |
| 19:09:06.218 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa3004c29788dba2a span_id=e5db98dedd7def35 session_id=aegis-sp-a-09d482f |
| 19:09:06.234 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa3004c29788dba2a span_id=969418f470d3ef07 session_id=aegis-sp-a-09d482f |
| 19:09:06.266 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa3004c29788dba2a span_id=d595fb52b5a166c4 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:06.267 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa3004c29788dba2a span_id=ec5261dd9e1d60b1 session_id=aegis-sp-a-09d482f |
| 19:09:06.371 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaService | trace_id=6aa3004c29788dba2a span_id=44e2e5ec22fc0624 |
| 19:09:06.384 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=7d5d32dcea04ef50 |
| 19:09:06.777 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=23d1ca714eb2e3b6 |
| 19:09:06.781 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067346781,"body":{"isError":false,"lo | session_id=aegis-sp-a-09d482f trace_id=6aa3004c29788dba2a |
| 19:09:06.786 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067346786,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:06.867 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067346867,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:06.890 | runtime-span | lambda-segment | ben-fpf-intake-application/LambdaService | trace_id=6aa3004c29788dba2a span_id=4de45dd9c65cff34 |
| 19:09:06.901 | runtime-span | lambda-segment | ben-fpf-intake-application/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=1302058377b4b9be |
| 19:09:07.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5566 out=123 masked_before_model=True | request_id=de08b2c6-5428-4571 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:07.066 | lambda | call | intake_application -> ok | trace_id=6aa3004c29788dba2a session_id=aegis-sp-a-09d482f request_id=4fb4dfcc-8ffd-4ccb tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:07.070 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=2188a946c73e000c |
| 19:09:07.074 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067347074,"body":{"isError":false,"re | trace_id=6aa3004c29788dba2a |
| 19:09:07.074 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067347074,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:07.080 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa3004c29788dba2a span_id=290da3c4f6d8b02b session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:07.081 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5566 out=123 | trace_id=6aa3004c29788dba2a span_id=6f5b4d7b6d4eb81d session_id=aegis-sp-a-09d482f request_id=de08b2c6-5428-4571 |
| 19:09:07.081 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5566 out=123 | trace_id=6aa3004c29788dba2a span_id=418658f9ecb88241 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:07.082 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa3004c29788dba2a span_id=579d7478832d7337 session_id=aegis-sp-a-09d482f |
| 19:09:10.153 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa3004c29788dba2a span_id=4571278bf4d50ba2 session_id=aegis-sp-a-09d482f |
| 19:09:10.164 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa3004c29788dba2a span_id=8cd6c8797e6fa2cd session_id=aegis-sp-a-09d482f |
| 19:09:10.172 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa3004c29788dba2a span_id=b1f222367c663076 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:10.173 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa3004c29788dba2a span_id=3d6affa9267f8c49 session_id=aegis-sp-a-09d482f |
| 19:09:10.283 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaService | trace_id=6aa3004c29788dba2a span_id=5a7c146991e15c22 |
| 19:09:10.288 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=662c777d5320e193 |
| 19:09:10.454 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=5a602a2b3d5df420 |
| 19:09:10.457 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067350457,"body":{"isError":false,"lo | session_id=aegis-sp-a-09d482f trace_id=6aa3004c29788dba2a |
| 19:09:10.493 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067350493,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:10.580 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067350580,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:10.609 | runtime-span | lambda-segment | ben-fpf-mask-pii/LambdaService | trace_id=6aa3004c29788dba2a span_id=3cdad4dd08913ca6 |
| 19:09:10.615 | runtime-span | lambda-segment | ben-fpf-mask-pii/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=605b8412bed75b7e |
| 19:09:11.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5989 out=391 masked_before_model=True | request_id=7cfd4ab6-97e7-43f9 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:11.140 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa3004c29788dba2a session_id=aegis-sp-a-09d482f request_id=91bf7955-a176-45a7 tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:11.140 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=240fb8cbc183c7dd |
| 19:09:11.145 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067351145,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:11.145 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067351145,"body":{"isError":false,"re | trace_id=6aa3004c29788dba2a |
| 19:09:11.151 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa3004c29788dba2a span_id=ef32ee50ba22b7ac session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:11.152 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5989 out=391 | trace_id=6aa3004c29788dba2a span_id=b1d6060306ffc0d2 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:11.153 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa3004c29788dba2a span_id=2506cd3f5864cdb2 session_id=aegis-sp-a-09d482f |
| 19:09:11.153 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5989 out=391 | trace_id=6aa3004c29788dba2a span_id=fa96a2ce5ea3e3c4 session_id=aegis-sp-a-09d482f request_id=7cfd4ab6-97e7-43f9 |
| 19:09:15.847 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa3004c29788dba2a span_id=e85701d3f78defce session_id=aegis-sp-a-09d482f |
| 19:09:15.854 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa3004c29788dba2a span_id=b49c32c55c5e0cb4 session_id=aegis-sp-a-09d482f |
| 19:09:15.862 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa3004c29788dba2a span_id=537be82ddd012340 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:15.863 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa3004c29788dba2a span_id=e33855cfb22e5327 session_id=aegis-sp-a-09d482f |
| 19:09:15.957 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaService | trace_id=6aa3004c29788dba2a span_id=2f6f4f746cd16a13 |
| 19:09:15.962 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=f8b6c1b260aa06f5 |
| 19:09:16.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6611 out=560 masked_before_model=True | request_id=6ae558eb-e834-4d63 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:16.136 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=c0de302e3571a8a4 |
| 19:09:16.139 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067356139,"body":{"isError":false,"lo | session_id=aegis-sp-a-09d482f trace_id=6aa3004c29788dba2a |
| 19:09:16.142 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067356142,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:16.217 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067356217,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:16.252 | runtime-span | lambda-segment | ben-fpf-assess-eligibility/LambdaService | trace_id=6aa3004c29788dba2a span_id=29cecbc37cd3a3f4 |
| 19:09:16.259 | runtime-span | lambda-segment | ben-fpf-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=751c45a164102b1b |
| 19:09:16.289 | lambda | call | assess_eligibility -> ok | trace_id=6aa3004c29788dba2a session_id=aegis-sp-a-09d482f request_id=0c57c0fe-4bb4-4950 tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:16.289 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=e562956aea948cba |
| 19:09:16.294 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067356294,"body":{"isError":false,"re | trace_id=6aa3004c29788dba2a |
| 19:09:16.295 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067356295,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:16.300 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa3004c29788dba2a span_id=f49ab3912daee4c7 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:16.301 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6611 out=560 | trace_id=6aa3004c29788dba2a span_id=96074ac48c0cee39 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:16.302 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6611 out=560 | trace_id=6aa3004c29788dba2a span_id=2919f1bef9900726 session_id=aegis-sp-a-09d482f request_id=6ae558eb-e834-4d63 |
| 19:09:16.303 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa3004c29788dba2a span_id=f1302ef598ce2739 session_id=aegis-sp-a-09d482f |
| 19:09:22.809 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa3004c29788dba2a span_id=5e3ce91d905bbde4 session_id=aegis-sp-a-09d482f |
| 19:09:22.815 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa3004c29788dba2a span_id=bfba432375daf5c8 session_id=aegis-sp-a-09d482f |
| 19:09:22.848 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa3004c29788dba2a span_id=a6eb24ebe5c3b43e session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:22.849 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa3004c29788dba2a span_id=3a53e7a3c3baffe5 session_id=aegis-sp-a-09d482f |
| 19:09:22.952 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaService | trace_id=6aa3004c29788dba2a span_id=0624b441d9bbdfcc |
| 19:09:22.958 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=27a155486f218a91 |
| 19:09:23.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7220 out=331 masked_before_model=True | request_id=49e37502-1513-424d session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:23.134 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=98f5bf8e4388ea31 |
| 19:09:23.138 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067363138,"body":{"isError":false,"lo | session_id=aegis-sp-a-09d482f trace_id=6aa3004c29788dba2a |
| 19:09:23.142 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067363142,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:23.224 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067363224,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:23.252 | runtime-span | lambda-segment | ben-fpf-core-tools/LambdaService | trace_id=6aa3004c29788dba2a span_id=288ac356122229f4 |
| 19:09:23.258 | runtime-span | lambda-segment | ben-fpf-core-tools/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=27966ca5e07a796a |
| 19:09:23.278 | lambda | call | benefits_core -> committed=False | trace_id=6aa3004c29788dba2a session_id=aegis-sp-a-09d482f request_id=7a140430-904c-4eec tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:23.278 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=d2feef8c95253031 |
| 19:09:23.282 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067363282,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:23.282 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067363282,"body":{"isError":false,"re | trace_id=6aa3004c29788dba2a |
| 19:09:23.288 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa3004c29788dba2a span_id=9bfd47635b2b2c21 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:23.290 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7220 out=331 | trace_id=6aa3004c29788dba2a span_id=213346d4bb6887d2 session_id=aegis-sp-a-09d482f request_id=49e37502-1513-424d |
| 19:09:23.290 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7220 out=331 | trace_id=6aa3004c29788dba2a span_id=8b4ffe4f62fffcee session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:23.297 | runtime-span | span | SSM.GetParameter | trace_id=6aa3004c29788dba2a span_id=76c8a64f8b490372 session_id=aegis-sp-a-09d482f |
| 19:09:23.338 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa3004c29788dba2a span_id=e367c3817db4fca4 session_id=aegis-sp-a-09d482f |
| 19:09:28.536 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa3004c29788dba2a span_id=1736b1dbef025929 session_id=aegis-sp-a-09d482f |
| 19:09:28.543 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa3004c29788dba2a span_id=6dda02a8318dba2f session_id=aegis-sp-a-09d482f |
| 19:09:28.552 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa3004c29788dba2a span_id=de6faf64581a2fa2 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:28.553 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa3004c29788dba2a span_id=2cf3aaf654476a8b session_id=aegis-sp-a-09d482f |
| 19:09:28.656 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaService | trace_id=6aa3004c29788dba2a span_id=36d24ae47bcbb534 |
| 19:09:28.660 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=e074e9cb582dc5b0 |
| 19:09:28.832 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=66603d38f264a05e |
| 19:09:28.837 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067368837,"body":{"isError":false,"lo | session_id=aegis-sp-a-09d482f trace_id=6aa3004c29788dba2a |
| 19:09:28.841 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067368841,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:28.924 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067368924,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:28.950 | runtime-span | lambda-segment | ben-fpf-write-audit/LambdaService | trace_id=6aa3004c29788dba2a span_id=487a43ac89de7e0f |
| 19:09:28.956 | runtime-span | lambda-segment | ben-fpf-write-audit/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=800acaf4c55442e9 |
| 19:09:29.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7853 out=113 masked_before_model=True | request_id=8e25b6fe-5323-4a55 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:29.000 | worm | evidence | INTENT benefits-determination seq=0 chain=592cf91f979f… | trace_id=6aa3004c29788dba2a session_id=aegis-sp-a-09d482f request_id=32963f5c-2832-4ad0 tenant=sp-a |
| 19:09:29.725 | lambda | call | write_audit -> stored=True | trace_id=6aa3004c29788dba2a session_id=aegis-sp-a-09d482f request_id=32963f5c-2832-4ad0 tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:29.726 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=4d4514171e882115 |
| 19:09:29.730 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067369730,"body":{"isError":false,"re | trace_id=6aa3004c29788dba2a |
| 19:09:29.731 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067369731,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:29.736 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa3004c29788dba2a span_id=f9db973f11a397f1 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:29.738 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7853 out=113 | trace_id=6aa3004c29788dba2a span_id=faba865d75202598 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:29.739 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7853 out=113 | trace_id=6aa3004c29788dba2a span_id=5ddd216e8e5cd1d4 session_id=aegis-sp-a-09d482f request_id=8e25b6fe-5323-4a55 |
| 19:09:29.740 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa3004c29788dba2a span_id=49130eefa5c4acbf session_id=aegis-sp-a-09d482f |
| 19:09:32.401 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa3004c29788dba2a span_id=a1620002d135cbd6 session_id=aegis-sp-a-09d482f |
| 19:09:32.408 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa3004c29788dba2a span_id=158e0dc6de44538d session_id=aegis-sp-a-09d482f |
| 19:09:32.412 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa3004c29788dba2a span_id=db32a45d6e40e491 session_id=aegis-sp-a-09d482f |
| 19:09:32.421 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa3004c29788dba2a span_id=59634db1d5c5f038 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:32.422 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa3004c29788dba2a span_id=0e11726c2acbc514 session_id=aegis-sp-a-09d482f |
| 19:09:32.523 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaService | trace_id=6aa3004c29788dba2a span_id=6b549602297eb9e7 |
| 19:09:32.527 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=ab0dd61d9e455226 |
| 19:09:32.696 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=1f3bded8853fe601 |
| 19:09:32.699 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067372699,"body":{"isError":false,"lo | session_id=aegis-sp-a-09d482f trace_id=6aa3004c29788dba2a |
| 19:09:32.942 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067372942,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:33.035 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067373035,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:33.071 | runtime-span | lambda-segment | ben-fpf-request-signoff/LambdaService | trace_id=6aa3004c29788dba2a span_id=0d41bfdfc54c2fb4 |
| 19:09:33.257 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=e90eecf05a27043d |
| 19:09:33.642 | runtime-span | lambda-segment | ben-fpf-request-signoff/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=ac289812246e58c6 |
| 19:09:35.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8017 out=439 masked_before_model=True | request_id=3e67b103-3632-41af session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:35.168 | lambda | call | request_signoff -> requested=False | trace_id=6aa3004c29788dba2a session_id=aegis-sp-a-09d482f request_id=d46f0597-8692-4927 tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:35.169 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa3004c29788dba2a span_id=cc541bd97a126040 |
| 19:09:35.181 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067375181,"body":{"isError":false,"re | trace_id=6aa3004c29788dba2a |
| 19:09:35.181 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067375181,"body":{"isError":false,"lo | trace_id=6aa3004c29788dba2a |
| 19:09:35.187 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa3004c29788dba2a span_id=68ff1592502704c3 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:35.188 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8017 out=439 | trace_id=6aa3004c29788dba2a span_id=a6cdf05a283f95b0 session_id=aegis-sp-a-09d482f tenant=sp-a case_id=OBS-SPA-A7E56 |
| 19:09:35.190 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa3004c29788dba2a span_id=af7f56038b4ca018 session_id=aegis-sp-a-09d482f |
| 19:09:35.190 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8017 out=439 | trace_id=6aa3004c29788dba2a span_id=b01d2a9d262ccd16 session_id=aegis-sp-a-09d482f request_id=3e67b103-3632-41af |
| 19:09:44.568 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa3004c29788dba2a span_id=56addb7194806771 session_id=aegis-sp-a-09d482f |
| 19:09:44.574 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa3004c29788dba2a span_id=c2733b07eaac8e06 session_id=aegis-sp-a-09d482f |
