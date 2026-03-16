FROM seahorn/seahorn-llvm14:nightly AS seahorn_base

ARG USER_ID
ARG GROUP_ID

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

RUN groupadd --gid ${GROUP_ID} dualis && \
    useradd --uid ${USER_ID} --gid ${GROUP_ID} --create-home dualis

USER dualis

COPY --chown=dualis:dualis benchmarks /Dualis/benchmarks
COPY --chown=dualis:dualis logs /Dualis/logs
COPY --chown=dualis:dualis scripts /Dualis/scripts
COPY --chown=dualis:dualis requirements.txt /Dualis/requirements.txt
COPY --chown=dualis:dualis .env /Dualis/.env

RUN pip install --no-cache-dir -r /Dualis/requirements.txt

RUN chmod +x /Dualis/scripts/*.py

WORKDIR /Dualis/scripts
