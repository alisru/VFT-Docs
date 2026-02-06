# Sync Documentation (File Version)
$rootSummaryPath = "e:\Vector Field Theory\VFT Docs\file_summaries.md"
$content = Get-Content $rootSummaryPath -Raw

$folders = @("Actualism\Nihilism", "Actualism\Stoicism")

foreach ($folderRelPath in $folders) {
    $folderFullPath = Join-Path "e:\Vector Field Theory\VFT Docs" $folderRelPath
    $readmePath = Join-Path $folderFullPath "README.md"
    
    $folderName = Split-Path $folderRelPath -Leaf
    $nl = [Environment]::NewLine
    $readmeContent = "# $folderName - Content Summaries${nl}${nl}## Files${nl}${nl}"
    
    $files = Get-ChildItem -Path $folderFullPath -Filter "*.docx"
    foreach ($file in $files) {
        $fileName = $file.Name
        $escapedName = [regex]::Escape($fileName)
        $pattern = "(?s)### $escapedName\r?\n(.*?)(?=\r?\n### |\z)"
        $match = [regex]::Match($content, $pattern)
        
        if ($match.Success) {
            $block = $match.Value
            $inner = $match.Groups[1].Value
            
            # 1. Update Path in global content
            $newPathLine = "**Path**: ``$folderRelPath\$fileName``"
            
            $lines = $block -split "\r?\n"
            $newLines = @()
            foreach ($line in $lines) {
                if ($line -match '\*\*Path\*\*: `') {
                    $newLines += $newPathLine
                }
                else {
                    $newLines += $line
                }
            }
            $newBlock = $newLines -join $nl
            
            $content = $content.Replace($block, $newBlock)
            
            # 2. Add to README
            $readmeContent += "### $fileName${nl}$inner${nl}${nl}---${nl}${nl}"
        }
        else {
            Write-Warning "Summary not found for $fileName"
            $readmeContent += "### $fileName${nl}(Summary missing)${nl}${nl}---${nl}${nl}"
        }
    }
    
    $readmeContent | Out-File -FilePath $readmePath -Encoding UTF8
    Write-Host "Updated README for $folderRelPath"
}

$content | Out-File -FilePath $rootSummaryPath -Encoding UTF8
Write-Host "Updated global file_summaries.md"
