FROM alpine
COPY cowrie-to-csv.py /app/cowrie-to-csv.py
RUN apk update && apk add python3
WORKDIR /app

EXPOSE 8000

CMD ["python3","-u","/app/cowrie-to-csv.py"]