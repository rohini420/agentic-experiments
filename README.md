# 🧠 Agentic POC: AI-Driven Deployment with LangGraph + ECS

This project demonstrates an **AI Agent-based CI/CD pipeline** that performs secure, intelligent deployments to AWS ECS Fargate, orchestrated via LangGraph.

---

## ✅ Completed Phases

### 📦 Phase 1–3: Flask App Setup
- Simple 12-Factor-style app built using Flask
- `GET /` returns app metadata (app name, env, message)
- Dockerized with `Dockerfile`

### 🔁 Phase 4–6: GitHub Actions → ECS Deployment
- GitHub Actions build pipeline
- Image pushed to AWS ECR
- Deployment to ECS Fargate via `deploy.yml`

### 🧪 Phase 7–8: Testing Automation
- `trivy_agent.py`: Security scan using Trivy
- `smoke_test.sh`: Verifies health of the running app

### 🧠 Phase 9–10: LangGraph Agents
- **Planner Agent**: Orchestrates deployment phases
- **LLM Agent**: Decides whether to deploy based on test results
- **Deploy Agent**: Triggers ECS Fargate update (with `force-new-deployment`)

---

## 🤖 Project Structure

```
.
├── app/
│   ├── main.py                 # Flask App
│   └── gunicorn.conf.py        # Gunicorn Config
├── agents/
│   ├── planner_agent.py        # Orchestration Agent
│   ├── llm_decision_agent.py   # LLM-based Decision Maker
│   ├── deploy_agent.py         # ECS Deployment Agent
│   └── trivy_agent.py          # Security Scanning Agent
├── smoke_test.sh               # Bash Smoke Test
├── Dockerfile                  # App Container
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions Pipeline
├── .env                        # Environment Variables (not committed)
├── .gitignore                  # Git ignore file
└── README.md                   # This file
```

---

## 🚀 Deployment Flow

1. **Build** & tag Docker image (`agentic-poc:latest`)
2. **Push** image to AWS ECR
3. **ECS Fargate** pulls new image & deploys
4. **Health Check** via `smoke_test.sh`
5. **LLM Agent** makes deploy decision based on test results
6. **Deployment** triggered via ECS APIs

---

## ⚙️ Prerequisites

- **Python 3.9+**
- **Docker** + **AWS CLI** + ECR access
- **OpenAI API Key** (`OPENAI_API_KEY`)
- **AWS credentials** (via env or IAM)

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd agentic-poc

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials
```

---

## 🔐 Environment Configuration

Create a `.env` file with:

```env
OPENAI_API_KEY=your_openai_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1
ECR_REPOSITORY=your-ecr-repo-uri
ECS_CLUSTER=your-ecs-cluster-name
ECS_SERVICE=your-ecs-service-name
```

⚠️ **Important**: `.env` is in `.gitignore` and should never be committed to version control.

---

## 🏃 Running the Project

### Local Development

```bash
# Run Flask app locally
python app/main.py

# Or with Docker
docker build -t agentic-poc:latest .
docker run -p 5000:5000 agentic-poc:latest
```

### Running Agents

```bash
# Run security scan
python agents/trivy_agent.py

# Run smoke test
./smoke_test.sh

# Run deployment orchestration
python agents/planner_agent.py
```

---

## 👩‍💻 Sample Output

When you access the running application:

```json
{
  "app": "agentic-poc",
  "env": "staging",
  "message": "hello from AI Agents POC"
}
```

---

## 🧪 Testing

### Manual Testing

```bash
# Health check
curl http://localhost:5000/

# Expected response
{"app":"agentic-poc","env":"staging","message":"hello from AI Agents POC"}
```

### Automated Testing

```bash
# Run smoke test
bash smoke_test.sh

# Run security scan
python agents/trivy_agent.py
```

---

## 🧠 Next Phase (Coming Soon)

- [ ] Automate `docker build`, `tag`, `push` via agent
- [ ] Add rollback strategy based on health checks
- [ ] Integrate MCP server for multi-agent coordination
- [ ] GitHub PR checks with agent-generated responses
- [ ] Advanced monitoring and alerting integration
- [ ] Multi-environment deployment support (dev/staging/prod)

---

## 📚 Documentation

### Agent Architecture

The system uses multiple specialized agents:

1. **Planner Agent**: Coordinates the overall deployment workflow
2. **Trivy Agent**: Performs security vulnerability scanning
3. **LLM Decision Agent**: Uses OpenAI to make intelligent deployment decisions
4. **Deploy Agent**: Executes the actual ECS deployment

### Key Technologies

- **LangGraph**: Agent orchestration framework
- **LangChain**: LLM integration and tooling
- **AWS ECS Fargate**: Serverless container deployment
- **GitHub Actions**: CI/CD automation
- **Trivy**: Container security scanning
- **Flask + Gunicorn**: Python web application

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## ✨ Credits

Built by **Rohini Swathi B.** | Guided by LangGraph, LangChain, and AWS ❤️

---

## 📧 Contact

For questions or feedback, please open an issue in the GitHub repository.

---

## 🔗 Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [Trivy Security Scanner](https://trivy.dev/)
- [Flask Documentation](https://flask.palletsprojects.com/)
