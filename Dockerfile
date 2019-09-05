FROM python:3

ADD findFood.py /

RUN pip install httplib2

CMD [ "python", "./findFood.py" ]