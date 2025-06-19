## Running the app

```bash
# cd into the root level directory of the project
sudo docker-compose build web

docker compose up -d

# git bash into web container
docker exec -it <dockerContainerId> bash

# once inside container, run the following; exit the container bash when done
python manage.py makemigrations
python manage.py migrate
```

access localhost:8000

## Troubleshooting

```bash
# deleting the DB in data (permission issues etc)
sudo rm -rf ./data/db
```
