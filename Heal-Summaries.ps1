# Heal Missing Summaries
function Get-DocxText {
    param([string]$DocxPath, [int]$MaxChars = 2000)
    $tempDir = Join-Path $env:TEMP ("docx_extract_" + [guid]::NewGuid().ToString())
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
    try {
        $zipPath = Join-Path $tempDir "temp.zip"
        Copy-Item -Path $DocxPath -Destination $zipPath -Force
        Expand-Archive -Path $zipPath -DestinationPath $tempDir -Force
        $docXmlPath = Join-Path $tempDir "word\document.xml"
        if (Test-Path $docXmlPath) {
            [xml]$docXml = Get-Content -Path $docXmlPath -Encoding UTF8
            $nsManager = New-Object System.Xml.XmlNamespaceManager($docXml.NameTable)
            $nsManager.AddNamespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")
            $textNodes = $docXml.SelectNodes("//w:t", $nsManager)
            # Simple space join
            $fullText = ($textNodes | ForEach-Object { $_.InnerText }) -join " "
            # Cleanup
            $fullText = $fullText -replace '\s+', ' '
            if ($fullText.Length -gt $MaxChars) { return $fullText.Substring(0, $MaxChars) }
            return $fullText
        }
        return ""
    }
    catch { return "" }
    finally { if (Test-Path $tempDir) { Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue } }
}

$vftRoot = "e:\Vector Field Theory\VFT Docs"
$readmes = Get-ChildItem -Path "$vftRoot\Actualism" -Recurse -Filter "README.md"

foreach ($readme in $readmes) {
    $content = Get-Content $readme.FullName -Raw
    if ($content -match "\(Summary missing\)") {
        Write-Host "Processing $($readme.FullName)"
        $folderPath = $readme.DirectoryName
        
        # Regex to find blocks with missing summary
        # Pattern: ### (filename) [newline] (Summary missing)
        # We capture filename
        $matches = [regex]::Matches($content, "(?m)^### (.*?)\r?\n\(Summary missing\)")
        
        foreach ($match in $matches) {
            $fileName = $match.Groups[1].Value.Trim()
            $filePath = Join-Path $folderPath $fileName
            
            # Identify file (handle char mismatch if needed, but try exact first)
            $targetFile = $null
            if (Test-Path $filePath) {
                $targetFile = $filePath
            }
            else {
                # Try finding by partial name
                $partial = $fileName
                if ($fileName.Length -gt 15) { $partial = $fileName.Substring(0, 15) }
                $found = Get-ChildItem -Path $folderPath -Filter "*$partial*" | Select-Object -First 1
                if ($found) { $targetFile = $found.FullName }
            }
            
            if ($targetFile) {
                Write-Host "  Generating summary for $fileName"
                $text = Get-DocxText -DocxPath $targetFile
                if ($text) {
                    $summary = "**Summary (Auto-generated)**: " + $text.Substring(0, [Math]::Min(300, $text.Length)) + "..."
                    
                    # Replace in content
                    # We accept the precise string we matched: "(Summary missing)"
                    # We are careful not to replace ALL "(Summary missing)" at once if we want to be specific, 
                    # but actually we are iterating matches.
                    # Better: Replace the specific match block.
                    
                    $block = $match.Value # ### filename \n (Summary missing)
                    $newBlock = "### $fileName`r`n$summary"
                    $content = $content.Replace($block, $newBlock)
                }
                else {
                    Write-Warning "  Could not extract text from $targetFile"
                }
            }
            else {
                Write-Warning "  File not found on disk: $fileName"
            }
        }
        
        $content | Out-File -FilePath $readme.FullName -Encoding UTF8
        Write-Host "  Updated $($readme.Name)"
    }
}
