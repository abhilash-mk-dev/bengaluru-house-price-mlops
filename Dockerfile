FROM python:3.10-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY serving ./serving
COPY ui ./ui
COPY model_artifact ./model_artifact
COPY model_artifact/requirements.txt .

RUN pip install -r requirements.txt
RUN pip install streamlit requests

EXPOSE 8000
EXPOSE 7860

CMD bash -c "\
uvicorn serving.app:app --host 0.0.0.0 --port 8000 & \
streamlit run ui/app.py --server.port 7860 --server.address 0.0.0.0 \
"
