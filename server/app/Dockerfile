FROM python

WORKDIR /server

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD uvicorn db.main:app --reload --host 0.0.0.0 --port 80
