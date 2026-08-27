# Stage 3 — package the analysis as a container application

Start from the verified uv project and give the agent `prompts/02-containerize.md`. Review the proposed Dockerfile before building.

The agent decides the exact CLI flag names and the default input filename
while preserving whatever the original script already used, so don't assume
they match another run of this lesson. Steps 2 and 3 below are written
generically for that reason — substitute the placeholders with what your
agent actually produced.

## 1. Build

```powershell
docker build -t mels-icecream:lesson .
```

Note that `mels-icecream:lesson` is just a local tag; call it whatever you like.


Linux note:
You might need to add the sudo command before docker.


## 2. Discover the application contract

Before mounting anything, ask the image itself what it expects — flag names,
defaults, and required inputs are whatever the agent preserved from the
original script, not a fixed convention:

```powershell
docker run --rm mels-icecream:lesson --help
```

Note from the output:
- the default/expected input file name (e.g. `MelsIceCreamHabits.csv`, `data.csv`, ...)
- the flag (or positional argument) used to pass the input path
- the flag used to choose an output directory, if any
- any other overridable parameters (e.g. a prediction temperature)

## 3. Run the container you have built

A container's filesystem is isolated from the host by default — it can only
see paths you explicitly connect with a **bind mount** via `-v` (or
`--mount`). This is how *any* containerized application, not just this one,
exchanges files with the outside world:

```
-v <host-path>:<container-path>[:ro]
```

- `<host-path>` is a real directory on your machine; you choose it.
- `<container-path>` is fixed by the image (whatever the `Dockerfile`/app
  expects, e.g. `/data/input`) — check step 2's `--help` output or the
  project's docs if it isn't obvious.
- `:ro` makes the mount read-only *inside the container*; omit it for a
  writable mount. Use `:ro` for inputs you don't want the process to touch,
  and leave outputs writable.
- You pass one `-v` flag per directory (or file) you want to expose; a
  container with no `-v` flags at all cannot read or write anything on the
  host.

Applying that pattern here: place the real input file inside a local `data/`
directory first (it must match the exact name the container expects from
step 2), and create an `outputs/` directory for results.

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

The container reads its input CSV from `/data/input` and writes its output
files under `/data/output`. The input mount is read-only. No host Python or
venv is used. If the default command doesn't already write into
`/data/output`, pass the output flag you found in step 2 explicitly (see
below).

Override the parameters after the image name, using the exact flag names
from step 2 (do not assume `--input`/`--output`/`--predict-temperature` —
substitute whatever your `--help` output showed). Because `<container-path>`
is fixed by the image, only the CLI arguments change between runs — the `-v`
mounts stay the same:

```powershell
docker run --rm -v "${PWD}/data:/data/input:ro" -v "${PWD}/outputs:/data/output" mels-icecream:lesson <input-path-or-flag> <output-dir-flag> /data/output <other-flag> 35
```

## 4. Inspect the application contract

```powershell
docker run --rm mels-icecream:lesson --help
docker image inspect mels-icecream:lesson
```

- Which host paths can the process read and write?
- Which environment layers are now inside the image?
- Why are the CSV and outputs outside it?
- What flexibility of an interactive Python environment has been intentionally removed?
- What image identifier would be needed to reproduce this exact build later?
- Do this project's actual override flags match the placeholders above, or did the agent preserve different names from the original script?
