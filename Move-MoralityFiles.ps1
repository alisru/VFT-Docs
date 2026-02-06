# Move Morality Files and Sync Documentation
$vftRoot = "e:\Vector Field Theory\VFT Docs"
$summaryPath = Join-Path $vftRoot "file_summaries.md"

# Define Moves
$moves = @(
    @{
        File   = "The Solomon-Briggs Moral Type Indicator (SBMTI) V3.0.docx";
        Source = "Actualism\Consciousness";
        Dest   = "Actualism\Morality"
    },
    @{
        File   = "The NEWS Axiom for belief.docx";
        Source = "Actualism\Consciousness";
        Dest   = "Actualism\Morality"
    },
    @{
        File   = "Morality; The Terminal Sanction A Vector Analysis of the Batman-Joker Paradox.docx";
        Source = "Actualism\Nihilism";
        Dest   = "Actualism\Morality"
    },
    @{
        File   = "The Rose Field of Life: An Allegory of the Way v0.5.docx";
        Source = "Actualism\Consciousness";
        Dest   = "Actualism\Theology & Spirituality"
    },
    @{
        File   = "The Rose Field of Life: An Allegory of the Way.docx";
        Source = "Actualism\Consciousness";
        Dest   = "Actualism\Theology & Spirituality"
    }
)

# Load Global Summary
$summaryContent = Get-Content $summaryPath -Raw
# Load Source Lists for README Cleanup
$readmeCache = @{}

foreach ($move in $moves) {
    $srcDir = Join-Path $vftRoot $move.Source
    $destDir = Join-Path $vftRoot $move.Dest
    
    # 0. Ensure Dest Exists
    if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null }
    
    # 1. Find and Move File
    $srcPath = Join-Path $srcDir $move.File
    # Handle filename differences
    if (-not (Test-Path $srcPath)) {
        # Try simplified match
        $partial = $move.File.Substring(0, 15)
        $found = Get-ChildItem -Path $srcDir -Filter "*$partial*" | Select-Object -First 1
        if ($found) {
            $srcPath = $found.FullName
            $move.File = $found.Name
        }
        else {
            Write-Warning "File not found: $($move.File) in $($move.Source)"
            continue
        }
    }
    
    $destPath = Join-Path $destDir $move.File
    Move-Item -Path $srcPath -Destination $destPath -Force
    Write-Host "Moved $($move.File) to $($move.Dest)"
    
    # 2. Update Global Summary Path
    $escapedName = [regex]::Escape($move.File)
    $pattern = "(?s)### $escapedName\r?\n(.*?)(?=\r?\n### |\z)"
    $match = [regex]::Match($summaryContent, $pattern)
    
    if ($match.Success) {
        $block = $match.Value
        $inner = $match.Groups[1].Value # Save inner content for README append later?
        
        # New Path line
        $newPath = "$($move.Dest)\$($move.File)"
        $newPathLine = "**Path**: ``$newPath``"
        
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
        $newBlock = $newLines -join [Environment]::NewLine
        $summaryContent = $summaryContent.Replace($block, $newBlock)
        
        # 3. Queue for README updates
        # Remove from Source README
        $srcReadme = Join-Path $srcDir "README.md"
        if (-not $readmeCache.ContainsKey($srcReadme)) {
            if (Test-Path $srcReadme) { $readmeCache[$srcReadme] = Get-Content $srcReadme -Raw }
        }
        if ($readmeCache.ContainsKey($srcReadme)) {
            $srcMatch = [regex]::Match($readmeCache[$srcReadme], $pattern)
            if ($srcMatch.Success) {
                $readmeCache[$srcReadme] = $readmeCache[$srcReadme].Replace($srcMatch.Value, "")
            }
        }
        
        # Add to Dest README
        $destReadme = Join-Path $destDir "README.md"
        if (-not $readmeCache.ContainsKey($destReadme)) {
            if (Test-Path $destReadme) { 
                $readmeCache[$destReadme] = Get-Content $destReadme -Raw 
            }
            else {
                $readmeCache[$destReadme] = "# $($move.Dest | Split-Path -Leaf) - Content Summaries`r`n`r`n## Files`r`n`r`n"
            }
        }
        
        # Check if already exists in dest readme (idempotency)
        if ($readmeCache[$destReadme] -notmatch "### $escapedName") {
            # Copy block from global summary (or just the inner part)
            # Use the $inner content retrieved earlier from global summary
            $readmeCache[$destReadme] += "### $($move.File)`r`n$inner`r`n`r`n---`r`n`r`n"
        }
    }
    else {
        Write-Warning "Summary entry not found for $($move.File)"
    }
}

# Save Updates
$summaryContent | Out-File -FilePath $summaryPath -Encoding UTF8
Write-Host "Updated Global Summary"

foreach ($path in $readmeCache.Keys) {
    # Clean up double separators
    $content = $readmeCache[$path]
    $content = $content -replace "(?s)---\s+---", "---"
    $content | Out-File -FilePath $path -Encoding UTF8
    Write-Host "Updated README: $path"
}
