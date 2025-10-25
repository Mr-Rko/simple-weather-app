 #pull base image for requirement tools and others packages
FROM python:3.7

#creating a directory for copying
WORKDIR /app

#copy source code from host file to /app
COPY . .

#installing the requirements for running the app
RUN pip install -r requirements.txt

#run the app
ENTRYPOINT ["python"]
CMD ["run.py"]
