FROM tensorflow/tensorflow:latest-py3-jupyter

MAINTAINER Yiqiu Jia <yiqiujia@hotmail.com>

RUN pip install muggle_ocr
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN pip install tornado
ADD imgs /tf/tensorflow-tutorials/imgs
RUN ls /tf/tensorflow-tutorials/imgs
ADD Untitled.ipynb /tf/tensorflow-tutorials/
ADD main.py /tf/tensorflow-tutorials/
ADD update.py /tf/tensorflow-tutorials/

RUN echo $(date "+%Y-%m-%d_%H:%M:%S") >> /.image_times && \
	echo $(date "+%Y-%m-%d_%H:%M:%S") > /.image_time && \
	echo "land007/muggle_ocr" >> /.image_names && \
	echo "land007/muggle_ocr" > /.image_name

#CMD source /etc/bash.bashrc && jupyter notebook --notebook-dir=/tf --ip 0.0.0.0 --no-browser --allow-root
CMD cd /tf/tensorflow-tutorials/ && /usr/bin/python3 update.py & /usr/bin/python3 /usr/local/bin/jupyter-notebook --notebook-dir=/tf --ip 0.0.0.0 --no-browser --allow-root

#docker rm -f muggle_ocr ; docker run -it --privileged -p 8888:8888 --name muggle_ocr land007/muggle_ocr:latest
#docker rm -f muggle_ocr ; docker run -it --privileged -p 8888:8888 -p 8080:8080 --name muggle_ocr land007/muggle_ocr:latest
#docker exec -it muggle_ocr bash
#> docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t land007/muggle_ocr --push .
#docker build -t land007/muggle_ocr:latest .
