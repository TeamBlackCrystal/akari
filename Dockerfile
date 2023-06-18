FROM python:3.11
WORKDIR /akari
COPY requirements.txt /akari/
RUN pip install -r requirements.txt
COPY . /akari
CMD python ./tools/config-gen.py && alembic upgrade head && python main.py
