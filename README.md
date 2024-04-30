# Video to MP3 converter

A microservice application to convert video files to mp3.

## Overview

![alt text](https://img001.prntscr.com/file/img001/Xuo-_8dAQJOn3GOIB5wdUw.png)

[Video](https://www.youtube.com/watch?v=hmkF77F9TLw)

## Local development

### Prerequisites

Before you begin, ensure you have the following installed:

- [Python](https://www.python.org/downloads/)
- [MongoDB](https://www.mongodb.com/try/download/community)
- [Docker](https://docs.docker.com/get-docker/)
- [Kubernetes](https://kubernetes.io/docs/setup/)
- [MySQL](https://www.mysql.com/downloads/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [minikube](https://minikube.sigs.k8s.io/docs/start/)
- [k9s](https://k9scli.io/)

### Create a MySQL database

Create a new MySQL database instance to store user credentials:

```
mysql -u root -p < python/src/auth/init.sql
```

### Create .env file

Create `python/src/.env` file with secrets:

```
SENDER_EMAIL_ADDRESS=<email>
SENDER_PASSWORD=<password>
```

### Add secrets from `.env` to Kubernetes

```
kubectl create secret generic video2mp3-secrets --from-env-file=python/src/.env
```

### Expose ingress services

Add the following to the `/etc/hosts` file:

```
127.0.0.1 mp3converter.com
127.0.0.1 rabbitmq-manager.com
```

To get the ingress services to work you’ll need to open a new terminal and run:

```
minikube tunnel
```

### Build, tag, and push the Docker containers

Run these commands for every service:

```
docker build ./python/src/<service> -t <registry>/<service>:latest
docker push <registry>/<service>:latest
```

### Run the services

Run `kubectl apply` for every service located in the `python/src` folder:

```
kubectl apply -f python/src/<service>
```

## Application usage

Use `curl` to communicate with the application:

1. Call the `login` endpoint to obtain a JWT token:
   ```
   curl -X POST http://mp3converter.com/login -u test@gmail.com:Admin123
   ```
2. Use the token to upload a video file:
   ```
   cd <video_file_location>
   curl -X POST -F 'file=@./<video_file>' -H 'Authorization: Bearer <token>' http://mp3converter.com/upload
   ```
3. After the video file is uploaded and converted, you should receive an email with the mp3 file ID. Use that ID to download the mp3 file:
   ```
   curl --output mp3_download.mp3 -X GET -H 'Authorization: Bearer <token>' 'http://mp3converter.com/download?fid=<file_id>'
   ```

## Useful commands

### Scale deployment replicas:

```
kubectl scale deployment <service> --replicas=0
```

### Manage the cluster

Run this command to manage the cluster:

```
k9s
```
