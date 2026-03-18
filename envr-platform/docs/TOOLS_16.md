# Sixteen toolchain components

| # | Tool | Role |
|---|------|------|
| 1 | bash | Shell automation and system_check |
| 2 | Python 3 + pip | Scripting, env reports, automation |
| 3 | Node.js + npm | JavaScript runtime, small services |
| 4 | Git | Version control and identity management |
| 5 | OpenSSH client | Remote Git over SSH |
| 6 | curl | HTTP checks and API smoke tests |
| 7 | build-essential (gcc/g++/make) | Native C++ builds |
| 8 | OpenJDK | Java compile and run |
| 9 | golang-go | Go builds and CLIs |
| 10 | docker.io (optional) | Containerized deploy parity |
| 11 | unzip | Archive handling |
| 12 | ca-certificates | TLS for package and Git operations |
| 13 | jq (optional) | JSON in CI scripts |
| 14 | rsync | Asset sync to servers |
| 15 | systemd (OS) | Service scheduling reference |
| 16 | Vite / Next (via npm) | Frontend build stacks when projects add them |

Install batch on Ubuntu: see `scripts/install_all_ubuntu.sh`.
