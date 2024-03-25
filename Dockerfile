FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    libglib2.0-0

RUN pip install opencv-python

RUN pip install fastapi

RUN pip install uvicorn

RUN pip install openai

RUN pip install serpapi

RUN pip install google-search-results

RUN pip install requests

RUN pip install pydantic

RUN pip install typing

RUN pip install reportlab

RUN pip install python-dotenv

EXPOSE 8000

CMD ["python3", "main.py"]
