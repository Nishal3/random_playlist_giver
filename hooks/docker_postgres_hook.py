import docker
from sqlalchemy import create_engine


class DockerPostgreHook(BaseHook):
    def __init__(self, postgres_container_name: str, postgres_database: str):
        self.postgres_container_name = postgres_container_name
        self.postgres_database = postgres_database

    def get_connection(self):
        docker_client = docker.from_env()
        postgres_container = docker_client.containers.get(self.postgres_container_name)
        postgres_ip_addr = postgres_container.attrs["NetworkSettings"]["Addresses"][
            "docker.com"
        ][0]["Address"]

        engine = create_engine(
            f"postgresql://airflow:airflow@{postgres_ip_addr}:5432/{self.postgres_database}",
            future=True,
        )

        conn = engine.connect()
        return conn
