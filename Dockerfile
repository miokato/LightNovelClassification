FROM miok/nlpenv


WORKDIR /code/
COPY . /code/

EXPOSE 8000

RUN pip install -r requirements.txt
