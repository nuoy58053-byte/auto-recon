# Auto-Recon v3.7

**一键自动化渗透测试情报收集工具**（Subfinder + Masscan + Shodan + Nuclei + BloodHound）

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 功能亮点
- Subfinder 子域名枚举
- Masscan 超高速全端口扫描
- Shodan API 情报查询
- Nuclei 全模板漏洞扫描（已解决模板问题）
- BloodHound 内网域控分析（可选）
- 自动生成 Excel 报告

## Docker 一键使用（推荐）

```bash
docker run -it --rm \
  -v $(pwd)/output:/output \
  -e SHODAN_KEY=你的ShodanKey \
  ghcr.io/nuoy58053-byte/auto-recon:latest \
  -t hackerone.com

本地安装使用
git clone https://github.com/nuoy58053-byte/auto-recon.git
cd auto-recon
python3.9 auto_recon.py -t example.com --shodan-key 你的Key
