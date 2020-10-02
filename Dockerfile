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
#RUN mv /root/.torch/models/ColorizeStable_gen.pth /data/models/ColorizeStable_gen.pth
#RUN wget -O /root/.torch/models/resnet101-5d3b4d8f.pth https://download.pytorch.org/models/resnet101-5d3b4d8f.pth
#wget -O /data/models/ColorizeStable_gen.pth https://www.dropbox.com/s/mwjep3vyqk5mkjc/ColorizeStable_gen.pth?dl=0

ADD . /data/
EXPOSE 80

CMD ["python3", "app.py"]
