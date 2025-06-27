# Erstellt lokale .env aus Vorlage
if (-not (Test-Path ".env") -and (Test-Path ".env.template")) {
    Copy-Item ".env.template" ".env"
    Write-Host ".env wurde erstellt."
} else {
    Write-Host ".env ist vorhanden oder keine Vorlage."
}
