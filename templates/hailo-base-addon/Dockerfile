FROM ubuntu:22.04

# Add metadata
LABEL \
    io.hass.name="Hailo AI Add-on Template" \
    io.hass.description="Template for building custom Hailo AI add-ons" \
    io.hass.arch="armhf|armv7|aarch64|amd64|i386" \
    io.hass.type="addon" \
    io.hass.version="1.0.0"

# Environment variables
ENV \
    LANG="C.UTF-8" \
    DEBIAN_FRONTEND="noninteractive" \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0 \
    S6_CMD_WAIT_FOR_SERVICES=1 \
    S6_SERVICES_READYTIME=50

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Build arguments
ARG S6_OVERLAY_VERSION=3.1.6.2
ARG BASHIO_VERSION=0.16.2
ARG TEMPIO_VERSION=2021.09.0

# Install base system packages
RUN \
    set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        jq \
        tzdata \
        curl \
        ca-certificates \
        python3 \
        python3-pip \
        python3-venv \
        build-essential \
        pkg-config \
        libffi-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libwebp-dev \
        libopenjp2-7-dev \
        zlib1g-dev \
        ffmpeg \
        libavcodec-dev \
        libavformat-dev \
        libswscale-dev \
    && rm -rf /var/lib/apt/lists/*

# Install S6-Overlay for proper init system
# Download architecture-specific overlay
RUN ARCH=$(dpkg --print-architecture) \
    && S6_ARCH=${ARCH} \
    && if [ "${ARCH}" = "amd64" ]; then S6_ARCH="x86_64"; fi \
    && if [ "${ARCH}" = "arm64" ]; then S6_ARCH="aarch64"; fi \
    && if [ "${ARCH}" = "armel" ]; then S6_ARCH="arm"; fi \
    && if [ "${ARCH}" = "i386" ]; then S6_ARCH="i686"; fi \
    && curl -L -f -o /tmp/s6-overlay-arch.tar.xz \
        "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-${S6_ARCH}.tar.xz" \
    && tar -C / -Jxpf /tmp/s6-overlay-arch.tar.xz \
    && rm -f /tmp/s6-overlay-arch.tar.xz

# Download noarch overlay
RUN curl -L -f -o /tmp/s6-overlay-noarch.tar.xz \
        "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz" \
    && tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz \
    && rm -f /tmp/s6-overlay-noarch.tar.xz \
    && mkdir -p /etc/fix-attrs.d \
    && mkdir -p /etc/services.d

# Install Bashio for Home Assistant integration
RUN \
    mkdir -p /usr/src/bashio \
    && curl -L -f -s \
        "https://github.com/hassio-addons/bashio/archive/v${BASHIO_VERSION}.tar.gz" \
        | tar -xzf - --strip 1 -C /usr/src/bashio \
    && mv /usr/src/bashio/lib /usr/lib/bashio \
    && ln -s /usr/lib/bashio/bashio /usr/bin/bashio \
    && rm -rf /usr/src/bashio

# Install Tempio for configuration templating
RUN \
    ARCH=$(dpkg --print-architecture) \
    && if [ "${ARCH}" = "amd64" ]; then TEMPIO_ARCH="amd64"; fi \
    && if [ "${ARCH}" = "armhf" ]; then TEMPIO_ARCH="armv6"; fi \
    && if [ "${ARCH}" = "armv7" ]; then TEMPIO_ARCH="armv7"; fi \
    && if [ "${ARCH}" = "aarch64" ]; then TEMPIO_ARCH="aarch64"; fi \
    && if [ "${ARCH}" = "i386" ]; then TEMPIO_ARCH="i386"; fi \
    && curl -L -f -s -o /usr/bin/tempio \
        "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${TEMPIO_ARCH}" \
    && chmod a+x /usr/bin/tempio

# Create working directory
WORKDIR /app

# Copy application files
COPY hailo_packages/ ./hailo_packages/
COPY src/ ./src/
COPY requirements.txt ./
COPY run.sh /
COPY rootfs/ /

# Install Hailo packages (architecture-specific)
RUN \
    ARCH=$(dpkg --print-architecture) \
    && if [ "${ARCH}" = "aarch64" ]; then \
        dpkg --unpack hailo_packages/*_arm64.deb || true; \
        python3 -m pip install hailo_packages/*-cp*-linux_aarch64.whl; \
    fi

# Install Python dependencies
RUN \
    python3 -m pip install --upgrade pip \
    && python3 -m pip install -r requirements.txt

# Make run script executable
RUN chmod a+x /run.sh

# S6-Overlay entrypoint
ENTRYPOINT ["/init"]
CMD ["/run.sh"]