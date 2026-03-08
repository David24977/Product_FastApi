# FastAPI Product Microservice with AI Analysis

## Backend microservice built with FastAPI and PostgreSQL that integrates AI-powered product analysis using Groq LLM.

## The project demonstrates how to integrate Large Language Models (LLMs) into a backend API while maintaining clean architecture and backend business logic separation.

## Features

- REST API built with FastAPI

- AI-powered product analysis

- Integration with Groq LLM API

- Clean architecture (Router / Service / Repository)

- Async external AI client using httpx

- Validation using Pydantic

- Environment configuration via .env

- Business logic handled in backend (not by AI)

## AI Product Analysis

### The system analyzes products using an LLM to automatically generate:

- product category

- product tags

- price evaluation

- Business rules such as stock status are calculated in the backend.

## Example Endpoint
````
POST /products/{product_id}/ai/analyze
````

## Example response:

````
{
  "category": "electronics",
  "tags": [
    "mouse",
    "gaming",
    "computer"
  ],
  "price_evaluation": "normal",
  "stock_status": "low"
}
````
|Field   |Source
|-----   |------
|category|AI model
|tags	   |AI model
|price_evaluation	|AI model
stock_status	|Backend logic

## Architecture

### The application follows a layered architecture similar to enterprise backend systems.
````
Router
 ↓
ProductService
 ↓
AIService
 ↓
AIClient
 ↓
Groq LLM API
````

## Layer Responsibilities
|Layer	|Responsibility
|-----  |--------------
|Router	|HTTP endpoints
|Service	|Business logic
|Repository	|Database access
|AIService	|Prompt construction
|AIClient	External |AI communication
|Schemas	|Data validation

## Project Structure
````
Product_FastApi
│
├── app
│   ├── clients
│   │   └── ai_client.py
│   │
│   ├── core
│   │   └── config.py
│   │
│   ├── models
│   │   └── product.py
│   │
│   ├── repositories
│   │   └── product_repository.py
│   │
│   ├── routers
│   │   └── product_router.py
│   │
│   ├── schemas
│   │   ├── product_ai.py
│   │   └── product_ai_response.py
│   │
│   └── services
│       ├── ai_service.py
│       └── product_service.py
│
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
````

## Environment Configuration

### The application uses environment variables stored in .env.

### Example:

````
APP_NAME=product-microservice
APP_ENV=dev

DB_HOST=localhost
DB_PORT=5432
DB_NAME=product_db
DB_USER=postgres
DB_PASSWORD=your_password

AI_API_KEY=your_api_key
AI_BASE_URL=https://api.groq.com/openai/v1
AI_MODEL=llama-3.1-8b-instant
````

### Configuration is managed using Pydantic Settings.

## Installation

### Clone the repository:

````
git clone https://github.com/yourusername/product_fastapi.git
cd product_fastapi
````

## Create a virtual environment:
````
python -m venv .venv
````
## Activate environment:

# Windows
````
.venv\Scripts\activate
````
# Linux / macOS
````
source .venv/bin/activate
````

## Install dependencies:
````
pip install -r requirements.txt
````
## Running the API

### Start the server:
````
uvicorn main:app --reload
````
## API documentation available at:
````
http://127.0.0.1:8000/docs
````
## Technologies

- FastAPI

- PostgreSQL

- SQLAlchemy

- Pydantic

- httpx

- Groq LLM API

- Python Async

## Design Principles

### The system follows an important rule when integrating AI into backend systems.

## AI handles

- classification

- semantic tagging

- price interpretation

## Backend handles

- business rules

- stock calculations

- validations

- deterministic logic

### This ensures predictable and reliable backend behavior.

## Future Improvements

### Possible enhancements:

- AI result caching

- support for multiple LLM providers

- authentication and authorization

- product recommendation system

- pagination and filtering

## Author
### David Ferrer
## Backend project developed to demonstrate modern Python backend development with AI integration.
