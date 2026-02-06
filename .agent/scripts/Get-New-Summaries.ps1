# Get-New-Summaries.ps1
$MD_Docs = "e:\Vector Field Theory\VFT Docs\_VFT MD"

# Find files modified in the last 15 minutes (covering the conversion time)
$RecentFiles = Get-ChildItem -Path $MD_Docs -Recurse -Filter "*.md" | Where-Object { $_.LastWriteTime -gt (Get-Date).AddMinutes(-20) }

$Summaries = @()

foreach ($File in $RecentFiles) {
    # Read first 10 lines
    $Content = Get-Content $File.FullName -TotalCount 10
    $Preview = $Content -join "`n"
    
    # Determine Category relative to _VFT MD
    $RelativePath = $File.FullName.Substring($MD_Docs.Length)
    if ($RelativePath.StartsWith("\")) { $RelativePath = $RelativePath.Substring(1) }
    $Category = [System.IO.Path]::GetDirectoryName($RelativePath)
    
    $Summaries += [PSCustomObject]@{
        Name     = $File.Name
        Category = $Category
        Preview  = $Preview
        Path     = $RelativePath
    }
}

$Summaries | ConvertTo-Json -Depth 2
