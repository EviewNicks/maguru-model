# 🏛️ Maguru AI Backend (`maguru-model`) Architecture Specification

**Author:** Technical Architecture Lead & AI Engineer  
**Status:** Approved Enterprise Architecture Specification  
**Version:** 2.1.0 (Modular 4-Agent Architecture, LangGraph CLI & Supabase Persistence)

---

## 1. 📌 Executive Architecture Overview

`maguru-model` adalah backend microservice AI terdedikasi berbasis Python (FastAPI + LangChain / LangGraph / LangServe) yang menggerakkan seluruh kecerdasan buatan pada ekosistem platform **Maguru**, meliputi:

1. **Stateful AI Co-Teacher Agent (`app/agents/co_teacher/`)**: Asisten belajar interaktif dengan *multi-turn memory persistence* (`thread_id`), personalisasi salam murid (*greeting*), dan *RAG context enrichment* via Server-Sent Events (SSE) streaming.
2. **Pedagogical Code Explainer Agent (`app/agents/code_explainer/`)**: Pembongkar potongan kode baris-per-baris dengan model mental dan visualisasi LangGraph.
3. **Progressive Scaffolding Hint Generator Agent (`app/agents/hint_generator/`)**: Asisten latihan adaptif dengan 3 tingkat petunjuk bertingkat (*progressive hints*) berbasis LangGraph.
4. **Automated Quiz Engine Agent (`app/agents/quiz_engine/`)**: Generator kuis pilihan ganda otomatis dan evaluator feedback jawaban murid.
5. **LangGraph CLI & Studio Manifest (`langgraph.json`)**: Konfigurasi declarative multi-graph yang memungkinkan visualisasi diagram alir dan time-travel debugging via `langgraph dev`.
6. **Supabase PostgreSQL Checkpointer (`app/db/checkpointer.py`)**: Persistensi state percakapan jangka panjang menggunakan `PostgresSaver` dengan *connection pooling* (`psycopg_pool`) dan graceful fallback ke `InMemorySaver`.
7. **Multi-Model Failover Resilience Pool (`app/shared/llm.py`)**: Ketahanan tinggi terhadap *Rate-Limit (429)* atau *Endpoint Offline* menggunakan model pool OpenRouter.
8. **RAG Vector Knowledge Base (`app/shared/rag_service.py` & `app/shared/vector_store.py`)**: Ingestion dokumen dan similarity search menggunakan PostgreSQL `pgvector`.

---

## 2. 🧱 Clean Layered Architecture (N-Tier for AI Microservices)

Arsitektur `maguru-model` mengadopsi **Clean Modular Layering** yang memisahkan tanggung jawab sistem secara tegas:

```mermaid
graph TD
    subgraph Presentation_API_Layer ["1. API & Presentation Layer (app/api/ & LangServe)"]
        Routes["FastAPI Routers (app/api/v1/)"]
        LangServeRoutes["LangServe Playground & SSE Routes (/chatbot, /hint, /explain-code, /generate-quiz)"]
    end

    subgraph State_Graph_Layer ["2. Orchestration & Graph Layer (app/graphs/ & app/chains/)"]
        QAGraph["StateGraph QA Assistant (app/graphs/qa_graph.py)"]
        QuizGraph["Direct Quiz Graph (app/graphs/quiz_graph.py)"]
        LCELChains["LCEL Reasoning Pipelines (app/chains/)"]
    end

    subgraph Business_Service_Layer ["3. Business & Domain Service Layer (app/services/)"]
        RAGService["RAG Ingestion & Vector Search (app/services/rag_service.py)"]
    end

    subgraph Infrastructure_Data_Layer ["4. Infrastructure & Data Layer (app/core/, app/db/, app/schemas/)"]
        ModelPool["Multi-Model Pool & Fallback Engine (app/core/llm.py)"]
        Config["App Configuration & Env Loader (app/core/config.py)"]
        Checkpointer["LangGraph State Persistence Provider (app/db/checkpointer.py)"]
        VectorDB["PGVector Store Provider (app/db/vector_store.py)"]
        Schemas["Pydantic v2 DTO & Schemas (app/schemas/)"]
    end

    Presentation_API_Layer --> State_Graph_Layer
    State_Graph_Layer --> Business_Service_Layer
    State_Graph_Layer --> Infrastructure_Data_Layer
    Business_Service_Layer --> Infrastructure_Data_Layer
```

