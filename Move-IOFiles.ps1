# Move-IOFiles.ps1

$IO = "e:\Vector Field Theory\VFT Docs\io"
$Docs = "e:\Vector Field Theory\VFT Docs"

# Define mappings
$Moves = @{
    "Actualism_ 7x7x7 Analysis The Conceptual Framework v2(1).docx"                                                                                            = "Actualism"
    "Actualism_ 7x7x7 Analysis The Conceptual Framework v2.docx"                                                                                               = "Actualism"
    "The Triadic Matrix.docx"                                                                                                                                  = "Actualism"
    
    "The Psochic Hegemony_ Brief.docx"                                                                                                                         = "Actualism\Hegemony"
    "The Psochic Hegemony_ Definition & Mechanics(1).docx"                                                                                                     = "Actualism\Hegemony"
    "The Psochic Hegemony_ Definition & Mechanics(2).docx"                                                                                                     = "Actualism\Hegemony"
    "The Psochic Hegemony_ Definition & Mechanics.docx"                                                                                                        = "Actualism\Hegemony"
    "How to Draw the Hegemony Graph.docx"                                                                                                                      = "Actualism\Hegemony"
    "HEGEMONIC STRATEGIC INTERFACE (HSI) v5.6 _ TYRANNY CHECK.docx"                                                                                            = "Actualism\Hegemony"
    "Role_ Psochic Hegemony Engine.docx"                                                                                                                       = "Actualism\Hegemony"
    
    "The Alethekanon Master Judgment Protocol v2,7.docx"                                                                                                       = "Actualism\Judgement"
    "The Alethekanon Master Judgment Protocol v2.8.docx"                                                                                                       = "Actualism\Judgement"
    
    "The 16 Pessimisms_ An Architecture of Entropy.docx"                                                                                                       = "Actualism\Pessimism"
    "The 16 Pessimisms_ The Integrated Architecture.docx"                                                                                                      = "Actualism\Pessimism"
    "The Hydra Protocol_ Pessimism & The Cauterizing Truth.docx"                                                                                               = "Actualism\Pessimism"
    
    "The 7 Sins & Virtues_ A Plane-by-Plane Breakdown.docx"                                                                                                    = "Actualism\Morality"
    "The 7 Sins and Virtues_ Plane State Mapping.docx"                                                                                                         = "Actualism\Morality"
    
    "Alethekanon Integrated Directives v24.7.docx"                                                                                                             = "Actualism\Theology & Spirituality"
    "Alethekanon Scribe Protocol.docx"                                                                                                                         = "Actualism\Theology & Spirituality"
    "Etemenanki Construction & Ark Protocol.docx"                                                                                                              = "Actualism\Theology & Spirituality"
    "The Geometry of Truth_ Ancient vs Modern Cosmology.docx"                                                                                                  = "Actualism\Theology & Spirituality"
    
    "The Vector Field Hypothesis_ A Unified Model of Reality.docx"                                                                                             = "Actualism\Truth"
    "The VFT System Key Registry_ The 5 Permissions.docx"                                                                                                      = "Actualism\Truth"
    
    "The Speciography of the Abyss_ A Taxonomy of Nets(1).docx"                                                                                                = "Actualism\Matrix"
    "The Speciography of the Abyss_ A Taxonomy of Nets.docx"                                                                                                   = "Actualism\Matrix"
    
    "Analysis_ The Big Four_s Big Bet (Class War Edition).docx"                                                                                                = "WWSUTRU"
    "Analysis_ The Big Four_s Big Bet (Forensic Edition).docx"                                                                                                 = "WWSUTRU"
    "Analysis_ The Big Four_s Big Bet (Humanized Edition).docx"                                                                                                = "WWSUTRU"
    "Analysis_ The Big Four_s Big Bet (Red Pill Edition).docx"                                                                                                 = "WWSUTRU"
    "Article_The Banking Hostage Crisis v2.docx"                                                                                                               = "WWSUTRU"
    "The Banking Hostage Crisis.docx"                                                                                                                          = "WWSUTRU"
    "Hegemonic Analysis of Trump_s Foreign Influence.docx"                                                                                                     = "WWSUTRU"
    "Investigative Report_ The Manchurian Executive.docx"                                                                                                      = "WWSUTRU"
    "The Sewell Report.docx"                                                                                                                                   = "WWSUTRU"
    "The Synchronous Failure Protocol_ A Diachronic Analysis of State Collapse Vectors and their Convergent Application to the United States (2025–2026).docx" = "WWSUTRU"
    "The Vanguard Thesis_ Earth vs. The Board.docx"                                                                                                            = "WWSUTRU"
    "Version Comparison.docx"                                                                                                                                  = "WWSUTRU"
}

foreach ($File in $Moves.Keys) {
    $Source = Join-Path $IO $File
    $Category = $Moves[$File]
    $DestDir = Join-Path $Docs $Category
    $Dest = Join-Path $DestDir $File

    if (Test-Path $Source) {
        if (-not (Test-Path $DestDir)) {
            New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
        }
        
        Move-Item -Path $Source -Destination $Dest -Force
        Write-Host "Moved: $File -> $Category" -ForegroundColor Green
    }
    else {
        Write-Warning "File not found: $File"
    }
}
