# One Spirit Workflow & Business Analytics System

Web-based workflow and business evaluation dashboard developed by **GVSys (Gueh Visual Systems)** to modernize event and project operations for **PT. One Spirit Asia**.

This repository transitions the original Excel-based manual workflow into a centralized, relational database-backed web application with dynamic executive analytics.

---

## 1. Local Demo Instructions (Panduan Menjalankan Sistem)

Follow these steps to run the complete environment locally on Docker:

### Prerequisites:
- Docker Desktop installed and running.

### Startup Command:
Run the following command in the project root directory:
```bash
docker compose down
docker compose up -d --build
```

### Verification (Checklist Kesehatan Sistem):
- Check that all containers are healthy:
  ```bash
  docker compose ps
  ```
- **Backend API Health Check**: Open `http://localhost:8000/health` in your browser. It should return:
  ```json
  {"status":"ok","service":"onespirit-backend"}
  ```
- **Interactive Swagger Documentation**: Open `http://localhost:8000/docs` to inspect API endpoints.

---

## 2. Key Port/Service URLs

| Service | Local URL | Role Context |
| :--- | :--- | :--- |
| **Frontend Application** | [http://localhost:5173/](http://localhost:5173/) | Workflow board, Executive Dashboard UI, Excel Import UI |
| **Backend REST API** | [http://localhost:8000/](http://localhost:8000/) | Fast API backend service |
| **Interactive API Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) | Swagger developer API endpoints documentation |
| **API Health Check** | [http://localhost:8000/health](http://localhost:8000/health) | Live system diagnostics |

*Note: Initial seed credentials (login) are prepared inside the database seed configuration.*

---

## 3. Presentation & Alignment Resources (Aset Demo Klien)

To prepare for a structured presentation to PT. One Spirit Asia, please refer to the following documents in the `docs/` folder:

- **[Client Demo Flow (Panduan Alur Rapat)](file:///E:/GVsys%20Project/One%20Spirit/docs/client-demo-flow.md)**: A step-by-step roadmap for walking the client through the UI features.
- **[Demonstration Speech Script (Skrip Bicara)](file:///E:/GVsys%20Project/One%20Spirit/docs/demo-script.md)**: Script template in Indonesian for natural presenter speech during the meeting.
- **[Pre/Post Demo Checklist (Daftar Periksa)](file:///E:/GVsys%20Project/One%20Spirit/docs/demo-checklist.md)**: Technical diagnostics to verify before presenting to prevent issues.
- **[Demo Data Selection Guidelines (Panduan Pilihan Data)](file:///E:/GVsys%20Project/One%20Spirit/docs/demo-data-recommendation.md)**: Highlights which projects to present (ideal case vs data quality warnings).
- **[Proposal Requirement Alignment (Kepatuhan Proposal)](file:///E:/GVsys%20Project/One%20Spirit/docs/proposal-alignment.md)**: Details implemented features against GVSys proposal (100% Implemented).
- **[MVP Scope Boundaries (Batas Cakupan MVP)](file:///E:/GVsys%20Project/One%20Spirit/docs/mvp-scope.md)**: Categorizes MVP items vs proposed Fase 2 items (integrations, billing nominals).
- **[Client Business Questionnaire (Kuesioner Validasi)](file:///E:/GVsys%20Project/One%20Spirit/docs/client-validation-questions.md)**: Validation questions to clarify status timelines and PO/PM assignments with management.
- **[MVP Technical Limits (Batasan Sistem)](file:///E:/GVsys%20Project/One%20Spirit/docs/known-limitations-before-client-demo.md)**: Document listing constraints in client-safe language (Local-first, manual import validations).

For a complete index of all developer sprint logs and walk-throughs, refer to the **[Documentation Index (Indeks Dokumentasi)](file:///E:/GVsys%20Project/One%20Spirit/docs/README.md)**.

---

## 4. Known Deploy Constraints
- **Local-First Prototype**: The application is configured for local running (Docker containers). Production cloud deployment (AWS/GCP/DigitalOcean) and automatic cloud backup systems are **not** included in the MVP and are recommended for the next phase.
- **Development Database**: The database is seeded automatically with development initial roles and test records. Full baseline production data migration will be finalized after client data structures are validated.
