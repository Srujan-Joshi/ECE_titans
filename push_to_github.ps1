# Push to GitHub for Srujan-Joshi
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host " SENTINEL-X 1A: Push to GitHub Repository for Srujan-Joshi" -ForegroundColor Cyan
Write-Host "====================================================================="

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Git is not installed or not in your PATH." -ForegroundColor Red
    Write-Host "Download Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "Or install GitHub Desktop: https://desktop.github.com/" -ForegroundColor Yellow
    exit 1
}

$repoName = "sentinel-x-threat-fusion"
Write-Host "[1/5] Initializing Git repository..." -ForegroundColor Green
git init

Write-Host "[2/5] Staging files..." -ForegroundColor Green
git add .

Write-Host "[3/5] Creating commit..." -ForegroundColor Green
git commit -m "feat: complete frontend, backend, and open benchmarks for SENTINEL-X 1A"

Write-Host "[4/5] Setting branch to main and linking origin..." -ForegroundColor Green
git branch -M main
git remote remove origin 2>$null
git remote add origin "https://github.com/Srujan-Joshi/$repoName.git"

Write-Host "[5/5] Pushing to https://github.com/Srujan-Joshi/$repoName.git ..." -ForegroundColor Green
git push -u origin main
