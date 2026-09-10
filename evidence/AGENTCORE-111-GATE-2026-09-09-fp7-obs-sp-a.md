# Case trace — `OBS-SPA-0FA57` (tenant `sp-a`)

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
| sessions | ['aegis-sp-a-8f09edf069c04298b5d64c4f909127e5'] |
| single_tenant | True |
| tenants_seen | ['sp-a'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 00:30:14.595 | lambda | call | ingest_application -> ingested=True | trace_id=6aa1fa16145b37092a request_id=9414c4ad-1885-458b tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:15.182 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa1fa173d0f3f5227 span_id=7793a4b04f214083 session_id=aegis-sp-a-8f09edf |
| 00:30:16.478 | runtime-span | runtime-http | POST /invocations | trace_id=6aa1fa173d0f3f5227 span_id=e7d9aa49431d97c0 session_id=aegis-sp-a-8f09edf |
| 00:30:16.562 | runtime-span | span | SSM.GetParameter | trace_id=6aa1fa173d0f3f5227 span_id=26a069b6e7ef6b12 session_id=aegis-sp-a-8f09edf |
| 00:30:16.602 | runtime-span | span | SSM.GetParameter | trace_id=6aa1fa173d0f3f5227 span_id=ad83d9d7c7003d0a session_id=aegis-sp-a-8f09edf |
| 00:30:16.670 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa1fa173d0f3f5227 span_id=e131b754197fa51a session_id=aegis-sp-a-8f09edf |
| 00:30:16.714 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa1fa173d0f3f5227 span_id=684ff98c475cf38d session_id=aegis-sp-a-8f09edf |
| 00:30:16.791 | runtime-span | span | mcp.session | trace_id=6aa1fa173d0f3f5227 span_id=cbf239da0dae819d session_id=aegis-sp-a-8f09edf |
| 00:30:16.951 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa1fa173d0f3f5227 span_id=b2ba0c5c217dedea session_id=aegis-sp-a-8f09edf |
| 00:30:17.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5344 out=140 masked_before_model=True | request_id=f0f5edbf-12f0-488f session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:17.171 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaService | trace_id=6aa1fa173d0f3f5227 span_id=03c84d9184647c1d |
| 00:30:17.181 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=19696a6fd71d96e0 |
| 00:30:17.271 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=e7b8ae7c7c190ebe |
| 00:30:17.275 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000217275,"body":{"isError":false,"lo | session_id=aegis-sp-a-8f09edf trace_id=6aa1fa173d0f3f5227 |
| 00:30:17.279 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000217279,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:17.358 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000217358,"body":{"isError":false,"re | trace_id=6aa1fa173d0f3f5227 |
| 00:30:17.366 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=46645 out=2102 | trace_id=6aa1fa173d0f3f5227 span_id=81832562ebfa937c session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:17.367 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1fa173d0f3f5227 span_id=70e7ecee7eb46609 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:17.368 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5344 out=140 | trace_id=6aa1fa173d0f3f5227 span_id=74d12b7ac553b8c8 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:17.370 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5344 out=140 | trace_id=6aa1fa173d0f3f5227 span_id=a4dbcc8c357c2a42 session_id=aegis-sp-a-8f09edf request_id=f0f5edbf-12f0-488f |
| 00:30:17.371 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa173d0f3f5227 span_id=6ed574100de330c0 session_id=aegis-sp-a-8f09edf |
| 00:30:20.675 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa173d0f3f5227 span_id=69b30a2318116aec session_id=aegis-sp-a-8f09edf |
| 00:30:20.688 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1fa173d0f3f5227 span_id=2a0fb4b46a044eb8 session_id=aegis-sp-a-8f09edf |
| 00:30:20.718 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa1fa173d0f3f5227 span_id=7c9e6958055ff719 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:20.719 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa1fa173d0f3f5227 span_id=d6b1d9894e7a3dac session_id=aegis-sp-a-8f09edf |
| 00:30:20.757 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaService | trace_id=6aa1fa173d0f3f5227 span_id=47ceed221229ad62 |
| 00:30:20.762 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=68e9837f43b7ff95 |
| 00:30:21.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5562 out=122 masked_before_model=True | request_id=f3930862-92f2-4a5e session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:21.121 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=565cf5df73969e8d |
| 00:30:21.124 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000221124,"body":{"isError":false,"lo | session_id=aegis-sp-a-8f09edf trace_id=6aa1fa173d0f3f5227 |
| 00:30:21.127 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000221127,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:21.216 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000221216,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:21.244 | runtime-span | lambda-segment | ben-fp7-intake-application/LambdaService | trace_id=6aa1fa173d0f3f5227 span_id=72a1672d667f17b9 |
| 00:30:21.249 | runtime-span | lambda-segment | ben-fp7-intake-application/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=1ed961253bd693d7 |
| 00:30:21.440 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=9b1cae8302ad7874 |
| 00:30:21.441 | lambda | call | intake_application -> ok | trace_id=6aa1fa173d0f3f5227 session_id=aegis-sp-a-8f09edf request_id=9315c56c-eb42-424f tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:21.445 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000221445,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:21.445 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000221445,"body":{"isError":false,"re | trace_id=6aa1fa173d0f3f5227 |
| 00:30:21.450 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1fa173d0f3f5227 span_id=c0c017135e6ab6f9 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:21.451 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5562 out=122 | trace_id=6aa1fa173d0f3f5227 span_id=83822b916b808c98 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:21.452 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa173d0f3f5227 span_id=e276985b1c31d976 session_id=aegis-sp-a-8f09edf |
| 00:30:21.452 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5562 out=122 | trace_id=6aa1fa173d0f3f5227 span_id=d7ca07364318e131 session_id=aegis-sp-a-8f09edf request_id=f3930862-92f2-4a5e |
| 00:30:24.617 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa173d0f3f5227 span_id=afeaf3e93dc8caaa session_id=aegis-sp-a-8f09edf |
| 00:30:24.623 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1fa173d0f3f5227 span_id=54dd1cf6917ce11d session_id=aegis-sp-a-8f09edf |
| 00:30:24.631 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa1fa173d0f3f5227 span_id=f5dd71fa54de1c06 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:24.632 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa1fa173d0f3f5227 span_id=309b89790712023f session_id=aegis-sp-a-8f09edf |
| 00:30:24.733 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaService | trace_id=6aa1fa173d0f3f5227 span_id=78a49938087ef0d3 |
| 00:30:24.741 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=3786e76f92f13eb0 |
| 00:30:24.897 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=8d5b1a127019e20f |
| 00:30:24.902 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000224902,"body":{"isError":false,"lo | session_id=aegis-sp-a-8f09edf trace_id=6aa1fa173d0f3f5227 |
| 00:30:24.906 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000224906,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:24.989 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000224989,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:25.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5991 out=397 masked_before_model=True | request_id=f2f30b85-26a1-4dd3 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:25.013 | runtime-span | lambda-segment | ben-fp7-mask-pii/LambdaService | trace_id=6aa1fa173d0f3f5227 span_id=4f1cd32e1294cdc7 |
| 00:30:25.020 | runtime-span | lambda-segment | ben-fp7-mask-pii/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=75e8b5205b7e7e4d |
| 00:30:25.562 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa1fa173d0f3f5227 session_id=aegis-sp-a-8f09edf request_id=f054a587-c587-4ccb tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:25.563 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=ea054bb1c337eece |
| 00:30:25.568 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000225568,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:25.568 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000225568,"body":{"isError":false,"re | trace_id=6aa1fa173d0f3f5227 |
| 00:30:25.574 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5991 out=397 | trace_id=6aa1fa173d0f3f5227 span_id=d3132fcfe32547b3 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:25.574 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1fa173d0f3f5227 span_id=ed0a1eec313652d6 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:25.575 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa173d0f3f5227 span_id=d6ebd02ea6244f55 session_id=aegis-sp-a-8f09edf |
| 00:30:25.575 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5991 out=397 | trace_id=6aa1fa173d0f3f5227 span_id=e2489a83087fb849 session_id=aegis-sp-a-8f09edf request_id=f2f30b85-26a1-4dd3 |
| 00:30:30.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6619 out=566 masked_before_model=True | request_id=08760cf8-471c-4671 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:30.093 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa173d0f3f5227 span_id=73c96123267566d9 session_id=aegis-sp-a-8f09edf |
| 00:30:30.099 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1fa173d0f3f5227 span_id=59dd2ac85ae5a0b2 session_id=aegis-sp-a-8f09edf |
| 00:30:30.110 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa1fa173d0f3f5227 span_id=f5bfd78e0bb62271 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:30.111 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa1fa173d0f3f5227 span_id=2c73954d8be37c86 session_id=aegis-sp-a-8f09edf |
| 00:30:30.227 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaService | trace_id=6aa1fa173d0f3f5227 span_id=0a32793a836deaad |
| 00:30:30.232 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=c77a194abee37cc5 |
| 00:30:30.391 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=512a0c5a2e748597 |
| 00:30:30.394 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000230394,"body":{"isError":false,"lo | session_id=aegis-sp-a-8f09edf trace_id=6aa1fa173d0f3f5227 |
| 00:30:30.398 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000230398,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:30.480 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000230480,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:30.512 | runtime-span | lambda-segment | ben-fp7-assess-eligibility/LambdaService | trace_id=6aa1fa173d0f3f5227 span_id=1428464622644239 |
| 00:30:30.524 | runtime-span | lambda-segment | ben-fp7-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=c3ec62f9f44b12de |
| 00:30:30.545 | lambda | call | assess_eligibility -> ok | trace_id=6aa1fa173d0f3f5227 session_id=aegis-sp-a-8f09edf request_id=4db5e18c-f48f-4e3b tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:30.545 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=a4a902ad95249def |
| 00:30:30.554 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000230554,"body":{"isError":false,"re | trace_id=6aa1fa173d0f3f5227 |
| 00:30:30.554 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000230554,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:30.559 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1fa173d0f3f5227 span_id=83e377a81ebf0268 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:30.560 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6619 out=566 | trace_id=6aa1fa173d0f3f5227 span_id=9f15b67bc758bcc1 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:30.561 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa173d0f3f5227 span_id=ff1ac1bebf0fa2cd session_id=aegis-sp-a-8f09edf |
| 00:30:30.561 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6619 out=566 | trace_id=6aa1fa173d0f3f5227 span_id=b4727c3cafd3f025 session_id=aegis-sp-a-8f09edf request_id=08760cf8-471c-4671 |
| 00:30:36.926 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa173d0f3f5227 span_id=4b901012ce07c580 session_id=aegis-sp-a-8f09edf |
| 00:30:36.932 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1fa173d0f3f5227 span_id=f6c20ac2b08bed11 session_id=aegis-sp-a-8f09edf |
| 00:30:36.963 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa1fa173d0f3f5227 span_id=1f1f264ee9669b3f session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:36.964 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa1fa173d0f3f5227 span_id=37f9207b7df62e57 session_id=aegis-sp-a-8f09edf |
| 00:30:37.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7233 out=333 masked_before_model=True | request_id=126ec0f3-9ee3-496b session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:37.075 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaService | trace_id=6aa1fa173d0f3f5227 span_id=26e8a24d27c863d4 |
| 00:30:37.079 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=7dba2245b6f57750 |
| 00:30:37.260 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=db22e8985a703026 |
| 00:30:37.264 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000237264,"body":{"isError":false,"lo | session_id=aegis-sp-a-8f09edf trace_id=6aa1fa173d0f3f5227 |
| 00:30:37.268 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000237268,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:37.350 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000237350,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:37.381 | runtime-span | lambda-segment | ben-fp7-core-tools/LambdaService | trace_id=6aa1fa173d0f3f5227 span_id=17aeee1bded3b0a6 |
| 00:30:37.386 | runtime-span | lambda-segment | ben-fp7-core-tools/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=684d0d3e5a596b6f |
| 00:30:37.411 | lambda | call | benefits_core -> committed=False | trace_id=6aa1fa173d0f3f5227 session_id=aegis-sp-a-8f09edf request_id=8f472e85-48e4-493d tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:37.412 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=0ef110739f56eb69 |
| 00:30:37.415 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000237415,"body":{"isError":false,"re | trace_id=6aa1fa173d0f3f5227 |
| 00:30:37.415 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000237415,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:37.420 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1fa173d0f3f5227 span_id=afeacedfe70ebe23 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:37.421 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7233 out=333 | trace_id=6aa1fa173d0f3f5227 span_id=237136531b519045 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:37.422 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7233 out=333 | trace_id=6aa1fa173d0f3f5227 span_id=48f88395a375de73 session_id=aegis-sp-a-8f09edf request_id=126ec0f3-9ee3-496b |
| 00:30:37.427 | runtime-span | span | SSM.GetParameter | trace_id=6aa1fa173d0f3f5227 span_id=4708a25a1becacd9 session_id=aegis-sp-a-8f09edf |
| 00:30:37.464 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa173d0f3f5227 span_id=319b0e1f668b48f9 session_id=aegis-sp-a-8f09edf |
| 00:30:42.629 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa173d0f3f5227 span_id=7de047737e88e23e session_id=aegis-sp-a-8f09edf |
| 00:30:42.640 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1fa173d0f3f5227 span_id=e77b13d98a5d5225 session_id=aegis-sp-a-8f09edf |
| 00:30:42.650 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa1fa173d0f3f5227 span_id=11e3c84242cffb96 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:42.651 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa1fa173d0f3f5227 span_id=2d65ecb4c3a65cb1 session_id=aegis-sp-a-8f09edf |
| 00:30:42.768 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaService | trace_id=6aa1fa173d0f3f5227 span_id=28e2d190d3493c0e |
| 00:30:42.804 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=b8e0341479ccf3be |
| 00:30:42.960 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=e2e5f4398b5da399 |
| 00:30:42.964 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000242964,"body":{"isError":false,"lo | session_id=aegis-sp-a-8f09edf trace_id=6aa1fa173d0f3f5227 |
| 00:30:42.967 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000242967,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:43.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7867 out=111 masked_before_model=True | request_id=8dc3dd14-cd56-449f session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:43.000 | worm | evidence | INTENT benefits-determination seq=0 chain=a6ba170e79e5… | trace_id=6aa1fa173d0f3f5227 session_id=aegis-sp-a-8f09edf request_id=99262cb0-3c8b-4375 tenant=sp-a |
| 00:30:43.040 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000243040,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:43.063 | runtime-span | lambda-segment | ben-fp7-write-audit/LambdaService | trace_id=6aa1fa173d0f3f5227 span_id=69832f518ba5a3fd |
| 00:30:43.068 | runtime-span | lambda-segment | ben-fp7-write-audit/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=bd9ab38f0f6d55a8 |
| 00:30:43.808 | lambda | call | write_audit -> stored=True | trace_id=6aa1fa173d0f3f5227 session_id=aegis-sp-a-8f09edf request_id=99262cb0-3c8b-4375 tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:43.822 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=2cb0d3690a9b3e81 |
| 00:30:43.826 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000243826,"body":{"isError":false,"re | trace_id=6aa1fa173d0f3f5227 |
| 00:30:43.826 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000243826,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:43.831 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1fa173d0f3f5227 span_id=70dcf13f4968ff45 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:43.832 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7867 out=111 | trace_id=6aa1fa173d0f3f5227 span_id=6e0968e0b01cc3fa session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:43.833 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7867 out=111 | trace_id=6aa1fa173d0f3f5227 span_id=926b2779ca615848 session_id=aegis-sp-a-8f09edf request_id=8dc3dd14-cd56-449f |
| 00:30:43.834 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa173d0f3f5227 span_id=1a3f32dea661fdf1 session_id=aegis-sp-a-8f09edf |
| 00:30:47.429 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa173d0f3f5227 span_id=b00b7a91889ec128 session_id=aegis-sp-a-8f09edf |
| 00:30:47.435 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa1fa173d0f3f5227 span_id=f90936594742c3ff session_id=aegis-sp-a-8f09edf |
| 00:30:47.440 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1fa173d0f3f5227 span_id=19ee75ef1dc0926f session_id=aegis-sp-a-8f09edf |
| 00:30:47.449 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa1fa173d0f3f5227 span_id=8e31965ca28fde05 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:47.450 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa1fa173d0f3f5227 span_id=4447c3a6a26079b5 session_id=aegis-sp-a-8f09edf |
| 00:30:47.564 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaService | trace_id=6aa1fa173d0f3f5227 span_id=487d3323030ef573 |
| 00:30:47.571 | runtime-span | lambda-segment | ben-fp7-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=294adb314350f51b |
| 00:30:47.744 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=a1ae9dc62cc5018d |
| 00:30:47.749 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000247749,"body":{"isError":false,"lo | session_id=aegis-sp-a-8f09edf trace_id=6aa1fa173d0f3f5227 |
| 00:30:47.754 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000247754,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:47.838 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000247838,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:47.875 | runtime-span | lambda-segment | ben-fp7-request-signoff/LambdaService | trace_id=6aa1fa173d0f3f5227 span_id=28a16d3046aa5db5 |
| 00:30:48.041 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=13424d915a2390b5 |
| 00:30:48.319 | runtime-span | lambda-segment | ben-fp7-request-signoff/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=1d0d30ae96f40cc0 |
| 00:30:49.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8029 out=433 masked_before_model=True | request_id=798be624-61f0-46aa session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:49.782 | lambda | call | request_signoff -> requested=False | trace_id=6aa1fa173d0f3f5227 session_id=aegis-sp-a-8f09edf request_id=480edb1d-f610-4f6e tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:49.784 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1fa173d0f3f5227 span_id=dca93f7770bfbdeb |
| 00:30:49.789 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000249789,"body":{"isError":false,"lo | trace_id=6aa1fa173d0f3f5227 |
| 00:30:49.789 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp7-ben-gw-tqqn6mu0zj","event_timestamp":1789000249789,"body":{"isError":false,"re | trace_id=6aa1fa173d0f3f5227 |
| 00:30:49.794 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1fa173d0f3f5227 span_id=868693604bc5e45c session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:49.795 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8029 out=433 | trace_id=6aa1fa173d0f3f5227 span_id=3d68f662367ccc17 session_id=aegis-sp-a-8f09edf tenant=sp-a case_id=OBS-SPA-0FA57 |
| 00:30:49.796 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8029 out=433 | trace_id=6aa1fa173d0f3f5227 span_id=a0437b3fa06285ca session_id=aegis-sp-a-8f09edf request_id=798be624-61f0-46aa |
| 00:30:49.797 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa173d0f3f5227 span_id=c88ee0bb36587be4 session_id=aegis-sp-a-8f09edf |
| 00:30:58.542 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1fa173d0f3f5227 span_id=2788d9c3bf732e14 session_id=aegis-sp-a-8f09edf |
| 00:30:58.548 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1fa173d0f3f5227 span_id=b881bd761f903d74 session_id=aegis-sp-a-8f09edf |
