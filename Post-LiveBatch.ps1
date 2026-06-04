# Prompt user for min and max delays between threads
$minDelayInput = Read-Host "Enter minimum delay between threads in seconds (Leave blank to use file default)"
$maxDelayInput = Read-Host "Enter maximum delay between threads in seconds (Leave blank to use file default)"

# Build argument list dynamically
$argsList = @("--live")

if (-not [string]::IsNullOrWhiteSpace($minDelayInput)) {
    $argsList += "--min-delay"
    $argsList += $minDelayInput.Trim()
}

if (-not [string]::IsNullOrWhiteSpace($maxDelayInput)) {
    $argsList += "--max-delay"
    $argsList += $maxDelayInput.Trim()
}

Write-Host ""
Write-Host "--------------------------------------------------------------------------------"
Write-Host "Scheduling live batch posting."
Write-Host "Command: .\.venv\Scripts\python.exe bluesky_bot/post_batch.py $($argsList -join ' ')"
Write-Host "--------------------------------------------------------------------------------"
Write-Host ""

& .\.venv\Scripts\python.exe bluesky_bot/post_batch.py $argsList
