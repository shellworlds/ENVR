# Lenovo ThinkPad, Ubuntu Linux

```bash
sudo apt update
cd /path/to/ITMISAE/envr-platform
chmod +x scripts/install_all_ubuntu.sh scripts/verify_toolchain.sh step-01/system_check.sh
./scripts/install_all_ubuntu.sh
./scripts/verify_toolchain.sh
./step-01/system_check.sh | tee reports/latest-system.txt
```

AMD Gen5 class machines: 32 GB RAM and 1 TB NVMe are sufficient for parallel Node, Java, and Go builds.
