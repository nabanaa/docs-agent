# Docs Agent

A production-ready AI Agent architecture integrating **Google Gemini 2.0 Flash** with a high-performance Python backend. Designed for cloud scalability and enterprise-grade document interaction.

## 🌟 Overview
This project serves as a template for building "Agentic" workflows. It decouples the AI logic from the user interface using a microservices-style architecture, making it easy to deploy on platforms like **Microsoft Azure** or **Google Cloud**.

## 🛠️ Tech Stack
- **Language:** Python 3.11+
- **LLM Engine:** Google Gemini (via `google-genai` SDK)
- **Backend:** FastAPI (Async ASGI framework)
- **Validation:** Pydantic v2
- **Frontend:** Streamlit
- **DevOps:** Docker & Docker Compose

## 🚀 Key Features
- **Asynchronous Processing:** Non-blocking API calls to Gemini for high concurrency.
- **Strict Typing:** Full Pydantic validation for Request/Response schemas.
- **Auto-Documentation:** Interactive Swagger UI available out-of-the-box.
- **Containerized Environment:** Pre-configured Docker setup for "plug-and-play" deployment.
- **Security First:** Environment variable management using `pydantic-settings`.

## 📦 Getting Started

### Prerequisites
- Docker and Docker Compose installed.
- A Google AI Studio API Key (Gemini).

### Installation
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/nabanaa/docs-agent.git](https://github.com/nabanaa/docs-agent.git)
   cd docs-agent
   ```
2. **Setup Environment Variables: Copy the example file and fill in your API keys:**
   ```bash
   cp .env.example .env
   ```
3. **Run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```
## 🏗️ Project Structure
- `app/main.py`: FastAPI entry point and routing.
- `app/services/ai_engine.py`: Gemini API integration and logic.
- `app/core/config.py`: Configuration and environment management.
- `ui/`: Streamlit frontend application.
- `docker-compose.yml`: Multi-container orchestration.

## 📈 Roadmap
- [ ] **RAG Integration:** Connect a Vector Database (like ChromaDB or Qdrant) to store document embeddings.
- [ ] **Document Processing:** Add an endpoint to upload and parse PDF/TXT files.
- [ ] **Azure Deployment:** Set up GitHub Actions for automated deployment to Azure App Service.

---
Created by [nabanaa](https://github.com/nabanaa)
