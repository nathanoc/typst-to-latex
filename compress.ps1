$guid = New-Guid

$compress = @{
    Path = "src/typst_to_latex/*"
    CompressionLevel = "Fastest"
    "DestinationPath" = "temp-$($guid).zip"
}

Compress-Archive @compress

if (Test-Path "typst_to_latex.ankiaddon") {
    Remove-Item "typst_to_latex.ankiaddon"
}

Rename-Item "temp-$($guid).zip" "typst_to_latex.ankiaddon"