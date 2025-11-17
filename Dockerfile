FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
# default command: run extraction
CMD ["python", "-c", "from enterprise_kg_eval.main import run; run()"]
