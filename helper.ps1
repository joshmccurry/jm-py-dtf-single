$instance_id = "" #blank instanceid
$url = "http://localhost:7071/api/orchestrators/Orchestrator?instanceId=" 
#Initial Execution
$response = Invoke-RestMethod -Method 'GET' -Uri "$url$instance_id" -ContentType "application/json"
Write-Host $response
$instance_id = $response.id
Start-Sleep -Milliseconds 100

#Subsquent executions are idempotent unless complete
Invoke-RestMethod -Method 'GET' -Uri "$url$instance_id" -ContentType "application/json"

#Start final execution after completion
Start-Sleep -Milliseconds 5000
Invoke-RestMethod -Method 'GET' -Uri "$url$instance_id" -ContentType "application/json"