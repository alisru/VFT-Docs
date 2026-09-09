# build_dict_js.ps1
# Regenerates qqci_dictionary.js from qqci_dictionary.json
# Run this whenever you update the JSON
$jsonPath = Join-Path $PSScriptRoot "qqci_dictionary.json"
$jsPath = Join-Path $PSScriptRoot "qqci_dictionary.js"
$json = Get-Content $jsonPath -Raw -Encoding UTF8
"// Auto-generated from qqci_dictionary.json -- do not edit directly`n// Run: .\build_dict_js.ps1 to regenerate`nconst QQCI_DICT = $json;" | Set-Content $jsPath -Encoding UTF8
Write-Host "qqci_dictionary.js regenerated OK"


