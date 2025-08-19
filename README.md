# GW2 Random Build Generator

A web app that generates random Guild Wars 2 builds for PvP.


## Local development

Requirements:
- Python 3.11+

Install and run:
```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
set PORT=64429 # PowerShell: $env:PORT=64429
uvicorn server:app --host 0.0.0.0 --port %PORT% --reload
```
Open http://127.0.0.1:64429/

## Docker

Build and run:
```bash
docker build -t gw2-randomizer .
docker run --rm -e -p 64429:64429 gw2-randomizer
```
Open http://127.0.0.1:64429/

## Repo layout
- `server.py`: FastAPI app and API routes
- `static/index.html`: Single-page UI
- `buildgen.py`, `gw2APIdicts.py`: Build generation and chat link encoder inputs

