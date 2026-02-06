# Convert Shadow Repo (Docx to MD) using Pandoc
param(
    [string]$SourceRoot = "e:\Vector Field Theory\VFT Docs",
    [string]$DestRoot = "e:\Vector Field Theory\VFT Docs\_VFT MD",
    [string[]]$Excludes = @("_VFT MD", ".git", ".vs", "node_modules", "bin", "obj")
)

# Function to repair content after Pandoc
function Repair-MarkdownMath {
    param([string]$FilePath)
    
    if (-not (Test-Path $FilePath)) { return }
    
    $content = Get-Content -Path $FilePath -Raw -Encoding UTF8
    if ([string]::IsNullOrWhiteSpace($content)) { return }
    
    # Regex to find CodeCogs image links
    # Pattern looks for: [![](media/image...)...](https://www.codecogs.com/eqnedit.php?latex=...#0)
    # matching strictly on the CodeCogs base URL
    # Improved to handle Pandoc attributes {width=...}
    
    $pattern = '\[!\[.*?\]\(.*?\).*?\]\(https://www\.codecogs\.com/eqnedit\.php\?latex=([^)#]+).*?\)'
    
    # We use a MatchEvaluator to decode the URI component
    $evaluator = { param($match) 
        $encodedLatex = $match.Groups[1].Value
        try {
            $decoded = [uri]::UnescapeDataString($encodedLatex)
            # Return as inline math
            return " $$ " + $decoded + " $$ "
        }
        catch {
            return $match.Value # Fallback if decode fails
        }
    }
    
    $newContent = [regex]::Replace($content, $pattern, $evaluator)
    
    if ($newContent -ne $content) {
        $newContent | Out-File -FilePath $FilePath -Encoding UTF8 -Force
        Write-Host "      - Fixed Math Equations" -ForegroundColor Gray
    }
}

Write-Host "Starting Shadow Sync with Pandoc..." -ForegroundColor Cyan
Write-Host "Source: $SourceRoot"
Write-Host "Dest:   $DestRoot"

# Ensure pandoc is available or warn
if (-not (Get-Command "pandoc" -ErrorAction SilentlyContinue)) {
    Write-Error "Pandoc is not installed or not in PATH. Please install Pandoc to continue."
    exit 1
}

# 1. Get all files in source, filtering out excluded directories
#    We use a more robust exclusion check on the FullName
$files = Get-ChildItem -Path $SourceRoot -Recurse -Force | Where-Object {
    $itemPath = $_.FullName
    $relPath = $itemPath.Substring($SourceRoot.Length)
    
    # Check if any part of the path matches an exclude item
    # This prevents recursing into the destination folder if it sits inside source
    $shouldSkip = $false
    foreach ($ex in $Excludes) {
        $escaped = [regex]::Escape($ex)
        if ($relPath -match "\\$escaped(\\|`$)") { 
            $shouldSkip = $true
            break 
        }
    }
    return -not $shouldSkip
}

$count = 0
$total = $files.Count

