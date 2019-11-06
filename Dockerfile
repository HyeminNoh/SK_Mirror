FROM ubuntu:latest

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

# COPY stuff
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

# Port forwardnig
EXPOSE 5000

## Run web app
CMD python main.py