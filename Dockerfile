FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1 HOME=/tmp IR_DATASETS_HOME=/app/.ir_datasets
CMD ["bash"]