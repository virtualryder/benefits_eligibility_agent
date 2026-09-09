# Case trace — `OBS-SPB-A78AB` (tenant `sp-b`)

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
| sessions | ['aegis-sp-b-eeeaf65d1678453c8b20b90d288bd171'] |
| single_tenant | True |
| tenants_seen | ['sp-b'] |
| tool_spans | 12 |
| worm_records | 1 |

| time (UTC) | source | kind | what | join keys |
|---|---|---|---|---|
| 20:01:53.047 | lambda | call | ingest_application -> ingested=True | trace_id=6aa1bb3044d4eef60a request_id=80e19e51-741d-4d09 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:01:53.501 | runtime-span | runtime-invoke | AgentCore.Runtime.Invoke | trace_id=6aa1bb313823d11440 span_id=42c5a37c7baafbb1 session_id=aegis-sp-b-eeeaf65 |
| 20:01:54.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5342 out=139 masked_before_model=True | request_id=c7d999c9-dbee-4dd4 session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:01:54.053 | runtime-span | runtime-http | POST /invocations | trace_id=6aa1bb313823d11440 span_id=cb6868aebfd066d3 session_id=aegis-sp-b-eeeaf65 |
| 20:01:54.123 | runtime-span | span | SSM.GetParameter | trace_id=6aa1bb313823d11440 span_id=4f50297eff538ec8 session_id=aegis-sp-b-eeeaf65 |
| 20:01:54.162 | runtime-span | span | SSM.GetParameter | trace_id=6aa1bb313823d11440 span_id=f5fb521ff62b669b session_id=aegis-sp-b-eeeaf65 |
| 20:01:54.212 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa1bb313823d11440 span_id=0cbb647a6428b4c0 session_id=aegis-sp-b-eeeaf65 |
| 20:01:54.262 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa1bb313823d11440 span_id=768f4ebfc3dcd660 session_id=aegis-sp-b-eeeaf65 |
| 20:01:54.341 | runtime-span | span | mcp.session | trace_id=6aa1bb313823d11440 span_id=291241c5d57635aa session_id=aegis-sp-b-eeeaf65 |
| 20:01:54.416 | runtime-span | mcp-list | mcp tools/list | trace_id=6aa1bb313823d11440 span_id=ef56b193dca00e41 session_id=aegis-sp-b-eeeaf65 |
| 20:01:54.684 | runtime-span | lambda-segment | ben-fp4-tenant-interceptor/LambdaService | trace_id=6aa1bb313823d11440 span_id=27feabda4268468f |
| 20:01:54.691 | runtime-span | lambda-segment | ben-fp4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=3a4456888281497b |
| 20:01:54.692 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=f171080e1a9e4dd4 |
| 20:01:54.695 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984114695,"body":{"isError":false,"lo | session_id=aegis-sp-b-eeeaf65 trace_id=6aa1bb313823d11440 |
| 20:01:54.700 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984114700,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:01:54.779 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984114779,"body":{"isError":false,"re | trace_id=6aa1bb313823d11440 |
| 20:01:54.787 | runtime-span | agent | invoke_agent Strands Agents model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=46704 out=2174 | trace_id=6aa1bb313823d11440 span_id=a760131db4ea8b97 session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:01:54.788 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1bb313823d11440 span_id=ac114b693d2b77a3 session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:01:54.789 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5342 out=139 | trace_id=6aa1bb313823d11440 span_id=db1a88e59bda0dc0 session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:01:54.792 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1bb313823d11440 span_id=0285ed3fedbd07e4 session_id=aegis-sp-b-eeeaf65 |
| 20:01:54.792 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5342 out=139 | trace_id=6aa1bb313823d11440 span_id=db1c78e5c1738d8e session_id=aegis-sp-b-eeeaf65 request_id=c7d999c9-dbee-4dd4 |
| 20:01:58.519 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1bb313823d11440 span_id=cf9f538348da7431 session_id=aegis-sp-b-eeeaf65 |
| 20:01:58.532 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1bb313823d11440 span_id=2d8ebc64ab3728c0 session_id=aegis-sp-b-eeeaf65 |
| 20:01:58.561 | runtime-span | tool | execute_tool intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa1bb313823d11440 span_id=64bf36aca39a5d97 session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:01:58.562 | runtime-span | tool | mcp tools/call intake-application___intake_application tool=intake-application___intake_application | trace_id=6aa1bb313823d11440 span_id=4f2c9b3240d1d746 session_id=aegis-sp-b-eeeaf65 |
| 20:01:58.672 | runtime-span | lambda-segment | ben-fp4-tenant-interceptor/LambdaService | trace_id=6aa1bb313823d11440 span_id=0fe49231c44764a9 |
| 20:01:58.676 | runtime-span | lambda-segment | ben-fp4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=a19cee833e7b0681 |
| 20:01:58.876 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=c162df6520ae75b3 |
| 20:01:58.880 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984118880,"body":{"isError":false,"lo | session_id=aegis-sp-b-eeeaf65 trace_id=6aa1bb313823d11440 |
| 20:01:58.883 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984118883,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:01:58.955 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984118955,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:01:58.979 | runtime-span | lambda-segment | ben-fp4-intake-application/LambdaService | trace_id=6aa1bb313823d11440 span_id=619423df32069934 |
| 20:01:58.988 | runtime-span | lambda-segment | ben-fp4-intake-application/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=a3f4221336427beb |
| 20:01:59.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5559 out=121 masked_before_model=True | request_id=a7979b20-cf62-4a2c session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:01:59.171 | lambda | call | intake_application -> ok | trace_id=6aa1bb313823d11440 session_id=aegis-sp-b-eeeaf65 request_id=b1173dae-7da9-4e75 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:01:59.171 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=f0b7b7f31ec19122 |
| 20:01:59.175 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984119175,"body":{"isError":false,"re | trace_id=6aa1bb313823d11440 |
| 20:01:59.175 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984119175,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:01:59.180 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5559 out=121 | trace_id=6aa1bb313823d11440 span_id=f529ddea37be6edc session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:01:59.180 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1bb313823d11440 span_id=ff490ad585132baa session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:01:59.181 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1bb313823d11440 span_id=47d2c0b1ea855d1c session_id=aegis-sp-b-eeeaf65 |
| 20:01:59.181 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5559 out=121 | trace_id=6aa1bb313823d11440 span_id=8163af8e8feddbfc session_id=aegis-sp-b-eeeaf65 request_id=a7979b20-cf62-4a2c |
| 20:02:02.154 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1bb313823d11440 span_id=3b5f6b200a6e32b8 session_id=aegis-sp-b-eeeaf65 |
| 20:02:02.161 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1bb313823d11440 span_id=1b8bb6a89e5bb4bc session_id=aegis-sp-b-eeeaf65 |
| 20:02:02.169 | runtime-span | tool | execute_tool mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa1bb313823d11440 span_id=1a488c11b920992b session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:02.170 | runtime-span | tool | mcp tools/call mask-pii___mask_pii tool=mask-pii___mask_pii | trace_id=6aa1bb313823d11440 span_id=060db4ec19a58401 session_id=aegis-sp-b-eeeaf65 |
| 20:02:02.311 | runtime-span | lambda-segment | ben-fp4-tenant-interceptor/LambdaService | trace_id=6aa1bb313823d11440 span_id=48a2ea34114d67da |
| 20:02:02.314 | runtime-span | lambda-segment | ben-fp4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=78373b91cadaefa9 |
| 20:02:02.472 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=c3205518a5db50cd |
| 20:02:02.475 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984122475,"body":{"isError":false,"lo | session_id=aegis-sp-b-eeeaf65 trace_id=6aa1bb313823d11440 |
| 20:02:02.479 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984122479,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:02:02.565 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984122565,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:02:02.581 | runtime-span | lambda-segment | ben-fp4-mask-pii/LambdaService | trace_id=6aa1bb313823d11440 span_id=255922a85ec016ff |
| 20:02:02.586 | runtime-span | lambda-segment | ben-fp4-mask-pii/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=cfce417191535a0b |
| 20:02:03.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5985 out=395 masked_before_model=True | request_id=8456ac59-ef85-4c25 session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:03.048 | lambda | call | mask_pii -> deidentified=True | trace_id=6aa1bb313823d11440 session_id=aegis-sp-b-eeeaf65 request_id=433eba56-549a-45e7 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:03.048 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=e924291f6f821247 |
| 20:02:03.054 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984123054,"body":{"isError":false,"re | trace_id=6aa1bb313823d11440 |
| 20:02:03.054 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984123054,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:02:03.058 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1bb313823d11440 span_id=88d9b57fa14f5065 session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:03.059 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5985 out=395 | trace_id=6aa1bb313823d11440 span_id=2c6c422bdb59cbd3 session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:03.060 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1bb313823d11440 span_id=85f280dece20058f session_id=aegis-sp-b-eeeaf65 |
| 20:02:03.060 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=5985 out=395 | trace_id=6aa1bb313823d11440 span_id=dd02565d0cabdbc9 session_id=aegis-sp-b-eeeaf65 request_id=8456ac59-ef85-4c25 |
| 20:02:07.827 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1bb313823d11440 span_id=d8db878334c49705 session_id=aegis-sp-b-eeeaf65 |
| 20:02:07.833 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1bb313823d11440 span_id=07adf2c4b710d4a0 session_id=aegis-sp-b-eeeaf65 |
| 20:02:07.844 | runtime-span | tool | execute_tool assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa1bb313823d11440 span_id=2521d8c860a7bbd9 session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:07.845 | runtime-span | tool | mcp tools/call assess-eligibility___assess_eligibility tool=assess-eligibility___assess_eligibility | trace_id=6aa1bb313823d11440 span_id=a04543005164be2c session_id=aegis-sp-b-eeeaf65 |
| 20:02:07.980 | runtime-span | lambda-segment | ben-fp4-tenant-interceptor/LambdaService | trace_id=6aa1bb313823d11440 span_id=73d549a6e19d51ca |
| 20:02:07.986 | runtime-span | lambda-segment | ben-fp4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=2522bdf870e49806 |
| 20:02:08.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6611 out=564 masked_before_model=True | request_id=ae35f703-a383-4779 session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:08.171 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=1b415f46f4f4a376 |
| 20:02:08.175 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984128175,"body":{"isError":false,"lo | session_id=aegis-sp-b-eeeaf65 trace_id=6aa1bb313823d11440 |
| 20:02:08.179 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984128179,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:02:08.280 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984128280,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:02:08.315 | runtime-span | lambda-segment | ben-fp4-assess-eligibility/LambdaService | trace_id=6aa1bb313823d11440 span_id=433dfe806d3162a9 |
| 20:02:08.320 | runtime-span | lambda-segment | ben-fp4-assess-eligibility/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=daa232a579b19e56 |
| 20:02:08.348 | lambda | call | assess_eligibility -> ok | trace_id=6aa1bb313823d11440 session_id=aegis-sp-b-eeeaf65 request_id=22b6ab5c-b499-43de tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:08.350 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=18c3f19783189d57 |
| 20:02:08.355 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984128355,"body":{"isError":false,"re | trace_id=6aa1bb313823d11440 |
| 20:02:08.355 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984128355,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:02:08.360 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1bb313823d11440 span_id=57ff060018bc25ff session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:08.361 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6611 out=564 | trace_id=6aa1bb313823d11440 span_id=aed81c8004764e18 session_id=aegis-sp-b-eeeaf65 request_id=ae35f703-a383-4779 |
| 20:02:08.361 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=6611 out=564 | trace_id=6aa1bb313823d11440 span_id=203e6315de2f06a2 session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:08.362 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1bb313823d11440 span_id=3c19d6a3e9f40662 session_id=aegis-sp-b-eeeaf65 |
| 20:02:16.533 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1bb313823d11440 span_id=bc2788015831b8f6 session_id=aegis-sp-b-eeeaf65 |
| 20:02:16.540 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1bb313823d11440 span_id=02c7c841ebc9a047 session_id=aegis-sp-b-eeeaf65 |
| 20:02:16.569 | runtime-span | tool | execute_tool ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa1bb313823d11440 span_id=eb029dc6b4ffffd6 session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:16.570 | runtime-span | tool | mcp tools/call ben-core___draft_notice tool=ben-core___draft_notice | trace_id=6aa1bb313823d11440 span_id=62f8874c60f5f8ad session_id=aegis-sp-b-eeeaf65 |
| 20:02:16.688 | runtime-span | lambda-segment | ben-fp4-tenant-interceptor/LambdaService | trace_id=6aa1bb313823d11440 span_id=4c19ada30268e301 |
| 20:02:16.694 | runtime-span | lambda-segment | ben-fp4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=10a5ee66be316f7b |
| 20:02:16.873 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=cdbdecec9ea9921c |
| 20:02:16.878 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984136878,"body":{"isError":false,"lo | session_id=aegis-sp-b-eeeaf65 trace_id=6aa1bb313823d11440 |
| 20:02:16.886 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984136886,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:02:16.968 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984136968,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:02:16.992 | runtime-span | lambda-segment | ben-fp4-core-tools/LambdaService | trace_id=6aa1bb313823d11440 span_id=0982ddec67a23b6a |
| 20:02:16.998 | runtime-span | lambda-segment | ben-fp4-core-tools/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=321ff2b68fb1ad63 |
| 20:02:17.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7223 out=370 masked_before_model=True | request_id=fcff5bae-62ad-4ab5 session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:17.020 | lambda | call | benefits_core -> committed=False | trace_id=6aa1bb313823d11440 session_id=aegis-sp-b-eeeaf65 request_id=a08960a5-cd93-4c80 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:17.020 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=587e6ae1ceb40423 |
| 20:02:17.025 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984137025,"body":{"isError":false,"re | trace_id=6aa1bb313823d11440 |
| 20:02:17.025 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984137025,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:02:17.031 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1bb313823d11440 span_id=0b6a3e780b4206ca session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:17.032 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7223 out=370 | trace_id=6aa1bb313823d11440 span_id=679593ec6ea49a1b session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:17.033 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7223 out=370 | trace_id=6aa1bb313823d11440 span_id=2557ac6ed23b7178 session_id=aegis-sp-b-eeeaf65 request_id=fcff5bae-62ad-4ab5 |
| 20:02:17.039 | runtime-span | span | SSM.GetParameter | trace_id=6aa1bb313823d11440 span_id=c985205be27ddfba session_id=aegis-sp-b-eeeaf65 |
| 20:02:17.082 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1bb313823d11440 span_id=f4c7bc72bf962adc session_id=aegis-sp-b-eeeaf65 |
| 20:02:22.687 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1bb313823d11440 span_id=ab37bbbdad5c6d64 session_id=aegis-sp-b-eeeaf65 |
| 20:02:22.693 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1bb313823d11440 span_id=f6b6171096be6d32 session_id=aegis-sp-b-eeeaf65 |
| 20:02:22.718 | runtime-span | tool | execute_tool write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa1bb313823d11440 span_id=d0fa1137aa3dbbf5 session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:22.719 | runtime-span | tool | mcp tools/call write-audit___write_audit tool=write-audit___write_audit | trace_id=6aa1bb313823d11440 span_id=97f1addedfaddb5a session_id=aegis-sp-b-eeeaf65 |
| 20:02:22.825 | runtime-span | lambda-segment | ben-fp4-tenant-interceptor/LambdaService | trace_id=6aa1bb313823d11440 span_id=6289d046bae8d28d |
| 20:02:22.831 | runtime-span | lambda-segment | ben-fp4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=0947667d4bf0c646 |
| 20:02:22.996 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=4c7df51e8b382c2a |
| 20:02:23.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7911 out=111 masked_before_model=True | request_id=393f653d-fe22-40eb session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:23.000 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984143000,"body":{"isError":false,"lo | session_id=aegis-sp-b-eeeaf65 trace_id=6aa1bb313823d11440 |
| 20:02:23.000 | worm | evidence | INTENT benefits-determination seq=0 chain=1012443cc0b5… | trace_id=6aa1bb313823d11440 session_id=aegis-sp-b-eeeaf65 request_id=f91d7b24-1e12-4eec tenant=sp-b |
| 20:02:23.003 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984143003,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:02:23.090 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984143090,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:02:23.119 | runtime-span | lambda-segment | ben-fp4-write-audit/LambdaService | trace_id=6aa1bb313823d11440 span_id=6c0caf19cd1c4f92 |
| 20:02:23.125 | runtime-span | lambda-segment | ben-fp4-write-audit/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=ccad901a2ab6f7c9 |
| 20:02:23.615 | lambda | call | write_audit -> stored=True | trace_id=6aa1bb313823d11440 session_id=aegis-sp-b-eeeaf65 request_id=f91d7b24-1e12-4eec tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:23.616 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=4a43fae7770fedbb |
| 20:02:23.620 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984143620,"body":{"isError":false,"re | trace_id=6aa1bb313823d11440 |
| 20:02:23.620 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984143620,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:02:23.624 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1bb313823d11440 span_id=8057ece773577b48 session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:23.625 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7911 out=111 | trace_id=6aa1bb313823d11440 span_id=61a4f7e55886c22f session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:23.626 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=7911 out=111 | trace_id=6aa1bb313823d11440 span_id=9efd8d6f2c1d9cdb session_id=aegis-sp-b-eeeaf65 request_id=393f653d-fe22-40eb |
| 20:02:23.627 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1bb313823d11440 span_id=21564817f774b8e9 session_id=aegis-sp-b-eeeaf65 |
| 20:02:26.000 | bedrock-model-log | model-invocation | Converse us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8073 out=474 masked_before_model=True | request_id=2d8e0913-dcb6-4941 session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:26.297 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1bb313823d11440 span_id=e270cb4f81e1e3a3 session_id=aegis-sp-b-eeeaf65 |
| 20:02:26.303 | runtime-span | span | DynamoDB.GetItem | trace_id=6aa1bb313823d11440 span_id=de41546e53a2d8a4 session_id=aegis-sp-b-eeeaf65 |
| 20:02:26.307 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1bb313823d11440 span_id=db0e3226a14b874b session_id=aegis-sp-b-eeeaf65 |
| 20:02:26.316 | runtime-span | tool | mcp tools/call request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa1bb313823d11440 span_id=dfb51c642e6091d3 session_id=aegis-sp-b-eeeaf65 |
| 20:02:26.316 | runtime-span | tool | execute_tool request-signoff___request_signoff tool=request-signoff___request_signoff | trace_id=6aa1bb313823d11440 span_id=03828511ad6fce97 session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:26.434 | runtime-span | lambda-segment | ben-fp4-tenant-interceptor/LambdaService | trace_id=6aa1bb313823d11440 span_id=1925bbb7767f2c2c |
| 20:02:26.440 | runtime-span | lambda-segment | ben-fp4-tenant-interceptor/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=5446e144be85777c |
| 20:02:26.616 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=38d267690110ea93 |
| 20:02:26.620 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984146620,"body":{"isError":false,"lo | session_id=aegis-sp-b-eeeaf65 trace_id=6aa1bb313823d11440 |
| 20:02:26.624 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984146624,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:02:26.693 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984146693,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:02:26.723 | runtime-span | lambda-segment | ben-fp4-request-signoff/LambdaService | trace_id=6aa1bb313823d11440 span_id=291cf5338a41098c |
| 20:02:26.729 | runtime-span | lambda-segment | ben-fp4-request-signoff/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=3a59a41d893d560e |
| 20:02:26.753 | runtime-span | lambda-segment | Overhead/LambdaExecutionEnvironment | trace_id=6aa1bb313823d11440 span_id=01081a0af47c5057 |
| 20:02:26.754 | lambda | call | request_signoff -> requested=False | trace_id=6aa1bb313823d11440 session_id=aegis-sp-b-eeeaf65 request_id=566d8e07-f4dc-4e33 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:26.758 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984146758,"body":{"isError":false,"lo | trace_id=6aa1bb313823d11440 |
| 20:02:26.758 | gateway | request | {"resource_arn":"arn:aws:bedrock-agentcore:us-east-1:111122223333:gateway/ben-fp4-ben-gw-crd9cfinmo","event_timestamp":1788984146758,"body":{"isError":false,"re | trace_id=6aa1bb313823d11440 |
| 20:02:26.762 | runtime-span | cycle | execute_event_loop_cycle | trace_id=6aa1bb313823d11440 span_id=1bb53c418989733d session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:26.764 | runtime-span | model | chat model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8073 out=474 | trace_id=6aa1bb313823d11440 span_id=46be1fad43e3266c session_id=aegis-sp-b-eeeaf65 tenant=sp-b case_id=OBS-SPB-A78AB |
| 20:02:26.765 | runtime-span | model | chat us.anthropic.claude-sonnet-4-5-20250929-v1:0 model=us.anthropic.claude-sonnet-4-5-20250929-v1:0 in=8073 out=474 | trace_id=6aa1bb313823d11440 span_id=d59af3630563d499 session_id=aegis-sp-b-eeeaf65 request_id=2d8e0913-dcb6-4941 |
| 20:02:26.766 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1bb313823d11440 span_id=ad5d85a3386858e7 session_id=aegis-sp-b-eeeaf65 |
| 20:02:37.836 | runtime-span | span | DynamoDB.UpdateItem | trace_id=6aa1bb313823d11440 span_id=fdc2dd514d49c006 session_id=aegis-sp-b-eeeaf65 |
| 20:02:37.842 | runtime-span | span | CloudWatch.PutMetricData | trace_id=6aa1bb313823d11440 span_id=14ac771c3a56c56e session_id=aegis-sp-b-eeeaf65 |
