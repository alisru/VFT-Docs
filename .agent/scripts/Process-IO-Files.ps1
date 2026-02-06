# Process-IO-Files.ps1

$IO = "e:\Vector Field Theory\VFT Docs\io"
$Docs = "e:\Vector Field Theory\VFT Docs"
$MD_Docs = "e:\Vector Field Theory\VFT Docs\_VFT MD"
$MD_IO = "e:\Vector Field Theory\VFT Docs\_VFT MD\io"

# Define mappings (Mirroring Move-IOFiles.ps1)
$Moves = @{
    "Actualism_ 7x7x7 Analysis The Conceptual Framework v2(1).docx" = "Actualism"
    "Actualism_ 7x7x7 Analysis The Conceptual Framework v2.docx"    = "Actualism"
    "The Triadic Matrix.docx"                                       = "Actualism"
    
    "The Psochic Hegemony_ Brief.docx"                              = "Actualism\Hegemony"
    "The Psochic Hegemony_ Definition & Mechanics(1).docx"          = "Actualism\Hegemony"
    "The Psochic Hegemony_ Definition & Mechanics(2).docx"          = "Actualism\Hegemony"
    "The Psochic Hegemony_ Definition & Mechanics.docx"             = "Actualism\Hegemony"
    "How to Draw the Hegemony Graph.docx"                           = "Actualism\Hegemony"
    "HEGEMONIC STRATEGIC INTERFACE (HSI) v5.6 _ TYRANNY CHECK.docx" = "Actualism\Hegemony"
    "Role_ Psochic Hegemony Engine.docx"                            = "Actualism\Hegemony"
    
    "The Alethekanon Master Judgment Protocol v2,7.docx"            = "Actualism\Judgement"
    "The Alethekanon Master Judgment Protocol v2.8.docx"            = "Actualism\Judgement"
    
    "The 16 Pessimisms_ An Architecture of Entropy.docx"            = "Actualism\Pessimism"
    "The 16 Pessimisms_ The Integrated Architecture.docx"           = "Actualism\Pessimism"
    "The Hydra Protocol_ Pessimism & The Cauterizing Truth.docx"    = "Actualism\Pessimism"
    
    "The 7 Sins & Virtues_ A Plane-by-Plane Breakdown.docx"         = "Actualism\Morality"
    "The 7 Sins and Virtues_ Plane State Mapping.docx"              = "Actualism\Morality"
    
    "Alethekanon Integrated Directives v24.7.docx"                  = "Actualism\Theology & Spirituality"
    "Alethekanon Scribe Protocol.docx"                              = "Actualism\Theology & Spirituality"
    "Etemenanki Construction & Ark Protocol.docx"                   = "Actualism\Theology & Spirituality"
    "The Geometry of Truth_ Ancient vs Modern Cosmology.docx"       = "Actualism\Theology & Spirituality"
    
    "The Vector Field Hypothesis_ A Unified Model of Reality.docx"  = "Actualism\Truth"
    "The VFT System Key Registry_ The 5 Permissions.docx"           = "Actualism\Truth"
    
    "The Speciography of the Abyss_ A Taxonomy of Nets(1).docx"     = "Actualism\Matrix"
    "The Speciography of the Abyss_ A Taxonomy of Nets.docx"        = "Actualism\Matrix"
    
    "Analysis_ The Big Four_s Big Bet (Class War Edition).docx"     = "WWSUTRU"
    "Analysis_ The Big Four_s Big Bet (Forensic Edition).docx"      = "WWSUTRU"
    "Analysis_ The Big Four_s Big Bet (Humanized Edition).docx"     = "WWSUTRU"
    "Analysis_ The Big Four_s Big Bet (Red Pill Edition).docx"      = "WWSUTRU"
    "Article_The Banking Hostage Crisis v2.docx"                    = "WWSUTRU"
    "The Banking Hostage Crisis.docx"                               = "WWSUTRU"
    "Hegemonic Analysis of Trump_s Foreign Influence.docx"          = "WWSUTRU"
    "Investigative Report_ The Manchurian Executive.docx"           = "WWSUTRU"
    "The Sewell Report.docx"                                        = "WWSUTRU"
    "The Vanguard Thesis_ Earth vs. The Board.docx"                 = "WWSUTRU"
    "Version Comparison.docx"                                       = "WWSUTRU"
}

