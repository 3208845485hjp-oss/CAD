param([string]$AutoCAD = 'D:\CAD2024\AutoCAD 2024', [string]$Python = 'python')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot
$exe = Join-Path $AutoCAD 'accoreconsole.exe'
if (-not (Test-Path -LiteralPath $exe)) { throw 'Please pass -AutoCAD with the AutoCAD installation folder.' }
$signature = Get-AuthenticodeSignature -LiteralPath $exe
if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notmatch 'Autodesk') { throw 'An Autodesk-signed console is required.' }
& $Python -m venv (Join-Path $projectRoot '.venv')
if ($LASTEXITCODE) { throw 'Python venv creation failed' }
$venvPython = Join-Path $projectRoot '.venv/Scripts/python.exe'
& $venvPython -m pip install -r (Join-Path $projectRoot 'requirements.txt')
if ($LASTEXITCODE) { throw 'Dependency installation failed' }
$codexBase = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$destination = Join-Path $codexBase 'skills/cad-edit'
if (Test-Path -LiteralPath $destination) { throw "Skill already exists: $destination. Keep it or back it up before installing." }
New-Item -ItemType Directory -Path (Split-Path $destination) -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $projectRoot 'skills/cad-edit') -Destination $destination -Recurse
$config = @{accoreconsole=@($exe);prefer_lt=$false;python=$venvPython;project=$projectRoot} | ConvertTo-Json
[IO.File]::WriteAllText((Join-Path $destination 'cadcore.json'), $config)
[IO.File]::WriteAllText((Join-Path $projectRoot 'skills/cad-edit/cadcore.json'), $config)
Write-Host "Installed: $destination"
Write-Host "Python: $venvPython"
Write-Host 'Available on your next Codex turn. Test: scripts/demo.py --out <new-folder>'
