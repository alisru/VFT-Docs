# Move 42 Files
$vftRoot = "e:\Vector Field Theory\VFT Docs"
$summaryPath = Join-Path $vftRoot "file_summaries.md"
$content = Get-Content $summaryPath -Raw

# Define Moves
$moves = @(
    @{ Pattern = "*Framework for the Judgment*"; Dest = "Actualism\Judgement" },
    @{ Pattern = "*Social Physics*"; Dest = "Actualism\Society" },
    @{ Pattern = "*Landscape of Social Reality*"; Dest = "Actualism\Society" },
    @{ Pattern = "*proofs of QI*"; Dest = "Actualism\Physics" },
    @{ Pattern = "*Experimental Validation*"; Dest = "Actualism\Physics" },
    @{ Pattern = "*pls remove*"; Dest = "_Archive\Drafts" },
    @{ Pattern = "*review this theory*"; Dest = "_Archive\Drafts" },
    @{ Pattern = "*Complete File Catalog*"; Dest = "WWSUTRU\CoreTools" },
    @{ Pattern = "*The_Theory_of_Everything*"; Dest = "Actualism" }
)

$srcDir = Join-Path $vftRoot "Actualism\42"

foreach ($move in $moves) {
    $destDir = Join-Path $vftRoot $move.Dest
    if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null }
    
    # Get File via Pattern (handling special chars by using wildcard on partials if needed, matching user pattern)
    $files = Get-ChildItem -Path $srcDir -Filter $move.Pattern
    
    foreach ($file in $files) {
        $destPath = Join-Path $destDir $file.Name
        Move-Item -Path $file.FullName -Destination $destPath -Force
        Write-Host "Moved $($file.Name) to $($move.Dest)"
        
        # Update Global Summary
        # Use simple string replace for path if we catch it, matching filename
        # Regex escape filename for safety
        $safeName = [regex]::Escape($file.Name)
        # Try to find the summary block
        # Because filename chars might differ in summary vs disk (colons), try matching by significant part?
        # Or just use the SafeName first.
        $regex = "(?s)### .*?$safeName.*?\r?\n(.*?)(?=\r?\n### |\z)"
        if ($content -match $regex) {
            # We found it exactly
            $block = $matches[0]
            $newPathLine = "**Path**: ``$($move.Dest)\$($file.Name)``"
             
            # Replace path line in block
            $lines = $block -split "\r?\n"
            $newLines = @()
            foreach ($line in $lines) {
                if ($line -match '\*\*Path\*\*: `') { $newLines += $newPathLine }
                else { $newLines += $line }
            }
            $newBlock = $newLines -join [Environment]::NewLine
            $content = $content.Replace($block, $newBlock)
        }
        
        # Add Placeholder to Dest README
        $destReadme = Join-Path $destDir "README.md"
        $entry = "${docnl}### $($file.Name)${docnl}(Summary missing)${docnl}${docnl}---${docnl}${docnl}"
        if (Test-Path $destReadme) {
            Add-Content -Path $destReadme -Value $entry -Encoding UTF8
        }
        else {
            # Create if needed
            Set-Content -Path $destReadme -Value "# $($move.Dest | Split-Path -Leaf) - Content Summaries`r`n`r`n## Files`r`n`r`n$entry" -Encoding UTF8
        }
    }
}

# Save Global Summary
$content | Out-File -FilePath $summaryPath -Encoding UTF8
Write-Host "Updated file_summaries.md"

# Populate 42 README with remaining files placeholders
$readme42 = Join-Path $srcDir "README.md"
$remaining = Get-ChildItem -Path $srcDir -Filter "*.docx"
$text = "# The 42 Framework`r`n`r`n## Files`r`n`r`n"
foreach ($f in $remaining) {
    $text += "### $($f.Name)`r`n(Summary missing)`r`n`r`n---`r`n`r`n"
}
$text | Out-File -FilePath $readme42 -Encoding UTF8
Write-Host "Reset 42 README"
