# Case trace — `OBS-SPB-13CA8` (tenant `sp-b`)

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
| sessions | ['aegis-sp-b-57f054d0c6434f47a1999ecd0be0b014'] |
| single_tenant | True |
| tenants_seen | ['sp-b'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 12:45:05.740 | lambda | call | ingest_application -> ingested=True | trace_id=6aa154d11419134356 request_id=45a7467f-65a3-49dd tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:06.203 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa154d22d3e6b0b2a span_id=8cd200a1d32b4386 session_id=aegis-sp-b-57f054d |
| 12:45:06.782 | runtime-span | runtime-http | POST /invocations | trace_id=6aa154d22d3e6b0b2a span_id=a0d53627a8bd5944 session_id=aegis-sp-b-57f054d |
| 12:45:06.878 | runtime-span | span | SSM.GetParameter | trace_id=6aa154d22d3e6b0b2a span_id=4818c85147789fe4 session_id=aegis-sp-b-57f054d |
| 12:45:06.924 | runtime-span | span | SSM.GetParameter | trace_id=6aa154d22d3e6b0b2a span_id=71dda1cdbfd4a41a session_id=aegis-sp-b-57f054d |
| 12:45:06.989 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa154d22d3e6b0b2a span_id=708b98abbe19aea0 session_id=aegis-sp-b-57f054d |
| 12:45:07.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5340 out=138 masked_before_model=True | request_id=b21c75a3-2f7f-4f4a session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:07.038 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa154d22d3e6b0b2a span_id=7b55e18f9e394eaf session_id=aegis-sp-b-57f054d |
| 12:45:07.141 | runtime-span | span | mcp.session | trace_id=6aa154d22d3e6b0b2a span_id=e0a87c811bc0547d session_id=aegis-sp-b-57f054d |
| 12:45:07.263 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa154d22d3e6b0b2a span_id=b7b16f81f8362191 session_id=aegis-sp-b-57f054d |
| 12:45:07.490 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaService | trace_id=6aa154d22d3e6b0b2a span_id=189d37faf9dde09a |
| 12:45:07.494 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=f51d377ed0980d60 |
| 12:45:07.520 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=ead11977edd6bbf6 |
| 12:45:07.522 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957907522,"body":{"isError":false,"lo | session_id=aegis-sp-b-57f054d trace_id=6aa154d22d3e6b0b2a |
| 12:45:07.527 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957907527,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:07.613 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957907613,"body":{"isError":false,"re | trace_id=6aa154d22d3e6b0b2a |
| 12:45:07.621 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=46545 out=2115 | trace_id=6aa154d22d3e6b0b2a span_id=f7dc2e4a14bcfa72 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:07.622 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa154d22d3e6b0b2a span_id=84212b59c5adcf20 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:07.623 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5340 out=138 | trace_id=6aa154d22d3e6b0b2a span_id=1a6720a962710348 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:07.633 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5340 out=138 | trace_id=6aa154d22d3e6b0b2a span_id=68c1bee680a113e9 session_id=aegis-sp-b-57f054d request_id=b21c75a3-2f7f-4f4a |
| 12:45:07.634 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154d22d3e6b0b2a span_id=eeb802248ac4772c session_id=aegis-sp-b-57f054d |
| 12:45:11.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5556 out=118 masked_before_model=True | request_id=c3937bfb-e6a9-4d97 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:11.003 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154d22d3e6b0b2a span_id=c4c13af255cda2d6 session_id=aegis-sp-b-57f054d |
| 12:45:11.019 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa154d22d3e6b0b2a span_id=1639a97be05201d2 session_id=aegis-sp-b-57f054d |
| 12:45:11.050 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa154d22d3e6b0b2a span_id=7f85d7861f6e863f session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:11.051 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa154d22d3e6b0b2a span_id=2a63457524242343 session_id=aegis-sp-b-57f054d |
| 12:45:11.164 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaService | trace_id=6aa154d22d3e6b0b2a span_id=61bc757c24301e00 |
| 12:45:11.175 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=c0dd39cc5b2a092b |
| 12:45:11.340 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=d2c7ce0942fa9363 |
| 12:45:11.344 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957911344,"body":{"isError":false,"lo | session_id=aegis-sp-b-57f054d trace_id=6aa154d22d3e6b0b2a |
| 12:45:11.350 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957911350,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:11.429 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957911429,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:11.441 | runtime-span | lambda-segment | ben-fp2-intake-application/LambdaService | trace_id=6aa154d22d3e6b0b2a span_id=7f980d927db27522 |
| 12:45:11.447 | runtime-span | lambda-segment | ben-fp2-intake-application/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=f0c89e18c9cde103 |
| 12:45:11.613 | lambda | call | intake_application -> ok | trace_id=6aa154d22d3e6b0b2a session_id=aegis-sp-b-57f054d request_id=39929a3f-8f45-4911 tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:11.614 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=83b5a692c69ab3fa |
| 12:45:11.617 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957911617,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:11.617 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957911617,"body":{"isError":false,"re | trace_id=6aa154d22d3e6b0b2a |
| 12:45:11.622 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa154d22d3e6b0b2a span_id=76016313a88c1d22 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:11.623 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5556 out=118 | trace_id=6aa154d22d3e6b0b2a span_id=6aa40f7a59b102aa session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:11.624 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154d22d3e6b0b2a span_id=81e61cdd76bde95d session_id=aegis-sp-b-57f054d |
| 12:45:11.624 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5556 out=118 | trace_id=6aa154d22d3e6b0b2a span_id=73f3342a150e155e session_id=aegis-sp-b-57f054d request_id=c3937bfb-e6a9-4d97 |
| 12:45:14.249 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154d22d3e6b0b2a span_id=7cc7a2dfd6fa3d30 session_id=aegis-sp-b-57f054d |
| 12:45:14.256 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa154d22d3e6b0b2a span_id=9d81f692546e66e5 session_id=aegis-sp-b-57f054d |
| 12:45:14.264 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa154d22d3e6b0b2a span_id=fbd9a9f2f71d9479 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:14.265 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa154d22d3e6b0b2a span_id=d82c2b9d54e8ed3a session_id=aegis-sp-b-57f054d |
| 12:45:14.376 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaService | trace_id=6aa154d22d3e6b0b2a span_id=0cb7b24cfec4e639 |
| 12:45:14.381 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=98898055b801083a |
| 12:45:14.519 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=7b86f56283da17f7 |
| 12:45:14.522 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957914522,"body":{"isError":false,"lo | session_id=aegis-sp-b-57f054d trace_id=6aa154d22d3e6b0b2a |
| 12:45:14.526 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957914526,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:14.607 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957914607,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:14.636 | runtime-span | lambda-segment | ben-fp2-mask-pii/LambdaService | trace_id=6aa154d22d3e6b0b2a span_id=1f57ab3ff1e814d4 |
| 12:45:14.640 | runtime-span | lambda-segment | ben-fp2-mask-pii/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=a1ebce8394db8bdf |
| 12:45:15.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5975 out=391 masked_before_model=True | request_id=c7e83411-f352-46a4 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:15.129 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa154d22d3e6b0b2a session_id=aegis-sp-b-57f054d request_id=17f07fd2-fabb-49c3 tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:15.129 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=5196cb343ea02484 |
| 12:45:15.135 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957915135,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:15.135 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957915135,"body":{"isError":false,"re | trace_id=6aa154d22d3e6b0b2a |
| 12:45:15.141 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa154d22d3e6b0b2a span_id=9aea6de99f18653c session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:15.142 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5975 out=391 | trace_id=6aa154d22d3e6b0b2a span_id=f3ba01bef4995d14 session_id=aegis-sp-b-57f054d request_id=c7e83411-f352-46a4 |
| 12:45:15.142 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5975 out=391 | trace_id=6aa154d22d3e6b0b2a span_id=9077d57827acb542 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:15.143 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154d22d3e6b0b2a span_id=a7905ac993214b56 session_id=aegis-sp-b-57f054d |
| 12:45:19.581 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154d22d3e6b0b2a span_id=1cd4bcde095ad844 session_id=aegis-sp-b-57f054d |
| 12:45:19.587 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa154d22d3e6b0b2a span_id=d84354d12363fc91 session_id=aegis-sp-b-57f054d |
| 12:45:19.595 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa154d22d3e6b0b2a span_id=fb8cf62b8228ce84 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:19.596 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa154d22d3e6b0b2a span_id=df7b84e948d0135e session_id=aegis-sp-b-57f054d |
| 12:45:19.711 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaService | trace_id=6aa154d22d3e6b0b2a span_id=63956b2fafb81198 |
| 12:45:19.715 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=650d8604ea4b1312 |
| 12:45:19.856 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=5e6c4c370b1b39e7 |
| 12:45:19.861 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957919861,"body":{"isError":false,"lo | session_id=aegis-sp-b-57f054d trace_id=6aa154d22d3e6b0b2a |
| 12:45:19.866 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957919866,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:19.966 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957919966,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:19.992 | runtime-span | lambda-segment | ben-fp2-assess-eligibility/LambdaService | trace_id=6aa154d22d3e6b0b2a span_id=619796347b1d4590 |
| 12:45:19.998 | runtime-span | lambda-segment | ben-fp2-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=e3dc8dd73a13d6b4 |
| 12:45:20.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6597 out=560 masked_before_model=True | request_id=13aa7720-bcac-4fb5 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:20.018 | lambda | call | assess_eligibility -> ok | trace_id=6aa154d22d3e6b0b2a session_id=aegis-sp-b-57f054d request_id=0863668a-2042-402e tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:20.019 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=f74f93ac1e400fed |
| 12:45:20.024 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957920024,"body":{"isError":false,"re | trace_id=6aa154d22d3e6b0b2a |
| 12:45:20.024 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957920024,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:20.029 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa154d22d3e6b0b2a span_id=9eb843e6b175b1c5 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:20.030 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6597 out=560 | trace_id=6aa154d22d3e6b0b2a span_id=4b846b5e0fb473b4 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:20.031 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6597 out=560 | trace_id=6aa154d22d3e6b0b2a span_id=6c9a361e4ff7e719 session_id=aegis-sp-b-57f054d request_id=13aa7720-bcac-4fb5 |
| 12:45:20.032 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154d22d3e6b0b2a span_id=e39b8391a808a637 session_id=aegis-sp-b-57f054d |
| 12:45:26.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7205 out=356 masked_before_model=True | request_id=06850514-2c22-40bc session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:26.272 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154d22d3e6b0b2a span_id=9a244d021e853a2b session_id=aegis-sp-b-57f054d |
| 12:45:26.278 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa154d22d3e6b0b2a span_id=a1268e8033994e2d session_id=aegis-sp-b-57f054d |
| 12:45:26.313 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa154d22d3e6b0b2a span_id=1a2be37ccc12f146 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:26.314 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa154d22d3e6b0b2a span_id=8061ccb29b2f1470 session_id=aegis-sp-b-57f054d |
| 12:45:26.452 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaService | trace_id=6aa154d22d3e6b0b2a span_id=3cb56b3a766f6f44 |
| 12:45:26.457 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=ee165838cc0b9a6b |
| 12:45:26.617 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=4ac8ddfa6e2e057f |
| 12:45:26.621 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957926621,"body":{"isError":false,"lo | session_id=aegis-sp-b-57f054d trace_id=6aa154d22d3e6b0b2a |
| 12:45:26.626 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957926626,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:26.716 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957926716,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:26.746 | runtime-span | lambda-segment | ben-fp2-core-tools/LambdaService | trace_id=6aa154d22d3e6b0b2a span_id=552d7f45704edc2b |
| 12:45:26.752 | runtime-span | lambda-segment | ben-fp2-core-tools/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=58d98151c4dca760 |
| 12:45:26.771 | lambda | call | benefits_core -> committed=False | trace_id=6aa154d22d3e6b0b2a session_id=aegis-sp-b-57f054d request_id=c166391b-b9e6-4d15 tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:26.772 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=2315b4c8a7b2b212 |
| 12:45:26.777 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957926777,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:26.777 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957926777,"body":{"isError":false,"re | trace_id=6aa154d22d3e6b0b2a |
| 12:45:26.783 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa154d22d3e6b0b2a span_id=f2f9d647689fb655 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:26.784 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7205 out=356 | trace_id=6aa154d22d3e6b0b2a span_id=db4720c4b8980595 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:26.785 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7205 out=356 | trace_id=6aa154d22d3e6b0b2a span_id=bde71f3b8b3dd32b session_id=aegis-sp-b-57f054d request_id=06850514-2c22-40bc |
| 12:45:26.792 | runtime-span | span | SSM.GetParameter | trace_id=6aa154d22d3e6b0b2a span_id=395b9323fb365302 session_id=aegis-sp-b-57f054d |
| 12:45:26.831 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154d22d3e6b0b2a span_id=543cd92fce2a7369 session_id=aegis-sp-b-57f054d |
| 12:45:31.920 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154d22d3e6b0b2a span_id=a48d91389240d3ea session_id=aegis-sp-b-57f054d |
| 12:45:31.926 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa154d22d3e6b0b2a span_id=fd32cbe99ab8ee0b session_id=aegis-sp-b-57f054d |
| 12:45:31.938 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa154d22d3e6b0b2a span_id=3852702da4f53af1 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:31.939 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa154d22d3e6b0b2a span_id=c84698b13de877bc session_id=aegis-sp-b-57f054d |
| 12:45:32.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7855 out=111 masked_before_model=True | request_id=1fd0bad1-96c4-4e10 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:32.000 | worm | evidence | INTENT benefits-determination seq=0 chain=dd9e2fb23c17… | trace_id=6aa154d22d3e6b0b2a session_id=aegis-sp-b-57f054d request_id=f6114404-b58c-4f84 tenant=sp-b |
| 12:45:32.048 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaService | trace_id=6aa154d22d3e6b0b2a span_id=7ee72b6726543df8 |
| 12:45:32.054 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=65cf5ec1cca1ae7f |
| 12:45:32.195 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=ccb0be5a0b3f57d1 |
| 12:45:32.198 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957932198,"body":{"isError":false,"lo | session_id=aegis-sp-b-57f054d trace_id=6aa154d22d3e6b0b2a |
| 12:45:32.201 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957932201,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:32.279 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957932279,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:32.303 | runtime-span | lambda-segment | ben-fp2-write-audit/LambdaService | trace_id=6aa154d22d3e6b0b2a span_id=50d2a7ae40a0ccc4 |
| 12:45:32.313 | runtime-span | lambda-segment | ben-fp2-write-audit/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=7e089dfc49a58dbc |
| 12:45:32.813 | lambda | call | write_audit -> stored=True | trace_id=6aa154d22d3e6b0b2a session_id=aegis-sp-b-57f054d request_id=f6114404-b58c-4f84 tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:32.814 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=ffb6cb74cc39a6aa |
| 12:45:32.818 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957932818,"body":{"isError":false,"re | trace_id=6aa154d22d3e6b0b2a |
| 12:45:32.818 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957932818,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:32.824 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa154d22d3e6b0b2a span_id=27102c1fe5151dc2 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:32.825 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7855 out=111 | trace_id=6aa154d22d3e6b0b2a span_id=4e794dbd59da33d3 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:32.826 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7855 out=111 | trace_id=6aa154d22d3e6b0b2a span_id=77abfa9e7efefec0 session_id=aegis-sp-b-57f054d request_id=1fd0bad1-96c4-4e10 |
| 12:45:32.827 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154d22d3e6b0b2a span_id=0fe4c7f229396be0 session_id=aegis-sp-b-57f054d |
| 12:45:36.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8017 out=441 masked_before_model=True | request_id=90ba31f0-e4ae-464c session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:36.149 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154d22d3e6b0b2a span_id=baa7cc3b41e51ffd session_id=aegis-sp-b-57f054d |
| 12:45:36.155 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa154d22d3e6b0b2a span_id=afb5909354e6bb6c session_id=aegis-sp-b-57f054d |
| 12:45:36.163 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa154d22d3e6b0b2a span_id=1878224b342d5584 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:36.164 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa154d22d3e6b0b2a span_id=7c51589a370a4f1a session_id=aegis-sp-b-57f054d |
| 12:45:36.256 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaService | trace_id=6aa154d22d3e6b0b2a span_id=1ea343d58cf7c0b2 |
| 12:45:36.262 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=ab93c200c8b49e3a |
| 12:45:36.415 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=ca760e6f129bccbf |
| 12:45:36.418 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957936418,"body":{"isError":false,"lo | session_id=aegis-sp-b-57f054d trace_id=6aa154d22d3e6b0b2a |
| 12:45:36.423 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957936423,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:36.522 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957936522,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:36.556 | runtime-span | lambda-segment | ben-fp2-request-signoff/LambdaService | trace_id=6aa154d22d3e6b0b2a span_id=0750e7ca614e84d2 |
| 12:45:36.561 | runtime-span | lambda-segment | ben-fp2-request-signoff/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=8f7f22b602e1f3ea |
| 12:45:36.591 | lambda | call | request_signoff -> requested=False | trace_id=6aa154d22d3e6b0b2a session_id=aegis-sp-b-57f054d request_id=62aa5c58-99e6-43bc tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:36.592 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154d22d3e6b0b2a span_id=3868062214cfe1ae |
| 12:45:36.595 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957936595,"body":{"isError":false,"lo | trace_id=6aa154d22d3e6b0b2a |
| 12:45:36.595 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957936595,"body":{"isError":false,"re | trace_id=6aa154d22d3e6b0b2a |
| 12:45:36.600 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa154d22d3e6b0b2a span_id=35b72448154c96ef session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:36.602 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8017 out=441 | trace_id=6aa154d22d3e6b0b2a span_id=0e5ea3d074b90b26 session_id=aegis-sp-b-57f054d tenant=sp-b case_id=OBS-SPB-13CA8 |
| 12:45:36.603 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8017 out=441 | trace_id=6aa154d22d3e6b0b2a span_id=a25df07f89c3be46 session_id=aegis-sp-b-57f054d request_id=90ba31f0-e4ae-464c |
| 12:45:36.604 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154d22d3e6b0b2a span_id=4895673b40ba71a6 session_id=aegis-sp-b-57f054d |
| 12:45:45.400 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154d22d3e6b0b2a span_id=4f30f0ffb6f1803c session_id=aegis-sp-b-57f054d |
| 12:45:45.407 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa154d22d3e6b0b2a span_id=edfd661742a0875a session_id=aegis-sp-b-57f054d |
| 12:45:45.411 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa154d22d3e6b0b2a span_id=a16df2e36bb849b7 session_id=aegis-sp-b-57f054d |
