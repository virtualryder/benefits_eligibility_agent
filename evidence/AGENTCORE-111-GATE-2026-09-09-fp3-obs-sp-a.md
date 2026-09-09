# Case trace — `OBS-SPA-6752F` (tenant `sp-a`)

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
| sessions | ['aegis-sp-a-5fe496b21f114394b77a69f055c09dc7'] |
| single_tenant | True |
| tenants_seen | ['sp-a'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 18:28:33.192 | lambda | call | ingest_application -> ingested=True | trace_id=6aa1a5506be1eeb074 request_id=4f89d221-eacc-4866 tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:33.661 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa1a5511d9cfffc5c span_id=664174a42bc7edcd session_id=aegis-sp-a-5fe496b |
| 18:28:34.174 | runtime-span | runtime-http | POST /invocations | trace_id=6aa1a5511d9cfffc5c span_id=ca26afef7782fcf4 session_id=aegis-sp-a-5fe496b |
| 18:28:34.244 | runtime-span | span | SSM.GetParameter | trace_id=6aa1a5511d9cfffc5c span_id=09437931d8b451bb session_id=aegis-sp-a-5fe496b |
| 18:28:34.286 | runtime-span | span | SSM.GetParameter | trace_id=6aa1a5511d9cfffc5c span_id=53c2de9f2fd66ebc session_id=aegis-sp-a-5fe496b |
| 18:28:34.347 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa1a5511d9cfffc5c span_id=ecf5bbb1f038cc1b session_id=aegis-sp-a-5fe496b |
| 18:28:34.409 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa1a5511d9cfffc5c span_id=3b65ce3873b31710 session_id=aegis-sp-a-5fe496b |
| 18:28:34.484 | runtime-span | span | mcp.session | trace_id=6aa1a5511d9cfffc5c span_id=b3525cdf8765ea23 session_id=aegis-sp-a-5fe496b |
| 18:28:34.626 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa1a5511d9cfffc5c span_id=992dcafd6ec0e1da session_id=aegis-sp-a-5fe496b |
| 18:28:34.878 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaService | trace_id=6aa1a5511d9cfffc5c span_id=2bdc2a45bfcfe269 |
| 18:28:34.882 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=95382cf79e2efc60 |
| 18:28:34.903 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=1e732a6b4438f47b |
| 18:28:34.906 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978514906,"body":{"isError":false,"lo | session_id=aegis-sp-a-5fe496b trace_id=6aa1a5511d9cfffc5c |
| 18:28:34.909 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978514909,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:28:35.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5340 out=214 masked_before_model=True | request_id=8842d500-7656-4274 session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:35.009 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978515009,"body":{"isError":false,"re | trace_id=6aa1a5511d9cfffc5c |
| 18:28:35.017 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=33204 out=2084 | trace_id=6aa1a5511d9cfffc5c span_id=c02ff81dcd4ce7c8 session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:35.018 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1a5511d9cfffc5c span_id=e453b85d72c234d2 session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:35.019 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5340 out=214 | trace_id=6aa1a5511d9cfffc5c span_id=a4f85411f8ce115f session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:35.021 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5340 out=214 | trace_id=6aa1a5511d9cfffc5c span_id=966a51f49debfba7 session_id=aegis-sp-a-5fe496b request_id=8842d500-7656-4274 |
| 18:28:35.022 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a5511d9cfffc5c span_id=595a79596744c4d7 session_id=aegis-sp-a-5fe496b |
| 18:28:39.742 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a5511d9cfffc5c span_id=2aac7cded48eb67e session_id=aegis-sp-a-5fe496b |
| 18:28:39.756 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1a5511d9cfffc5c span_id=8db6354962da8fd4 session_id=aegis-sp-a-5fe496b |
| 18:28:39.786 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa1a5511d9cfffc5c span_id=dd9e5f27585af8c2 session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:39.786 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa1a5511d9cfffc5c span_id=0035e7c084e5bba4 session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:39.787 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa1a5511d9cfffc5c span_id=75b6d10fcdc36aae session_id=aegis-sp-a-5fe496b |
| 18:28:39.788 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa1a5511d9cfffc5c span_id=6260ecd348539ef9 session_id=aegis-sp-a-5fe496b |
| 18:28:39.885 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaService | trace_id=6aa1a5511d9cfffc5c span_id=4ef3e1f28a4d24d1 |
| 18:28:39.890 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=0f6b8e5fe686fcd9 |
| 18:28:39.908 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaService | trace_id=6aa1a5511d9cfffc5c span_id=49c87186b31d4a03 |
| 18:28:40.245 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=f3e6468eac12e4b6 |
| 18:28:40.260 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=c5ea027a4fd4d6d3 |
| 18:28:40.263 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978520263,"body":{"isError":false,"lo | session_id=aegis-sp-a-5fe496b trace_id=6aa1a5511d9cfffc5c |
| 18:28:40.267 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978520267,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:28:40.360 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=12f3787c31d4233a |
| 18:28:40.368 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978520368,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:28:40.392 | runtime-span | lambda-segment | ben-fp3-intake-application/LambdaService | trace_id=6aa1a5511d9cfffc5c span_id=16dde35ad2ef277c |
| 18:28:40.398 | runtime-span | lambda-segment | ben-fp3-intake-application/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=0cb32751d7c9b9ac |
| 18:28:40.568 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=a781de2240a3fafd |
| 18:28:40.569 | lambda | call | intake_application -> ok | trace_id=6aa1a5511d9cfffc5c session_id=aegis-sp-a-5fe496b request_id=f109c78e-b8b9-4ae2 tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:40.576 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978520576,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:28:40.576 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978520576,"body":{"isError":false,"re | trace_id=6aa1a5511d9cfffc5c |
| 18:28:44.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5984 out=397 masked_before_model=True | request_id=8b9d072d-2142-4bad session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:44.048 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=0554462d19390238 |
| 18:28:44.052 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978524052,"body":{"isError":false,"lo | session_id=aegis-sp-a-5fe496b trace_id=6aa1a5511d9cfffc5c |
| 18:28:44.056 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978524056,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:28:44.135 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978524135,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:28:44.165 | runtime-span | lambda-segment | ben-fp3-mask-pii/LambdaService | trace_id=6aa1a5511d9cfffc5c span_id=63fa128212771c01 |
| 18:28:44.175 | runtime-span | lambda-segment | ben-fp3-mask-pii/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=87ad38beec2ebdf6 |
| 18:28:44.658 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa1a5511d9cfffc5c session_id=aegis-sp-a-5fe496b request_id=076a9b18-61c2-4625 tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:44.659 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=ed9d9828e928544d |
| 18:28:44.663 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978524663,"body":{"isError":false,"re | trace_id=6aa1a5511d9cfffc5c |
| 18:28:44.663 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978524663,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:28:44.669 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5984 out=397 | trace_id=6aa1a5511d9cfffc5c span_id=ab7afe2532f5ea74 session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:44.669 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1a5511d9cfffc5c span_id=ba13f5bb5cc18ca1 session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:44.670 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a5511d9cfffc5c span_id=6fc0c833c8efb544 session_id=aegis-sp-a-5fe496b |
| 18:28:44.670 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5984 out=397 | trace_id=6aa1a5511d9cfffc5c span_id=7737d8313816386e session_id=aegis-sp-a-5fe496b request_id=8b9d072d-2142-4bad |
| 18:28:49.886 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a5511d9cfffc5c span_id=669adbc01aa3a0da session_id=aegis-sp-a-5fe496b |
| 18:28:49.894 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1a5511d9cfffc5c span_id=27e36fc835517dde session_id=aegis-sp-a-5fe496b |
| 18:28:49.932 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa1a5511d9cfffc5c span_id=4458f2406be10949 session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:49.933 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa1a5511d9cfffc5c span_id=20fa9b43d91cadee session_id=aegis-sp-a-5fe496b |
| 18:28:50.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6612 out=565 masked_before_model=True | request_id=e37204a9-1bf9-47de session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:50.036 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaService | trace_id=6aa1a5511d9cfffc5c span_id=18289c3c33540351 |
| 18:28:50.042 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=491b1c6c4f0cef1b |
| 18:28:50.191 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=933b081cbac971bb |
| 18:28:50.195 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978530195,"body":{"isError":false,"lo | session_id=aegis-sp-a-5fe496b trace_id=6aa1a5511d9cfffc5c |
| 18:28:50.199 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978530199,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:28:50.271 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978530271,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:28:50.296 | runtime-span | lambda-segment | ben-fp3-assess-eligibility/LambdaService | trace_id=6aa1a5511d9cfffc5c span_id=3f5bcbf71c96ecf8 |
| 18:28:50.301 | runtime-span | lambda-segment | ben-fp3-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=56f80428f94d533d |
| 18:28:50.325 | lambda | call | assess_eligibility -> ok | trace_id=6aa1a5511d9cfffc5c session_id=aegis-sp-a-5fe496b request_id=71e2be74-b5b0-41e0 tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:50.326 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=aac5ed1de5957a25 |
| 18:28:50.329 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978530329,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:28:50.329 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978530329,"body":{"isError":false,"re | trace_id=6aa1a5511d9cfffc5c |
| 18:28:50.335 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1a5511d9cfffc5c span_id=593eb28487581be1 session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:50.336 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6612 out=565 | trace_id=6aa1a5511d9cfffc5c span_id=8cc3bd4ec6a1a78a session_id=aegis-sp-a-5fe496b request_id=e37204a9-1bf9-47de |
| 18:28:50.336 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6612 out=565 | trace_id=6aa1a5511d9cfffc5c span_id=fea1af05b724684a session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:50.342 | runtime-span | span | SSM.GetParameter | trace_id=6aa1a5511d9cfffc5c span_id=f0c62ecd4100d701 session_id=aegis-sp-a-5fe496b |
| 18:28:50.379 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a5511d9cfffc5c span_id=3be37f2e2e48fa3f session_id=aegis-sp-a-5fe496b |
| 18:28:56.608 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a5511d9cfffc5c span_id=691226632af6fe45 session_id=aegis-sp-a-5fe496b |
| 18:28:56.614 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1a5511d9cfffc5c span_id=51c37ea41837f6cd session_id=aegis-sp-a-5fe496b |
| 18:28:56.638 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa1a5511d9cfffc5c span_id=16a72b11ad159b5d session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:56.639 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa1a5511d9cfffc5c span_id=c542daa4a0aab2b3 session_id=aegis-sp-a-5fe496b |
| 18:28:56.768 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaService | trace_id=6aa1a5511d9cfffc5c span_id=76a4640bc8aeff19 |
| 18:28:56.774 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=51034b25229345e2 |
| 18:28:56.924 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=7e44820a224e9980 |
| 18:28:56.928 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978536928,"body":{"isError":false,"lo | session_id=aegis-sp-a-5fe496b trace_id=6aa1a5511d9cfffc5c |
| 18:28:56.933 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978536933,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:28:57.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7225 out=419 masked_before_model=True | request_id=78e6cead-83e8-42ac session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:57.022 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978537022,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:28:57.042 | runtime-span | lambda-segment | ben-fp3-core-tools/LambdaService | trace_id=6aa1a5511d9cfffc5c span_id=40d9cd45369c07c8 |
| 18:28:57.047 | runtime-span | lambda-segment | ben-fp3-core-tools/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=a235502e2e0a352d |
| 18:28:57.072 | lambda | call | benefits_core -> committed=False | trace_id=6aa1a5511d9cfffc5c session_id=aegis-sp-a-5fe496b request_id=b2b14860-34f1-42b6 tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:57.072 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=f5e019a367c497b9 |
| 18:28:57.078 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978537078,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:28:57.078 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978537078,"body":{"isError":false,"re | trace_id=6aa1a5511d9cfffc5c |
| 18:28:57.083 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1a5511d9cfffc5c span_id=6ad16a1a451b6482 session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:57.084 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7225 out=419 | trace_id=6aa1a5511d9cfffc5c span_id=efb29027ed779de6 session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:28:57.085 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a5511d9cfffc5c span_id=3e69226e52423e69 session_id=aegis-sp-a-5fe496b |
| 18:28:57.085 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7225 out=419 | trace_id=6aa1a5511d9cfffc5c span_id=6fbcb5904e33b842 session_id=aegis-sp-a-5fe496b request_id=78e6cead-83e8-42ac |
| 18:29:02.920 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a5511d9cfffc5c span_id=baa742b81263bc7d session_id=aegis-sp-a-5fe496b |
| 18:29:02.926 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1a5511d9cfffc5c span_id=5a54fe5622d069b1 session_id=aegis-sp-a-5fe496b |
| 18:29:02.951 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa1a5511d9cfffc5c span_id=9b8ff217d8f4fe98 session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:29:02.952 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa1a5511d9cfffc5c span_id=6f6a740877d71bd6 session_id=aegis-sp-a-5fe496b |
| 18:29:02.952 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa1a5511d9cfffc5c span_id=6c748f0408ba836a session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:29:02.953 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa1a5511d9cfffc5c span_id=15a828c3103f14f5 session_id=aegis-sp-a-5fe496b |
| 18:29:03.000 | worm | evidence | INTENT benefits-determination seq=0 chain=4833701eda95… | trace_id=6aa1a5511d9cfffc5c session_id=aegis-sp-a-5fe496b request_id=40ef2351-6ffe-4b06 tenant=sp-a |
| 18:29:03.076 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaService | trace_id=6aa1a5511d9cfffc5c span_id=6493040ee663a43d |
| 18:29:03.081 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=b326d316a4d27960 |
| 18:29:03.092 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaService | trace_id=6aa1a5511d9cfffc5c span_id=28be5388d6583dae |
| 18:29:03.097 | runtime-span | lambda-segment | ben-fp3-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=2267db969fb72a2a |
| 18:29:03.243 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=b6d03b8d87ac0c8e |
| 18:29:03.246 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978543246,"body":{"isError":false,"lo | session_id=aegis-sp-a-5fe496b trace_id=6aa1a5511d9cfffc5c |
| 18:29:03.249 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978543249,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:29:03.287 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=13c688d7a1ef4929 |
| 18:29:03.290 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978543290,"body":{"isError":false,"lo | session_id=aegis-sp-a-5fe496b trace_id=6aa1a5511d9cfffc5c |
| 18:29:03.294 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978543294,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:29:03.324 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978543324,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:29:03.352 | runtime-span | lambda-segment | ben-fp3-write-audit/LambdaService | trace_id=6aa1a5511d9cfffc5c span_id=669fbaf0deb027cf |
| 18:29:03.354 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978543354,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:29:03.359 | runtime-span | lambda-segment | ben-fp3-write-audit/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=397edb11cc98185c |
| 18:29:03.377 | runtime-span | lambda-segment | ben-fp3-request-signoff/LambdaService | trace_id=6aa1a5511d9cfffc5c span_id=6fe5cb13224e8deb |
| 18:29:03.530 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=f6789b5b18f8cf29 |
| 18:29:03.855 | runtime-span | lambda-segment | ben-fp3-request-signoff/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=5e7b1ce751199cff |
| 18:29:04.159 | lambda | call | write_audit -> stored=True | trace_id=6aa1a5511d9cfffc5c session_id=aegis-sp-a-5fe496b request_id=40ef2351-6ffe-4b06 tenant=sp-a case_id=OBS-SPA-6752F |
| 18:29:04.159 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=f92385533136b392 |
| 18:29:04.165 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978544165,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:29:04.165 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978544165,"body":{"isError":false,"re | trace_id=6aa1a5511d9cfffc5c |
| 18:29:05.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8043 out=489 masked_before_model=True | request_id=aa061d46-cc76-439b session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:29:05.269 | lambda | call | request_signoff -> requested=False | trace_id=6aa1a5511d9cfffc5c session_id=aegis-sp-a-5fe496b request_id=84f0da90-b5e3-47e7 tenant=sp-a case_id=OBS-SPA-6752F |
| 18:29:05.270 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1a5511d9cfffc5c span_id=6d12d23398423243 |
| 18:29:05.274 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978545274,"body":{"isError":false,"re | trace_id=6aa1a5511d9cfffc5c |
| 18:29:05.274 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp3-ben-gw-hctkitwudd","event_timestamp":1788978545274,"body":{"isError":false,"lo | trace_id=6aa1a5511d9cfffc5c |
| 18:29:05.279 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1a5511d9cfffc5c span_id=900c6a404cd2a5c3 session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:29:05.280 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8043 out=489 | trace_id=6aa1a5511d9cfffc5c span_id=fa9350409500cddd session_id=aegis-sp-a-5fe496b tenant=sp-a case_id=OBS-SPA-6752F |
| 18:29:05.281 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa1a5511d9cfffc5c span_id=5a909a3a40e73956 session_id=aegis-sp-a-5fe496b |
| 18:29:05.281 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8043 out=489 | trace_id=6aa1a5511d9cfffc5c span_id=74a8afc2edf5d6db session_id=aegis-sp-a-5fe496b request_id=aa061d46-cc76-439b |
| 18:29:05.286 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a5511d9cfffc5c span_id=1e36185d92f0a724 session_id=aegis-sp-a-5fe496b |
| 18:29:13.852 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1a5511d9cfffc5c span_id=9964ee9b093201f5 session_id=aegis-sp-a-5fe496b |
| 18:29:13.858 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1a5511d9cfffc5c span_id=04e30899e2f77dc5 session_id=aegis-sp-a-5fe496b |
