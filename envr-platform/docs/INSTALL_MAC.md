# Apple Mac

Install Homebrew if missing: https://brew.sh

```bash
brew install python@3.12 node go openjdk git curl rsync jq
xcode-select --install
```

Copy `envr-platform` tree. Run `bash step-01/system_check.sh` (Linux-oriented sections may need adaptation; use `sysctl hw.memsize` and `system_profiler SPHardwareDataType` for Mac-specific reports).
