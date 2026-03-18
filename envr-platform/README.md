# ENVR Platform

Branch URLs on GitHub: `https://github.com/shellworlds/REPO/tree/BRANCH` (include **tree**). Not `.../ZENVR/ZENVR91`. See docs/URL_FORMAT_AND_ACCESS.md.

Lenovo ThinkPad Ubuntu primary. See INDEX.md, POC_REPORT.md, REPO_MATRIX.md.

Quick start:

```bash
./step-01/system_check.sh
sudo ./scripts/install_all_ubuntu.sh
./scripts/verify_toolchain.sh
pip3 install -r src/requirements.txt --user
cd src && npm install && node server.js
go run main.go
javac Hello.java && java Hello
g++ -std=c++17 -o probe main.cpp && ./probe
python3 main.py
```

Public GitHub (shellworlds): run `gh auth login` then `./scripts/setup_shellworlds_public_all.sh`. URLs in PUBLIC_SHELLWORLDS_URLS.md.
