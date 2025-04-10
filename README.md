# struct-address

## Setup
First change the GROQ_API_KEY value in the .env file

### Building and starting the app
```
docker-compose up -d --build
```

## Testing

### Swagger UI
To view swagger UI go [here](http://127.0.0.1:8000/docs)

### Pytest
When container is running run
```
docker-compose exec structaddress pytest
```

### Sending multiple requests
File test.sh contains 10 requests for different addresses
```
./test.sh
```