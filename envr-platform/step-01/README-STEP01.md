# Step 01: Run system check (single step)

## Lenovo ThinkPad, Ubuntu Linux (primary)

Copy-paste in terminal:

```bash
cd /path/to/envr-platform/step-01
chmod +x system_check.sh
./system_check.sh | tee step01-system-report.txt
```

## macOS (reference for other users)

```bash
cd /path/to/envr-platform/step-01
chmod +x system_check.sh
# Script is Linux-oriented; on Mac, install coreutils or adapt paths; optional:
bash system_check.sh 2>/dev/null | tee step01-system-report.txt
```

## Windows (reference)

Use WSL2 Ubuntu, then run the Linux block above. Native CMD is not supported for this shell script.

## After you run Step 01

Reply with confirmation or the saved `step01-system-report.txt` excerpt. Step 02 will only follow your feedback.

## Install prompts (later steps)

Full one-shot install across Python, Node, Java, Go, etc. is deferred until after Step 01 approval, per staged delivery.
