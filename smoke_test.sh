#!/bin/bash
set -e

APP_URL=${APP_URL:-localhost:8080}

echo "Running smoke test..."

response=$(curl -s --fail "http://${APP_URL}/") || {
  echo "Curl failed. Cannot reach http://${APP_URL}/"
  exit 1
}

echo "Response: $response"

if echo "$response" | grep -q 'hello from AI Agents POC'; then
  echo "✅ Smoke test passed!"
else
  echo "❌ Smoke test failed!"
  exit 1
fi


