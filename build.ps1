# Build script for Book of Verse PDF
# PowerShell script for Windows

param(
    [switch]$Clean,
    [switch]$PreprocessOnly,
    [switch]$PrintReady,
    [string]$Output = ""
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Paths
$DocsDir = Join-Path $ScriptDir "..\verse-book-source\docs"
$BuildDir = Join-Path $ScriptDir "build"
$TemplateDir = Join-Path $ScriptDir "templates"
$OutputDir = Join-Path $ScriptDir "output"
$ScriptsDir = Join-Path $ScriptDir "scripts"

# Ensure directories exist
New-Item -ItemType Directory -Force -Path $BuildDir | Out-Null
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

if ($Clean) {
    Write-Host "Cleaning build directory..." -ForegroundColor Yellow
    Remove-Item -Path "$BuildDir\*" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "$OutputDir\*" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Clean complete." -ForegroundColor Green
    exit 0
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Building Book of Verse PDF" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Step 1: Check prerequisites
Write-Host "`n[1/4] Checking prerequisites..." -ForegroundColor Yellow

$missingTools = @()

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    $missingTools += "Python 3"
}

if (-not (Get-Command pandoc -ErrorAction SilentlyContinue)) {
    $missingTools += "Pandoc"
}

if (-not (Get-Command xelatex -ErrorAction SilentlyContinue)) {
    $missingTools += "XeLaTeX (TeX Live or MiKTeX)"
}

if ($missingTools.Count -gt 0) {
    Write-Host "`nMissing required tools:" -ForegroundColor Red
    foreach ($tool in $missingTools) {
        Write-Host "  - $tool" -ForegroundColor Red
    }
    Write-Host "`nPlease install the missing tools and try again." -ForegroundColor Red
    Write-Host "See README.md for installation instructions." -ForegroundColor Yellow
    exit 1
}

Write-Host "All prerequisites found." -ForegroundColor Green

# Step 2: Preprocess markdown
Write-Host "`n[2/4] Preprocessing markdown files..." -ForegroundColor Yellow

$preprocessScript = Join-Path $ScriptsDir "preprocess.py"
$combinedMd = Join-Path $BuildDir "combined.md"

python $preprocessScript $DocsDir $combinedMd

if ($LASTEXITCODE -ne 0) {
    Write-Host "Preprocessing failed!" -ForegroundColor Red
    exit 1
}

Write-Host "Preprocessing complete: $combinedMd" -ForegroundColor Green

if ($PreprocessOnly) {
    Write-Host "`nPreprocessing only - stopping here." -ForegroundColor Yellow
    exit 0
}

# Step 3: Convert to LaTeX with Pandoc
Write-Host "`n[3/4] Converting to PDF with Pandoc..." -ForegroundColor Yellow

if ($PrintReady) {
    $template = Join-Path $TemplateDir "print-ready.tex"
    if (-not $Output) { $Output = "output\BookOfVerse-print.pdf" }
    Write-Host "  Using print-ready template (crop marks, bleed)" -ForegroundColor Yellow
} else {
    $template = Join-Path $TemplateDir "pandoc-template.tex"
    if (-not $Output) { $Output = "output\BookOfVerse.pdf" }
}
$outputPdf = Join-Path $ScriptDir $Output

# Pandoc options for high-quality output
$pandocArgs = @(
    $combinedMd,
    "-o", $outputPdf,
    "--template=$template",
    "--pdf-engine=xelatex",
    "--toc",
    "--toc-depth=3",
    "--number-sections",
    "--top-level-division=chapter",
    "--highlight-style=tango",
    "--variable=date:$(Get-Date -Format 'MMMM yyyy')",
    "--metadata=title:Book of Verse",
    "--metadata=author:Tim Sweeney and the Verse Team",
    "-V", "documentclass=book",
    "-V", "papersize=letter",
    "-V", "fontsize=11pt"
)

Write-Host "Running: pandoc $($pandocArgs -join ' ')" -ForegroundColor DarkGray

& pandoc @pandocArgs

if ($LASTEXITCODE -ne 0) {
    Write-Host "PDF generation failed!" -ForegroundColor Red
    exit 1
}

# Step 4: Verify output
Write-Host "`n[4/4] Verifying output..." -ForegroundColor Yellow

if (Test-Path $outputPdf) {
    $fileInfo = Get-Item $outputPdf
    $sizeMB = [math]::Round($fileInfo.Length / 1MB, 2)
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "  Build Successful!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Output: $outputPdf" -ForegroundColor White
    Write-Host "Size: $sizeMB MB" -ForegroundColor White
} else {
    Write-Host "Output file not found!" -ForegroundColor Red
    exit 1
}
