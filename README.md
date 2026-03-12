# Auto-Recon v3.7

**一键自动化渗透测试情报收集工具**（Subfinder + Masscan + Shodan + Nuclei + BloodHound）

## 安全使用说明（重要！）
**你的 Shodan Key 永远不会出现在代码或镜像中**，只在运行时通过环境变量传入。

## Docker 一键使用（推荐，最安全）

```bash
# 1. 先创建输出目录
mkdir -p ~/recon_output

# 2. 运行（把 YOUR_SHODAN_KEY_HERE 换成你自己的 Key）
podman run -it --rm \
  -v ~/recon_output:/output \
  -e SHODAN_KEY=YOUR_SHODAN_KEY_HERE \
  ghcr.io/nuoy58053-byte/auto-recon:latest \
  -t hackerone.com
本地运行（同样安全）
Bashpython3.9 auto_recon.py -t hackerone.com --shodan-key YOUR_SHODAN_KEY_HERE
Key 只会留在你自己的机器上，GitHub 上永远看不到。
项目特点

Subfinder 子域名枚举
Masscan 超高速全端口扫描
Shodan API 情报查询
Nuclei 全模板漏洞扫描
BloodHound 内网域控分析（可选）
自动生成 Excel 报告

作者：nuoy58053-byte（基于启明星辰面试第11题自研并开源）
