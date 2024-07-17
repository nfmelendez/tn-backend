
# True North Backend Challange

Backend that handle login and the different operations to support the calculator functionality and random string generation via a random.org third-party.

## Technologies
- AWS lambda with Python 3.12
- AWS Dynamodb
- Serverless framework
- Flask




## Usage

### Prerequisites

- It uses serverless framework.
- You need to have `Python3.12` installed locally, pyenv is recommended


### Deployment

install dependencies with:

```
npm install
```

and then perform deployment with:

```
serverless deploy
```

After running deploy, you should see output similar to:

```
Deploying "aws-python-flask-dynamodb-api" to stage "dev" (us-east-1)

Using Python specified in "runtime": python3.12

Packaging Python WSGI handler...

✔ Service deployed to stack aws-python-flask-dynamodb-api-dev (123s)

endpoints:
  ANY - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/
  ANY - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/{proxy+}
functions:
  api: aws-python-flask-dynamodb-api-dev-api (41 MB)
```


It also create the dynamodb tables 


### Testing

For testing setup with pyenv  `Python 3.12.2` and run

```
 python -m pytest
```

Result should be:

```
================================================================================================================================= test session starts ==================================================================================================================================
platform linux -- Python 3.12.2, pytest-8.2.2, pluggy-1.5.0
rootdir: /home/nfmelendez-linux/challanges/trueNorth
collected 3 items                                                                                                                                                                                                                                                                      

test/test_endpoints.py ...                                                                                                                                                                                                                                                       [100%]

================================================================================================================================== 3 passed in 0.36s ===================================================================================================================================
```