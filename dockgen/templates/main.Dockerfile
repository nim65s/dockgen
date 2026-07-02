FROM {{ args.from }} AS base

WORKDIR /src

SHELL ["/bin/bash", "-euxc"]

RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    --mount=type=cache,sharing=locked,target=/var/lib/apt \
    apt update \
    && DEBIAN_FRONTEND=noninteractive apt install -qqy --no-install-recommends \
    {{ apt_deps }}

{% if pip_deps %}
RUN --mount=type=cache,sharing=locked,target=/root/.cache/pip \
    python3 -m venv --system-site-packages /usr/local \
 && source /usr/local/bin/activate \
 && pip install \
    {{ pip_deps }}
{% endif %}

RUN cd /usr/local/lib/python3.* \
 && rmdir dist-packages \
 && ln -s site-packages dist-packages

ENV JOBS={{ args.jobs }} \
    CMAKE_BUILD_TYPE=Release \
    CMAKE_INSTALL_PREFIX=/usr/local \
    CTEST_PARALLEL_LEVEL={{ args.jobs }} \
    CTEST_OUTPUT_ON_FAILURE=ON \
    VIRTUAL_ENV=/usr/local
