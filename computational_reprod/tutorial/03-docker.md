# Stage 3 — package the analysis as a container application

Start from the verified uv project and give the agent `prompts/02-containerize.md`. Review the proposed Dockerfile before building.

## 1. Build

```powershell
docker build -t mels-icecream:lesson .
```

## 2. Run through the boundary

PowerShell:

```powershell
New-Item -ItemType Directory -Force outputs | Out-Null
docker run --rm `
  -v "${PWD}/data:/data/input:ro" `
  -v "${PWD}/outputs:/data/output" `
  mels-icecream:lesson
```

Bash:

```bash
mkdir -p outputs
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "$PWD/data:/data/input:ro" \
  -v "$PWD/outputs:/data/output" \
  mels-icecream:lesson
```

The container reads `/data/input/data.csv` and writes four files under `/data/output`. The input mount is read-only. No host Python or venv is used.

Override the parameters after the image name:

```powershell
docker run --rm -v "${PWD}/data:/data/input:ro" -v "${PWD}/outputs:/data/output" mels-icecream:lesson --input /data/input/data.csv --output /data/output --predict-temperature 35
```

## 3. Inspect the application contract

```powershell
docker run --rm mels-icecream:lesson --help
docker image inspect mels-icecream:lesson
```

- Which host paths can the process read and write?
- Which environment layers are now inside the image?
- Why are the CSV and outputs outside it?
- What flexibility of an interactive Python environment has been intentionally removed?
- What image identifier would be needed to reproduce this exact build later?
