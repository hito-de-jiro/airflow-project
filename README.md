--- build docker container ---
docker compose up --build
🔹 Web UI: http://localhost:8080 (login: admin/admin)
🔹 Flower UI (Celery monitoring): http://localhost:5555 (login: admin/admin)

--- list of containers ---
docker ps -a

--- airflow-init logs ---
docker logs airflow-init

--- rebuild ---
docker compose down -v
docker compose up --build

--- logs ----
docker logs airflow-docker-airflow-webserver-1
docker logs airflow-docker-airflow-scheduler-1
docker logs airflow-docker-airflow-worker-1

--- check ports ---
netstat -an | grep 8080   # або
lsof -i :8080

python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"