---

## 3. 📂 Standard Directory Structure

```text
maguru-model/
├── langgraph.json               # LangGraph CLI & Studio Declarative Manifest
├── app/                         # Core Application Package
│   ├── __init__.py
│   ├── main.py                  # FastAPI Application Factory & Lifespan Handler
│   │
│   ├── agents/                  # Modular 4-Agent Domain Packages (Vertical Slices)
│   │   ├── __init__.py          # Export of chain factories across all 4 agents
│   │   ├── co_teacher/          # Co-Teacher Agent (StateGraph, RAG, Greeting, Stream)
│   │   │   ├── __init__.py
│   │   │   ├── graph.py         # StateGraph QA with thread_id persistence
│   │   │   ├── greeting.py      # Personalized greeting generator
│   │   │   └── entrypoint.py    # LangServe chain factory
│   │   ├── code_explainer/      # Code Explainer Agent (StateGraph & LCEL)
│   │   │   ├── __init__.py
│   │   │   ├── graph.py         # StateGraph Code Explainer
│   │   │   └── entrypoint.py    # Pedagogical explanation logic
│   │   ├── hint_generator/      # Progressive Hint Agent (StateGraph & LCEL)
│   │   │   ├── __init__.py
│   │   │   ├── graph.py         # StateGraph Progressive Hint
│   │   │   └── entrypoint.py    # 3-level hint logic
│   │   └── quiz_engine/         # Quiz Engine Agent (StateGraph, Multi-Q, Feedback)
│   │       ├── __init__.py
│   │       ├── graph.py         # StateGraph Quiz Generator
│   │       └── entrypoint.py    # Evaluation & feedback logic
│   │
│   ├── shared/                  # Common Cross-Cutting Infrastructure
│   │   ├── __init__.py
│   │   ├── config.py            # Global Settings proxy
│   │   ├── llm.py               # OpenRouter Multi-Model Pool Provider
│   │   ├── checkpointer.py      # Checkpointer singleton proxy
│   │   ├── vector_store.py      # PGVector Store Provider
│   │   └── rag_service.py       # RAG Retrieval Service proxy
│   │
│   ├── api/                     # REST API Routes & Endpoints
│   │   ├── __init__.py
│   │   ├── router.py            # Aggregated APIRouter
│   │   └── v1/
│   │       ├── chat.py          # POST /api/v1/chat/stream & POST /api/v1/chat
│   │       ├── ingest.py        # POST /api/v1/ingest & POST /admin/ingest
│   │       ├── quiz.py          # POST /api/v1/generate-quiz
│   │       └── health.py        # GET /health & GET /
│   │
│   ├── db/                      # Persistence & Database Providers
│   │   ├── __init__.py
│   │   ├── checkpointer.py      # Supabase PostgresSaver with ConnectionPool & fallback
│   │   └── vector_store.py      # PGVector Provider (langchain-postgres)
│   │
│   ├── prompts/                 # Externalized YAML Prompt Templates
│   ├── schemas/                 # Pydantic v2 Data Transfer Objects (DTO)
│   ├── chains/                  # Backward Compatibility LCEL Shims
│   └── graphs/                  # Backward Compatibility Graph Shims
│
├── tests/                       # Automated Test Suite (38 Tests, 100% Pass)
│   ├── conftest.py
│   ├── test_agents_modular.py   # MoSCoW Unit & Integration Tests for 4 Agents
│   ├── test_checkpointer.py     # PostgresSaver Connection Pool & Fallback Tests
│   ├── test_graphs.py           # LangGraph State & Streaming Tests
│   └── ...
│
├── server.py                    # Root Entrypoint Wrapper
├── requirements.txt             # Python Dependencies
└── pytest.ini                   # Pytest Configuration
```

---

## 4. 🔄 System Data & Execution Flows

