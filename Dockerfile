FROM python:3.10.9-alpine

# Create app directory
WORKDIR /gradish

# Install app dependencies
COPY ./requirements.txt /gradish/requirements.txt

RUN pip install -r requirements.txt

# Bundle app source
COPY . /gradish

EXPOSE 5000
CMD ["./bootstrap.sh"]

