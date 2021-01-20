FROM ubuntu:18.04
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y libzmq3-dev python3-pip libmysqlclient-dev
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip
# Make a directory
RUN mkdir /my_app_dir
WORKDIR /my_app_dir
COPY . /my_app_dir/
ADD requirements.txt /my_app_dir/
RUN pip install --upgrade pip && pip install -r requirements.txt                                                   
CMD ["python3","manage.py","runserver","0.0.0.0:8000"]
#ADD . /my_app_dir/
