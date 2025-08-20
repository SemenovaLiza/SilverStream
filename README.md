# Проектная работа: диплом

Архитектура сервиса
![alt text](architecture.png)

Запуск dev версии

```
make build-n-run
```

ASYNC API - клиентское апи, для фронта
```
http://0.0.0.0:8000/api/openapi
```

RS API - апи рекоммендательной системы
```
http://0.0.0.0:8888/api/openapi
```

RS - внутреннее апи рекоммендательной системы
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