foreach ($item in $files) {
    try {
        $relPath = $item.FullName.Substring($SourceRoot.Length)
        if ($relPath.StartsWith("\")) { $relPath = $relPath.Substring(1) }
        
        # Sanitize the relative path for the destination
        # We process segment by segment to avoid breaking directory separators could be complex
        # Simpler approach: Reconstruct the dest path using the item's relative directory and a sanitized filename
        
        $itemDirName = [System.IO.Path]::GetDirectoryName($relPath)
        $itemFileName = [System.IO.Path]::GetFileName($item.FullName)
        
        # Replace invalid chars in filename with ' - ' or similar
        # Invalid chars: < > : " / \ | ? * and any control chars
        # We'll use a more aggressive regex: Replace anything that isn't a safe char
        # Safe chars: Alphanumeric, space, dot, underscore, hyphen, parentheses, brackets, comma
        # Actually, let's just strip specific known bads and then anything non-ascii if needed, but unicode is fine usually.
        # The main issue is likely the Colon.
        
        $safeFileName = $itemFileName 
        $safeFileName = $safeFileName -replace '[:：]', ' - '  # Standard and Fullwidth Colon
        $safeFileName = $safeFileName -replace '[<>"/\\|?*]', '-' 
        $safeFileName = $safeFileName -replace '\s+', ' '     # Collapse spaces
        $safeFileName = $safeFileName.Trim()
        
        # Rebuild relative path
        if ($itemDirName) {
            $destRelPath = Join-Path $itemDirName $safeFileName
        }
        else {
            $destRelPath = $safeFileName
        }
        
        $destPath = Join-Path $DestRoot $destRelPath
        
        # Handle Directories
        if ($item.PSIsContainer) {
            if (-not (Test-Path $destPath)) {
                # Write-Host "Creating Directory: $relPath" -ForegroundColor DarkGray
                New-Item -ItemType Directory -Path $destPath -Force | Out-Null
            }
        }
        # Handle Docx Files
        elseif ($item.Extension -eq ".docx" -and $item.Name -notlike "~$*") {
            $mdPath = [System.IO.Path]::ChangeExtension($destPath, ".md")
            
            $doConvert = $true
            if (Test-Path $mdPath) {
                $srcTime = $item.LastWriteTime
                $destTime = (Get-Item $mdPath).LastWriteTime
                # Only convert if source is newer
                if ($destTime -ge $srcTime) { $doConvert = $false }
            }
            
            if ($doConvert) {
                Write-Host "Converting: $relPath" -ForegroundColor Green
                
                # Use Pandoc for conversion
                # -f docx: From docx
                # -t markdown-smart: To markdown (standard, no smart quotes unless requested, but simple markdown is usually better for broad AI comp)
                # --wrap=none: Important! Prevents hard line wrapping which corrupts semantic chunks for AI
                $pandocArgs = @(
                    "-f", "docx",
                    "-t", "markdown+hard_line_breaks-smart",
                    "--wrap=none",
                    "--extract-media=.", 
                    "-o", $mdPath,
                    $item.FullName
                )
                
                # Check for images folder if we extracted media (Pandoc puts them relative to working dir or output)
                # For simplicity in this shadow repo, we might skip media extraction or point it to a specific assets folder
                # Let's strip extract-media for now to keep it simple text-only unless requested, 
                # as handling relative media paths in a shadow repo mirrors can get messy quickly without a dedicated plan.
                # EDIT: User asked for "Shadow copy ... easier for you to read". Text is priority.
                $pandocArgs = @(
                    "-f", "docx",
                    "-t", "markdown+hard_line_breaks-smart",
                    "--wrap=none",
                    "-o", $mdPath,
                    $item.FullName
                )
                
                # Use call operator & which handles array arguments/quoting correctly
                & pandoc @pandocArgs 2>&1 | Out-Null
                
                if ($LASTEXITCODE -ne 0) {
                    Write-Warning "Pandoc failed for: $relPath"
                }
                else {
                    # Header removed per user preference
                    # $header = "# $($item.Name)`n`n*Auto-converted by Pandoc*`n`n--`n`n"
                    # $final = $header + $originalContent
                    # In-place edit isn't needed if we just let Pandoc write it, but Pandoc wrote it to $mdPath already.
                    # The previous logic read it back, added a header, and wrote it out again.
                    # We can just skip this whole block if we don't want the header.
                    # However, keeping the 'success' logic is good.
                     
                    # We just do nothing here as Pandoc already wrote the file.
                    Write-Host "   Converted: $relPath" -ForegroundColor DarkGray
                    
                    # Repair Math
                    Repair-MarkdownMath -FilePath $mdPath
                }
                $count++
            }
        }
    }
    catch {
        Write-Warning "Error processing $($item.FullName): $($_.Exception.Message)"
    }
}

Write-Host "Shadow Sync Complete. Converted $count files." -ForegroundColor Cyan
