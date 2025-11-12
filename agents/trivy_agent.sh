#!/bin/bash
echo "[🔍] Running Trivy scan on local image:latest"
trivy image --severity HIGH,CRITICAL agentic-poc:latest || exit 1

