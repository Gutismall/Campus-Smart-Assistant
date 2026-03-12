# 🎓 Campus Smart Assistant

The **Campus Smart Assistant** is a comprehensive, AI-powered platform designed to enhance the academic experience for students, lecturers, and administrators. By leveraging LLM Tools, the assistant provides intelligent, context-aware responses to queries regarding schedules, campus locations, course syllabi, and administrative procedures.   

## 🚀 Key Features

- **AI Chatbot (LLM Tools)**: Integration with Google Gemini and OpenAI to provide accurate answers based on campus-specific data.
- **Role-Based Access**: Specialized interfaces and permissions for Students, Lecturers, and System Administrators.
- **Data Management**: Automated database migrations and seeding for campus entities (Buildings, Divisions, Tests, etc.).
- **Cloud Native**: Fully containerized with Docker and ready for AWS deployment via Terraform.
- **CI/CD Automated**: Streamlined deployment pipeline using GitHub Actions.

---

## 🔑 Environment Configuration

This section lists all the environment variables and secrets required to run the project locally and in production.

### 1. Database Configuration
Used by both the backend and the database container.

| Variable | Description | Example / Default |
| :--- | :--- | :--- |
| `POSTGRES_USER` | Database administrator username |
| `POSTGRES_PASSWORD` | Database administrator password |
| `POSTGRES_DB` | Name of the database |
| `DATABASE_URL` | Full connection string (Backend only) |

### 2. Backend Configuration (`backend/.env`)
Core settings for the FastAPI backend.

| Variable | Description | Requirement |
| :--- | :--- | :--- |
| `ADMIN_EMAIL` | Default administrator email for seeding | Required |
| `ADMIN_PASSWORD` | Default administrator password for seeding | Required |
| `JWT_SECRET` | Secret key for signing JWT tokens | Required (Long random string) |
| `JWT_EXPIRE_HOURS` | Token expiration time | Default: `24` |
| `LLM_PROVIDER` | AI Provider selection | `gemini` or `openai` |

### 3. AI / LLM Configuration
API keys for the selected LLM provider.

| Variable | Description | Provider |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | Google Gemini API Key | Gemini |
| `GEMINI_MODEL` | Gemini model version |
| `OPENAI_API_KEY` | OpenAI API Key | OpenAI |
| `OPENAI_MODEL` | OpenAI model version |

### 4. Frontend Configuration (`frontend/.env`)
Settings for the Next.js frontend.

| Variable | Description | Example |
| :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | URL of the backend API | `http://localhost:8000` |

### 5. Infrastructure (Terraform)
Variables required for AWS deployment (set in `Terraform/terraform.tfvars`).

| Variable | Description |
| :--- | :--- |
| `db_password` | RDS instance password |
| `db_username` | RDS instance username |
| `db_name` | RDS database name |
| `admin_email` | Admin user email for ECS |
| `admin_password` | Admin user password for ECS |
| `gemini_api_key` | Gemini API key for ECS |
| `jwt_secret` | JWT secret for ECS |
| `text_to_sql_schema_context` | Database schema context for the AI |
| `llm_provider` | `gemini` or `openai` |

### 6. CI/CD (GitHub Secrets)
The following secrets MUST be configured in your GitHub Repository settings (`Settings > Secrets and variables > Actions`).

| Secret Name | Description |
| :--- | :--- |
| `AWS_ACCESS_KEY_ID` | AWS Access Key for deployment |
| `AWS_SECRET_ACCESS_KEY` | AWS Secret Key for deployment |
| `NEXT_PUBLIC_API_URL` | Production API URL (Passed during build) |

---

## 🛠 Setup Instructions

### Local Development (Docker)
1.  Navigate to `db/` and create a `.env` file with `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB`.
2.  Navigate to `backend/` and create a `.env` file using the variables listed above.
3.  Navigate to `frontend/` and create a `.env` file with `NEXT_PUBLIC_API_URL`.
4.  Run `docker-compose up --build` from the root directory.

### Production Deployment (Terraform)
1.  Ensure `Terraform/terraform.tfvars` is populated with the required values.
2.  Provide AWS credentials via environment variables or AWS CLI.
3.  Run `terraform apply`.
