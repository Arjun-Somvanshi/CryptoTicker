
# CryptoTicker

A web backend that allows it's users to set a target price for Bitcoin,
and then sends them an email when the target price is reached.

### Tech Stack:
* FastAPI
* MongoDB
* Docker




## Run CryptoTicker
You require to have installed [docker](https://docs.docker.com/engine/install/), preferably on a unix like system.

Run CryptoTicker with docker commands

```bash
  git clone https://github.com/Arjun-Somvanshi/CryptoTicker.git

  cd CryptoTicker

  docker-compose build
  docker-compose up -d
```

Run CryptoTicker with the provided run bash script

```bash
  git clone https://github.com/Arjun-Somvanshi/CryptoTicker.git

  cd CryptoTicker

  chmod +x run
  ./run
```

The web server will run on the host: 0.0.0.0 and the port is 80. In your browser 
just visit or click on: [0.0.0.0:80](http://0.0.0.0:80) to view the home page.

To access the interative API go to [0.0.0.0:80/docs](http://0.0.0.0:80/docs).

There are other bash scripts provided in the project to automate rebuilding manually.

## Schemas
Throughout the project to ensure encapsulation I have used 
[Pydantic](https://pydantic-docs.helpmanual.io/).
To explain a few of the input parameters in the API we must take a look
at the existing classes that represent entities in the schema.

```python
class AlertSchema(BaseModel):
    alert_id: str = Field(default="", title="Unique ID")
    status: str = Field(default="", title="The status of the alert: created/deleted/triggered")
    targetPrice: int = Field(gt=0, title="The target price at which the alert will get triggered")
    email: EmailStr 
    class Config:
        schema_extra = {
                "example": {
                    "status": "created",
                    "targetPrice": 24000,
                    "email": "arjunsomvanshi@gmail.com"
                    }
                }

class UserSchema(BaseModel):
    username: str
    email: EmailStr 
    password: str 
    alerts: list
    class Config:
        schema_extra = {
            "example": {
                "username": "Arjun Somvanshi",
                "email": "arjunsomvanshi@gmail.com",
                "password": "usuallyStrongPassword",
                "alerts": []
            }
        }

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    class Config:
        schema_extra = {
            "example": {
                "email": "arjunsomvanshi@gmail.com",
                "password": "usuallyStrongPassword"
            }
        }
```

These classes are the entities that we work with in the API and 
also while dealing with database connections. Now you can understand
the API better.
## API Reference

#### Get a basic response

```http
  GET /
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| None | `string` | A simple hello world like response |

#### Signup as a user

```http
  POST /user/signup/
```

| Body      | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| user| `UserSchema` | **Required**. User object to be added    |

Takes a UserSchema object and returns access token. Appends user
to database.

#### Login as a user

```http
  POST /user/login/
```

| Body      | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| user| `LoginSchema` | **Required**. Login object to be added    |

Takes a LoginSchema object and returns access token if the
user is valid.

#### Create an Alert

```http
  POST /alerts/create/
```

| Body      | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| alert| `AlertSchema` | **Required**. AlertSchema object to be added    |
| access_token| `string`| **Required** To authenticate user session |

Takes an AlertSchema object and adds it to the database.

#### Delete an Alert

```http
  POST /alerts/delete/
```

| Body      | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| alert| `AlertSchema` | **Required**. AlertSchema object to be deleted  |
| access_token| `string`| **Required** To authenticate user session |

Takes an AlertSchema object and updates it's status to deleted

#### Fetch Alerts with filter-string

```http
  Get /alerts/fetch/
```

| Parameter     | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| email | `EmailStr` | **Required**. The user's email for whom the alerts must be fetched  |
|filterStr|`string`  | An optional filter which should be in = ["created", "triggered", "deleted"]
| access_token| `string`| **Required** To authenticate user session |

Takes the user email and filterStr and returns a list of alert documents (json objects)




## Sending Alerts
Using the schedule package along with threading, we can achieve
a thread which has reoccuring events.
The event mentioned above in our case is: `job()` in the file
`app/job_scheduler.py`. The function is scheduled to execute every
20 seconds as of now, using the `get_bitcoin_price()` and database
collection of `alerts` we compare the prices and log the events onto 
the console and also send out an email using smtplib.

