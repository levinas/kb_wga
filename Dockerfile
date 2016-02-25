FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

# RUN apt-get update

# -----------------------------------------

RUN apt-get install libffi-dev libssl-dev
RUN pip install --upgrade requests[security]

# Install Mugsy
RUN \
    wget http://downloads.sourceforge.net/project/mugsy/mugsy_x86-64-v1r2.3.tgz && \
    tar xf mugsy_x86-64-v1r2.3.tgz && \
    mv mugsy_x86-64-v1r2.3/ /kb/deployment/mugsy && \
    echo 'export MUGSY_INSTALL=/kb/deployment/mugsy' >> /kb/deployment/user-env.sh && \
    echo 'export PATH=$PATH:$MUGSY_INSTALL:$MUGSY_INSTALL/mapping' >> /kb/deployment/user-env.sh && \
    echo 'export PERL5LIB=$PERL5LIB:$MUGSY_INSTALL/perllibs' >> /kb/deployment/user-env.sh

# Install progressiveMauve
RUN \
    wget http://darlinglab.org/mauve/snapshots/2015/2015-02-13/linux-x64/mauve_linux_snapshot_2015-02-13.tar.gz && \
    tar xf mauve_linux_snapshot_2015-02-13.tar.gz && \
    mv mauve_snapshot_2015-02-13/linux-x64 /kb/deployment/mauve && \
    echo 'export PATH=$PATH:/kb/deployment/mauve' >> /kb/deployment/user-env.sh

# Copy local wrapper files, and build

COPY ./ /kb/module
RUN mkdir -p /kb/module/work

WORKDIR /kb/module

RUN make

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
