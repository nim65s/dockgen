FROM {{ args.from }} AS base

WORKDIR /src

SHELL ["/bin/bash", "-euxc"]

RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    --mount=type=cache,sharing=locked,target=/var/lib/apt \
    apt update \
    && DEBIAN_FRONTEND=noninteractive apt install -qqy --no-install-recommends \
    {{ apt_deps }}

RUN cd /usr/local/lib/python3.* \
 && ln -s dist-packages site-packages

ENV JOBS={{ args.jobs }} \
    CMAKE_BUILD_TYPE=Release \
    CTEST_PARALLEL_LEVEL={{ args.jobs }} \
    CTEST_OUTPUT_ON_FAILURE=ON
