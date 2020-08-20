FROM gkswjdzz/deoldify-models AS build
FROM nvcr.io/nvidia/pytorch:19.04-py3

RUN apt-get -y update

RUN apt-get install -y python3-pip software-properties-common wget ffmpeg

RUN apt-get -y update

RUN mkdir -p /root/.torch/models

RUN mkdir -p /data/upload

ADD requirements.txt /data/

WORKDIR /data

RUN pip install -r requirements.txt
RUN pip install Flask
RUN pip install Pillow
RUN pip install scikit-image
RUN pip install requests

COPY --from=build /models/ /root/.torch/models
RUN mkdir -p /data/models
RUN mv /root/.torch/models/ColorizeArtistic_gen.pth /data/models/ColorizeArtistic_gen.pth

ADD . /data/
EXPOSE 80

CMD ["python3", "app.py"]
