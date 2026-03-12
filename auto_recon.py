#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化信息收集脚本 v3.7 - 最终增强版（全 http 模板 + 更多结果）
"""

import argparse
import subprocess
import os
import pandas as pd
from datetime import datetime
from shodan import Shodan
import dns.resolver
from bloodhound import BloodHound

def run_command(cmd, desc="执行命令", sudo=False, timeout=1800):
    print(f"[+] {desc}...")
    try:
        if sudo:
            cmd = ["sudo"] + cmd
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0 and result.stderr:
            print(f"[!] 警告：{desc} → {result.stderr[:600]}")
        return result.stdout
    except subprocess.TimeoutExpired:
        print(f"[!] {desc} 超时")
        return ""
    except Exception as e:
        print(f"[!] {desc} 失败：{e}")
        return ""

def resolve_subdomains(subdomains):
    ips = set()
    resolver = dns.resolver.Resolver()
    resolver.timeout = 5
    for sub in subdomains:
        try:
            for rdata in resolver.resolve(sub, 'A'):
                ips.add(str(rdata))
        except:
            pass
    return list(ips)

def main():
    parser = argparse.ArgumentParser(description="自动化信息收集脚本 v3.7")
    parser.add_argument("-t", "--target", required=True, help="目标域名或IP段")
    parser.add_argument("--shodan-key", required=True, help="Shodan API Key")
    parser.add_argument("--rate", type=int, default=3000, help="Masscan速率")
    parser.add_argument("--domain", help="内网域名")
    parser.add_argument("--username", help="域用户名")
    parser.add_argument("--password", help="域密码")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"recon_{args.target.replace('/', '_')}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    print(f"[+] 输出目录：{output_dir}")

    # 1. 子域名
    print("\n=== 步骤1：Subfinder 子域名枚举 ===")
    sub_output = f"{output_dir}/subdomains.txt"
    run_command(["subfinder", "-d", args.target, "-o", sub_output], "Subfinder")
    with open(sub_output, "r") as f:
        subdomains = [line.strip() for line in f if line.strip()]

    # 2. Masscan
    print("\n=== 步骤2：Masscan 全端口扫描 ===")
    ips = resolve_subdomains(subdomains)
    masscan_output = f"{output_dir}/masscan.xml"
    run_command(["masscan", "-p", "1-65535", "--rate", str(args.rate), "-oX", masscan_output] + ips, "Masscan", sudo=True)

    # 3. Shodan
    print("\n=== 步骤3：Shodan API 查询 ===")
    api = Shodan(args.shodan_key)
    shodan_results = []
    for ip in ips[:50]:
        try:
            host = api.host(ip)
            shodan_results.append({"ip": ip, "org": host.get("org",""), "ports": len(host.get("ports",[])), "vulns": len(host.get("vulns",[]))})
        except:
            pass

    # 4. Nuclei（增强版：扫描全部 http 模板）
    print("\n=== 步骤4：Nuclei 全模板扫描（预计 10-25 分钟） ===")
    nuclei_output = f"{output_dir}/nuclei.txt"
    template_dir = os.path.expanduser("~/.nuclei-templates")
    run_command([
        "nuclei", "-l", sub_output,
        "-t", f"{template_dir}/http/",
        "-o", nuclei_output,
        "-severity", "critical,high,medium,low",
        "-silent", "-nc", "-timeout", "10",
        "-c", "30", "-rl", "80"
    ], "Nuclei 全模板扫描", timeout=1800)

    # 5. BloodHound（可选）
    if args.domain and args.username and args.password:
        print("\n=== 步骤5：BloodHound 域控采集 ===")
        bh = BloodHound(domain=args.domain, username=args.username, password=args.password)
        bh_output = f"{output_dir}/bloodhound"
        os.makedirs(bh_output, exist_ok=True)
        bh.run(collection_methods=["All"], output_dir=bh_output)

    # 生成报告
    print("\n=== 生成报告 ===")
    report_data = [{"类型": "子域名", "目标": sub} for sub in subdomains]
    for item in shodan_results:
        report_data.append({"类型": "Shodan情报", "目标": item["ip"], "备注": f"端口:{item['ports']} 漏洞:{item['vulns']}"})
    pd.DataFrame(report_data).to_excel(f"{output_dir}/full_report.xlsx", index=False)

    print(f"\n🎉 扫描完成！报告目录：{output_dir}")
    print(f"   🛡️  Nuclei结果：{nuclei_output}（现在会包含 low/medium 结果）")

if __name__ == "__main__":
    main()
