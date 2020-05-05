# easy-rider-backend

Easy Rider&#39;s backend is a Django REST application implementing an API used by easy-rider-frontend.

## Local Setup

```bash
# Install all the dependencies
$ make install

# Create a local database and run all the migrations
$ make migrate

# Create a super user
$ make createsuperuser
Email address: admin@easyrider.com
Role: 4
Password: <ADMIN_PASSWORD>
Password (again): <ADMIN_PASSWORD>

# Run a local server at localhost:3000
$ make run
```

## Test
```bash
# Get a JWT token
$ curl --location --request POST 'localhost:8000/api/auth/obtain_token/' \
  --header 'Content-Type: application/json' \
  --header 'Content-Type: text/plain' \
  --data-raw '{
    "email": "admin@easyrider.com",
    "password": "<ADMIN_PASSWORD>"
}'
{"token":<TOKEN>}

# Create a new user
$ curl --location --request POST 'localhost:8000/api/users/' \
  --header 'Authorization: Bearer <TOKEN>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
	"email": "user01@easyrider.com",
	"password": "<USER_PASSWORD>"
}'

# Create a new trip for a user
$ curl --location --request POST 'localhost:8000/api/users/2/trips/' \
  --header 'Authorization: Bearer <TOKEN>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
	"user": 2,
	"destination": "Wroclaw", 
	"startDate": "2020-06-01", 
	"endDate": "2020-06-15", 
	"comment": "Test"
}'
```
