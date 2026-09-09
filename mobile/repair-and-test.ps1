$ErrorActionPreference = "Stop"
Write-Host "MediCare AI mobile verification" -ForegroundColor Cyan
if (-not (Test-Path package.json)) { throw "Run this script from the mobile folder." }
if (Test-Path node_modules) { Remove-Item -Recurse -Force node_modules }
if (Test-Path package-lock.json) { Remove-Item -Force package-lock.json }
npm install
npm run typecheck
npx --yes expo-doctor
Write-Host "MediCare AI mobile verification completed." -ForegroundColor Green
