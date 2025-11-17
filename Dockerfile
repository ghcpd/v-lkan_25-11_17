FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x setup.sh run_test.sh
RUN ./setup.sh

ENTRYPOINT ["python", "-m", "enterprise_kg_eval.cli", "--engine", "regex"]
