FROM seahorn/seahorn-llvm14:nightly AS seahorn_base

USER root

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    g++ \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt
RUN git clone https://github.com/AFLplusplus/AFLplusplus.git && \
    cd AFLplusplus && \
    make source-only

ENV PATH="/opt/AFLplusplus:/home/usea/seahorn/bin:${PATH}"

COPY cvc5-files/bin/ /usr/local/bin/
COPY cvc5-files/include/ /usr/local/include/
COPY cvc5-files/lib/ /usr/local/lib/
COPY cvc5-files/licenses/ /usr/local/share/licenses/cvc5/
COPY cvc5-files/cvc5/ /usr/local/share/cvc5/

COPY bin/ /usr/local/bin/
RUN chmod +x /usr/local/bin/chc_verifier*

RUN ldconfig

COPY benchmarks /Dualis/benchmarks
COPY logs /Dualis/logs
COPY scripts /Dualis/scripts

RUN pip install --no-cache-dir -r /Dualis/scripts/requirements.txt

RUN chmod +x /Dualis/scripts/*.py

WORKDIR /Dualis/scripts
