# Silver Stream streaming platform

Service architecture
![alt text](SS_Architecture.png)

dev version launch
```
make build-n-run
```

ASYNC API - client's API, for front
```
http://0.0.0.0:8000/api/openapi
```

RS API - Recommendation system API
```
http://0.0.0.0:8888/api/openapi
```

RS - Inner API of recommendation system
```
http://0.0.0.0:8080/rs/docs
```

- containers
sudo docker stop $(sudo docker ps -aq)
sudo docker rm -f $(sudo docker ps -aq)

- images
sudo docker rmi -f $(sudo docker images -aq)

- volumes
sudo docker volume rm $(sudo docker volume ls -q)

- all unused network
sudo docker network prune -f

- verifying everything is clean
sudo docker ps -a
sudo docker images -a
sudo docker volume ls
The Story of Star Wars