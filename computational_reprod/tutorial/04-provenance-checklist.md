# Epilogue — the container is not the provenance record

The attached computational-reproducibility lecture treats containers as one useful but incomplete layer. Finish by recording what would be needed to identify this particular run.

## Minimal run record

| Component | Example evidence |
| --- | --- |
| Code | Git commit ID and clean/dirty status |
| Input | Path or dataset identifier plus SHA-256 |
| Parameters | Exact command or machine-readable configuration |
| Local environment | Python version plus `uv.lock` checksum |
| Container environment | Image name plus immutable image digest |
| Outputs | Filenames plus SHA-256 checksums |
| Platform | OS/architecture; CPU/GPU details when numerically relevant |

PowerShell examples:

```powershell
git rev-parse HEAD
git status --short
Get-FileHash data/data.csv -Algorithm SHA256
Get-FileHash uv.lock -Algorithm SHA256
docker image inspect mels-icecream:lesson --format '{{.Id}}'
Get-ChildItem outputs -File | Get-FileHash -Algorithm SHA256
```

The decisive question is not “did Docker run?” but “can another researcher identify the code, data, environment, invocation, and resulting artifacts?”
