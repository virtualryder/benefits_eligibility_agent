# Case trace — `OBS-PHAA-A02CF` (tenant `pha-a`)

| metric | value |
|---|---|
| agent_spans | 1 |
| gateway_requests | 33 |
| lambda_calls | 7 |
| lambda_calls_joined_to_evidence | 6 |
| masked_before_model_all | True |
| model_invocations | 6 |
| model_invocations_joined_to_spans | 6 |
| model_invocations_tagged_tenant | 6 |
| model_spans | 12 |
| sessions | ['aegis-pha-a-ecc419578e674a1e8eed1a07fce88122'] |
| single_tenant | True |
| tenants_seen | ['pha-a'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 02:28:16.636 | lambda | call | ingest_application -> ingested=True | trace_id=6a98db4040de182e30 request_id=a1fbf392-35bb-4ac1 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:17.055 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6a98db4066bb8a8d03 span_id=c6c04bb320da9171 session_id=aegis-pha-a-ecc419 |
| 02:28:17.729 | runtime-span | runtime-http | POST /invocations | trace_id=6a98db4066bb8a8d03 span_id=900ff04fbf5296c0 session_id=aegis-pha-a-ecc419 |
| 02:28:17.800 | runtime-span | span | SSM.GetParameter | trace_id=6a98db4066bb8a8d03 span_id=62967ea26b4d735e session_id=aegis-pha-a-ecc419 |
| 02:28:17.927 | runtime-span | span | mcp.session | trace_id=6a98db4066bb8a8d03 span_id=9408f7a7212061d9 session_id=aegis-pha-a-ecc419 |
| 02:28:18.000 | bedrock-model-log | model-invocation | ConverseStream us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=3520 out=99 masked_before_model=True | request_id=82eaa3c5-d277-4ec3 session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:18.061 | runtime-span | mcp-list | mcp tools/list | trace_id=6a98db4066bb8a8d03 span_id=53a3f557b3e01ecb session_id=aegis-pha-a-ecc419 |
| 02:28:18.324 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaService | trace_id=6a98db4066bb8a8d03 span_id=4360b92d1230a534 |
| 02:28:18.340 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=73742c939cafc79f |
| 02:28:18.340 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=e6dd323fdc0333d2 |
| 02:28:18.346 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402498346,"body":{"isError":false,"lo | session_id=aegis-pha-a-ecc419 trace_id=6a98db4066bb8a8d03 |
| 02:28:18.350 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402498350,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:18.464 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402498464,"body":{"isError":false,"re | trace_id=6a98db4066bb8a8d03 |
| 02:28:18.470 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=26899 out=1742 | trace_id=6a98db4066bb8a8d03 span_id=5f8d6cf4fbd8cc0a session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:18.471 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6a98db4066bb8a8d03 span_id=150ddce12867fc42 session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:18.472 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=3520 out=99 | trace_id=6a98db4066bb8a8d03 span_id=74bebf94816208fa session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:18.475 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=3520 out=99 | trace_id=6a98db4066bb8a8d03 span_id=ed2c5488dd61163d session_id=aegis-pha-a-ecc419 request_id=82eaa3c5-d277-4ec3 |
| 02:28:20.000 | bedrock-model-log | model-invocation | ConverseStream us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=3697 out=99 masked_before_model=True | request_id=c8f785da-4cd1-4446 session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:20.620 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6a98db4066bb8a8d03 span_id=61abf93070668250 session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:20.621 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6a98db4066bb8a8d03 span_id=d7109c07107c6eaf session_id=aegis-pha-a-ecc419 |
| 02:28:20.719 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaService | trace_id=6a98db4066bb8a8d03 span_id=52b5ed813f2be3e1 |
| 02:28:20.724 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=3b53171c9f47b460 |
| 02:28:20.724 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=f321c94371cfd44a |
| 02:28:20.728 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402500728,"body":{"isError":false,"lo | session_id=aegis-pha-a-ecc419 trace_id=6a98db4066bb8a8d03 |
| 02:28:20.732 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402500732,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:20.802 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402500802,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:20.826 | runtime-span | lambda-segment | ben-mt4-intake-application/LambdaService | trace_id=6a98db4066bb8a8d03 span_id=754e980124ac2980 |
| 02:28:20.831 | runtime-span | lambda-segment | ben-mt4-intake-application/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=94a0becc730cd9d2 |
| 02:28:20.975 | lambda | call | intake_application -> ok | trace_id=6a98db4066bb8a8d03 session_id=aegis-pha-a-ecc419 request_id=85f09bf8-def1-4a16 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:20.982 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=fd27141bfe725de2 |
| 02:28:20.986 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402500986,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:20.986 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402500986,"body":{"isError":false,"re | trace_id=6a98db4066bb8a8d03 |
| 02:28:20.991 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6a98db4066bb8a8d03 span_id=ae9b34de969c8263 session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:20.992 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=3697 out=99 | trace_id=6a98db4066bb8a8d03 span_id=459a80e4874427fd session_id=aegis-pha-a-ecc419 request_id=c8f785da-4cd1-4446 |
| 02:28:20.992 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=3697 out=99 | trace_id=6a98db4066bb8a8d03 span_id=3c0403faf032df72 session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:24.345 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6a98db4066bb8a8d03 span_id=4dfa7706ac28268d session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:24.345 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6a98db4066bb8a8d03 span_id=cf1a19ae8dac647b session_id=aegis-pha-a-ecc419 |
| 02:28:24.444 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaService | trace_id=6a98db4066bb8a8d03 span_id=49803d17911e1d75 |
| 02:28:24.449 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=eced0d30c974eda4 |
| 02:28:24.449 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=9a4355934dbb31d4 |
| 02:28:24.454 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402504454,"body":{"isError":false,"lo | session_id=aegis-pha-a-ecc419 trace_id=6a98db4066bb8a8d03 |
| 02:28:24.458 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402504458,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:24.532 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402504532,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:24.562 | runtime-span | lambda-segment | ben-mt4-mask-pii/LambdaService | trace_id=6a98db4066bb8a8d03 span_id=5757c72d73e4d91c |
| 02:28:24.569 | runtime-span | lambda-segment | ben-mt4-mask-pii/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=cb3f5e38ac85bfaa |
| 02:28:25.000 | bedrock-model-log | model-invocation | ConverseStream us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=4083 out=379 masked_before_model=True | request_id=780a4692-0f6a-43c5 session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:25.031 | lambda | call | mask_pii -> deidentified=True | trace_id=6a98db4066bb8a8d03 session_id=aegis-pha-a-ecc419 request_id=b195bc5b-cd43-4c06 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:25.032 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=0f9acc905c6c0316 |
| 02:28:25.037 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402505037,"body":{"isError":false,"re | trace_id=6a98db4066bb8a8d03 |
| 02:28:25.037 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402505037,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:25.042 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6a98db4066bb8a8d03 span_id=3a6a57609678684c session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:25.043 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=4083 out=379 | trace_id=6a98db4066bb8a8d03 span_id=1db1f2517ab515ac session_id=aegis-pha-a-ecc419 request_id=780a4692-0f6a-43c5 |
| 02:28:25.043 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=4083 out=379 | trace_id=6a98db4066bb8a8d03 span_id=86364e7755cfb56d session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:29.000 | bedrock-model-log | model-invocation | ConverseStream us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=4667 out=312 masked_before_model=True | request_id=533b4f28-c989-4b1d session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:29.342 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6a98db4066bb8a8d03 span_id=42a15a12c544e074 session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:29.343 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6a98db4066bb8a8d03 span_id=3843ebc915967428 session_id=aegis-pha-a-ecc419 |
| 02:28:29.453 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaService | trace_id=6a98db4066bb8a8d03 span_id=0178c2f9408fdb41 |
| 02:28:29.459 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=def8a2c340d9885e |
| 02:28:29.460 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=541042cc558c82ed |
| 02:28:29.464 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402509464,"body":{"isError":false,"lo | session_id=aegis-pha-a-ecc419 trace_id=6a98db4066bb8a8d03 |
| 02:28:29.469 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402509469,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:29.538 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402509538,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:29.571 | runtime-span | lambda-segment | ben-mt4-assess-eligibility/LambdaService | trace_id=6a98db4066bb8a8d03 span_id=56749bb712676e8b |
| 02:28:29.577 | lambda | call | assess_eligibility -> ok | trace_id=6a98db4066bb8a8d03 session_id=aegis-pha-a-ecc419 request_id=17d5f272-cf19-4f58 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:29.577 | runtime-span | lambda-segment | ben-mt4-assess-eligibility/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=b2ff0b00fc3e80d4 |
| 02:28:29.577 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=ef905c5a4c0961a3 |
| 02:28:29.582 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402509582,"body":{"isError":false,"re | trace_id=6a98db4066bb8a8d03 |
| 02:28:29.582 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402509582,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:29.588 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=4667 out=312 | trace_id=6a98db4066bb8a8d03 span_id=f57be439d2b5ecba session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:29.588 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6a98db4066bb8a8d03 span_id=3ba06fc396b4a0ef session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:29.589 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=4667 out=312 | trace_id=6a98db4066bb8a8d03 span_id=a0fa8adc057fe525 session_id=aegis-pha-a-ecc419 request_id=533b4f28-c989-4b1d |
| 02:28:34.789 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6a98db4066bb8a8d03 span_id=504e1e9385348148 session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:34.790 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6a98db4066bb8a8d03 span_id=9d745671119c230d session_id=aegis-pha-a-ecc419 |
| 02:28:34.913 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaService | trace_id=6a98db4066bb8a8d03 span_id=78feabebcee96c4e |
| 02:28:34.918 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=27f911bbd7d393db |
| 02:28:34.919 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=1b3b9386d5921270 |
| 02:28:34.921 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402514921,"body":{"isError":false,"lo | session_id=aegis-pha-a-ecc419 trace_id=6a98db4066bb8a8d03 |
| 02:28:34.926 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402514926,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:34.993 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402514993,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:35.023 | runtime-span | lambda-segment | ben-mt4-core-tools/LambdaService | trace_id=6a98db4066bb8a8d03 span_id=63cb02d41a040ac8 |
| 02:28:35.029 | runtime-span | lambda-segment | ben-mt4-core-tools/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=2df65547d40997c1 |
| 02:28:42.000 | bedrock-model-log | model-invocation | ConverseStream us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5064 out=422 masked_before_model=True | request_id=391402d9-b7c2-480d session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:42.942 | lambda | call | benefits_core -> ok | trace_id=6a98db4066bb8a8d03 session_id=aegis-pha-a-ecc419 request_id=83614e31-4b21-4c9a tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:42.944 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=a854da45c6b235e7 |
| 02:28:42.948 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402522948,"body":{"isError":false,"re | trace_id=6a98db4066bb8a8d03 |
| 02:28:42.949 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402522949,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:42.954 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6a98db4066bb8a8d03 span_id=c890665618bf118b session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:42.955 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5064 out=422 | trace_id=6a98db4066bb8a8d03 span_id=6896cb680ff650b3 session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:42.956 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5064 out=422 | trace_id=6a98db4066bb8a8d03 span_id=760ae9ef5191bb14 session_id=aegis-pha-a-ecc419 request_id=391402d9-b7c2-480d |
| 02:28:47.000 | worm | evidence | INTENT benefits-determination seq=0 chain=be52dd870550… | trace_id=6a98db4066bb8a8d03 session_id=aegis-pha-a-ecc419 request_id=d1e18c4d-79bf-413e tenant=pha-a |
| 02:28:47.510 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6a98db4066bb8a8d03 span_id=6d89027a5f0e535e session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:47.510 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6a98db4066bb8a8d03 span_id=3aeb63b9c7376c4a session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:47.511 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6a98db4066bb8a8d03 span_id=52fd451e0b3a8013 session_id=aegis-pha-a-ecc419 |
| 02:28:47.511 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6a98db4066bb8a8d03 span_id=af3cd3e75d6139fa session_id=aegis-pha-a-ecc419 |
| 02:28:47.612 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaService | trace_id=6a98db4066bb8a8d03 span_id=6245ee56f4d98e3c |
| 02:28:47.619 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=f6285dad6e087807 |
| 02:28:47.620 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=6c4a48369134fe74 |
| 02:28:47.623 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402527623,"body":{"isError":false,"lo | session_id=aegis-pha-a-ecc419 trace_id=6a98db4066bb8a8d03 |
| 02:28:47.628 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402527628,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:47.647 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaService | trace_id=6a98db4066bb8a8d03 span_id=73ecc2c1f23e41b3 |
| 02:28:47.653 | runtime-span | lambda-segment | ben-mt4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=d139668df410512a |
| 02:28:47.654 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=b64ef76fe9debf5d |
| 02:28:47.657 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402527657,"body":{"isError":false,"lo | session_id=aegis-pha-a-ecc419 trace_id=6a98db4066bb8a8d03 |
| 02:28:47.660 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402527660,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:47.725 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402527725,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:47.726 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402527726,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:47.756 | runtime-span | lambda-segment | ben-mt4-write-audit/LambdaService | trace_id=6a98db4066bb8a8d03 span_id=3cd84cfa638a1331 |
| 02:28:47.757 | runtime-span | lambda-segment | ben-mt4-request-signoff/LambdaService | trace_id=6a98db4066bb8a8d03 span_id=15561dbc28fcd7ba |
| 02:28:47.761 | runtime-span | lambda-segment | ben-mt4-write-audit/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=e2b64813b7f76a7b |
| 02:28:48.111 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=7d0624e43f994b14 |
| 02:28:48.243 | lambda | call | write_audit -> stored=True | trace_id=6a98db4066bb8a8d03 session_id=aegis-pha-a-ecc419 request_id=d1e18c4d-79bf-413e tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:48.244 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=c523098b3421f67f |
| 02:28:48.248 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402528248,"body":{"isError":false,"re | trace_id=6a98db4066bb8a8d03 |
| 02:28:48.249 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402528249,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:48.479 | runtime-span | lambda-segment | ben-mt4-request-signoff/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=26c36849546d91a5 |
| 02:28:49.000 | bedrock-model-log | model-invocation | ConverseStream us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5868 out=431 masked_before_model=True | request_id=0226deb3-1912-46af session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:49.571 | lambda | call | request_signoff -> requested=False | trace_id=6a98db4066bb8a8d03 session_id=aegis-pha-a-ecc419 request_id=273a4238-64f0-41ba tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:49.572 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6a98db4066bb8a8d03 span_id=f0009d4fc28c94ef |
| 02:28:49.576 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402529576,"body":{"isError":false,"lo | trace_id=6a98db4066bb8a8d03 |
| 02:28:49.576 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-mt4-ben-gw-poykyej365","event_timestamp":1788402529576,"body":{"isError":false,"re | trace_id=6a98db4066bb8a8d03 |
| 02:28:49.582 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6a98db4066bb8a8d03 span_id=0a7af9e01724215e session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:49.583 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5868 out=431 | trace_id=6a98db4066bb8a8d03 span_id=19c27a4ea03dfb4c session_id=aegis-pha-a-ecc419 tenant=pha-a case_id=OBS-PHAA-A02CF |
| 02:28:49.584 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5868 out=431 | trace_id=6a98db4066bb8a8d03 span_id=f784b09a88bd8a30 session_id=aegis-pha-a-ecc419 request_id=0226deb3-1912-46af |