### Flow A: Stateful AI Co-Teacher Q&A Streaming (LangGraph + Memory)
```mermaid
sequenceDiagram
    autonumber
    actor Siswa as Frontend Next.js
    participant API as FastAPI / LangServe (/chatbot/stream)
    participant Graph as LangGraph QA StateGraph
    participant Mem as Checkpointer (thread_id)
    participant Vector as PGVector (Supabase)
    participant Pool as Model Failover Pool

    Siswa->>API: POST /api/v1/chat/stream {question, course_id, thread_id}
    API->>Graph: astream_qa_graph(question, course_id, thread_id)
    Graph->>Mem: Lookup previous conversation by thread_id
    Mem-->>Graph: Conversation history messages
    opt course_id is provided
        Graph->>Vector: Similarity Search (get_course_context)
        Vector-->>Graph: Relevant Course Content Chunks
    end
    Graph->>Pool: Invoke primary model with system instructions
    alt Primary model 429 / 404
        Pool->>Pool: Automatic Failover to Fallback Model 2 / Model 3
    end
    Pool-->>API: Yield Token-by-Token SSE Chunks
    API-->>Siswa: Real-time SSE Stream (Typing effect)
    Graph->>Mem: Save updated messages to checkpointer state
```

### Flow B: Automated Multi-Quiz Generation (Direct Lesson / RAG)
```mermaid
sequenceDiagram
    autonumber
    actor Admin as Admin / Guru / Siswa
    participant API as FastAPI Router (/api/v1/generate-quiz)
    participant Chain as Quiz Generator Chain
    participant Pool as Model Failover Pool
    participant Parser as JSON Extractor & Validator

    Admin->>API: POST /api/v1/generate-quiz {lesson_content, num_questions: 5, difficulty}
    API->>Chain: generate_quiz_questions(course_id, num_questions, difficulty, lesson_content)
    Chain->>Pool: Execute Prompt (Strict JSON formatting)
    Pool-->>Chain: Raw Output String
    Chain->>Parser: _extract_json_array(raw_output)
    Parser-->>Chain: Validated List of 5 MCQ Objects
    Chain-->>API: GenerateQuizResponseSchema
    API-->>Admin: HTTP 200 OK with Structured Questions Array
```

---

## 5. 🛠️ Technology Stack & Package Versions

| Komponen | Library / Teknologi | Peran dalam Arsitektur |
| :--- | :--- | :--- |
| **API Gateway** | `FastAPI (>=0.110.0)`, `Uvicorn`, `sse-starlette` | Web framework, route dispatcher, Server-Sent Events |
| **Graph Orchestrator** | `langgraph (>=0.2.20)` | StateGraph workflows, multi-turn memory, cyclic graphs |
| **LangChain Ecosystem**| `langchain (>=0.3.0)`, `langchain-core`, `langserve` | Prompt management, LCEL, runnable interfaces |
| **Model Integration** | `langchain-openai (>=0.2.0)`, `openai (>=1.30.0)` | OpenRouter API client, model fallback chains |
| **Vector Database** | `langchain-postgres (>=0.0.12)`, `psycopg (>=3.1.18)` | Modern PostgreSQL pgvector vector store provider |
| **Data Validation** | `pydantic (>=2.6.0)`, `pydantic-settings` | DTO data validation, environment configuration |
| **Testing Suite** | `pytest (>=8.0.0)`, `pytest-asyncio`, `pytest-cov` | Automated unit, architecture, and integration tests |

---

## 6. 🛡️ High-Availability Failover Strategy

Model gratis OpenRouter dikonfigurasi dalam urutan prioritas di `.env`:
```env
OPENROUTER_MODEL_1=nvidia/nemotron-3.5-lightning:free
OPENROUTER_MODEL_2=dots-studio/dots-3-note-preview:free
OPENROUTER_MODEL_3=liquid/lfm-2.5-2.6b:free
```

* **Mekanisme Otomatis**:
  Setiap chain dan graph dibungkus dengan `primary_llm.with_fallbacks([fallback_1, fallback_2])`.
  Jika model utama mengalami *Rate-Limit (429)*, *Model Offline (404)*, atau *Server Error (500)*, sistem **secara instan mengalihkan eksekusi ke model cadangan berikutnya** tanpa interupsi pada sisi pengguna.

---

## 7. 🧪 Quality Assurance & Test Verification

Status suite pengujian saat ini:
- **18 dari 18 Test Suites PASSED (100% Green)**.
- Seluruh endpoint API, singleton checkpointer, node StateGraph, dan chain parser telah tervalidasi secara otomatis.
