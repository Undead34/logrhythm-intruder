Set-Location $PSScriptRoot

if (Test-Path -Path (Join-Path $PSScriptRoot .\.venv\bin)){
    .\.venv\bin\activate.ps1
} else {
    .\.venv\Scripts\activate.ps1
}

python app.py
