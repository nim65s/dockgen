FROM base AS {{ project.name }}

{% if project.url == "." %}
ADD . .
{% else %}
ADD {{ project.tarball }} /src.tar.gz
{% endif %}

{% for dep in project.src_deps %}
COPY --from={{ dep }} /usr/local /usr/local
{% endfor %}

RUN {% if project.url == "." %}ls{% else %}tar xf /src.tar.gz --strip-components=1{% endif %} \
 && ldconfig \
 && cmake -B build \
          -DBUILD_TESTING=OFF \
          -Wno-dev \
 && cmake --build build -j {{ args.jobs }} \
 && cmake --build build -t install \
 && rm -rf {% if project.url == "." %}build{% else %}./*{% endif %}
