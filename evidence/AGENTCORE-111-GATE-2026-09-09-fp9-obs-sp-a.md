# Case trace — `OBS-SPA-91D3C` (tenant `sp-a`)

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
| sessions | ['aegis-sp-a-7f4228681535405e9379e9bbd3f1516e'] |
| single_tenant | True |
| tenants_seen | ['sp-a'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 03:18:26.414 | lambda | call | ingest_application -> ingested=True | trace_id=6aa2218270b321ef55 request_id=15245c6b-9e5e-4e5d tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:26.962 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa22182006d66df5a span_id=8b26f1b12e110288 session_id=aegis-sp-a-7f42286 |
| 03:18:27.465 | runtime-span | runtime-http | POST /invocations | trace_id=6aa22182006d66df5a span_id=525cba3ba72eb28b session_id=aegis-sp-a-7f42286 |
| 03:18:27.536 | runtime-span | span | SSM.GetParameter | trace_id=6aa22182006d66df5a span_id=2f1186dcefbb11e9 session_id=aegis-sp-a-7f42286 |
| 03:18:27.576 | runtime-span | span | SSM.GetParameter | trace_id=6aa22182006d66df5a span_id=b51558ce4a0d058e session_id=aegis-sp-a-7f42286 |
| 03:18:27.635 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa22182006d66df5a span_id=35bc919887569ae4 session_id=aegis-sp-a-7f42286 |
| 03:18:27.682 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa22182006d66df5a span_id=8ee6a32a970c8add session_id=aegis-sp-a-7f42286 |
| 03:18:27.759 | runtime-span | span | mcp.session | trace_id=6aa22182006d66df5a span_id=5e7f36bdf39f7cd7 session_id=aegis-sp-a-7f42286 |
| 03:18:27.856 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa22182006d66df5a span_id=ea9a75973231dbd4 session_id=aegis-sp-a-7f42286 |
| 03:18:28.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5341 out=136 masked_before_model=True | request_id=c44d58e2-e202-40e9 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:28.085 | runtime-span | lambda-segment | ben-fp9-tenant-interceptor/LambdaService | trace_id=6aa22182006d66df5a span_id=5557af106ed2fc06 |
| 03:18:28.091 | runtime-span | lambda-segment | ben-fp9-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=79c73237462e5886 |
| 03:18:28.111 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=4bf1cb8ca2f3629b |
| 03:18:28.114 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010308114,"body":{"isError":false,"lo | session_id=aegis-sp-a-7f42286 trace_id=6aa22182006d66df5a |
| 03:18:28.118 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010308118,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:28.201 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010308201,"body":{"isError":false,"re | trace_id=6aa22182006d66df5a |
| 03:18:28.207 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=46548 out=2073 | trace_id=6aa22182006d66df5a span_id=997466642a175eb7 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:28.208 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa22182006d66df5a span_id=ff44aaca4c3552e5 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:28.209 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5341 out=136 | trace_id=6aa22182006d66df5a span_id=91ae02270abaac58 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:28.212 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa22182006d66df5a span_id=5a3337b89812e73b session_id=aegis-sp-a-7f42286 |
| 03:18:28.212 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5341 out=136 | trace_id=6aa22182006d66df5a span_id=6bf3cc32aff69c07 session_id=aegis-sp-a-7f42286 request_id=c44d58e2-e202-40e9 |
| 03:18:31.628 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa22182006d66df5a span_id=3d5218155ff1f040 session_id=aegis-sp-a-7f42286 |
| 03:18:31.645 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa22182006d66df5a span_id=e2824c6af8776af3 session_id=aegis-sp-a-7f42286 |
| 03:18:31.671 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa22182006d66df5a span_id=dd25656e8266ed02 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:31.672 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa22182006d66df5a span_id=0b92d26e1b7312dd session_id=aegis-sp-a-7f42286 |
| 03:18:31.805 | runtime-span | lambda-segment | ben-fp9-tenant-interceptor/LambdaService | trace_id=6aa22182006d66df5a span_id=52306801dd6b3687 |
| 03:18:31.811 | runtime-span | lambda-segment | ben-fp9-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=95d9710f1df4cc26 |
| 03:18:32.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5555 out=118 masked_before_model=True | request_id=a0f4fe62-251b-41f7 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:32.168 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=ac542ad066d0c21e |
| 03:18:32.173 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010312173,"body":{"isError":false,"lo | session_id=aegis-sp-a-7f42286 trace_id=6aa22182006d66df5a |
| 03:18:32.178 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010312178,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:32.257 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010312257,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:32.272 | runtime-span | lambda-segment | ben-fp9-intake-application/LambdaService | trace_id=6aa22182006d66df5a span_id=5e1fe2ee645c8508 |
| 03:18:32.278 | runtime-span | lambda-segment | ben-fp9-intake-application/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=83d11bbe1f9d01cb |
| 03:18:32.462 | lambda | call | intake_application -> ok | trace_id=6aa22182006d66df5a session_id=aegis-sp-a-7f42286 request_id=a9798bd1-5665-4df3 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:32.463 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=479593b450993f08 |
| 03:18:32.469 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010312469,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:32.469 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010312469,"body":{"isError":false,"re | trace_id=6aa22182006d66df5a |
| 03:18:32.474 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa22182006d66df5a span_id=1d449aa73d34d2dc session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:32.475 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5555 out=118 | trace_id=6aa22182006d66df5a span_id=754b34cebb687a02 session_id=aegis-sp-a-7f42286 request_id=a0f4fe62-251b-41f7 |
| 03:18:32.475 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5555 out=118 | trace_id=6aa22182006d66df5a span_id=2217a7d7d35e0b04 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:32.476 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa22182006d66df5a span_id=4c8c0d603112de8c session_id=aegis-sp-a-7f42286 |
| 03:18:35.625 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa22182006d66df5a span_id=e275aed4441423e7 session_id=aegis-sp-a-7f42286 |
| 03:18:35.632 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa22182006d66df5a span_id=2626b98c40974f7b session_id=aegis-sp-a-7f42286 |
| 03:18:35.640 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa22182006d66df5a span_id=adf581cce75b6b9b session_id=aegis-sp-a-7f42286 |
| 03:18:35.640 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa22182006d66df5a span_id=63fd4f2be1018650 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:35.746 | runtime-span | lambda-segment | ben-fp9-tenant-interceptor/LambdaService | trace_id=6aa22182006d66df5a span_id=5fcfcc6a218aa57e |
| 03:18:35.752 | runtime-span | lambda-segment | ben-fp9-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=0745a028bbadc83d |
| 03:18:35.904 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=e056099f4fd16414 |
| 03:18:35.907 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010315907,"body":{"isError":false,"lo | session_id=aegis-sp-a-7f42286 trace_id=6aa22182006d66df5a |
| 03:18:35.911 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010315911,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:35.984 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010315984,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:36.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5982 out=400 masked_before_model=True | request_id=df50b408-6557-4de0 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:36.002 | runtime-span | lambda-segment | ben-fp9-mask-pii/LambdaService | trace_id=6aa22182006d66df5a span_id=0bf2d87970152c49 |
| 03:18:36.015 | runtime-span | lambda-segment | ben-fp9-mask-pii/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=2fbc7f30323af7ff |
| 03:18:36.504 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa22182006d66df5a session_id=aegis-sp-a-7f42286 request_id=3d3bcb76-8629-4e25 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:36.504 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=46bccb0464fc290d |
| 03:18:36.509 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010316509,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:36.509 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010316509,"body":{"isError":false,"re | trace_id=6aa22182006d66df5a |
| 03:18:36.514 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa22182006d66df5a span_id=4fc2e3070073f706 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:36.515 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5982 out=400 | trace_id=6aa22182006d66df5a span_id=eb29f9597f6d5c27 session_id=aegis-sp-a-7f42286 request_id=df50b408-6557-4de0 |
| 03:18:36.515 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5982 out=400 | trace_id=6aa22182006d66df5a span_id=f23118fc86b8fb2d session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:36.516 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa22182006d66df5a span_id=1cecc08d11b62078 session_id=aegis-sp-a-7f42286 |
| 03:18:41.668 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa22182006d66df5a span_id=6064dc2067e1d239 session_id=aegis-sp-a-7f42286 |
| 03:18:41.675 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa22182006d66df5a span_id=f122a769ad3bab9e session_id=aegis-sp-a-7f42286 |
| 03:18:41.702 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa22182006d66df5a span_id=2c361c97e2738e92 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:41.703 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa22182006d66df5a span_id=8af3e8f359e6dd80 session_id=aegis-sp-a-7f42286 |
| 03:18:41.820 | runtime-span | lambda-segment | ben-fp9-tenant-interceptor/LambdaService | trace_id=6aa22182006d66df5a span_id=74c3080ae2640d51 |
| 03:18:41.824 | runtime-span | lambda-segment | ben-fp9-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=a27dd95057831866 |
| 03:18:41.976 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=b7f18ed80f78bdde |
| 03:18:41.979 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010321979,"body":{"isError":false,"lo | session_id=aegis-sp-a-7f42286 trace_id=6aa22182006d66df5a |
| 03:18:41.983 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010321983,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:42.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6613 out=569 masked_before_model=True | request_id=7516f357-8b1f-42a3 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:42.125 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010322125,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:42.156 | runtime-span | lambda-segment | ben-fp9-assess-eligibility/LambdaService | trace_id=6aa22182006d66df5a span_id=66749e7a836f57eb |
| 03:18:42.163 | runtime-span | lambda-segment | ben-fp9-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=ecfa083e2a365a07 |
| 03:18:42.185 | lambda | call | assess_eligibility -> ok | trace_id=6aa22182006d66df5a session_id=aegis-sp-a-7f42286 request_id=9872c285-0d44-48f0 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:42.185 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=4869105498d843dc |
| 03:18:42.192 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010322192,"body":{"isError":false,"re | trace_id=6aa22182006d66df5a |
| 03:18:42.192 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010322192,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:42.197 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa22182006d66df5a span_id=8856a8736c7a075b session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:42.198 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6613 out=569 | trace_id=6aa22182006d66df5a span_id=799cc590fb3cda63 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:42.199 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa22182006d66df5a span_id=e4499d7aa8cfeebe session_id=aegis-sp-a-7f42286 |
| 03:18:42.199 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6613 out=569 | trace_id=6aa22182006d66df5a span_id=f007c93ada26000c session_id=aegis-sp-a-7f42286 request_id=7516f357-8b1f-42a3 |
| 03:18:48.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7231 out=300 masked_before_model=True | request_id=d86f3b3c-5407-499b session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:48.407 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa22182006d66df5a span_id=67a8ed4cbd32649d session_id=aegis-sp-a-7f42286 |
| 03:18:48.413 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa22182006d66df5a span_id=0d3310e83dc5b202 session_id=aegis-sp-a-7f42286 |
| 03:18:48.435 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa22182006d66df5a span_id=f4abab0718d1aaef session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:48.436 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa22182006d66df5a span_id=a04cd20972be2674 session_id=aegis-sp-a-7f42286 |
| 03:18:48.559 | runtime-span | lambda-segment | ben-fp9-tenant-interceptor/LambdaService | trace_id=6aa22182006d66df5a span_id=261613a97e965b8a |
| 03:18:48.563 | runtime-span | lambda-segment | ben-fp9-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=212a268a9c939a7d |
| 03:18:48.726 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=a0f0c350e2401963 |
| 03:18:48.729 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010328729,"body":{"isError":false,"lo | session_id=aegis-sp-a-7f42286 trace_id=6aa22182006d66df5a |
| 03:18:48.733 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010328733,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:48.807 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010328807,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:48.831 | runtime-span | lambda-segment | ben-fp9-core-tools/LambdaService | trace_id=6aa22182006d66df5a span_id=6dbfa3a72ed15645 |
| 03:18:48.835 | runtime-span | lambda-segment | ben-fp9-core-tools/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=f442912bcf42858b |
| 03:18:48.856 | lambda | call | benefits_core -> committed=False | trace_id=6aa22182006d66df5a session_id=aegis-sp-a-7f42286 request_id=5a5fe76b-fbac-47ee tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:48.856 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=2125282dc613ee7b |
| 03:18:48.860 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010328860,"body":{"isError":false,"re | trace_id=6aa22182006d66df5a |
| 03:18:48.861 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010328861,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:48.866 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa22182006d66df5a span_id=61e417e37df60b1a session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:48.867 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7231 out=300 | trace_id=6aa22182006d66df5a span_id=1b165851b909cee0 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:48.868 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7231 out=300 | trace_id=6aa22182006d66df5a span_id=cb50ac68314aa7a3 session_id=aegis-sp-a-7f42286 request_id=d86f3b3c-5407-499b |
| 03:18:48.873 | runtime-span | span | SSM.GetParameter | trace_id=6aa22182006d66df5a span_id=026897eaa5847be3 session_id=aegis-sp-a-7f42286 |
| 03:18:48.909 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa22182006d66df5a span_id=e626bef54aa680dc session_id=aegis-sp-a-7f42286 |
| 03:18:53.640 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa22182006d66df5a span_id=82ab72c70a90b47a session_id=aegis-sp-a-7f42286 |
| 03:18:53.646 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa22182006d66df5a span_id=a26d3f8614477ae3 session_id=aegis-sp-a-7f42286 |
| 03:18:53.654 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa22182006d66df5a span_id=7dc92bce7b358896 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:53.655 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa22182006d66df5a span_id=e17a6a57f3ae3f0b session_id=aegis-sp-a-7f42286 |
| 03:18:53.752 | runtime-span | lambda-segment | ben-fp9-tenant-interceptor/LambdaService | trace_id=6aa22182006d66df5a span_id=1a37c2fd63415882 |
| 03:18:53.757 | runtime-span | lambda-segment | ben-fp9-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=98c56010c5257ff4 |
| 03:18:53.761 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=521ff87fe32f624e |
| 03:18:53.765 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010333765,"body":{"isError":false,"lo | session_id=aegis-sp-a-7f42286 trace_id=6aa22182006d66df5a |
| 03:18:53.770 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010333770,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:53.859 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010333859,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:53.878 | runtime-span | lambda-segment | ben-fp9-write-audit/LambdaService | trace_id=6aa22182006d66df5a span_id=09e637a33ec50a08 |
| 03:18:53.883 | runtime-span | lambda-segment | ben-fp9-write-audit/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=fce06ae67469434c |
| 03:18:54.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7831 out=113 masked_before_model=True | request_id=63df8a64-f8e0-4c88 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:54.000 | worm | evidence | INTENT benefits-determination seq=0 chain=d4034241b451… | trace_id=6aa22182006d66df5a session_id=aegis-sp-a-7f42286 request_id=2b2d8a4b-0cc3-4c8b tenant=sp-a |
| 03:18:54.693 | lambda | call | write_audit -> stored=True | trace_id=6aa22182006d66df5a session_id=aegis-sp-a-7f42286 request_id=2b2d8a4b-0cc3-4c8b tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:54.694 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=0ee22d4a90960f56 |
| 03:18:54.698 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010334698,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:54.698 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010334698,"body":{"isError":false,"re | trace_id=6aa22182006d66df5a |
| 03:18:54.704 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa22182006d66df5a span_id=8a146d48c8b98e2d session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:54.705 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7831 out=113 | trace_id=6aa22182006d66df5a span_id=358bc3b8975c700d session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:54.706 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa22182006d66df5a span_id=0386278ae00a711b session_id=aegis-sp-a-7f42286 |
| 03:18:54.706 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7831 out=113 | trace_id=6aa22182006d66df5a span_id=291d4c0cba566df1 session_id=aegis-sp-a-7f42286 request_id=63df8a64-f8e0-4c88 |
| 03:18:57.467 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa22182006d66df5a span_id=802f2e5fbc3d31cc session_id=aegis-sp-a-7f42286 |
| 03:18:57.473 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa22182006d66df5a span_id=80693c9305e30c05 session_id=aegis-sp-a-7f42286 |
| 03:18:57.481 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa22182006d66df5a span_id=3ac995aed1a58666 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:57.482 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa22182006d66df5a span_id=1cdf4f302145775c session_id=aegis-sp-a-7f42286 |
| 03:18:57.576 | runtime-span | lambda-segment | ben-fp9-tenant-interceptor/LambdaService | trace_id=6aa22182006d66df5a span_id=1497bfcf15b13e32 |
| 03:18:57.580 | runtime-span | lambda-segment | ben-fp9-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=0f2dd4638fb27cfe |
| 03:18:57.748 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=589d34813a59056f |
| 03:18:57.757 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010337757,"body":{"isError":false,"lo | session_id=aegis-sp-a-7f42286 trace_id=6aa22182006d66df5a |
| 03:18:57.761 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010337761,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:57.832 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010337832,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:57.854 | runtime-span | lambda-segment | ben-fp9-request-signoff/LambdaService | trace_id=6aa22182006d66df5a span_id=5a1d283df3f92f31 |
| 03:18:58.078 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=dcca38362158a9f9 |
| 03:18:58.340 | runtime-span | lambda-segment | ben-fp9-request-signoff/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=5ca6f23a0c2b00f1 |
| 03:18:59.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7995 out=437 masked_before_model=True | request_id=18f98c81-ba4e-4e72 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:59.848 | lambda | call | request_signoff -> requested=False | trace_id=6aa22182006d66df5a session_id=aegis-sp-a-7f42286 request_id=c9a06f5b-ac86-453c tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:59.848 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa22182006d66df5a span_id=67d68f3cf8eef0bc |
| 03:18:59.852 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010339852,"body":{"isError":false,"lo | trace_id=6aa22182006d66df5a |
| 03:18:59.852 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp9-ben-gw-bwnx7pim1k","event_timestamp":1789010339852,"body":{"isError":false,"re | trace_id=6aa22182006d66df5a |
| 03:18:59.858 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa22182006d66df5a span_id=2b6d67a29cf5c9a6 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:59.859 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7995 out=437 | trace_id=6aa22182006d66df5a span_id=64a50205bfc33e12 session_id=aegis-sp-a-7f42286 tenant=sp-a case_id=OBS-SPA-91D3C |
| 03:18:59.860 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7995 out=437 | trace_id=6aa22182006d66df5a span_id=202c8138ef3eb0a3 session_id=aegis-sp-a-7f42286 request_id=18f98c81-ba4e-4e72 |
| 03:18:59.861 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa22182006d66df5a span_id=95bac03d92c38cb4 session_id=aegis-sp-a-7f42286 |
| 03:18:59.865 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa22182006d66df5a span_id=6df2a4fb959e7fe1 session_id=aegis-sp-a-7f42286 |
| 03:19:09.001 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa22182006d66df5a span_id=18ecd44a0c2f5074 session_id=aegis-sp-a-7f42286 |
| 03:19:09.007 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa22182006d66df5a span_id=a51808ee7bfec991 session_id=aegis-sp-a-7f42286 |
