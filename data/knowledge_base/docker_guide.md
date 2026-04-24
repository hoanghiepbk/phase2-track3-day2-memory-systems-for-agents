# Docker Guide — Common Commands & Troubleshooting

## Basic Commands
- `docker build -t myapp .` — Build an image from Dockerfile
- `docker run -p 8080:80 myapp` — Run container with port mapping
- `docker ps` — List running containers
- `docker logs <container>` — View container logs
- `docker exec -it <container> bash` — Shell into a running container

## Docker Compose
Use `docker-compose.yml` for multi-container applications:
```yaml
services:
  web:
    build: .
    ports:
      - "8080:80"
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
```

## Networking
Docker creates a bridge network by default. Containers on the same network can communicate using service names as hostnames. Use `docker network create mynet` for custom networks.

**Common pitfall**: When using Docker Compose, services reference each other by service name (e.g., `db:5432`), not `localhost`. This is because each container has its own network namespace.

## Troubleshooting
- **Port already in use**: `docker stop $(docker ps -q)` to stop all containers
- **Image not found**: Check Dockerfile path and build context
- **Permission denied**: Add user to docker group or use `sudo`
- **Container exits immediately**: Check logs with `docker logs` — usually a startup script error

## Volumes
Use volumes for persistent data: `docker run -v mydata:/app/data myapp`. Named volumes persist across container restarts.
