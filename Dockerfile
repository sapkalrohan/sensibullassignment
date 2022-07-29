# Using lightweight alpine image
FROM python:3.10-alpine

# Installing packages
RUN apk update
RUN pip install --no-cache-dir pipenv

# Defining working directory and adding source code
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY stock ./stock

# Install API dependencies
RUN pipenv install

# Start app
EXPOSE 19093
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]