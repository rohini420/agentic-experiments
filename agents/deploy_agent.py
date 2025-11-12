import os
import subprocess

def deploy_to_ecs():
    print("[🚀] Deploying to ECS (local agent)...")
    os.environ["AWS_REGION"] = os.getenv("AWS_REGION", "us-east-1")
    os.environ["AWS_ACCOUNT_ID"] = os.getenv("AWS_ACCOUNT_ID", "YOUR-ID-HERE")

    image = f"{os.environ['AWS_ACCOUNT_ID']}.dkr.ecr.{os.environ['AWS_REGION']}.amazonaws.com/agentic-poc"
    subprocess.run([
        "aws", "ecs", "update-service",
        "--cluster", "agentic-poc1",
        "--service", "agentic-poc-staging",
        "--force-new-deployment"
    ], check=True)

if __name__ == "__main__":
    deploy_to_ecs()

