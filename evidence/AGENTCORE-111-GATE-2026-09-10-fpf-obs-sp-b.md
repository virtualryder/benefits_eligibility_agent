# Case trace — `OBS-SPB-91850` (tenant `sp-b`)

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
| sessions | ['aegis-sp-b-4307b92030ec4911a197867b08112cdb'] |
| single_tenant | True |
| tenants_seen | ['sp-b'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 19:09:45.094 | lambda | call | ingest_application -> ingested=True | trace_id=6aa300787b9ae5010d request_id=59976bbc-dbce-447e tenant=sp-b case_id=OBS-SPB-91850 |
| 19:09:45.854 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa300797625bc4864 span_id=7a6eca1596035b5e session_id=aegis-sp-b-4307b92 |
| 19:09:46.449 | runtime-span | runtime-http | POST /invocations | trace_id=6aa300797625bc4864 span_id=353a76e2e3d38d28 session_id=aegis-sp-b-4307b92 |
| 19:09:46.540 | runtime-span | span | SSM.GetParameter | trace_id=6aa300797625bc4864 span_id=53d7a293e7c8e817 session_id=aegis-sp-b-4307b92 |
| 19:09:46.585 | runtime-span | span | SSM.GetParameter | trace_id=6aa300797625bc4864 span_id=c07dad69c8bad862 session_id=aegis-sp-b-4307b92 |
| 19:09:46.655 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa300797625bc4864 span_id=b0fe36f2133b5b00 session_id=aegis-sp-b-4307b92 |
| 19:09:46.706 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa300797625bc4864 span_id=88a0b45c82b48873 session_id=aegis-sp-b-4307b92 |
| 19:09:46.803 | runtime-span | span | mcp.session | trace_id=6aa300797625bc4864 span_id=a818c56c44549c48 session_id=aegis-sp-b-4307b92 |
| 19:09:46.924 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa300797625bc4864 span_id=6c39b326fa3adc3e session_id=aegis-sp-b-4307b92 |
| 19:09:47.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5338 out=214 masked_before_model=True | request_id=8424bde2-bca4-4b3c session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:09:47.186 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaService | trace_id=6aa300797625bc4864 span_id=72500d82c094d3db |
| 19:09:47.197 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=ac861bdba649bc4d |
| 19:09:47.220 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=9598ba645fbaf3e7 |
| 19:09:47.223 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067387223,"body":{"isError":false,"lo | session_id=aegis-sp-b-4307b92 trace_id=6aa300797625bc4864 |
| 19:09:47.228 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067387228,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:09:47.329 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067387329,"body":{"isError":false,"re | trace_id=6aa300797625bc4864 |
| 19:09:47.336 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=33253 out=2148 | trace_id=6aa300797625bc4864 span_id=5a8bd8924cc755eb session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:09:47.337 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa300797625bc4864 span_id=a094791607a53cd5 session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:09:47.338 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5338 out=214 | trace_id=6aa300797625bc4864 span_id=deea191be13697be session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:09:47.348 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa300797625bc4864 span_id=828d8f5eb7e1571e session_id=aegis-sp-b-4307b92 |
| 19:09:47.348 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5338 out=214 | trace_id=6aa300797625bc4864 span_id=5e240f295b1d32ce session_id=aegis-sp-b-4307b92 request_id=8424bde2-bca4-4b3c |
| 19:09:51.224 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa300797625bc4864 span_id=129ef33cbf7a17e7 session_id=aegis-sp-b-4307b92 |
| 19:09:51.260 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa300797625bc4864 span_id=7d59d316bbae3c2f session_id=aegis-sp-b-4307b92 |
| 19:09:51.294 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa300797625bc4864 span_id=124a99a518d7ecc4 session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:09:51.294 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa300797625bc4864 span_id=101ab500185b097d session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:09:51.296 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa300797625bc4864 span_id=a7bbadd9b0740828 session_id=aegis-sp-b-4307b92 |
| 19:09:51.296 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa300797625bc4864 span_id=cede3d24759a88c2 session_id=aegis-sp-b-4307b92 |
| 19:09:51.384 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaService | trace_id=6aa300797625bc4864 span_id=10022e68f78bbae5 |
| 19:09:51.390 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=e874aca65ce761a2 |
| 19:09:51.412 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaService | trace_id=6aa300797625bc4864 span_id=7645d629be93f86b |
| 19:09:51.569 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=ce4844e8e0c02bca |
| 19:09:51.580 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=8b959a239999fbe1 |
| 19:09:51.584 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067391584,"body":{"isError":false,"lo | session_id=aegis-sp-b-4307b92 trace_id=6aa300797625bc4864 |
| 19:09:51.589 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067391589,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:09:51.665 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067391665,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:09:51.686 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=149976975671c112 |
| 19:09:51.691 | runtime-span | lambda-segment | ben-fpf-intake-application/LambdaService | trace_id=6aa300797625bc4864 span_id=36cf55f886d82c1e |
| 19:09:51.697 | runtime-span | lambda-segment | ben-fpf-intake-application/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=9e05d1ffff7dee97 |
| 19:09:51.861 | lambda | call | intake_application -> ok | trace_id=6aa300797625bc4864 session_id=aegis-sp-b-4307b92 request_id=0f58487c-b762-4d7f tenant=sp-b case_id=OBS-SPB-91850 |
| 19:09:51.862 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=5f72d2f8b35084fc |
| 19:09:51.865 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067391865,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:09:51.865 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067391865,"body":{"isError":false,"re | trace_id=6aa300797625bc4864 |
| 19:09:55.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5985 out=399 masked_before_model=True | request_id=7929e009-a44b-46b0 session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:09:55.367 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=793254fdfe57ae4b |
| 19:09:55.370 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067395370,"body":{"isError":false,"lo | session_id=aegis-sp-b-4307b92 trace_id=6aa300797625bc4864 |
| 19:09:55.375 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067395375,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:09:55.455 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067395455,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:09:55.479 | runtime-span | lambda-segment | ben-fpf-mask-pii/LambdaService | trace_id=6aa300797625bc4864 span_id=07a9c40f4ac46a52 |
| 19:09:55.483 | runtime-span | lambda-segment | ben-fpf-mask-pii/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=dc72a3decd3939a2 |
| 19:09:55.962 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa300797625bc4864 session_id=aegis-sp-b-4307b92 request_id=2cc72d0a-d4b6-4f28 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:09:55.963 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=2d3924ffe17e4cea |
| 19:09:55.968 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067395968,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:09:55.968 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067395968,"body":{"isError":false,"re | trace_id=6aa300797625bc4864 |
| 19:09:55.974 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa300797625bc4864 span_id=8c58ff3a76b17e47 session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:09:55.975 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5985 out=399 | trace_id=6aa300797625bc4864 span_id=2af3e9344111c3f8 session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:09:55.976 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa300797625bc4864 span_id=bce01bc57a48e7b7 session_id=aegis-sp-b-4307b92 |
| 19:09:55.976 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5985 out=399 | trace_id=6aa300797625bc4864 span_id=c17c110ed749a163 session_id=aegis-sp-b-4307b92 request_id=7929e009-a44b-46b0 |
| 19:10:01.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6615 out=577 masked_before_model=True | request_id=a910eead-7bd1-4413 session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:10:01.103 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa300797625bc4864 span_id=bbf205b6b825af82 session_id=aegis-sp-b-4307b92 |
| 19:10:01.110 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa300797625bc4864 span_id=da7586ceeb03cf0c session_id=aegis-sp-b-4307b92 |
| 19:10:01.147 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa300797625bc4864 span_id=e6df54bf674a1805 session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:10:01.148 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa300797625bc4864 span_id=c7c45070a15fdd7e session_id=aegis-sp-b-4307b92 |
| 19:10:01.275 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaService | trace_id=6aa300797625bc4864 span_id=2ed1c73d0f54151c |
| 19:10:01.280 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=670baefe60033cf0 |
| 19:10:01.433 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=dbc1c06433e6296d |
| 19:10:01.437 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067401437,"body":{"isError":false,"lo | session_id=aegis-sp-b-4307b92 trace_id=6aa300797625bc4864 |
| 19:10:01.443 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067401443,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:10:01.533 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067401533,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:10:01.565 | runtime-span | lambda-segment | ben-fpf-assess-eligibility/LambdaService | trace_id=6aa300797625bc4864 span_id=0f9fb03766d442d0 |
| 19:10:01.571 | runtime-span | lambda-segment | ben-fpf-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=3f19aecbfa00a624 |
| 19:10:01.600 | lambda | call | assess_eligibility -> ok | trace_id=6aa300797625bc4864 session_id=aegis-sp-b-4307b92 request_id=51da15ab-4c01-4d3e tenant=sp-b case_id=OBS-SPB-91850 |
| 19:10:01.600 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=905b1acb7272a6cf |
| 19:10:01.607 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067401607,"body":{"isError":false,"re | trace_id=6aa300797625bc4864 |
| 19:10:01.607 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067401607,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:10:01.614 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa300797625bc4864 span_id=1cf6a9abb85bff38 session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:10:01.616 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6615 out=577 | trace_id=6aa300797625bc4864 span_id=098aa6c7b5e72f3b session_id=aegis-sp-b-4307b92 request_id=a910eead-7bd1-4413 |
| 19:10:01.616 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6615 out=577 | trace_id=6aa300797625bc4864 span_id=f77145e803ae28dc session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:10:01.623 | runtime-span | span | SSM.GetParameter | trace_id=6aa300797625bc4864 span_id=9bc86da93b0e3b50 session_id=aegis-sp-b-4307b92 |
| 19:10:01.663 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa300797625bc4864 span_id=ff0bde885d1ea45c session_id=aegis-sp-b-4307b92 |
| 19:10:08.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7243 out=441 masked_before_model=True | request_id=d7dcc7e2-e6e0-48b0 session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:10:08.170 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa300797625bc4864 span_id=10a520c0c71bdd52 session_id=aegis-sp-b-4307b92 |
| 19:10:08.177 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa300797625bc4864 span_id=a5aa827bac49c228 session_id=aegis-sp-b-4307b92 |
| 19:10:08.209 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa300797625bc4864 span_id=9febeaf5c6243796 session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:10:08.210 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa300797625bc4864 span_id=ae962c98890d6cb6 session_id=aegis-sp-b-4307b92 |
| 19:10:08.257 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaService | trace_id=6aa300797625bc4864 span_id=654e4790c586ba94 |
| 19:10:08.264 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=c6d5b4cf04d7b139 |
| 19:10:08.416 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=8f161786c432a5cf |
| 19:10:08.419 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067408419,"body":{"isError":false,"lo | session_id=aegis-sp-b-4307b92 trace_id=6aa300797625bc4864 |
| 19:10:08.421 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067408421,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:10:08.491 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067408491,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:10:08.524 | runtime-span | lambda-segment | ben-fpf-core-tools/LambdaService | trace_id=6aa300797625bc4864 span_id=3616f5f67c2c4012 |
| 19:10:08.530 | runtime-span | lambda-segment | ben-fpf-core-tools/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=cc599ff1a102414d |
| 19:10:08.552 | lambda | call | benefits_core -> committed=False | trace_id=6aa300797625bc4864 session_id=aegis-sp-b-4307b92 request_id=e9ce355f-fc1b-49b6 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:10:08.564 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=2d92d6452ee90529 |
| 19:10:08.570 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067408570,"body":{"isError":false,"re | trace_id=6aa300797625bc4864 |
| 19:10:08.570 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067408570,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:10:08.576 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa300797625bc4864 span_id=a6a957acd593f26c session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:10:08.577 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7243 out=441 | trace_id=6aa300797625bc4864 span_id=c4b64fbf8121782c session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:10:08.578 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7243 out=441 | trace_id=6aa300797625bc4864 span_id=6740d15be77d9bba session_id=aegis-sp-b-4307b92 request_id=d7dcc7e2-e6e0-48b0 |
| 19:10:08.580 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa300797625bc4864 span_id=42f0e1749c92480b session_id=aegis-sp-b-4307b92 |
| 19:10:14.000 | worm | evidence | INTENT benefits-determination seq=0 chain=f4d776d42a53… | trace_id=6aa300797625bc4864 session_id=aegis-sp-b-4307b92 request_id=2b409306-7e11-43ad tenant=sp-b |
| 19:10:14.111 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa300797625bc4864 span_id=5b698de52e55ddd0 session_id=aegis-sp-b-4307b92 |
| 19:10:14.118 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa300797625bc4864 span_id=02225d6d117b7d0c session_id=aegis-sp-b-4307b92 |
| 19:10:14.129 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa300797625bc4864 span_id=183026ee3383d9ce session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:10:14.130 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa300797625bc4864 span_id=a8b75780f56a9977 session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:10:14.131 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa300797625bc4864 span_id=3d09169aa0299bab session_id=aegis-sp-b-4307b92 |
| 19:10:14.131 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa300797625bc4864 span_id=a668ad50aebca5e9 session_id=aegis-sp-b-4307b92 |
| 19:10:14.188 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaService | trace_id=6aa300797625bc4864 span_id=75865c4009c55eae |
| 19:10:14.194 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=68bfef831febadda |
| 19:10:14.236 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaService | trace_id=6aa300797625bc4864 span_id=3ab4a6a333278102 |
| 19:10:14.241 | runtime-span | lambda-segment | ben-fpf-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=8efc80ee2311f247 |
| 19:10:14.383 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=19bdef4599bfd2cb |
| 19:10:14.385 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067414385,"body":{"isError":false,"lo | session_id=aegis-sp-b-4307b92 trace_id=6aa300797625bc4864 |
| 19:10:14.387 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067414387,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:10:14.439 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=2fc56554a92a9b75 |
| 19:10:14.441 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067414441,"body":{"isError":false,"lo | session_id=aegis-sp-b-4307b92 trace_id=6aa300797625bc4864 |
| 19:10:14.446 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067414446,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:10:14.462 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067414462,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:10:14.483 | runtime-span | lambda-segment | ben-fpf-write-audit/LambdaService | trace_id=6aa300797625bc4864 span_id=7f7b209b8c416dc7 |
| 19:10:14.487 | runtime-span | lambda-segment | ben-fpf-write-audit/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=7ede6864741e63dd |
| 19:10:14.526 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067414526,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:10:14.548 | runtime-span | lambda-segment | ben-fpf-request-signoff/LambdaService | trace_id=6aa300797625bc4864 span_id=457fb86e1919e767 |
| 19:10:14.560 | runtime-span | lambda-segment | ben-fpf-request-signoff/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=b141d314f6a526a8 |
| 19:10:14.581 | lambda | call | request_signoff -> requested=False | trace_id=6aa300797625bc4864 session_id=aegis-sp-b-4307b92 request_id=75e7bbbc-6b0e-49a3 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:10:14.582 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=8d66ce5ac74e6b42 |
| 19:10:14.585 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067414585,"body":{"isError":false,"re | trace_id=6aa300797625bc4864 |
| 19:10:14.585 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067414585,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:10:14.975 | lambda | call | write_audit -> stored=True | trace_id=6aa300797625bc4864 session_id=aegis-sp-b-4307b92 request_id=2b409306-7e11-43ad tenant=sp-b case_id=OBS-SPB-91850 |
| 19:10:14.976 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa300797625bc4864 span_id=a430b21f9e638651 |
| 19:10:14.981 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067414981,"body":{"isError":false,"lo | trace_id=6aa300797625bc4864 |
| 19:10:14.981 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpf-ben-gw-eeunb9jdig","event_timestamp":1789067414981,"body":{"isError":false,"re | trace_id=6aa300797625bc4864 |
| 19:10:14.986 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa300797625bc4864 span_id=b7508f119b4f062f session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:10:14.988 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8072 out=517 | trace_id=6aa300797625bc4864 span_id=43f092917bb827e3 session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:10:14.989 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8072 out=517 | trace_id=6aa300797625bc4864 span_id=6927a092cbde5df5 session_id=aegis-sp-b-4307b92 request_id=5edc0ee3-449b-42dd |
| 19:10:14.990 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa300797625bc4864 span_id=c71269c754f1773f session_id=aegis-sp-b-4307b92 |
| 19:10:15.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8072 out=517 masked_before_model=True | request_id=5edc0ee3-449b-42dd session_id=aegis-sp-b-4307b92 tenant=sp-b case_id=OBS-SPB-91850 |
| 19:10:24.413 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa300797625bc4864 span_id=bd0b1f289dfd1d8f session_id=aegis-sp-b-4307b92 |
| 19:10:24.420 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa300797625bc4864 span_id=781b795f34bf1891 session_id=aegis-sp-b-4307b92 |
| 19:10:24.426 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa300797625bc4864 span_id=82b091a43dd4941f session_id=aegis-sp-b-4307b92 |
