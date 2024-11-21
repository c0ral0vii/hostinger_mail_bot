FROM python:3.12-slim

ENV PATH="/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

CMD ["sh", "-c", "alembic revision --autogenerate -m 'start' && alembic upgrade head && python main.py"]