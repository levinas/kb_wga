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
    wget http://downloads.sourceforge.net/project/mugsy/mugsy_x86-64-v1r2.2.tgz && \
    tar xf mugsy_x86-64-v1r2.2.tgz && \
    mv mugsy_x86-64-v1r2.2/ /kb/deployment/mugsy && \
    echo 'export MUGSY_INSTALL=/kb/deployment/mugsy' >> /kb/deployment/user-env.sh && \
    echo 'export PATH=$PATH:$MUGSY_INSTALL:$MUGSY_INSTALL/mapping' >> /kb/deployment/user-env.sh && \
    echo 'export PERL5LIB=$PERL5LIB:$MUGSY_INSTALL/perllibs' >> /kb/deployment/user-env.sh

# Copy local wrapper files, and build

COPY ./ /kb/module
RUN mkdir -p /kb/module/work

WORKDIR /kb/module

RUN make

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
