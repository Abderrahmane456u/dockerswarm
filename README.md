# TP Docker Swarm – Flask avec secrets et scaling

## Description
Ce TP montre comment déployer une **application Flask** dans un **cluster Docker Swarm**, utiliser un **secret**, mettre à l’échelle les services, et nettoyer l’environnement.  
Chaque conteneur Flask renvoie son **hostname** et le **secret**.

---

## Structure du projet

tp_swarm/
├── app/
│ ├── app.py
│ ├── Dockerfile
│ └── requirements.txt
├── secret.txt
└── stack.yml

---

## Étapes du TP

### 1️⃣ Build de l’image Docker
```bash
cd app
docker build -t flask-swarm-demo:1.0 .
docker secret create app_secret ../secret.txt
docker secret ls
cd ..
docker stack deploy -c stack.yml tp12
docker stack ls
docker service ls
docker service ps tp12_web
5️⃣ Tester dans le navigateur

Ouvre : http://localhost:8080

Rafraîchis plusieurs fois → le HOSTNAME change selon le conteneur qui répond.
Le secret s’affiche à côté du hostname.

6️⃣ Scaling (mise à l’échelle)
docker service scale tp12_web=5
docker service ps tp12_web


Tu dois voir 5 tâches Running.

7️⃣ Nettoyage
docker stack rm tp12
docker secret rm app_secret
docker swarm leave --force
docker stack ls
docker service ls
docker secret ls

Fichiers importants
Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]

requirements.txt
flask

stack.yml
version: "3.9"

services:
  web:
    image: flask-swarm-demo:1.0
    ports:
      - "8080:5000"
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
      update_config:
        parallelism: 1
        order: start-first
        delay: 5s
      rollback_config:
        parallelism: 1
        order: start-first
        delay: 5s
    secrets:
      - app_secret

secrets:
  app_secret:
    external: true


---

Si tu veux, je peux te faire **une version encore plus courte et synthétique** qui tient sur **une page GitHub**, avec uniquement les commandes à exécuter et la structure des fichiers.  

Veux‑tu que je fasse ça ?
