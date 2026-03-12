FROM rockylinux:8

RUN dnf update -y && \
    dnf install -y epel-release git make gcc golang python39 python39-pip python39-devel sudo && \
    dnf clean all

RUN go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest && \
    cp ~/go/bin/* /usr/local/bin/

RUN dnf install -y masscan

COPY requirements.txt /app/requirements.txt
RUN python3.9 -m pip install --no-cache-dir -r /app/requirements.txt

RUN git clone https://github.com/projectdiscovery/nuclei-templates.git /root/.nuclei-templates

COPY auto_recon.py /app/auto_recon.py
RUN chmod +x /app/auto_recon.py

WORKDIR /app
ENV PATH="/usr/local/bin:$PATH"

ENTRYPOINT ["python3.9", "auto_recon.py"]
