FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install openai numpy openenv-core fastapi uvicorn pyyaml
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]