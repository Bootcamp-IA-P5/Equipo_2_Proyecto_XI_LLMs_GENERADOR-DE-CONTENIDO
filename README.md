# 🤖 Project XI - LLM Content Generator

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.124+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic-orange?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)

**Una plataforma avanzada de generación de contenido multi-agente potenciada por LLMs y RAG.**

[Repositorio](https://github.com/Bootcamp-IA-P5/Equipo_2_Proyecto_XI_LLMs_GENERADOR-DE-CONTENIDO) • [Gestión del Proyecto](https://github.com/orgs/Bootcamp-IA-P5/projects/29/views/1) • [Documentación de API](/docs)

</div>

---

## 📖 Descripción del Proyecto

**Project XI** es un ecosistema inteligente diseñado para automatizar la creación de contenido de alta calidad para diversas plataformas (Redes Sociales, Blogs, Informes Financieros, etc.). Utilizando una arquitectura de **Sistemas Multi-Agente** con **LangGraph** y técnicas de **RAG (Retrieval-Augmented Generation)**, el sistema es capaz de investigar, redactar y optimizar contenido basándose en fuentes de datos en tiempo real y bases de conocimiento personalizadas.

### ✨ Características Principales
- 🧠 **Sistemas Multi-Agente:** Flujos de trabajo orquestados con LangGraph para investigación y redacción.
- 📚 **RAG & Graph RAG:** Recuperación inteligente de información desde documentos y grafos de conocimiento.
- 📈 **Integración de Datos Reales:** Conexión con APIs financieras (yfinance) y de noticias (Arxiv, RSS).
- 🎨 **Interfaz Moderna:** Aplicación web reactiva construida con React 19 y Tailwind CSS.
- 🛡️ **IA Responsable:** Implementación de Guardrails para asegurar la calidad y ética del contenido generado.

---

## 🛠️ Stack Tecnológico

<table align="center">
  <tr>
    <td align="center"><b>Backend</b></td>
    <td align="center"><b>AI & LLM</b></td>
    <td align="center"><b>Frontend</b></td>
  </tr>
  <tr>
    <td>
      <ul>
        <li>FastAPI</li>
        <li>Python 3.11</li>
        <li>PostgreSQL / SQLAlchemy</li>
        <li>Pydantic v2</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>LangChain / LangGraph</li>
        <li>ChromaDB (Vector Database)</li>
        <li>Groq / Ollama</li>
        <li>Guardrails AI</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>React 19</li>
        <li>Vite</li>
        <li>Tailwind CSS</li>
        <li>Axios / React Router</li>
      </ul>
    </td>
  </tr>
</table>

---

## 🚀 Comenzando

### 🐳 Inicio Rápido con Docker (Recomendado)

Si tienes Docker instalado, puedes levantar todo el entorno con un solo comando:

```bash
docker-compose up --build
```

La aplicación estará disponible en:
- **Frontend:** [http://localhost:3000](http://localhost:3000)
- **API Backend:** [http://localhost:8000](http://localhost:8000)
- **Documentación Swagger:** [http://localhost:8000/docs](http://localhost:8000/docs)

### 🔧 Instalación Manual

#### Backend
1. Navega al directorio backend: `cd backend`
2. Crea un entorno virtual: `python -m venv .venv`
3. Instala dependencias: `pip install -r requirements.txt`
4. Configura el archivo `.env` (usa `.env.example` como guía).
5. Ejecuta: `uvicorn app.main:app --reload`

#### Frontend
1. Navega al directorio frontend: `cd frontend`
2. Instala dependencias: `npm install`
3. Ejecuta el servidor de desarrollo: `npm run dev`

---

## 🗂️ Estructura del Proyecto

```text
.
├── backend/                # API y Lógica de Agentes
│   ├── app/                # Código fuente de FastAPI
│   │   ├── agents/         # Definición de Agentes LangGraph
│   │   ├── rag/            # Lógica de RAG y Vectores
│   │   └── api/            # Endpoints y Rutas
│   └── tests/              # Suite de Pruebas
├── frontend/               # Interfaz de Usuario
│   ├── src/                # Componentes y Páginas React
│   └── public/             # Recursos Estáticos
└── docker-compose.yml      # Orquestación de Contenedores
```

---

## 👥 Equipo de Desarrollo

| Rol | Miembro | GitHub |
| :--- | :--- | :--- |
| 🎯 **Scrum Master** | Umit | [@user](https://github.com/) |
| 📊 **Product Owner** | Ignacio | [@user](https://github.com/) |
| 💻 **Developer** | Yeder | [@user](https://github.com/) |
| 💻 **Developer** | Maria | [@user](https://github.com/) |

---

## 🔄 Estado del Proyecto

- [x] Arquitectura Base (Backend & Frontend)
- [x] Integración de LangGraph agents
- [/] Implementación de Graph RAG (En progreso)
- [ ] Implementación de Guardrails avanzada
- [ ] Despliegue en Producción

---
<div align="center">
Desarrollado con ❤️ para el Bootcamp de IA F5
</div>
