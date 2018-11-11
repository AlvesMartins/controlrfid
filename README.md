
### Create Image
docker build . -t api

### Deploy
docker-compose up -d

##Logs
docker-compose logs

## View Container
docker-compose ps

## Create User Admin
docker exec -it api-server python /data/web/ControlRfid/manage.py createsuperuser --username admin

## Web   http://localhost:8000
### Api Rest http://localhost:8000/api/1/
### PhpAdmin http://localhost:8181

## Destoy Container
docker-compose kill

### Remove container
docker-compose rm
