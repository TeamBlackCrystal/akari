FROM python:3.11
WORKDIR /akari
COPY requirements.txt /akari/
RUN pip install -r requirements.txt --no-deps
COPY . /akari
CMD python ./tools/config-gen.py && python main.py
