import docker
import os

client = docker.from_env()

def run_test_container(repository_url: str, test_command: str):
    try:
        container = client.containers.run(
            "python:3.11-slim",
            f"echo 'Running tests for {repository_url}: {test_command}'",
            detach=True
        )
        result = container.wait()
        logs = container.logs().decode("utf-8")
        
        return {
            "status_code": result["StatusCode"],
            "logs": logs
        }
    except Exception as e:
        return {
            "status_code": -1,
            "logs": str(e)
        }