# Handle file with special characters (En-dash) dynamically to avoid script encoding issues
$SpecialFilePattern = "The Synchronous Failure Protocol*.docx"
$SpecialFile = Get-ChildItem -Path $IO -Filter $SpecialFilePattern | Select-Object -ExpandProperty Name -First 1
if ($SpecialFile) {
    $Moves[$SpecialFile] = "WWSUTRU"
}

# Ensure destination directories exist
if (-not (Test-Path $MD_IO)) { New-Item -ItemType Directory -Path $MD_IO -Force | Out-Null }

$ProcessedFiles = @()

foreach ($File in $Moves.Keys) {
    $SourcePath = Join-Path $IO $File
    
    if (Test-Path $SourcePath) {
        $Category = $Moves[$File]
        
        # Paths
        $DestDocxDir = Join-Path $Docs $Category
        $DestDocxPath = Join-Path $DestDocxDir $File
        
        $DestMDDir = Join-Path $MD_Docs $Category
        $FileNameMD = [System.IO.Path]::ChangeExtension($File, ".md")
        $DestMDPath = Join-Path $DestMDDir $FileNameMD
        
        # Check for existing MD in _VFT MD/io (staged) or target
        $ExistingMD_IO = Join-Path $MD_IO $FileNameMD
        
        if (Test-Path $ExistingMD_IO) {
            Write-Host "SKIP CONVERSION: MD already exists in IO mirror: $ExistingMD_IO" -ForegroundColor Yellow
            
            # Ensure target MD dir exists
            if (-not (Test-Path $DestMDDir)) { New-Item -ItemType Directory -Path $DestMDDir -Force | Out-Null }
            
            # Move the existing MD from IO mirror to proper home
            Move-Item -Path $ExistingMD_IO -Destination $DestMDPath -Force
            Write-Host "MOVED EXISTING MD: $FileNameMD -> $Category" -ForegroundColor Cyan
            
            # Add to processed list for summary
            $ProcessedFiles += [PSCustomObject]@{
                OriginalName = $File
                MDPath       = $DestMDPath
                Category     = $Category
            }

        }
        elseif (Test-Path $DestMDPath) {
            Write-Host "SKIP CONVERSION: MD already exists in target: $DestMDPath" -ForegroundColor Yellow
            # Already converted and in place. We should just move the docx if it's there.
            $ProcessedFiles += [PSCustomObject]@{
                OriginalName = $File
                MDPath       = $DestMDPath
                Category     = $Category
            }
        }
        else {
            # CONVERT
            Write-Host "CONVERTING: $File" -ForegroundColor White
             
            # Convert to temp location first or directly to destination? 
            # Let's convert to temp to ensure success
            $TempMD = Join-Path $env:TEMP $FileNameMD
             
            $PandocArgs = @("-f", "docx", "-t", "gfm", "-o", $TempMD, $SourcePath, "--wrap=none")
            $Process = Start-Process -FilePath "pandoc" -ArgumentList $PandocArgs -Wait -PassThru -NoNewWindow
             
            if ($Process.ExitCode -eq 0 -and (Test-Path $TempMD)) {
                # Ensure target MD dir exists
                if (-not (Test-Path $DestMDDir)) { New-Item -ItemType Directory -Path $DestMDDir -Force | Out-Null }
                 
                Move-Item -Path $TempMD -Destination $DestMDPath -Force
                Write-Host "CONVERTED & MOVED MD: $FileNameMD -> $Category" -ForegroundColor Green
                 
                $ProcessedFiles += [PSCustomObject]@{
                    OriginalName = $File
                    MDPath       = $DestMDPath
                    Category     = $Category
                }
            }
            else {
                Write-Error "Pandoc Conversion Failed for $File"
            }
        }
        
        # Move Original DOCX
        if (-not (Test-Path $DestDocxDir)) { New-Item -ItemType Directory -Path $DestDocxDir -Force | Out-Null }
        Move-Item -Path $SourcePath -Destination $DestDocxPath -Force
        Write-Host "MOVED DOCX: $File -> $Category" -ForegroundColor Gray
    }
}

# Output JSON for the agent
$ProcessedFiles | ConvertTo-Json -Depth 2
