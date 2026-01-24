# Mirath

## Prerequisites

Before running the project, make sure you have the following installed:

- **Python 3.10+**
- **Conda** (Anaconda or Miniconda)
- **Git**
- **Docker**  

## How to Run

1- Clone repo:
```bash
git clone <repo-link>
cd project-folder
```
2️- Create a new environment:
```bash
conda create -n env-name python=3.10
```
3️- Activate the environment:
```bash
conda activate env-name
```

### Install the required packages
```bash
cd src
cp .env.example .env
pip install -r requirements.txt
```
### Configure environment variables:
Edit the `.env` file with your API keys and configuration:
```env
CONNECTION_URL=your_mongodb_connection_string
DATABASE_NAME=your_database_name
COHERE_API_KEY=your_api_key
GEMINI_API_KEY=your_api_key
QDRANT_URL=qdrant_connection_url
DISTANCE_METHOD=select_an_appropriate_method(Cosine, Dot)
```

### Run Docker Compose Services
```bash
docker compose up
```
### Run the FastAPI server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
### Access Services
- FastAPI: http://localhost:5000

## Endpoints documentation

## 1- GET /health-check

### Description
Health check endpoint to verify that the AI service is running successfully.
### Method
`GET`
### Body
No request body
### Success Response
```json
{
  "app_name": "Mirath"
}
```
**Status Code:** `200 OK`

### Error Responses
`500 Internal Server Error`

## 2- POST /upload/papers

### Description
Upload research papers, generate embeddings, and store them in the database and vector database.
### Method
`POST`
### Body
```json
{
  "file": "file_name.json",
  "survey": false
}
```
### Success Response
```json
{
  "message from mongo": "Data uploaded successfully.",
  "message from qdrant": "Data inserted into vector database successfully."
}
```
**Status Code:** `200 OK`

### Error Responses
```json
{
  "message from mongo": "Unable to upload some records.",
  "message from qdrant": "Error inserting data into vector database."
}
```
**Status Code:** `400 Bad Request`

## 3- DELETE /papers

### Description
Delete research papers from both the database and the vector database using their IDs.
### Method
DELETE
### Body
```json
{
  "ids": ["paper_id1", "paper_id2", ...]
}
```
### Success Response
```json
{
  "result from qdrant": "Paper deleted successfully.",
  "result from mongo": "Paper deleted successfully.",
  "not_found": ["file_id1", "file_id2", ...]
}
```
**Status Code:** `200 OK`

### Error Responses
```json
{
  "result from qdrant": "Cannot delete paper because this ID is not in the database.",
  "result from mongo": "Cannot delete paper because this ID is not in the database.",
  "not_found": ["file_id1", "file_id2", ...]
}
```
**Status Code:** `404 Not Found`

## 4- POST /create/papers

### Description
Create research papers by storing their data and generating embeddings.
### Method
POST
### Body
```json
{
  "papers": [{
    "id": "id_1",
    "title": "title_1",
    "authors": ["author_1",...],
    "citation": "citation_1",
    "publishedAt": "publishedAt_1",
    "categories": ["cat_1",...],
    "abstract": "abstract_1"
  }, ...]
}
```
### Success Response
```json
{
  "result from qdrant": "Data uploaded successfully.",
  "result from mongo": "Data uploaded successfully.",
  "failed ids": ["failed_id1", "failed_id2", ...]
}
```
**Status Code:** `201 OK`

### Error Responses
```json
{
  "result from qdrant": "Failed to create papers",
  "result from mongo": "Failed to create papers",
  "failed ids": ["failed_id1", "failed_id2", ...]
}
```
**Status Code:** `400 Bad Request`

## 5- POST /search/papers
### Description
Search for relevant research papers based on user question using vector similarity search.
### Method
POST
### Body
```json
{
    "question": "user_question",
    "limit": 3
}
```
### Success Response
```json
{
    "response": ["id1", "id2", "id3"]
}
```
**Status Code:** `200 OK`

### Error Responses
```json
{
  "response": "Cannot embed the provided text."
}
```
**Status Code:** `400 Bad Request`