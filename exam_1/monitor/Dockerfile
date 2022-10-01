FROM python:3-alpine

COPY app/requirement.txt requirement.txt
RUN pip install -r requirement.txt 

USER 1000
WORKDIR /app
