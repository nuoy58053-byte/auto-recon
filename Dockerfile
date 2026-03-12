FROM rockylinux:8.10

RUN dnf update -y && \
    dnf install -y epel-release dnf-plugins-core && \
    dnf config-manager --set-enabled powertools && \
    dnf install -y git make gcc gcc-c++ golang python39 python39-pip python39-devel sudo libpcap-devel masscan && \
    dnf clean all

RUN go env -w GOPROXY=https://goproxy.cn,direct

RUN go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest && \
    cp ~/go/bin/* /usr/local/bin/

COPY requirements.txt /app/requirements.txt
RUN python3.9 -m pip install --no-cache-dir -r /app/requirements.txt

# 复制脚本
COPY auto_recon.py /app/auto_recon.py
RUN chmod +x /app/auto_recon.py

WORKDIR /app
ENV PATH="/usr/local/bin:$PATH"

ENTRYPOINT ["python3.9", "auto_recon.py"]
