# Framework Tool

Shared Python development tools for the Framework and its products (ILeague,
IndicatorBlitz). This is a uv project without a package: it has no source code,
is never imported, and only pins tool versions, shared rules, and check scripts.
It was created with `uv init --bare --pin-python --python 3.13`.

| File | Purpose |
| --- | --- |
| `pyproject.toml`, `uv.lock` | Tool versions; currently `ruff==0.17.6` in the `dev` group |
| `ruff.toml` | Shared Ruff rules (`target-version = "py313"`) |
| `scripts/scpt_check_python.ps1` | Windows check script |
| `scripts/scpt_check_python.sh` | macOS check script (zsh; not yet verified on macOS) |

Products and Framework packages do not declare Ruff themselves. Versions are
pinned with `==` and never upgraded implicitly.

To upgrade Ruff, run `uv add --dev "ruff==<version>"` in this directory, then
run the check script against the Framework and every product (`src`). Ruff is
still 0.x: minor releases can change default rules or formatting, so fix or
reformat all repositories in the same change.

## VS Code

The Ruff extension bundles its own Ruff, which changes when the extension
updates. Point it at this project's Ruff in the user settings so the editor and
the check script use the same version (paths differ per machine):

```jsonc
// Windows
"ruff.path": ["D:\\Git\\python-framework\\framework_tool\\.venv\\Scripts\\ruff.exe"]
// macOS
"ruff.path": ["/Users/<user>/<path>/python-framework/framework_tool/.venv/bin/ruff"]
```

Run `uv sync` here first so `.venv` exists.

## Ruff rules

Ruff and the VS Code Ruff extension discover settings from the checked file's
location upward, so each repository keeps a small `ruff.toml` above its packages
that extends this file and adds its own first-party packages for import sorting:

```toml
extend = "<relative path>/framework_tool/ruff.toml"

[lint.isort]
known-first-party = ["<repository packages>", "framework_common"]
```

The Framework's root [`ruff.toml`](../ruff.toml) follows this pattern. Put
rules shared by every repository here; keep only repository-specific settings
in the extending files.

## Checking code

The scripts run Ruff through `uv run --project` against this project, so the
pinned version is used from any directory. `uv` creates this project's `.venv`
on first use.

Windows, from a product root next to `python-framework`:

```powershell
..\python-framework\framework_tool\scripts\scpt_check_python.ps1
..\python-framework\framework_tool\scripts\scpt_check_python.ps1 -Path src\ileague_api
..\python-framework\framework_tool\scripts\scpt_check_python.ps1 -Fix
```

macOS:

```zsh
../python-framework/framework_tool/scripts/scpt_check_python.sh
../python-framework/framework_tool/scripts/scpt_check_python.sh src/ileague_api
../python-framework/framework_tool/scripts/scpt_check_python.sh --fix
```

| Mode | Steps | Modifies files |
| --- | --- | --- |
| Default | `ruff check`, `ruff format --check` | No |
| `-Fix` / `--fix` | `ruff check --fix`, `ruff format` | Yes |

The path defaults to the current directory. Each step runs even if an earlier
one fails; the script exits with 1 when any step fails. Ruff skips `.venv` and
files ignored by Git.

Ruff can also be called directly:

```powershell
uv run --project ..\python-framework\framework_tool ruff check src
```
