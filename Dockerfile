FROM python:3.10-slim

WORKDIR /app

# install pip tools
RUN pip install --upgrade pip

# copy app code
COPY serving ./serving
COPY model_artifact ./model_artifact

# install requirements matching the model environment
COPY model_artifact/requirements.txt .
RUN pip install -r requirements.txt

# for local deployment, uncomment below lines
# EXPOSE 8000

# CMD ["uvicorn", "serving.app:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 7860

CMD ["uvicorn", "serving.app:app", "--host", "0.0.0.0", "--port", "7860"]
