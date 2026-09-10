# Case trace — `OBS-SPA-3B359` (tenant `sp-a`)

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
| sessions | ['aegis-sp-a-b8ecfbeea0414c32b95a5397921b7c13'] |
| single_tenant | True |
| tenants_seen | ['sp-a'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 14:55:39.829 | lambda | call | ingest_application -> ingested=True | trace_id=6aa2c4eb6f7fe86e46 request_id=a251548e-f572-4325 tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:40.329 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa2c4ec1cc469c404 span_id=0e541ad48e1e20a7 session_id=aegis-sp-a-b8ecfbe |
| 14:55:40.929 | runtime-span | runtime-http | POST /invocations | trace_id=6aa2c4ec1cc469c404 span_id=1a22ab32e8541970 session_id=aegis-sp-a-b8ecfbe |
| 14:55:41.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5339 out=135 masked_before_model=True | request_id=0d76e5c3-e57e-4eba session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:41.020 | runtime-span | span | SSM.GetParameter | trace_id=6aa2c4ec1cc469c404 span_id=00e343a005571649 session_id=aegis-sp-a-b8ecfbe |
| 14:55:41.061 | runtime-span | span | SSM.GetParameter | trace_id=6aa2c4ec1cc469c404 span_id=b6ef9a50c1fc2ef3 session_id=aegis-sp-a-b8ecfbe |
| 14:55:41.128 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa2c4ec1cc469c404 span_id=31beb81a6009405b session_id=aegis-sp-a-b8ecfbe |
| 14:55:41.175 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa2c4ec1cc469c404 span_id=bf3b86a86d8efdec session_id=aegis-sp-a-b8ecfbe |
| 14:55:41.272 | runtime-span | span | mcp.session | trace_id=6aa2c4ec1cc469c404 span_id=d52e3b3292591e56 session_id=aegis-sp-a-b8ecfbe |
| 14:55:41.420 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa2c4ec1cc469c404 span_id=636051be292a04c4 session_id=aegis-sp-a-b8ecfbe |
| 14:55:41.664 | runtime-span | lambda-segment | ben-fpb-tenant-interceptor/LambdaService | trace_id=6aa2c4ec1cc469c404 span_id=6122ad4cf1fe4896 |
| 14:55:41.668 | runtime-span | lambda-segment | ben-fpb-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=8fe22698f2386ccc |
| 14:55:41.768 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=e98c70c83ba665fc |
| 14:55:41.772 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052141772,"body":{"isError":false,"lo | session_id=aegis-sp-a-b8ecfbe trace_id=6aa2c4ec1cc469c404 |
| 14:55:41.776 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052141776,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:55:41.858 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052141858,"body":{"isError":false,"re | trace_id=6aa2c4ec1cc469c404 |
| 14:55:41.866 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=46453 out=2108 | trace_id=6aa2c4ec1cc469c404 span_id=58a5ea8cc4a646b6 session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:41.867 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2c4ec1cc469c404 span_id=6b1c3dcd64b89acd session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:41.868 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5339 out=135 | trace_id=6aa2c4ec1cc469c404 span_id=191013d2b7df844a session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:41.879 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5339 out=135 | trace_id=6aa2c4ec1cc469c404 span_id=618bda67e5835849 session_id=aegis-sp-a-b8ecfbe request_id=0d76e5c3-e57e-4eba |
| 14:55:41.880 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2c4ec1cc469c404 span_id=0f5be2cbc5e1ff15 session_id=aegis-sp-a-b8ecfbe |
| 14:55:45.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5552 out=117 masked_before_model=True | request_id=1678eeef-86d8-4cc2 session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:45.168 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2c4ec1cc469c404 span_id=a2549aa35a6b291b session_id=aegis-sp-a-b8ecfbe |
| 14:55:45.184 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2c4ec1cc469c404 span_id=c9ea6d7cfa6e717a session_id=aegis-sp-a-b8ecfbe |
| 14:55:45.215 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa2c4ec1cc469c404 span_id=60c39d4a69b05406 session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:45.216 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa2c4ec1cc469c404 span_id=8f65eff216b0e17a session_id=aegis-sp-a-b8ecfbe |
| 14:55:45.312 | runtime-span | lambda-segment | ben-fpb-tenant-interceptor/LambdaService | trace_id=6aa2c4ec1cc469c404 span_id=429f0c4621ad6cbf |
| 14:55:45.316 | runtime-span | lambda-segment | ben-fpb-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=21136ac08a84c6b2 |
| 14:55:45.676 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=0d2d9361bc598513 |
| 14:55:45.679 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052145679,"body":{"isError":false,"lo | session_id=aegis-sp-a-b8ecfbe trace_id=6aa2c4ec1cc469c404 |
| 14:55:45.682 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052145682,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:55:45.769 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052145769,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:55:45.795 | runtime-span | lambda-segment | ben-fpb-intake-application/LambdaService | trace_id=6aa2c4ec1cc469c404 span_id=4d7cf6a1d084dc50 |
| 14:55:45.807 | runtime-span | lambda-segment | ben-fpb-intake-application/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=a62d99be840efbf5 |
| 14:55:45.976 | lambda | call | intake_application -> ok | trace_id=6aa2c4ec1cc469c404 session_id=aegis-sp-a-b8ecfbe request_id=97b81d43-3800-4b92 tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:45.976 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=4fede8f8eed87801 |
| 14:55:45.981 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052145981,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:55:45.981 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052145981,"body":{"isError":false,"re | trace_id=6aa2c4ec1cc469c404 |
| 14:55:45.986 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2c4ec1cc469c404 span_id=69881db6fa3040e0 session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:45.987 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5552 out=117 | trace_id=6aa2c4ec1cc469c404 span_id=95f5827cfd65e9ba session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:45.988 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5552 out=117 | trace_id=6aa2c4ec1cc469c404 span_id=2ed539bbdb335ce5 session_id=aegis-sp-a-b8ecfbe request_id=1678eeef-86d8-4cc2 |
| 14:55:45.989 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2c4ec1cc469c404 span_id=c218c7a7c4d8e25a session_id=aegis-sp-a-b8ecfbe |
| 14:55:49.767 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2c4ec1cc469c404 span_id=1142c857e2155169 session_id=aegis-sp-a-b8ecfbe |
| 14:55:49.773 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2c4ec1cc469c404 span_id=419f832b623503d8 session_id=aegis-sp-a-b8ecfbe |
| 14:55:49.782 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa2c4ec1cc469c404 span_id=973abe9c7e5510ee session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:49.783 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa2c4ec1cc469c404 span_id=24b2d4945f2e5e05 session_id=aegis-sp-a-b8ecfbe |
| 14:55:49.884 | runtime-span | lambda-segment | ben-fpb-tenant-interceptor/LambdaService | trace_id=6aa2c4ec1cc469c404 span_id=73b038fb21bb8937 |
| 14:55:49.890 | runtime-span | lambda-segment | ben-fpb-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=0459bc285b92f8a8 |
| 14:55:50.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5971 out=392 masked_before_model=True | request_id=807cd4fe-833a-44a7 session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:50.056 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=19313215ca01ef1a |
| 14:55:50.060 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052150060,"body":{"isError":false,"lo | session_id=aegis-sp-a-b8ecfbe trace_id=6aa2c4ec1cc469c404 |
| 14:55:50.063 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052150063,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:55:50.137 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052150137,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:55:50.155 | runtime-span | lambda-segment | ben-fpb-mask-pii/LambdaService | trace_id=6aa2c4ec1cc469c404 span_id=6adde232611e93c5 |
| 14:55:50.161 | runtime-span | lambda-segment | ben-fpb-mask-pii/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=8ffcc0c87fc7d45c |
| 14:55:50.660 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa2c4ec1cc469c404 session_id=aegis-sp-a-b8ecfbe request_id=d258d948-5520-4320 tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:50.660 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=bc47cea022ad32c2 |
| 14:55:50.665 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052150665,"body":{"isError":false,"re | trace_id=6aa2c4ec1cc469c404 |
| 14:55:50.665 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052150665,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:55:50.670 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2c4ec1cc469c404 span_id=791d0edcc66b2746 session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:50.672 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5971 out=392 | trace_id=6aa2c4ec1cc469c404 span_id=c30b968a7e8d2977 session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:50.672 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5971 out=392 | trace_id=6aa2c4ec1cc469c404 span_id=9ff955b308728b35 session_id=aegis-sp-a-b8ecfbe request_id=807cd4fe-833a-44a7 |
| 14:55:50.673 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2c4ec1cc469c404 span_id=7ebdd80551b47627 session_id=aegis-sp-a-b8ecfbe |
| 14:55:55.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6594 out=561 masked_before_model=True | request_id=bb947842-81e2-4dab session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:55.101 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2c4ec1cc469c404 span_id=910d64a279ccafd6 session_id=aegis-sp-a-b8ecfbe |
| 14:55:55.108 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2c4ec1cc469c404 span_id=ac5b863488c0e865 session_id=aegis-sp-a-b8ecfbe |
| 14:55:55.116 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa2c4ec1cc469c404 span_id=b3221281e70a3266 session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:55.117 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa2c4ec1cc469c404 span_id=c9a8a24db9f4123a session_id=aegis-sp-a-b8ecfbe |
| 14:55:55.210 | runtime-span | lambda-segment | ben-fpb-tenant-interceptor/LambdaService | trace_id=6aa2c4ec1cc469c404 span_id=759310c68d5675e4 |
| 14:55:55.215 | runtime-span | lambda-segment | ben-fpb-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=395171fa8a8fb9bb |
| 14:55:55.356 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=33e7f3145a67d6b5 |
| 14:55:55.361 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052155361,"body":{"isError":false,"lo | session_id=aegis-sp-a-b8ecfbe trace_id=6aa2c4ec1cc469c404 |
| 14:55:55.365 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052155365,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:55:55.441 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052155441,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:55:55.467 | runtime-span | lambda-segment | ben-fpb-assess-eligibility/LambdaService | trace_id=6aa2c4ec1cc469c404 span_id=15b533063983e31d |
| 14:55:55.472 | runtime-span | lambda-segment | ben-fpb-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=ef7df15ad3416605 |
| 14:55:55.493 | lambda | call | assess_eligibility -> ok | trace_id=6aa2c4ec1cc469c404 session_id=aegis-sp-a-b8ecfbe request_id=e5afde54-efef-4908 tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:55.494 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=f882c306998fc9ae |
| 14:55:55.498 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052155498,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:55:55.498 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052155498,"body":{"isError":false,"re | trace_id=6aa2c4ec1cc469c404 |
| 14:55:55.503 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2c4ec1cc469c404 span_id=d226edab5531ba59 session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:55.504 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6594 out=561 | trace_id=6aa2c4ec1cc469c404 span_id=7832a20b57cd2acf session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:55:55.505 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6594 out=561 | trace_id=6aa2c4ec1cc469c404 span_id=67751314a0988edf session_id=aegis-sp-a-b8ecfbe request_id=bb947842-81e2-4dab |
| 14:55:55.506 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2c4ec1cc469c404 span_id=9f009080de8614db session_id=aegis-sp-a-b8ecfbe |
| 14:56:01.721 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2c4ec1cc469c404 span_id=df659e83d9877f96 session_id=aegis-sp-a-b8ecfbe |
| 14:56:01.727 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2c4ec1cc469c404 span_id=8b780119c15cfb32 session_id=aegis-sp-a-b8ecfbe |
| 14:56:01.761 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa2c4ec1cc469c404 span_id=803d179aea19c593 session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:56:01.762 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa2c4ec1cc469c404 span_id=d20acedc3b1461cc session_id=aegis-sp-a-b8ecfbe |
| 14:56:01.913 | runtime-span | lambda-segment | ben-fpb-tenant-interceptor/LambdaService | trace_id=6aa2c4ec1cc469c404 span_id=1713809b542064f6 |
| 14:56:01.917 | runtime-span | lambda-segment | ben-fpb-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=99ff5a5834aadde8 |
| 14:56:02.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7203 out=326 masked_before_model=True | request_id=8c8c6ae9-9aa6-49b6 session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:56:02.096 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=cfa60ff03a60bb68 |
| 14:56:02.100 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052162100,"body":{"isError":false,"lo | session_id=aegis-sp-a-b8ecfbe trace_id=6aa2c4ec1cc469c404 |
| 14:56:02.104 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052162104,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:56:02.196 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052162196,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:56:02.224 | runtime-span | lambda-segment | ben-fpb-core-tools/LambdaService | trace_id=6aa2c4ec1cc469c404 span_id=2c43d35215ca5b1d |
| 14:56:02.230 | runtime-span | lambda-segment | ben-fpb-core-tools/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=e51cd82c6029915f |
| 14:56:02.256 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=a7fe0aafc02871f1 |
| 14:56:02.257 | lambda | call | benefits_core -> committed=False | trace_id=6aa2c4ec1cc469c404 session_id=aegis-sp-a-b8ecfbe request_id=32c6a5a7-a260-4006 tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:56:02.261 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052162261,"body":{"isError":false,"re | trace_id=6aa2c4ec1cc469c404 |
| 14:56:02.261 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052162261,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:56:02.267 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2c4ec1cc469c404 span_id=9df9db063dec8fbb session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:56:02.269 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7203 out=326 | trace_id=6aa2c4ec1cc469c404 span_id=40fe9627e30f5244 session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:56:02.270 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7203 out=326 | trace_id=6aa2c4ec1cc469c404 span_id=f41928eb38378e11 session_id=aegis-sp-a-b8ecfbe request_id=8c8c6ae9-9aa6-49b6 |
| 14:56:02.277 | runtime-span | span | SSM.GetParameter | trace_id=6aa2c4ec1cc469c404 span_id=6a0fbbd9d770d277 session_id=aegis-sp-a-b8ecfbe |
| 14:56:02.321 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2c4ec1cc469c404 span_id=f83c8e6861fb422d session_id=aegis-sp-a-b8ecfbe |
| 14:56:07.405 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2c4ec1cc469c404 span_id=e3b13f87de51c474 session_id=aegis-sp-a-b8ecfbe |
| 14:56:07.411 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2c4ec1cc469c404 span_id=5f6df3dd2993dc25 session_id=aegis-sp-a-b8ecfbe |
| 14:56:07.420 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa2c4ec1cc469c404 span_id=7ae80652f0a19238 session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:56:07.421 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa2c4ec1cc469c404 span_id=2e2405b373d00d5d session_id=aegis-sp-a-b8ecfbe |
| 14:56:07.523 | runtime-span | lambda-segment | ben-fpb-tenant-interceptor/LambdaService | trace_id=6aa2c4ec1cc469c404 span_id=537b767ab481bc81 |
| 14:56:07.527 | runtime-span | lambda-segment | ben-fpb-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=94ddf83453178c83 |
| 14:56:07.695 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=b8955b9449659666 |
| 14:56:07.697 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052167697,"body":{"isError":false,"lo | session_id=aegis-sp-a-b8ecfbe trace_id=6aa2c4ec1cc469c404 |
| 14:56:07.701 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052167701,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:56:07.780 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052167780,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:56:07.800 | runtime-span | lambda-segment | ben-fpb-write-audit/LambdaService | trace_id=6aa2c4ec1cc469c404 span_id=125dac94faf327e4 |
| 14:56:07.811 | runtime-span | lambda-segment | ben-fpb-write-audit/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=bcc113f15de89a73 |
| 14:56:08.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7816 out=111 masked_before_model=True | request_id=900a4bc2-57c6-4df1 session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:56:08.000 | worm | evidence | INTENT benefits-determination seq=0 chain=2c6807c9bb51… | trace_id=6aa2c4ec1cc469c404 session_id=aegis-sp-a-b8ecfbe request_id=60f1516e-5e2f-4aa4 tenant=sp-a |
| 14:56:08.617 | lambda | call | write_audit -> stored=True | trace_id=6aa2c4ec1cc469c404 session_id=aegis-sp-a-b8ecfbe request_id=60f1516e-5e2f-4aa4 tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:56:08.641 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=4426f9d10cef1f17 |
| 14:56:08.646 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052168646,"body":{"isError":false,"re | trace_id=6aa2c4ec1cc469c404 |
| 14:56:08.646 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052168646,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:56:08.651 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2c4ec1cc469c404 span_id=598b65d8f949b345 session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:56:08.653 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7816 out=111 | trace_id=6aa2c4ec1cc469c404 span_id=f6c56a921a1929a2 session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:56:08.654 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7816 out=111 | trace_id=6aa2c4ec1cc469c404 span_id=9a40f833b29db6c8 session_id=aegis-sp-a-b8ecfbe request_id=900a4bc2-57c6-4df1 |
| 14:56:08.655 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2c4ec1cc469c404 span_id=a8866ee4c52f075e session_id=aegis-sp-a-b8ecfbe |
| 14:56:11.818 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2c4ec1cc469c404 span_id=8a931150ba0efaa4 session_id=aegis-sp-a-b8ecfbe |
| 14:56:11.831 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa2c4ec1cc469c404 span_id=9eee72f3e7eaede3 session_id=aegis-sp-a-b8ecfbe |
| 14:56:11.835 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2c4ec1cc469c404 span_id=0eb83eeda766ec54 session_id=aegis-sp-a-b8ecfbe |
| 14:56:11.843 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa2c4ec1cc469c404 span_id=c8a8c4af0d774bac session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:56:11.844 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa2c4ec1cc469c404 span_id=d8a0d1f9f411635b session_id=aegis-sp-a-b8ecfbe |
| 14:56:11.936 | runtime-span | lambda-segment | ben-fpb-tenant-interceptor/LambdaService | trace_id=6aa2c4ec1cc469c404 span_id=05a48e97d2f44d24 |
| 14:56:11.942 | runtime-span | lambda-segment | ben-fpb-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=9067f066f3f2741e |
| 14:56:12.102 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=976424edfc578b76 |
| 14:56:12.105 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052172105,"body":{"isError":false,"lo | session_id=aegis-sp-a-b8ecfbe trace_id=6aa2c4ec1cc469c404 |
| 14:56:12.109 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052172109,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:56:12.203 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052172203,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:56:12.221 | runtime-span | lambda-segment | ben-fpb-request-signoff/LambdaService | trace_id=6aa2c4ec1cc469c404 span_id=35b2a51db2bd7ebe |
| 14:56:12.383 | runtime-span | lambda-segment | Init/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=5896341435631675 |
| 14:56:12.710 | runtime-span | lambda-segment | ben-fpb-request-signoff/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=fe5e06aecc3e5e26 |
| 14:56:14.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7978 out=466 masked_before_model=True | request_id=adb25132-dd2a-405d session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:56:14.148 | lambda | call | request_signoff -> requested=False | trace_id=6aa2c4ec1cc469c404 session_id=aegis-sp-a-b8ecfbe request_id=2dd5f9be-d137-4132 tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:56:14.150 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa2c4ec1cc469c404 span_id=e5b95ce592c34a9c |
| 14:56:14.154 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052174154,"body":{"isError":false,"lo | trace_id=6aa2c4ec1cc469c404 |
| 14:56:14.154 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fpb-ben-gw-msjtyzf97e","event_timestamp":1789052174154,"body":{"isError":false,"re | trace_id=6aa2c4ec1cc469c404 |
| 14:56:14.159 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa2c4ec1cc469c404 span_id=2dacbeb9da0e9bab session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:56:14.161 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7978 out=466 | trace_id=6aa2c4ec1cc469c404 span_id=bba7593178054ed3 session_id=aegis-sp-a-b8ecfbe tenant=sp-a case_id=OBS-SPA-3B359 |
| 14:56:14.162 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7978 out=466 | trace_id=6aa2c4ec1cc469c404 span_id=24c108892f04fd1d session_id=aegis-sp-a-b8ecfbe request_id=adb25132-dd2a-405d |
| 14:56:14.163 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2c4ec1cc469c404 span_id=f0248cd7e3c7f355 session_id=aegis-sp-a-b8ecfbe |
| 14:56:23.104 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa2c4ec1cc469c404 span_id=727687ac064417ba session_id=aegis-sp-a-b8ecfbe |
| 14:56:23.110 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa2c4ec1cc469c404 span_id=eb5fc22868f3b0f6 session_id=aegis-sp-a-b8ecfbe |
