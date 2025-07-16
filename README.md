# dockgen

Generate fresh docker images

## Usage

```
usage: dockgen [-h] [-f FILE] [-q] [-v] [--token TOKEN] [--work-dir WORK_DIR]
               [--from FROM] [-o OUTPUT] [--jobs JOBS] [--build] [--name NAME]

Generate fresh docker images

options:
  -h, --help           show this help message and exit
  -f, --file FILE      Configuration file
  -q, --quiet          decrement verbosity level
  -v, --verbose        increment verbosity level
  --token TOKEN        Forge API token. Can be specified via `GITHUB_TOKEN` or `GITHUB_TOKEN_CMD`
  --work-dir WORK_DIR
  --from FROM          Base docker image
  -o, --output OUTPUT  Output Dockerfile
  --jobs JOBS          Number of build jobs
  --build              Build the docker image
  --name NAME          Docker image name
```

## Example

For the [eigenpy](https://github.com/stack-of-tasks/eigenpy) project, you can add a `dockgen.toml` with:
```toml
[jrl-cmakemodules]
url = "github:jrl-umi3218"

[eigenpy]
url = "."
apt_deps = ["libboost-all-dev", "libeigen3-dev", "python3-numpy", "python3-scipy"]
src_deps = ["jrl-cmakemodules"]
```
