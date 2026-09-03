# GPU Log Analyzer

## What it does
The GPU Log Analyzer reads a log file and counts entries with the levels `ERROR`, `WARNING`, and `INFO`. Level matching is case-insensitive and ignores surrounding whitespace. Unknown levels and malformed lines are ignored.

## Supported log format
Each input line must follow:

```text
LEVEL: message
```
Supported levels are ERROR, WARNING, and INFO.

## Run it

```powershell
python -m src.gpu_log_analyzer sample.log
```

## JSON output
Use `--json` when another program or CI job needs a machine-readable report:

```powershell
python -m src.gpu_log_analyzer --json sample.log
```

Example output:
```json
{"ERROR": 1, "WARNING": 1, "INFO": 1}
```

JSON output uses the same exit-code rule: the program returns `1` when one or
more ERROR entries exist, otherwise `0`.

## Example

Example `sample.log`:

```text
INFO: ecc is off
WARNING: GPU utilization is high
ERROR: GPU fallen off the bus
```

Expected output:

```text
ERROR: 1
WARNING: 1
INFO: 1
```

## Test it

```powershell
python -m pytest -p no:cacheprovider -q
```

## Current capabilities
Counts ERROR, WARNING, and INFO lines in the log file.

## Current limitations
It expects a simple `LEVEL: message` format and does not yet parse timestamps, GPU IDs, or structured logs.

## Exit codes

- Exit code `0`: the log was read and contains no ERROR entries.
- Exit code `1`: the log was read and contains one or more ERROR entries.
- Exit code `2`: the requested log file does not exist.


```powershell
python -m src.gpu_log_analyzer missing.log
echo $LASTEXITCODE
```


For exit codes `0` and `1`, the tool prints the ERROR, WARNING, and INFO counts.
For exit code `2`, it writes the missing-file diagnostic to standard error and
does not print a report.

## Output file mode

Use `--output <path>` to save the report to a file:

```powershell
python -m src.gpu_log_analyzer sample.log --output report.txt
```

For JSON output:

```powershell
python -m src.gpu_log_analyzer sample.log --json --output report.json
```

File-output mode writes nothing to standard output and retains the same exit-code rules. When `--output` is omitted, the report is printed to the terminal.

## Requirements

- Python 3.14
- pytest 9.1.1 for running tests





