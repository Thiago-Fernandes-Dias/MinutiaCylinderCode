FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV OPENMPI_VERSION=1.10.7
ENV OPENMPI_DIR=/opt/openmpi

RUN apt-get update && apt-get install -y \
    g++ make wget libtool flex libhwloc-dev \
    perl python3 \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q https://download.open-mpi.org/release/open-mpi/v1.10/openmpi-${OPENMPI_VERSION}.tar.gz \
    && tar xf openmpi-${OPENMPI_VERSION}.tar.gz \
    && cd openmpi-${OPENMPI_VERSION} \
    && ./configure --prefix=${OPENMPI_DIR} --enable-mpi-cxx \
    CFLAGS="-Wno-error" CXXFLAGS="-Wno-error" \
    && make -j$(nproc) \
    && make install \
    && cd / && rm -rf openmpi-${OPENMPI_VERSION}*

ENV PATH=${OPENMPI_DIR}/bin:${PATH}
ENV LD_LIBRARY_PATH=${OPENMPI_DIR}/lib

WORKDIR /app
COPY . .

RUN make -f mcc.mk clean
RUN make -f mcc.mk -j$(nproc) all
RUN chmod +x compare_all.py

ENTRYPOINT ["bash"]
