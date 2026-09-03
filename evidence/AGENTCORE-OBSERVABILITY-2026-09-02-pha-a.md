# Case trace — `OBS-PHAA-3CE46` (tenant `pha-a`)

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
| sessions | ['aegis-pha-a-bbc06cfdbc0f4eb29f63359870578efd'] |
| single_tenant | True |
| tenants_seen | ['pha-a'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 01:28:19.237 | lambda | call | ingest_application -> ingested=True | trace_id=6a98cd2f39a744276f request_id=06588e01-a3f1-475e tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:19.678 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6a98cd333312032c1c span_id=9b61e54ecef095f4 session_id=aegis-pha-a-bbc06c |
| 01:28:20.524 | runtime-span | runtime-http | POST /invocations | trace_id=6a98cd333312032c1c span_id=011958975f40f2aa session_id=aegis-pha-a-bbc06c |
| 01:28:20.602 | runtime-span | span | SSM.GetParameter | trace_id=6a98cd333312032c1c span_id=952488dc4ffe6f2f session_id=aegis-pha-a-bbc06c |
| 01:28:20.739 | runtime-span | span | mcp.session | trace_id=6a98cd333312032c1c span_id=de25238eb1583a46 session_id=aegis-pha-a-bbc06c |
| 01:28:20.891 | runtime-span | mcp-list | mcp tools/list | trace_id=6a98cd333312032c1c span_id=80d2ef42ca4fd9d0 session_id=aegis-pha-a-bbc06c |
| 01:28:21.000 | bedrock-model-log | model-invocation | ConverseStream us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=3519 out=97 masked_before_model=True | request_id=9530365b-958d-49c0 session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:21.109 | runtime-span | lambda-segment | ben-mt3-tenant-interceptor/LambdaService | trace_id=6a98cd333312032c1c span_id=57007742eda64774 |
| 01:28:21.121 | runtime-span | lambda-segment | ben-mt3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=4f18df7f01f9f010 |
| 01:28:21.121 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=c1639948d88ccf9d |
| 01:28:21.125 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398901125,"body":{"isError":false,"lo | session_id=aegis-pha-a-bbc06c trace_id=6a98cd333312032c1c |
| 01:28:21.130 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398901130,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:28:21.243 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398901243,"body":{"isError":false,"re | trace_id=6a98cd333312032c1c |
| 01:28:21.250 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6a98cd333312032c1c span_id=92bf2db273024dda session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:21.250 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=32490 out=1711 | trace_id=6a98cd333312032c1c span_id=72235c311b730e3f session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:21.251 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=3519 out=97 | trace_id=6a98cd333312032c1c span_id=85c6ffa835efdba0 session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:21.254 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=3519 out=97 | trace_id=6a98cd333312032c1c span_id=06889a412aefc87f session_id=aegis-pha-a-bbc06c request_id=9530365b-958d-49c0 |
| 01:28:24.554 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6a98cd333312032c1c span_id=3190bbbb1baaf9d8 session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:24.555 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6a98cd333312032c1c span_id=a93e636b4ccb95b1 session_id=aegis-pha-a-bbc06c |
| 01:28:24.664 | runtime-span | lambda-segment | ben-mt3-tenant-interceptor/LambdaService | trace_id=6a98cd333312032c1c span_id=0b20a67d53fff1e8 |
| 01:28:24.670 | runtime-span | lambda-segment | ben-mt3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=9dc133a3e36f9b81 |
| 01:28:24.672 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=55266d16fe385e87 |
| 01:28:24.675 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398904675,"body":{"isError":false,"lo | session_id=aegis-pha-a-bbc06c trace_id=6a98cd333312032c1c |
| 01:28:24.679 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398904679,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:28:24.770 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398904770,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:28:24.803 | runtime-span | lambda-segment | ben-mt3-intake-application/LambdaService | trace_id=6a98cd333312032c1c span_id=1886970f913d7861 |
| 01:28:24.914 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=799c7aeec337f288 |
| 01:28:25.006 | runtime-span | lambda-segment | ben-mt3-intake-application/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=b84d6b8451bff258 |
| 01:28:28.000 | bedrock-model-log | model-invocation | ConverseStream us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=3694 out=97 masked_before_model=True | request_id=40909599-e034-4baa session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:28.095 | lambda | call | intake_application -> ok | trace_id=6a98cd333312032c1c session_id=aegis-pha-a-bbc06c request_id=5f848b47-341f-46a2 tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:28.100 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=7652c2b454e46dd7 |
| 01:28:28.104 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398908104,"body":{"isError":false,"re | trace_id=6a98cd333312032c1c |
| 01:28:28.105 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398908105,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:28:28.109 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6a98cd333312032c1c span_id=e5eaa9b7198eaff5 session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:28.110 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=3694 out=97 | trace_id=6a98cd333312032c1c span_id=6fcce38a579a4d18 session_id=aegis-pha-a-bbc06c request_id=40909599-e034-4baa |
| 01:28:28.110 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=3694 out=97 | trace_id=6a98cd333312032c1c span_id=0e21f77df8fbbca9 session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:30.682 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6a98cd333312032c1c span_id=9017b97221f748a8 session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:30.683 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6a98cd333312032c1c span_id=288c5ed6990faf1d session_id=aegis-pha-a-bbc06c |
| 01:28:30.785 | runtime-span | lambda-segment | ben-mt3-tenant-interceptor/LambdaService | trace_id=6a98cd333312032c1c span_id=70ea2c2d18584f23 |
| 01:28:30.791 | runtime-span | lambda-segment | ben-mt3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=c75585aff88755ac |
| 01:28:30.792 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=fbbc877829de4547 |
| 01:28:30.795 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398910795,"body":{"isError":false,"lo | session_id=aegis-pha-a-bbc06c trace_id=6a98cd333312032c1c |
| 01:28:30.801 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398910801,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:28:30.889 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398910889,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:28:30.918 | runtime-span | lambda-segment | ben-mt3-mask-pii/LambdaService | trace_id=6a98cd333312032c1c span_id=576e5d1e34513140 |
| 01:28:31.047 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=64b4aeef04fb7186 |
| 01:28:31.389 | runtime-span | lambda-segment | ben-mt3-mask-pii/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=19a147ebaab0c7aa |
| 01:28:33.000 | bedrock-model-log | model-invocation | ConverseStream us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=4068 out=369 masked_before_model=True | request_id=78164790-8208-4fc6 session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:33.345 | lambda | call | mask_pii -> deidentified=True | trace_id=6a98cd333312032c1c session_id=aegis-pha-a-bbc06c request_id=eb781f90-0566-4fb8 tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:33.347 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=5c714a5e0d2bb88c |
| 01:28:33.351 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398913351,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:28:33.351 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398913351,"body":{"isError":false,"re | trace_id=6a98cd333312032c1c |
| 01:28:33.356 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6a98cd333312032c1c span_id=077fa3acbe032952 session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:33.357 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=4068 out=369 | trace_id=6a98cd333312032c1c span_id=8e003571c41e3463 session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:33.357 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=4068 out=369 | trace_id=6a98cd333312032c1c span_id=91f6ff459d219378 session_id=aegis-pha-a-bbc06c request_id=78164790-8208-4fc6 |
| 01:28:37.383 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6a98cd333312032c1c span_id=14139ca7777c8c0f session_id=aegis-pha-a-bbc06c |
| 01:28:37.383 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6a98cd333312032c1c span_id=e0f0ca8a105109ac session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:37.532 | runtime-span | lambda-segment | ben-mt3-tenant-interceptor/LambdaService | trace_id=6a98cd333312032c1c span_id=76ba1a19b0507981 |
| 01:28:37.537 | runtime-span | lambda-segment | ben-mt3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=10ec1d61d309c97a |
| 01:28:37.537 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=4c76e109873e94f4 |
| 01:28:37.541 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398917541,"body":{"isError":false,"lo | session_id=aegis-pha-a-bbc06c trace_id=6a98cd333312032c1c |
| 01:28:37.546 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398917546,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:28:37.632 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398917632,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:28:37.663 | runtime-span | lambda-segment | ben-mt3-assess-eligibility/LambdaService | trace_id=6a98cd333312032c1c span_id=7799b79ac5ac9ff9 |
| 01:28:37.796 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=7534b09f455be9b5 |
| 01:28:37.920 | runtime-span | lambda-segment | ben-mt3-assess-eligibility/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=900b8cb5ba867537 |
| 01:28:40.000 | bedrock-model-log | model-invocation | ConverseStream us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=4642 out=302 masked_before_model=True | request_id=a4b93159-c5f8-4a5d session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:40.936 | lambda | call | assess_eligibility -> ok | trace_id=6a98cd333312032c1c session_id=aegis-pha-a-bbc06c request_id=f830ba87-5dad-4f3b tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:40.936 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=b521081007d94493 |
| 01:28:40.942 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398920942,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:28:40.942 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398920942,"body":{"isError":false,"re | trace_id=6a98cd333312032c1c |
| 01:28:40.947 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=4642 out=302 | trace_id=6a98cd333312032c1c span_id=4fdaec35304834b9 session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:40.947 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6a98cd333312032c1c span_id=3af0af8d3b39f4a1 session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:40.948 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=4642 out=302 | trace_id=6a98cd333312032c1c span_id=b9ee1122ae18bfa9 session_id=aegis-pha-a-bbc06c request_id=a4b93159-c5f8-4a5d |
| 01:28:44.628 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6a98cd333312032c1c span_id=c6b5f20516782912 session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:44.629 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6a98cd333312032c1c span_id=9cdd463a1c1e1500 session_id=aegis-pha-a-bbc06c |
| 01:28:44.753 | runtime-span | lambda-segment | ben-mt3-tenant-interceptor/LambdaService | trace_id=6a98cd333312032c1c span_id=668987159e4d4740 |
| 01:28:44.759 | runtime-span | lambda-segment | ben-mt3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=dfc0d04a072846e3 |
| 01:28:44.760 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=e34672f65cf21a98 |
| 01:28:44.763 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398924763,"body":{"isError":false,"lo | session_id=aegis-pha-a-bbc06c trace_id=6a98cd333312032c1c |
| 01:28:44.767 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398924767,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:28:44.854 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398924854,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:28:44.875 | runtime-span | lambda-segment | ben-mt3-core-tools/LambdaService | trace_id=6a98cd333312032c1c span_id=3ee6ead92a1ea580 |
| 01:28:45.000 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=51c0f3ef15f48452 |
| 01:28:45.337 | runtime-span | lambda-segment | ben-mt3-core-tools/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=0594a937e695d842 |
| 01:28:54.000 | bedrock-model-log | model-invocation | ConverseStream us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5031 out=380 masked_before_model=True | request_id=ad4c09e8-fa48-49b8 session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:54.807 | lambda | call | benefits_core -> ok | trace_id=6a98cd333312032c1c session_id=aegis-pha-a-bbc06c request_id=dd43d65b-cd2f-4eed tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:54.808 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=f607a78b78cd74f8 |
| 01:28:54.814 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398934814,"body":{"isError":false,"re | trace_id=6a98cd333312032c1c |
| 01:28:54.814 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398934814,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:28:54.819 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6a98cd333312032c1c span_id=a3754e5faf16ab7a session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:54.820 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5031 out=380 | trace_id=6a98cd333312032c1c span_id=339ea2a379946489 session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:54.821 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5031 out=380 | trace_id=6a98cd333312032c1c span_id=c133e95e6659c2c2 session_id=aegis-pha-a-bbc06c request_id=ad4c09e8-fa48-49b8 |
| 01:28:59.661 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6a98cd333312032c1c span_id=618cc36f03a45544 session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:28:59.662 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6a98cd333312032c1c span_id=b3a4a2755ffb37ab session_id=aegis-pha-a-bbc06c |
| 01:28:59.729 | runtime-span | lambda-segment | ben-mt3-tenant-interceptor/LambdaService | trace_id=6a98cd333312032c1c span_id=7d85e879a9f7d3c3 |
| 01:28:59.733 | runtime-span | lambda-segment | ben-mt3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=dd8b39d4c63a9b93 |
| 01:28:59.734 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=f1222eca0ad880a0 |
| 01:28:59.741 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398939741,"body":{"isError":false,"lo | session_id=aegis-pha-a-bbc06c trace_id=6a98cd333312032c1c |
| 01:28:59.745 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398939745,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:28:59.820 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398939820,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:28:59.848 | runtime-span | lambda-segment | ben-mt3-write-audit/LambdaService | trace_id=6a98cd333312032c1c span_id=240837d2966152c1 |
| 01:29:00.023 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=5cc997af3f1023cc |
| 01:29:00.127 | runtime-span | lambda-segment | ben-mt3-write-audit/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=5f9eb17cd9cafca1 |
| 01:29:04.000 | bedrock-model-log | model-invocation | ConverseStream us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5694 out=97 masked_before_model=True | request_id=3b12628c-b7b4-43dd session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:29:04.000 | worm | evidence | INTENT benefits-determination seq=0 chain=2531584bbbe8… | trace_id=6a98cd333312032c1c session_id=aegis-pha-a-bbc06c request_id=c583d21c-a0ca-48b9 tenant=pha-a |
| 01:29:04.291 | lambda | call | write_audit -> stored=True | trace_id=6a98cd333312032c1c session_id=aegis-pha-a-bbc06c request_id=c583d21c-a0ca-48b9 tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:29:04.312 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=f8104749e58df69c |
| 01:29:04.319 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398944319,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:29:04.319 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398944319,"body":{"isError":false,"re | trace_id=6a98cd333312032c1c |
| 01:29:04.325 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6a98cd333312032c1c span_id=610651e1f8de79ff session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:29:04.326 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5694 out=97 | trace_id=6a98cd333312032c1c span_id=7c547c45d3e6caa8 session_id=aegis-pha-a-bbc06c request_id=3b12628c-b7b4-43dd |
| 01:29:04.326 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5694 out=97 | trace_id=6a98cd333312032c1c span_id=5c02843d22c9c7c6 session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:29:07.801 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6a98cd333312032c1c span_id=46e36f9ec9f0e5ce session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:29:07.802 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6a98cd333312032c1c span_id=5c14141ab88bae3a session_id=aegis-pha-a-bbc06c |
| 01:29:07.895 | runtime-span | lambda-segment | ben-mt3-tenant-interceptor/LambdaService | trace_id=6a98cd333312032c1c span_id=63904370b329cb6b |
| 01:29:07.904 | runtime-span | lambda-segment | ben-mt3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=85e7a084ab94d979 |
| 01:29:07.905 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=2135e731690b09de |
| 01:29:07.909 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398947909,"body":{"isError":false,"lo | session_id=aegis-pha-a-bbc06c trace_id=6a98cd333312032c1c |
| 01:29:07.911 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398947911,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:29:08.011 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398948011,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:29:08.035 | runtime-span | lambda-segment | ben-mt3-request-signoff/LambdaService | trace_id=6a98cd333312032c1c span_id=21f6f3d45e4cf058 |
| 01:29:08.216 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=eb6d063542d2d844 |
| 01:29:08.522 | runtime-span | lambda-segment | ben-mt3-request-signoff/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=aa94e66da20a9691 |
| 01:29:09.000 | bedrock-model-log | model-invocation | ConverseStream us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5842 out=369 masked_before_model=True | request_id=6e2fa7cb-04f2-44bd session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:29:09.604 | lambda | call | request_signoff -> requested=False | trace_id=6a98cd333312032c1c session_id=aegis-pha-a-bbc06c request_id=5169c38e-e1ad-4809 tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:29:09.604 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98cd333312032c1c span_id=c06869c4734da029 |
| 01:29:09.608 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398949608,"body":{"isError":false,"lo | trace_id=6a98cd333312032c1c |
| 01:29:09.608 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt3-ben-gw-yh5cl39ot7","event_timestamp":1788398949608,"body":{"isError":false,"re | trace_id=6a98cd333312032c1c |
| 01:29:09.613 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6a98cd333312032c1c span_id=0ef482d933325e04 session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:29:09.614 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5842 out=369 | trace_id=6a98cd333312032c1c span_id=24fa464ce407f776 session_id=aegis-pha-a-bbc06c tenant=pha-a case_id=OBS-PHAA-3CE46 |
| 01:29:09.615 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5842 out=369 | trace_id=6a98cd333312032c1c span_id=6b0f07ca18d9dc53 session_id=aegis-pha-a-bbc06c request_id=6e2fa7cb-04f2-44bd |
