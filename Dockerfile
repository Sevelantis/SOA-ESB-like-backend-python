FROM python:3.10

WORKDIR /home/app

#If we add the requirements and install dependencies first, docker can use cache if requirements don't change
ADD . /home/app
# longer but allows to download latest versions & takes less disk space, introducing pip parameter: --no-cache-dir 
RUN pip install --no-cache-dir -r ./dependencies/requirements/base.txt

CMD python3 src/main.py

EXPOSE 8888