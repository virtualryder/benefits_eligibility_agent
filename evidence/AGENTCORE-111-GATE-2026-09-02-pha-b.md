# Case trace — `OBS-PHAB-D8F93` (tenant `pha-b`)

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
| sessions | ['aegis-pha-b-285c820e84fb423aaf50f86f03e4cab9'] |
| single_tenant | True |
| tenants_seen | ['pha-b'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 02:28:58.072 | lambda | call | ingest_application -> ingested=True | trace_id=6a98db693530d6b176 request_id=432e3b1d-a5c2-4290 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:28:58.547 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6a98db6a241515fe01 span_id=c94cdb282dcc6c7d session_id=aegis-pha-b-285c82 |
| 02:28:59.000 | bedrock-model-log | model-invocation | ConverseStream us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=3519 out=154 masked_before_model=True | request_id=b10148eb-8ce1-4760 session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:28:59.189 | runtime-span | runtime-http | POST /invocations | trace_id=6a98db6a241515fe01 span_id=17266350ff3d4170 session_id=aegis-pha-b-285c82 |
| 02:28:59.284 | runtime-span | span | SSM.GetParameter | trace_id=6a98db6a241515fe01 span_id=884b32dfdfbb8454 session_id=aegis-pha-b-285c82 |
| 02:28:59.444 | runtime-span | span | mcp.session | trace_id=6a98db6a241515fe01 span_id=e830e6525bd575a1 session_id=aegis-pha-b-285c82 |
| 02:28:59.596 | runtime-span | mcp-list | mcp tools/list | trace_id=6a98db6a241515fe01 span_id=e11157db8f94d1ae session_id=aegis-pha-b-285c82 |
| 02:28:59.778 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaService | trace_id=6a98db6a241515fe01 span_id=03520c7ac7dd1f55 |
| 02:28:59.783 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=91ba4f726ab6313a |
| 02:28:59.783 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=463bfec8f966a087 |
| 02:28:59.786 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402539786,"body":{"isError":false,"lo | session_id=aegis-pha-b-285c82 trace_id=6a98db6a241515fe01 |
| 02:28:59.791 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402539791,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:28:59.875 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402539875,"body":{"isError":false,"re | trace_id=6a98db6a241515fe01 |
| 02:28:59.883 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=23636 out=1586 | trace_id=6a98db6a241515fe01 span_id=d0b5162e381f47f6 session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:28:59.884 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6a98db6a241515fe01 span_id=2ad6fbefe4370fa6 session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:28:59.885 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=3519 out=154 | trace_id=6a98db6a241515fe01 span_id=eca70dc1a0ff86e8 session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:28:59.888 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=3519 out=154 | trace_id=6a98db6a241515fe01 span_id=ac9c866c15ff83ee session_id=aegis-pha-b-285c82 request_id=b10148eb-8ce1-4760 |
| 02:29:02.513 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6a98db6a241515fe01 span_id=bc2f9e1c87e0854a session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:02.514 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6a98db6a241515fe01 span_id=cac6f3dcfe90a4bb session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:02.515 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6a98db6a241515fe01 span_id=baada38491e55b97 session_id=aegis-pha-b-285c82 |
| 02:29:02.515 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6a98db6a241515fe01 span_id=cbd748c00b1dd555 session_id=aegis-pha-b-285c82 |
| 02:29:02.572 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaService | trace_id=6a98db6a241515fe01 span_id=3f50c35e0d6deb41 |
| 02:29:02.580 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=8b929f0c6f17d0c3 |
| 02:29:02.582 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=7254efb470c39e74 |
| 02:29:02.584 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402542584,"body":{"isError":false,"lo | session_id=aegis-pha-b-285c82 trace_id=6a98db6a241515fe01 |
| 02:29:02.589 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402542589,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:29:02.641 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402542641,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:29:02.647 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaService | trace_id=6a98db6a241515fe01 span_id=258f0bc4bc9943a5 |
| 02:29:02.652 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=c77ec3198f718088 |
| 02:29:02.652 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=216d58b7c71cee38 |
| 02:29:02.656 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402542656,"body":{"isError":false,"lo | session_id=aegis-pha-b-285c82 trace_id=6a98db6a241515fe01 |
| 02:29:02.659 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402542659,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:29:02.663 | runtime-span | lambda-segment | ben-mt4-intake-application/LambdaService | trace_id=6a98db6a241515fe01 span_id=193df880578e10a2 |
| 02:29:02.670 | runtime-span | lambda-segment | ben-mt4-intake-application/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=c9a992452f30c169 |
| 02:29:02.733 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402542733,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:29:02.760 | runtime-span | lambda-segment | ben-mt4-mask-pii/LambdaService | trace_id=6a98db6a241515fe01 span_id=752e9bd6ede07cec |
| 02:29:02.766 | runtime-span | lambda-segment | ben-mt4-mask-pii/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=d01bc9b9449e0f65 |
| 02:29:02.844 | lambda | call | intake_application -> ok | trace_id=6a98db6a241515fe01 session_id=aegis-pha-b-285c82 request_id=e23d5829-a2e9-4019 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:02.844 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=cb439fd9176e56d6 |
| 02:29:02.849 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402542849,"body":{"isError":false,"re | trace_id=6a98db6a241515fe01 |
| 02:29:02.849 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402542849,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:29:03.000 | bedrock-model-log | model-invocation | ConverseStream us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=4079 out=365 masked_before_model=True | request_id=16566244-59c9-44af session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:03.229 | lambda | call | mask_pii -> deidentified=True | trace_id=6a98db6a241515fe01 session_id=aegis-pha-b-285c82 request_id=662e02bc-905f-49d6 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:03.230 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=b6dd09b13b06fac2 |
| 02:29:03.235 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402543235,"body":{"isError":false,"re | trace_id=6a98db6a241515fe01 |
| 02:29:03.235 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402543235,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:29:03.241 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6a98db6a241515fe01 span_id=21ede70200aa9738 session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:03.242 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=4079 out=365 | trace_id=6a98db6a241515fe01 span_id=7f90e4acf1a13eab session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:03.243 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=4079 out=365 | trace_id=6a98db6a241515fe01 span_id=9d2f539105e5f1d0 session_id=aegis-pha-b-285c82 request_id=16566244-59c9-44af |
| 02:29:08.757 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6a98db6a241515fe01 span_id=fe4f40d0acc2c01f session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:08.758 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6a98db6a241515fe01 span_id=dfc7d3567b0d0140 session_id=aegis-pha-b-285c82 |
| 02:29:08.885 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaService | trace_id=6a98db6a241515fe01 span_id=076d8021c0c04078 |
| 02:29:08.896 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=1c42c5c29c80afb5 |
| 02:29:08.896 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=55199bc3380f4022 |
| 02:29:08.900 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402548900,"body":{"isError":false,"lo | session_id=aegis-pha-b-285c82 trace_id=6a98db6a241515fe01 |
| 02:29:08.904 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402548904,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:29:08.978 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402548978,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:29:09.000 | bedrock-model-log | model-invocation | ConverseStream us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=4649 out=559 masked_before_model=True | request_id=d1bc0053-d4f4-406c session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:09.003 | runtime-span | lambda-segment | ben-mt4-assess-eligibility/LambdaService | trace_id=6a98db6a241515fe01 span_id=3485eada08d17c40 |
| 02:29:09.009 | runtime-span | lambda-segment | ben-mt4-assess-eligibility/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=34b4c941fc4ff471 |
| 02:29:09.011 | lambda | call | assess_eligibility -> ok | trace_id=6a98db6a241515fe01 session_id=aegis-pha-b-285c82 request_id=b401f965-a13e-47f5 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:09.011 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=0498062501db2628 |
| 02:29:09.016 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402549016,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:29:09.016 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402549016,"body":{"isError":false,"re | trace_id=6a98db6a241515fe01 |
| 02:29:09.023 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6a98db6a241515fe01 span_id=ed6858d34452d45f session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:09.024 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=4649 out=559 | trace_id=6a98db6a241515fe01 span_id=77ac5aa1308ed370 session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:09.025 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=4649 out=559 | trace_id=6a98db6a241515fe01 span_id=2a1cfe51c3bf4750 session_id=aegis-pha-b-285c82 request_id=d1bc0053-d4f4-406c |
| 02:29:16.000 | worm | evidence | INTENT benefits-determination seq=0 chain=ae2c49e93d0b… | trace_id=6a98db6a241515fe01 session_id=aegis-pha-b-285c82 request_id=2c3bec1c-c3d0-42ef tenant=pha-b |
| 02:29:16.098 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6a98db6a241515fe01 span_id=b5d48eec6fcf8ae8 session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:16.098 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6a98db6a241515fe01 span_id=8bf4230e4b620d21 session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:16.099 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6a98db6a241515fe01 span_id=3624d6d85887b3c5 session_id=aegis-pha-b-285c82 |
| 02:29:16.099 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6a98db6a241515fe01 span_id=28142edc83c4bff9 session_id=aegis-pha-b-285c82 |
| 02:29:16.165 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaService | trace_id=6a98db6a241515fe01 span_id=31adbc21e7d328a3 |
| 02:29:16.172 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=771f4bc6d6277731 |
| 02:29:16.172 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=b01f4ec1627dfe1f |
| 02:29:16.177 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402556177,"body":{"isError":false,"lo | session_id=aegis-pha-b-285c82 trace_id=6a98db6a241515fe01 |
| 02:29:16.182 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402556182,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:29:16.217 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaService | trace_id=6a98db6a241515fe01 span_id=424c96c1cdc09cc5 |
| 02:29:16.225 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=10179e4fb6f57119 |
| 02:29:16.225 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=b9701626b335f481 |
| 02:29:16.228 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402556228,"body":{"isError":false,"lo | session_id=aegis-pha-b-285c82 trace_id=6a98db6a241515fe01 |
| 02:29:16.233 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402556233,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:29:16.268 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402556268,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:29:16.287 | runtime-span | lambda-segment | ben-mt4-core-tools/LambdaService | trace_id=6a98db6a241515fe01 span_id=2cfcfc34136c40a5 |
| 02:29:16.292 | runtime-span | lambda-segment | ben-mt4-core-tools/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=563d2981cc96f9c2 |
| 02:29:16.307 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402556307,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:29:16.323 | runtime-span | lambda-segment | ben-mt4-write-audit/LambdaService | trace_id=6a98db6a241515fe01 span_id=2446b169555e65b8 |
| 02:29:16.329 | runtime-span | lambda-segment | ben-mt4-write-audit/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=33dbd99809e76769 |
| 02:29:17.065 | lambda | call | write_audit -> stored=True | trace_id=6a98db6a241515fe01 session_id=aegis-pha-b-285c82 request_id=2c3bec1c-c3d0-42ef tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:17.065 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=e92533a11b963912 |
| 02:29:17.071 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402557071,"body":{"isError":false,"re | trace_id=6a98db6a241515fe01 |
| 02:29:17.071 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402557071,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:29:23.000 | bedrock-model-log | model-invocation | ConverseStream us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5626 out=86 masked_before_model=True | request_id=3e7020f1-eb51-4671 session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:23.483 | lambda | call | benefits_core -> ok | trace_id=6a98db6a241515fe01 session_id=aegis-pha-b-285c82 request_id=b1ec3c23-f1fd-4986 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:23.488 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=c0f0b4b62597b6d5 |
| 02:29:23.493 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402563493,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:29:23.493 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402563493,"body":{"isError":false,"re | trace_id=6a98db6a241515fe01 |
| 02:29:23.499 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6a98db6a241515fe01 span_id=6308db4248ab7a51 session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:23.500 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5626 out=86 | trace_id=6a98db6a241515fe01 span_id=3ea3cbe8fe83a28e session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:23.501 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5626 out=86 | trace_id=6a98db6a241515fe01 span_id=b2836e577a86b204 session_id=aegis-pha-b-285c82 request_id=3e7020f1-eb51-4671 |
| 02:29:26.000 | bedrock-model-log | model-invocation | ConverseStream us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5763 out=422 masked_before_model=True | request_id=c56e1d10-5539-4ec1 session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:26.689 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6a98db6a241515fe01 span_id=2e334221103cece2 session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:26.690 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6a98db6a241515fe01 span_id=7f44de5193880846 session_id=aegis-pha-b-285c82 |
| 02:29:26.793 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaService | trace_id=6a98db6a241515fe01 span_id=02f1a2a0bd89b7e7 |
| 02:29:26.799 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=188863077dca285e |
| 02:29:26.800 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=4cd3b5ba3775cc6e |
| 02:29:26.803 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402566803,"body":{"isError":false,"lo | session_id=aegis-pha-b-285c82 trace_id=6a98db6a241515fe01 |
| 02:29:26.807 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402566807,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:29:26.887 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402566887,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:29:26.911 | runtime-span | lambda-segment | ben-mt4-request-signoff/LambdaService | trace_id=6a98db6a241515fe01 span_id=39be3635087eeb17 |
| 02:29:26.918 | runtime-span | lambda-segment | ben-mt4-request-signoff/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=59faf91aa762933f |
| 02:29:26.919 | lambda | call | request_signoff -> requested=False | trace_id=6a98db6a241515fe01 session_id=aegis-pha-b-285c82 request_id=d7dfd939-25db-445e tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:26.919 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db6a241515fe01 span_id=55c54a67f5bb9a0b |
| 02:29:26.923 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402566923,"body":{"isError":false,"re | trace_id=6a98db6a241515fe01 |
| 02:29:26.923 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402566923,"body":{"isError":false,"lo | trace_id=6a98db6a241515fe01 |
| 02:29:26.928 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6a98db6a241515fe01 span_id=da519af3e08360e6 session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:26.930 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5763 out=422 | trace_id=6a98db6a241515fe01 span_id=ea7311ddae174bdb session_id=aegis-pha-b-285c82 tenant=pha-b case_id=OBS-PHAB-D8F93 |
| 02:29:26.931 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5763 out=422 | trace_id=6a98db6a241515fe01 span_id=ea2a1373038e5292 session_id=aegis-pha-b-285c82 request_id=c56e1d10-5539-4ec1 |
