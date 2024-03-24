FROM python:3.9.7

WORKDIR /user/src/app

COPY requirements.txt ./ 
#Copy requirements.txt to the container

RUN pip install --no-cache-dir -r requirements.txt 
#Install dependencies

COPY . .

CMD ["uvicorn", "app.main:app", "--host","0.0.0.0", "--port", "8000"]
# Run the app

# docker build -t fastapi .
# docker image ls
# docker run
```