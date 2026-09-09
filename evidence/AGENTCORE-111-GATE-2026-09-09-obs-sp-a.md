# Case trace — `OBS-SPA-DD52B` (tenant `sp-a`)

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
| sessions | ['aegis-sp-a-e1fcc89d29314e7ebbd936b44cf7270f'] |
| single_tenant | True |
| tenants_seen | ['sp-a'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 12:44:22.080 | lambda | call | ingest_application -> ingested=True | trace_id=6aa154a52d9c81d642 request_id=41884f7a-ef2b-467d tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:22.504 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa154a6312c36493c span_id=76091a607b39b978 session_id=aegis-sp-a-e1fcc89 |
| 12:44:23.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5343 out=140 masked_before_model=True | request_id=f395a508-9e60-435b session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:23.036 | runtime-span | runtime-http | POST /invocations | trace_id=6aa154a6312c36493c span_id=62a0d90c52320aa5 session_id=aegis-sp-a-e1fcc89 |
| 12:44:23.105 | runtime-span | span | SSM.GetParameter | trace_id=6aa154a6312c36493c span_id=12aa1798fecd612c session_id=aegis-sp-a-e1fcc89 |
| 12:44:23.147 | runtime-span | span | SSM.GetParameter | trace_id=6aa154a6312c36493c span_id=84aaf6d1e203ec97 session_id=aegis-sp-a-e1fcc89 |
| 12:44:23.202 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa154a6312c36493c span_id=d4a12907f533a9cc session_id=aegis-sp-a-e1fcc89 |
| 12:44:23.245 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa154a6312c36493c span_id=a71419f0b310581a session_id=aegis-sp-a-e1fcc89 |
| 12:44:23.324 | runtime-span | span | mcp.session | trace_id=6aa154a6312c36493c span_id=866850aee928c191 session_id=aegis-sp-a-e1fcc89 |
| 12:44:23.464 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa154a6312c36493c span_id=e4a952d483eb067d session_id=aegis-sp-a-e1fcc89 |
| 12:44:23.704 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaService | trace_id=6aa154a6312c36493c span_id=32386315a328bf87 |
| 12:44:23.711 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=64e9515a1069ce39 |
| 12:44:23.732 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=0194f256e533a0f6 |
| 12:44:23.734 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957863734,"body":{"isError":false,"lo | session_id=aegis-sp-a-e1fcc89 trace_id=6aa154a6312c36493c |
| 12:44:23.739 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957863739,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:23.825 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957863825,"body":{"isError":false,"re | trace_id=6aa154a6312c36493c |
| 12:44:23.834 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=46676 out=2173 | trace_id=6aa154a6312c36493c span_id=58c5e180bb03f5ce session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:23.835 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa154a6312c36493c span_id=f60dc242f9c6a0cd session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:23.836 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5343 out=140 | trace_id=6aa154a6312c36493c span_id=a5244fea5f706ea3 session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:23.838 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5343 out=140 | trace_id=6aa154a6312c36493c span_id=0522ee659c2407aa session_id=aegis-sp-a-e1fcc89 request_id=f395a508-9e60-435b |
| 12:44:23.839 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154a6312c36493c span_id=e90536172cf46843 session_id=aegis-sp-a-e1fcc89 |
| 12:44:27.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5561 out=122 masked_before_model=True | request_id=38f43b32-ae8b-49fe session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:27.082 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154a6312c36493c span_id=d24cd1a3e242e30b session_id=aegis-sp-a-e1fcc89 |
| 12:44:27.095 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa154a6312c36493c span_id=3302b45e808481f2 session_id=aegis-sp-a-e1fcc89 |
| 12:44:27.125 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa154a6312c36493c span_id=64aa0c127609f658 session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:27.126 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa154a6312c36493c span_id=ae345b19afb37a50 session_id=aegis-sp-a-e1fcc89 |
| 12:44:27.232 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaService | trace_id=6aa154a6312c36493c span_id=0cf831dac9032de2 |
| 12:44:27.237 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=83acf705bb193a40 |
| 12:44:27.576 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=b7ef0de9b913b6a5 |
| 12:44:27.580 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957867580,"body":{"isError":false,"lo | session_id=aegis-sp-a-e1fcc89 trace_id=6aa154a6312c36493c |
| 12:44:27.584 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957867584,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:27.659 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957867659,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:27.690 | runtime-span | lambda-segment | ben-fp2-intake-application/LambdaService | trace_id=6aa154a6312c36493c span_id=0da1c48b6e402700 |
| 12:44:27.695 | runtime-span | lambda-segment | ben-fp2-intake-application/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=099540bc65955dbb |
| 12:44:27.878 | lambda | call | intake_application -> ok | trace_id=6aa154a6312c36493c session_id=aegis-sp-a-e1fcc89 request_id=899960c5-9360-401a tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:27.878 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=90fad9ce63b09d46 |
| 12:44:27.882 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957867882,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:27.882 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957867882,"body":{"isError":false,"re | trace_id=6aa154a6312c36493c |
| 12:44:27.888 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa154a6312c36493c span_id=8e176aad663c94a4 session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:27.889 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5561 out=122 | trace_id=6aa154a6312c36493c span_id=46c6048ded54264f session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:27.890 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154a6312c36493c span_id=973dddd6cecc4c4e session_id=aegis-sp-a-e1fcc89 |
| 12:44:27.890 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5561 out=122 | trace_id=6aa154a6312c36493c span_id=6cab7b94cb9fe96a session_id=aegis-sp-a-e1fcc89 request_id=38f43b32-ae8b-49fe |
| 12:44:30.844 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154a6312c36493c span_id=4a4033f530b7c83f session_id=aegis-sp-a-e1fcc89 |
| 12:44:30.850 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa154a6312c36493c span_id=0dbb29ebe0ab4b69 session_id=aegis-sp-a-e1fcc89 |
| 12:44:30.860 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa154a6312c36493c span_id=a64700e18e00d63d session_id=aegis-sp-a-e1fcc89 |
| 12:44:30.860 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa154a6312c36493c span_id=6e22e1fb4009566e session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:30.967 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaService | trace_id=6aa154a6312c36493c span_id=7837d6d2596ea123 |
| 12:44:30.972 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=7668af235c544ad3 |
| 12:44:31.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5988 out=395 masked_before_model=True | request_id=63fa3c31-781d-4aeb session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:31.115 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=b68e93238a00b726 |
| 12:44:31.118 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957871118,"body":{"isError":false,"lo | session_id=aegis-sp-a-e1fcc89 trace_id=6aa154a6312c36493c |
| 12:44:31.122 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957871122,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:31.214 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957871214,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:31.234 | runtime-span | lambda-segment | ben-fp2-mask-pii/LambdaService | trace_id=6aa154a6312c36493c span_id=20450c42fe1e3f46 |
| 12:44:31.240 | runtime-span | lambda-segment | ben-fp2-mask-pii/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=569022bbbeab2e78 |
| 12:44:31.711 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa154a6312c36493c session_id=aegis-sp-a-e1fcc89 request_id=1d6b7c86-1be2-42e3 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:31.712 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=a902900199d50f5b |
| 12:44:31.715 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957871715,"body":{"isError":false,"re | trace_id=6aa154a6312c36493c |
| 12:44:31.715 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957871715,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:31.721 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa154a6312c36493c span_id=dd272378449fa888 session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:31.722 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5988 out=395 | trace_id=6aa154a6312c36493c span_id=7855ffc424f1241a session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:31.723 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154a6312c36493c span_id=dde8bd325b7bc9ed session_id=aegis-sp-a-e1fcc89 |
| 12:44:31.723 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5988 out=395 | trace_id=6aa154a6312c36493c span_id=85850161c63db5f1 session_id=aegis-sp-a-e1fcc89 request_id=63fa3c31-781d-4aeb |
| 12:44:36.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6614 out=564 masked_before_model=True | request_id=bbb8b267-aacd-45a8 session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:36.243 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154a6312c36493c span_id=fdd7ee2c3d863e8b session_id=aegis-sp-a-e1fcc89 |
| 12:44:36.249 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa154a6312c36493c span_id=dc03fe213a5a725f session_id=aegis-sp-a-e1fcc89 |
| 12:44:36.256 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa154a6312c36493c span_id=9a562ccfe55abae7 session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:36.257 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa154a6312c36493c span_id=96dd4835293ad7cf session_id=aegis-sp-a-e1fcc89 |
| 12:44:36.357 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaService | trace_id=6aa154a6312c36493c span_id=4895fa8a095c45f7 |
| 12:44:36.362 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=18eb4a52b669d1d4 |
| 12:44:36.515 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=ccc1c795b7eb7673 |
| 12:44:36.518 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957876518,"body":{"isError":false,"lo | session_id=aegis-sp-a-e1fcc89 trace_id=6aa154a6312c36493c |
| 12:44:36.522 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957876522,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:36.602 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957876602,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:36.635 | runtime-span | lambda-segment | ben-fp2-assess-eligibility/LambdaService | trace_id=6aa154a6312c36493c span_id=62dc2f5e9bca42aa |
| 12:44:36.641 | runtime-span | lambda-segment | ben-fp2-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=a10aae993439fdca |
| 12:44:36.663 | lambda | call | assess_eligibility -> ok | trace_id=6aa154a6312c36493c session_id=aegis-sp-a-e1fcc89 request_id=6124cbcb-7b78-4b8c tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:36.664 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=dc9949afe7ca76e8 |
| 12:44:36.668 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957876668,"body":{"isError":false,"re | trace_id=6aa154a6312c36493c |
| 12:44:36.668 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957876668,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:36.674 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa154a6312c36493c span_id=fc2bf7e417ff7529 session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:36.675 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6614 out=564 | trace_id=6aa154a6312c36493c span_id=48cc65d2e573709c session_id=aegis-sp-a-e1fcc89 request_id=bbb8b267-aacd-45a8 |
| 12:44:36.675 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6614 out=564 | trace_id=6aa154a6312c36493c span_id=07e2aeae1891e095 session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:36.676 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154a6312c36493c span_id=c908b39407a7da6e session_id=aegis-sp-a-e1fcc89 |
| 12:44:43.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7226 out=363 masked_before_model=True | request_id=2967886f-3559-48c5 session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:43.258 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154a6312c36493c span_id=f025123ca9dddda7 session_id=aegis-sp-a-e1fcc89 |
| 12:44:43.264 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa154a6312c36493c span_id=b7f4836c8eba552b session_id=aegis-sp-a-e1fcc89 |
| 12:44:43.288 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa154a6312c36493c span_id=28c8df3ac60147a4 session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:43.289 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa154a6312c36493c span_id=0403dc67490e3a18 session_id=aegis-sp-a-e1fcc89 |
| 12:44:43.408 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaService | trace_id=6aa154a6312c36493c span_id=169ee5327cdd66b5 |
| 12:44:43.413 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=b4cdba2016ed4ef2 |
| 12:44:43.584 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=05c55e6ae269fea7 |
| 12:44:43.587 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957883587,"body":{"isError":false,"lo | session_id=aegis-sp-a-e1fcc89 trace_id=6aa154a6312c36493c |
| 12:44:43.591 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957883591,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:43.669 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957883669,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:43.687 | runtime-span | lambda-segment | ben-fp2-core-tools/LambdaService | trace_id=6aa154a6312c36493c span_id=0154bd35bb770dc4 |
| 12:44:43.692 | runtime-span | lambda-segment | ben-fp2-core-tools/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=e21bf8fdf211e85e |
| 12:44:43.713 | lambda | call | benefits_core -> committed=False | trace_id=6aa154a6312c36493c session_id=aegis-sp-a-e1fcc89 request_id=c1a79a95-efea-49ca tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:43.713 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=a2bfdc5a3c2753fe |
| 12:44:43.718 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957883718,"body":{"isError":false,"re | trace_id=6aa154a6312c36493c |
| 12:44:43.718 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957883718,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:43.724 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa154a6312c36493c span_id=2643abb15af95b67 session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:43.725 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7226 out=363 | trace_id=6aa154a6312c36493c span_id=6fd72fd1124e34b6 session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:43.726 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7226 out=363 | trace_id=6aa154a6312c36493c span_id=1f6f2af1ef17d4f4 session_id=aegis-sp-a-e1fcc89 request_id=2967886f-3559-48c5 |
| 12:44:43.731 | runtime-span | span | SSM.GetParameter | trace_id=6aa154a6312c36493c span_id=3b0f045cfb2648b8 session_id=aegis-sp-a-e1fcc89 |
| 12:44:43.768 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154a6312c36493c span_id=935bb9d7ceccbbd7 session_id=aegis-sp-a-e1fcc89 |
| 12:44:49.143 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154a6312c36493c span_id=a93a42600c405afb session_id=aegis-sp-a-e1fcc89 |
| 12:44:49.148 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa154a6312c36493c span_id=091c4c7c6224a95c session_id=aegis-sp-a-e1fcc89 |
| 12:44:49.158 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa154a6312c36493c span_id=cc0d81122c343305 session_id=aegis-sp-a-e1fcc89 |
| 12:44:49.158 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa154a6312c36493c span_id=69171ca6854d4f55 session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:49.272 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaService | trace_id=6aa154a6312c36493c span_id=617ef2b507be3507 |
| 12:44:49.284 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=1f8dfd0e1685ad6d |
| 12:44:49.439 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=f649d9f61331a7fa |
| 12:44:49.442 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957889442,"body":{"isError":false,"lo | session_id=aegis-sp-a-e1fcc89 trace_id=6aa154a6312c36493c |
| 12:44:49.446 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957889446,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:49.514 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957889514,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:49.538 | runtime-span | lambda-segment | ben-fp2-write-audit/LambdaService | trace_id=6aa154a6312c36493c span_id=6eeb3f14dc5d913e |
| 12:44:49.543 | runtime-span | lambda-segment | ben-fp2-write-audit/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=d785f2f80e77b193 |
| 12:44:50.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7891 out=111 masked_before_model=True | request_id=f8dfec93-d4d5-4ad1 session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:50.000 | worm | evidence | INTENT benefits-determination seq=0 chain=b19ae5d4e5b2… | trace_id=6aa154a6312c36493c session_id=aegis-sp-a-e1fcc89 request_id=c8bc6f54-01a9-434c tenant=sp-a |
| 12:44:50.335 | lambda | call | write_audit -> stored=True | trace_id=6aa154a6312c36493c session_id=aegis-sp-a-e1fcc89 request_id=c8bc6f54-01a9-434c tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:50.336 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=dc08315066650764 |
| 12:44:50.339 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957890339,"body":{"isError":false,"re | trace_id=6aa154a6312c36493c |
| 12:44:50.339 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957890339,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:50.345 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa154a6312c36493c span_id=7059a8a764c94356 session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:50.346 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7891 out=111 | trace_id=6aa154a6312c36493c span_id=a8d1b61dd116055e session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:50.347 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7891 out=111 | trace_id=6aa154a6312c36493c span_id=caab763bf91ad551 session_id=aegis-sp-a-e1fcc89 request_id=f8dfec93-d4d5-4ad1 |
| 12:44:50.348 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154a6312c36493c span_id=af8da608a7fe4d99 session_id=aegis-sp-a-e1fcc89 |
| 12:44:52.950 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154a6312c36493c span_id=fba4e318d2130ac2 session_id=aegis-sp-a-e1fcc89 |
| 12:44:52.956 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa154a6312c36493c span_id=b17240da9f7005bc session_id=aegis-sp-a-e1fcc89 |
| 12:44:52.964 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa154a6312c36493c span_id=5f9657a27caa1fa3 session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:52.965 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa154a6312c36493c span_id=7fab6f518a422182 session_id=aegis-sp-a-e1fcc89 |
| 12:44:53.101 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaService | trace_id=6aa154a6312c36493c span_id=5271aafcf69eeb9f |
| 12:44:53.106 | runtime-span | lambda-segment | ben-fp2-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=61f601a6143d71a5 |
| 12:44:53.260 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=da3413cd1e76cd2c |
| 12:44:53.264 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957893264,"body":{"isError":false,"lo | session_id=aegis-sp-a-e1fcc89 trace_id=6aa154a6312c36493c |
| 12:44:53.268 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957893268,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:53.380 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957893380,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:53.413 | runtime-span | lambda-segment | ben-fp2-request-signoff/LambdaService | trace_id=6aa154a6312c36493c span_id=0c817df5d4f46637 |
| 12:44:53.595 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=9e0d7788782441ab |
| 12:44:53.914 | runtime-span | lambda-segment | ben-fp2-request-signoff/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=7961286a61019495 |
| 12:44:55.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8053 out=478 masked_before_model=True | request_id=c4b82591-873b-476f session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:55.352 | lambda | call | request_signoff -> requested=False | trace_id=6aa154a6312c36493c session_id=aegis-sp-a-e1fcc89 request_id=0d572b4d-91b1-4170 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:55.353 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa154a6312c36493c span_id=096381a9a0bc0492 |
| 12:44:55.359 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957895359,"body":{"isError":false,"re | trace_id=6aa154a6312c36493c |
| 12:44:55.360 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp2-ben-gw-qyhssqjsnn","event_timestamp":1788957895360,"body":{"isError":false,"lo | trace_id=6aa154a6312c36493c |
| 12:44:55.365 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa154a6312c36493c span_id=05155b34a5e11d70 session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:55.366 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8053 out=478 | trace_id=6aa154a6312c36493c span_id=b50c6adaf7266d4f session_id=aegis-sp-a-e1fcc89 tenant=sp-a case_id=OBS-SPA-DD52B |
| 12:44:55.367 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8053 out=478 | trace_id=6aa154a6312c36493c span_id=90b5310bb3a71d94 session_id=aegis-sp-a-e1fcc89 request_id=c4b82591-873b-476f |
| 12:44:55.368 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa154a6312c36493c span_id=8a40e321bed945fe session_id=aegis-sp-a-e1fcc89 |
| 12:44:55.372 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154a6312c36493c span_id=b02dc4703ce6df62 session_id=aegis-sp-a-e1fcc89 |
| 12:45:05.208 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa154a6312c36493c span_id=d8584f1e4a9258b2 session_id=aegis-sp-a-e1fcc89 |
| 12:45:05.214 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa154a6312c36493c span_id=d6516132301ef176 session_id=aegis-sp-a-e1fcc89 |
