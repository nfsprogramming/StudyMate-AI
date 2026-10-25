# StudyMate AI

[![CI](https://github.com/nfsprogramming/studymate-ai-study-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/nfsprogramming/studymate-ai-study-bot/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Node: 18+](https://img.shields.io/badge/Node-18%2B-green.svg)](https://nodejs.org/)

StudyMate AI is a full-stack educational study assistant combining a **FastAPI** backend with a **React (Vite)** frontend. It provides Socratic AI tutoring grounded in the Feynman technique, multimodal document question answering (PDFs and image notes), automated quiz generation with interactive scoring and DOCX export, and Google Classroom course and assignment synchronization.

---

## Live Demo

- **Web Application:** [https://study-mate-ai-study-bot.vercel.app](https://study-mate-ai-study-bot.vercel.app)

---

## Features

### 1. Socratic AI Tutoring & Feynman Technique
- **Intuitive Concept Breakdown:** Explanations follow an intuitive structure: Intuition &rarr; Simple Example &rarr; Technical Details &rarr; Common Pitfalls &rarr; Quick Check Questions.
- **Computer Science & AI/ML Disambiguation:** Defaults terminology to CS and software engineering domains (e.g., RAG, LLM, CNN, DP, OS, GC) unless otherwise specified.
- **Streaming Responses:** Real-time token streaming using Server-Sent Events (`/api/ask`).
- **Code Highlighting & Copy:** Automatic code block syntax highlighting powered by Prism with one-click copy.
- **Voice Interactions:** Web Speech API voice input and text-to-speech audio narration.
- **Chat History & Export:** Persists sessions to Firebase Firestore (when signed in) and exports conversations to CSV or Word DOCX.

### 2. Multimodal Study Material & PDF Processing
- **Document Ingestion:** Drag-and-drop document upload (`/api/upload`) supporting:
  - **PDF Documents:** Fast text and page extraction via `PyPDF2`.
  - **Images & Handwritten Notes:** Visual transcription and equation extraction via NVIDIA NIM `meta/llama-3.2-90b-vision-instruct`.
- **In-Memory Document Indexing:** Fast document referencing, listing, and removal (`/api/documents`).

### 3. Automated Quiz Generation & Scoring
- **AI-Generated Quizzes:** Generates customized multiple-choice questions from uploaded course materials or user-defined topics (`/api/generate-quiz`).
- **Configurable Difficulty & Length:** Select question counts (3 to 20) and difficulty levels (`easy`, `medium`, `hard`).
- **Resilient Fallback Mode:** Automated deterministic quiz generation fallback when external LLM endpoints are unreachable or unconfigured.
- **Detailed Results & Reports:** Interactive review of correct answers, explanations, and downloadable Word DOCX reports.

### 4. Google Classroom & Drive Synchronization
- **OAuth 2.0 Integration:** Connect Google Classroom to browse enrolled courses, coursework assignments, and announcements.
- **Drive Import:** Direct download and parsing of lecture PDFs from Google Drive into StudyMate memory.
- **Post Quizzes as Assignments:** Publish generated quizzes back to Google Classroom courses.
- **Interactive Demo Mode:** Built-in sandbox mode for exploring Classroom UI workflows without requiring live Google cloud credentials.

### 5. Authentication & Cloud Session Storage
- **Google Sign-In:** Authenticate with Firebase Authentication.
- **Firestore Synchronization:** Secure user-scoped cloud storage of chat history with granular Firestore security rules.

---

## Tech Stack

| Layer | Technology | Details |
|---|---|---|
| **Backend Framework** | FastAPI (Python 3.10+) | Uvicorn ASGI server, Pydantic v2 validation |
| **Frontend Framework** | React 18 & Vite 5 | Tailwind CSS v4, Lucide / Material Symbols |
| **AI / LLM Endpoints** | NVIDIA NIM API | Llama 3.1 70B Instruct & Llama 3.2 90B Vision |
| **PDF Extraction** | PyPDF2 | Stream-based text and page extraction |
| **Classroom Integration**| Google APIs Client | Google Classroom API v1 & Google Drive API v3 |
| **Auth & Cloud DB** | Firebase SDK | Firebase Auth & Cloud Firestore |
| **Document Export** | docx & file-saver | Word (.docx) and CSV report generation |
| **Production Server** | Gunicorn | Uvicorn worker process manager (`Procfile`) |

---

## Project Structure

```
├── .devcontainer/             # DevContainer definition for VS Code and GitHub Codespaces
│   └── devcontainer.json
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI (backend tests & frontend build)
├── backend/
│   ├── .env.example           # Backend environment variable template
│   ├── __init__.py
│   ├── google_classroom.py    # Google Classroom and Drive API connector
│   └── main.py                # FastAPI routes, AI streaming, quiz engine
├── frontend/
│   ├── public/                # Static assets (favicons)
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.jsx   # Streaming chat, markdown & code renderer
│   │   │   ├── DocumentList.jsx    # Uploaded document manager
│   │   │   ├── FileUpload.jsx      # Drag-and-drop file uploader
│   │   │   ├── GoogleClassroom.jsx # Classroom courses & assignment sync
│   │   │   └── QuizGenerator.jsx   # Quiz generation and grading UI
│   │   ├── App.jsx            # Main dashboard and tab router
│   │   ├── firebase.js        # Firebase authentication & Firestore client
│   │   └── main.jsx           # React DOM root entrypoint
│   ├── package.json           # Frontend dependencies and build scripts
│   ├── tailwind.config.js     # Tailwind CSS theme configuration
│   └── vite.config.js         # Vite bundler configuration & API proxy
├── tests/
│   └── test_api.py            # Automated API integration test suite
├── .env.example               # Root environment configuration template
├── .gitignore                 # Git ignore rules for Python, Node, and secrets
├── app.py                     # Root ASGI execution entrypoint
├── LICENSE                    # MIT License
├── Procfile                   # Production web process definition (Gunicorn)
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python backend dependencies
└── README.md                  # Project documentation
```

---

## Prerequisites

- **Python:** 3.10 or higher
- **Node.js:** 18.0 or higher
- **npm:** 9.0 or higher
- **NVIDIA NIM API Key:** Free developer keys available at [build.nvidia.com](https://build.nvidia.com) (optional for local fallback mode).

---

## Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/nfsprogramming/studymate-ai-study-bot.git
cd studymate-ai-study-bot
```

### 2. Backend Setup
1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   ```bash
   cp backend/.env.example backend/.env
   ```
   Edit `backend/.env` and add your NVIDIA API key:
   ```env
   NVIDIA_API_KEY=nvapi-your-key-here
   NVIDIA_VISION_API_KEY=nvapi-your-vision-key-here
   ```

4. Start the FastAPI backend server:
   ```bash
   python app.py
   ```
   The backend API will start at `http://localhost:8000`. Interactive API documentation is available at `http://localhost:8000/docs`.

### 3. Frontend Setup
1. Navigate to the `frontend/` directory and install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the Vite development server:
   ```bash
   npm run dev
   ```
   The user interface will be accessible at `http://localhost:3000`.

---

## Configuration

### Environment Variables (`backend/.env`)

| Variable | Description | Required | Default |
|---|---|---|---|
| `NVIDIA_API_KEY` | Primary API key for NVIDIA NIM LLM inference (`meta/llama-3.1-70b-instruct`) | Recommended | None (activates fallback mode) |
| `NVIDIA_VISION_API_KEY` | Key for vision models (`meta/llama-3.2-90b-vision-instruct`) | Optional | Falls back to `NVIDIA_API_KEY` |
| `GOOGLE_CREDENTIALS` | JSON string of Google OAuth 2.0 Web Client credentials | Optional | Read from `backend/credentials.json` |
| `GOOGLE_TOKEN` | JSON string of stored Google OAuth access/refresh token | Optional | Read from `backend/token.pickle` |

---

## Testing & Validation

### Backend Test Suite
Run the automated test suite using `pytest`:
```bash
pytest
```

### Frontend Build Validation
Compile and type-check the frontend production bundle:
```bash
cd frontend
npm run build
```

---

## Deployment

### Production Backend (PaaS / Docker / VPS)
The repository includes a `Procfile` for platforms such as Render, Railway, or Heroku:
```bash
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app
```

### Frontend Deployment (Vercel / Cloudflare Pages)
The frontend includes `frontend/vercel.json` for single-page application routing. Point your Vercel project root to the `frontend` directory with build command `npm run build` and output directory `dist`.

---

## Limitations

- **In-Memory Document Index:** Uploaded documents are indexed in-memory per worker process; restarting the server clears uploaded documents.
- **External AI Dependency:** Streaming chat and vision image extraction rely on NVIDIA NIM API endpoints; an internet connection and valid API credentials are required for live LLM responses.
- **Google Classroom Verification:** Access to live Google Classroom courses requires a configured Google Cloud OAuth 2.0 Client ID with educational scopes enabled.

---

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add amazing feature'`).
4. Ensure tests pass (`pytest` and `npm run build`).
5. Push to the branch (`git push origin feature/amazing-feature`).
6. Open a Pull Request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
