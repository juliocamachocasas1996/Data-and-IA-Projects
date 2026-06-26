# Prompt: Bootstrap New IA/Data Science Project (CH Robinson Artifactory)

Use this prompt to create a brand-new Python IA/Data Science project with a standard folder layout, a local virtual environment, and package installation from CH Robinson Artifactory.

## Instructions for Copilot Agent

You are setting up a new Python project on Windows in PowerShell.

### Inputs
- Project root path: <PROJECT_PATH>
- Python venv name: .venv
- Artifactory index URL: https://artifactory.chrobinson.com/artifactory/api/pypi/pypi/simple

### Goal
1. Create the project baseline folder structure.
2. Create and activate a Python virtual environment.
3. Configure pip to use CH Robinson Artifactory for this project.
4. Install the basic starter package set from Artifactory in a single pass.
5. Validate imports and versions.
6. Save a setup log and requirements file.

## Step 1 - Create folder baseline

Create these folders under <PROJECT_PATH>:
- 01_raw_data
- 02_processed_data
- 03_notebooks
- 04_scripts
- 05_reports
- 06_visualizations
- 07_docs
- 08_models
- 09_tests
- local/outputs

PowerShell:

$project = "<PROJECT_PATH>"
$folders = @(
  '01_raw_data','02_processed_data','03_notebooks','04_scripts','05_reports',
  '06_visualizations','07_docs','08_models','09_tests','local/outputs'
)
New-Item -ItemType Directory -Force -Path $project | Out-Null
foreach ($f in $folders) { New-Item -ItemType Directory -Force -Path (Join-Path $project $f) | Out-Null }

## Step 2 - Create virtual environment

PowerShell:

$pythonCmd = 'py -3.13'
Set-Location $project
& $pythonCmd -m venv .venv

$venvPython = Join-Path $project '.venv\Scripts\python.exe'
$venvPip = Join-Path $project '.venv\Scripts\pip.exe'

if (-not (Test-Path $venvPython)) { throw 'Virtual environment creation failed.' }
& $venvPython --version

## Step 3 - Pin pip to Artifactory (project-scoped)

Create/update <PROJECT_PATH>\.pip\pip.ini with:

[global]
index-url = https://artifactory.chrobinson.com/artifactory/api/pypi/pypi/simple
trusted-host = artifactory.chrobinson.com

PowerShell:

$pipDir = Join-Path $project '.pip'
$pipIni = Join-Path $pipDir 'pip.ini'
New-Item -ItemType Directory -Force -Path $pipDir | Out-Null
@"
[global]
index-url = https://artifactory.chrobinson.com/artifactory/api/pypi/pypi/simple
trusted-host = artifactory.chrobinson.com
"@ | Set-Content -Path $pipIni -Encoding ASCII

$env:PIP_CONFIG_FILE = $pipIni

## Step 4 - Install basic starter packages

All eight candidates are confirmed available on Artifactory. Install them in a single pass using wheel-only builds. If Artifactory is unreachable (VPN required), pip will emit a clear connection error — stop and ask the user to connect to VPN before retrying.

PowerShell:

$index = 'https://artifactory.chrobinson.com/artifactory/api/pypi/pypi/simple'
$available = @('pandas','numpy','requests','python-dotenv','tqdm','matplotlib','seaborn','plotly')
$missing = @()

& $venvPip install --only-binary :all: --index-url $index $available
if ($LASTEXITCODE -ne 0) { throw 'Package installation failed. Check VPN connectivity to Artifactory.' }

## Step 5 - Validate environment

IMPORTANT: Do NOT use `& $venvPython -c @"..."@` — PowerShell heredoc piped to -c is unreliable.
Instead, write the validation code to a temporary .py file, run it, then delete it.

PowerShell:

$validateScript = @"
import pandas, numpy, requests, dotenv, tqdm, matplotlib, seaborn, plotly
print('pandas:', pandas.__version__)
print('numpy:', numpy.__version__)
print('requests:', requests.__version__)
print('matplotlib:', matplotlib.__version__)
print('seaborn:', seaborn.__version__)
print('plotly:', plotly.__version__)
print('VALIDATION COMPLETE')
"@
$tmpPy = Join-Path $project 'validate_env_tmp.py'
$validateScript | Set-Content -Path $tmpPy -Encoding ASCII
& $venvPython $tmpPy
Remove-Item $tmpPy

## Step 6 - Save reproducibility files

1) Save requirements lock:

& $venvPip freeze | Set-Content -Path (Join-Path $project 'requirements.txt') -Encoding ASCII

2) Save setup log:

$today = Get-Date -Format 'yyyy-MM-dd'
$log = Join-Path $project "local/outputs/project-bootstrap-$today.txt"
$pyVer = (& $venvPython --version) | Out-String
@"
=== IA/DS Project Bootstrap Log ===
Date: $today
Project: $project
Python: $pyVer
Venv: $venvPython
Index: $index

Installed packages:
$($available -join ', ')

Not found on Artifactory:
$($missing -join ', ')

Result: SUCCESS
"@ | Set-Content -Path $log -Encoding ASCII

## Step 7 - Final output to user

Report:
- Created folders
- Python version
- Installed packages
- Missing packages
- requirements.txt path
- setup log path

## Rules
- Use only the project virtual environment executable for installs and tests.
- Use Artifactory index for all package operations.
- Use wheel-only installs (--only-binary :all:) to avoid local build toolchains.
- Never use `& python -c @"..."@` heredoc — always write Python validation to a temp .py file, run it, then delete it.
- Do not run per-package availability checks before install; install all candidates in one pip call.
- Stop and report clear errors for VPN/connectivity or installation issues.
