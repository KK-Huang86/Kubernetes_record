FROM python:3.12-slim
WORKDIR /app
RUN pip install requests
COPY list_pods.py .
CMD ["python", "list_pods.py"]
