# Repair Documentation
$vftRoot = "e:\Vector Field Theory\VFT Docs"
$summaryPath = Join-Path $vftRoot "file_summaries.md"
$content = Get-Content $summaryPath -Raw

# Affected Folders
$folders = @(
    "Actualism\Morality",
    "Actualism\Theology & Spirituality",
    "Actualism\Consciousness",
    "Actualism\Nihilism"
)

foreach ($folderRel in $folders) {
    $dir = Join-Path $vftRoot $folderRel
    $readmePath = Join-Path $dir "README.md"
    
    $folderName = Split-Path $folderRel -Leaf
    $nl = [Environment]::NewLine
    $readmeContent = "# $folderName - Content Summaries${nl}${nl}## Files${nl}${nl}"
    
    $files = Get-ChildItem -Path $dir -Filter "*.docx"
    foreach ($file in $files) {
        # Loose match for summary
        $partial = $file.Name.Substring(0, [Math]::Min(15, $file.Name.Length))
        $escapedPartial = [regex]::Escape($partial)
        $pattern = "(?s)### .*?$escapedPartial.*?\r?\n(.*?)(?=\r?\n### |\z)"
        $match = [regex]::Match($content, $pattern)
        
        if ($match.Success) {
            $block = $match.Value
            $inner = $match.Groups[1].Value
            $fullHeader = $block -split "\r?\n" | Select-Object -First 1
            
            # Update Path in Global if needed
            # We assume the match is the right file.
            # Construct new path line
            $newPathLine = "**Path**: ``$folderRel\$($file.Name)``"
            
            # Update the block in global content
            # We need to find the specific line in the *original* block from $content
            if ($inner -notmatch [regex]::Escape($folderRel)) {
                # Update path in global content
                # This is tricky with regex replacement on the big string if multiple matches
                # But we can replace the *block* with a patched version
                
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
                
                # Update inner for README
                $innerMatch = [regex]::Match($newBlock, "(?s)### .*?\r?\n(.*?)(?=\r?\n### |\z)")
                if ($innerMatch.Success) { $inner = $innerMatch.Groups[1].Value }
                Write-Host "Patched path for $($file.Name)"
            }

            $readmeContent += "### $($file.Name)${nl}$inner${nl}${nl}---${nl}${nl}"
        }
        else {
            Write-Warning "Summary not found for $($file.Name)"
            $readmeContent += "### $($file.Name)${nl}(Summary missing)${nl}${nl}---${nl}${nl}"
        }
    }
    
    $readmeContent | Out-File -FilePath $readmePath -Encoding UTF8
    Write-Host "Regenerated README for $folderRel"
}

$content | Out-File -FilePath $summaryPath -Encoding UTF8
Write-Host "Saved Global Summary"
