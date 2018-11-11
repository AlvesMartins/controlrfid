
# Install Docker
curl -fsSL https://get.docker.com |sh

# Install Docker Compose 
curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-cdockeompose

# Create Image
docker build . -t api

# Deploy
docker-compose up -d

# Logs Container
docker-compose logs

# View Container
docker-compose ps

# Create User Admin
docker exec -it api-server python /data/web/ControlRfid/manage.py createsuperuser --username admin

# Web   http://localhost:8000
# Api Rest http://localhost:8000/api/1/
# PhpAdmin http://localhost:8181

# Destoy Container
docker-compose kill

# Remove container
docker-compose rm
