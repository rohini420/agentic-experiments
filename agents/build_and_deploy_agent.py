# build_and_deploy_agent.py
import subprocess
import os
import logging
from typing import Dict

def run_command(cmd: str) -> None:
    logging.info(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {cmd}")

def build_and_push_docker_image(app_name: str, account_id: str, region: str, tag: str = "latest") -> str:
    image_uri = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{app_name}:{tag}"
    
    # Authenticate Docker to ECR
    run_command(f"aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {account_id}.dkr.ecr.{region}.amazonaws.com")

    # Build Docker image
    run_command(f"docker build -t {app_name}:{tag} .")

    # Tag image for ECR
    run_command(f"docker tag {app_name}:{tag} {image_uri}")

    # Push to ECR
    run_command(f"docker push {image_uri}")

    return image_uri

def force_ecs_deployment(cluster: str, service: str, region: str) -> None:
    run_command(f"aws ecs update-service --cluster {cluster} --service {service} --force-new-deployment --region {region}")

def main():
    app_name = os.getenv("APP_NAME", "agentic-poc")
    account_id = os.getenv("AWS_ACCOUNT_ID", "473191218617")
    region = os.getenv("AWS_REGION", "us-east-1")
    cluster = os.getenv("ECS_CLUSTER", "agentic-poc1")
    service = os.getenv("ECS_SERVICE", "agentic-poc-staging")

    logging.basicConfig(level=logging.INFO)
    logging.info("🚀 Starting build and deploy pipeline...")

    image_uri = build_and_push_docker_image(app_name, account_id, region)
    logging.info(f"✅ Image pushed to ECR: {image_uri}")

    force_ecs_deployment(cluster, service, region)
    logging.info("✅ ECS deployment triggered.")

if __name__ == "__main__":
    main()

