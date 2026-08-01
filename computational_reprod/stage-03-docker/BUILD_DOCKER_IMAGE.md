# Build the Docker image

## Prerequisite

Install and start [Docker Desktop](https://www.docker.com/products/docker-desktop/). In the VS Code terminal, check that Docker is available:

```powershell
docker --version
```

## Build the image

Open `stage-03-docker` as the current folder in VS Code, or move into it from the tutorial root:

```powershell
cd stage-03-docker
```

Build the image and give it the name `mels-icecream` with the tag `lesson`:

```powershell
docker build -t mels-icecream:lesson .
```

The final `.` tells Docker to use the current folder as the build context. Docker reads the `Dockerfile` and copies the required project files from this folder into the image. The first build may take several minutes because Docker must download the base images and install the locked dependencies.

Confirm that the image was created:

```powershell
docker image ls mels-icecream
```

## Test the image

Create the output folder and run the analysis:

```powershell
New-Item -ItemType Directory -Force outputs | Out-Null
docker run --rm `
  -v "${PWD}/data:/data/input:ro" `
  -v "${PWD}/outputs:/data/output" `
  mels-icecream:lesson
```

The container reads `data/data.csv` through the read-only input mount and writes the result files to `outputs/`. The `--rm` option removes the stopped container after the analysis, but it does not delete the image or the output files.

To rebuild after changing the code or dependencies, run the same `docker build` command again.
