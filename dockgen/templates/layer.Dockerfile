FROM base AS {{ project.name }}

ADD {{ project.tarball }} /src.tar.gz
{% for dep in project.src_deps %}
COPY --from={{ dep }} /usr/local /usr/local
{% endfor %}

RUN tar xf /src.tar.gz --strip-components=1 \
 && ldconfig \
 && cmake -B build \
          -DBUILD_TESTING=OFF \
          -Wno-dev \
 && cmake --build build -j {{ args.jobs }} \
 && cmake --build build -t install \
 && rm -rf ./*
