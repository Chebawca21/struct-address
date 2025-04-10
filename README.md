# struct-address

## Setup
First change the GROK_API_KEY in the docker-compose.yml

### Building and starting the app
```
docker-compose up -d --build
```

## Testing
When container is running run
```
docker-compose exec structaddress pytest
```