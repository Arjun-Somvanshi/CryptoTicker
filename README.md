
# CryptoTicker

A web backend that allows it's users to set a target price for Bitcoin,
and then sends them an email when the target price is reached.

### Tech Stack:
* FastAPI
* MongoDB
* Docker

### OS:
* Arch Linux (5.18.3-arch1-1)

Testing the app on a linux based distribution would be the easiest, non-unix like systems
might misbehave.


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

## Suggested way of TESTING the API
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

class UserSchema(BaseModel):
    username: str
    email: EmailStr 
    password: str 
    alerts: list

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

# Additional nested config class code is available in the app/models.py file
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
a thread which has re-occuring events.
The event mentioned above in our case is: `job()` in the file
`app/job_scheduler.py`. The function is scheduled to execute every
`20 seconds` as of now. Using the `get_bitcoin_price()` and database
collection of `alerts` we compare the prices and log the events onto 
the console and also send out an email using smtplib. The logs I have added can be a bit messy,
I did not edit them out, but it's readable.

In the `.env` file I have stored my google app-password, it's a dummy account, 
and I learnt that .env is best practice in such scenarios. Basically we 
use smptlib to make a connection to google's smpt port `587` and then we 
pass in our credentials (email and app-password), this authenticates us and allows
one to send emails. The parameters to the `send_email` function are attributes of the 
`AlertSchema` object that need to be sent so that the email has some soul.

## MongoDB
I have experience with json files mostly so I chose this as my database,
turned out to be a good decision. MongoDB is a no-sql database, along with 
it's docker container running alongside my FastAPI, I was able to connect
after a few hours of blood and sweat. Have a look at the helper functions
that are using the `pymongo` API to make a connection and interact with the database,
it's the usual CRUD operations.

## JWT Bearer Tokens
I have used `pyJWT` and `python-decouple` to implement this feature.
The JWT handler is responsible for signing the tokens and also for 
encoding/decoding. The `.env` file has the 24-Byte Key (192 bits) which is a strong key,
this key is supposed to be a secret since it will be used for signing tokens.
The `signJWT()` in `app/auth/auth_handler.py` handles signing based on `user_id` which in my case
is the useremail, I have made that a unique attribute in the `userSchema` document. It also sets a 
an expiry time for the token, and returns this.
Similarly, `decodeJWT` takes a token string and verifies if it was signed by our secret key it 
also checks if the token has expired or not. The `bearer` files holds the magic though,
it is what assists us to verify the protcted route by confirming if the reques is authentic.
FastAPI provides a basic validation class through `HTTPBearer`, the class is extended into what
I am using in the `app/bearer.py`


## Password Hashing
`app/security.py` is responsible for the cryptographic hash functions 
that are being used to verify passwords and to store them securely. `bcrypt`
provides round based hashing, I have set it to 14 rounds which makes it computationally 
expensive for attackers to bruteforce in a given time.

## Ticker
I didn't have much time for studying the webSocket api of Binance, in the `app/ticker.py` I 
have simply used `requests` to get the cost of Bitcoin from the coinmarketcap API endpoint
provided in the problem statement.
