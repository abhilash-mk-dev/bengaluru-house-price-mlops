FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install mlflow==3.1.4 \
    scikit-learn==1.6.1 \
    cloudpickle==3.1.1 \
    pandas==2.3.2 \
    numpy==2.0.2 \
    psutil==7.0.0 \
    fastapi uvicorn[standard]


COPY serving/app.py ./serving/app.py

EXPOSE 8000

CMD ["uvicorn", "serving.app:app", "--host", "0.0.0.0", "--port", "8000"]
