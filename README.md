# Mirath
A smart research assistant application designed to help students, researchers, and anyone interested in academic research discover papers, explore research topics, and interact with AI-powered tools.

## Key Features
- Collected and stored research papers using **CrewAI** and **MongoDB**.
- Implemented **semantic search** using **Cohere Embeddings** and **QdrantDB** to retrieve relevant papers based on user queries.
- Built an AI chatbot using **LangGraph** and **Gemini** that can:
  - Answer general research-related questions.
  - Generate personalized learning roadmaps.
  - Supported multimodal inputs:
    - Extract text from images using **PaddleOCR**.
    - Convert voice to text using **Whisper**.
- Added helper features for research paper reading:
  - Text translation.
  - Text summarization.
  - Concept explanation.
## Upcoming Features
- Fine-tuned summarization model for structured scientific paper summarization across key facets:
  - Purpose
  - Method
  - Findings
  - Value
- AI-powered recommendation system for retrieving relevant research papers.

## Tech Stack
- Python, FastAPI 
- Langchain, LangGraph, CrewAI 
- QdrantDB, MongoDB 
- Cohere, Gemini, PaddleOCR, Whisper 
- Docker 

## Project File Tree

```markdown
├── 📂 docker
│  ├── 📄 __init__.py
│  ├── 📄 .env
│  ├── 📄 .env.example
│  ├── 📄 .gitignore
│  ├── ⚙️ docker-compose.yml
│  └── 📄 Dockerfile
├── 📂 facets_summarization
│  ├── 📄 __init__.py
│  ├── 📄 data_pre_evaluation.ipynb
│  └── 📄 data_preprocessing.ipynb
├── 📂 ScrapingDataCrew
│  ├── 📂 Agents
│  │  ├── 📂 scheme
│  │  │  ├── 📄 __init__.py
│  │  │  ├── 📄 Categories.py
│  │  │  ├── 📄 Links.py
│  │  │  └── 📄 PaperContent.py
│  │  ├── 📂 tools
│  │  │  ├── 📄 __init__.py
│  │  │  ├── 📄 FetchCategory.py
│  │  │  ├── 📄 FetchPaperLinks.py
│  │  │  └── 📄 ScrapePaper.py
│  │  ├── 📄 __init__.py
│  │  ├── 📄 CollectCategory.py
│  │  ├── 📄 ScrapePaper.py
│  │  └── 📄 SearchPapers.py
│  ├── 📂 CrewArtifactsEX
│  │  ├── 📄 __init__.py
│  │  ├── ⚙️ CategoryCollection.json
│  │  ├── ⚙️ ResearchLinks.json
│  │  └── ⚙️ ScrapePapers.json
│  ├── 📄 .env.example
│  ├── 📄 model.py
│  ├── 📄 requirements.txt
│  └── 📄 RunCrew.py
├── 📂 src
│  ├── 📂 assets
│  │  ├── 📂 data
│  │  ├── 📂 vectordb
│  │  │  └── 📂 qdrant_data
│  │  ├── 📄 __init__.py
│  │  └── 📄 .gitignore
│  ├── 📂 chatbot
│  │  ├── 📄 __init__.py
│  │  ├── 📄 Assets.py
│  │  ├── 📄 AssistantEnum.py
│  │  ├── 📄 AssistantGraph.py
│  │  ├── 📄 AssistantPrompts.py
│  │  └── 📄 AssistantScheme.py
│  ├── 📂 controllers
│  │  ├── 📄 __init__.py
│  │  ├── 📄 BaseController.py
│  │  ├── 📄 ChatController.py
│  │  ├── 📄 NLPController.py
│  │  ├── 📄 PapersController.py
│  │  └── 📄 UploadDataController.py
│  ├── 📂 enums
│  │  ├── 📄 __init__.py
│  │  ├── 📄 DatabaseEnum.py
│  │  ├── 📄 FileExtensionEnum.py
│  │  └── 📄 ResponseEnum.py
│  ├── 📂 helpers
│  │  ├── 📄 __init__.py
│  │  ├── 📄 config.py
│  │  ├── 📄 ocr_config.py
│  │  ├── 📄 services_config.py
│  │  └── 📄 stream_config.py
│  ├── 📂 llm
│  │  ├── 📂 providers
│  │  │  ├── 📄 __init__.py
│  │  │  ├── 📄 CohereProvider.py
│  │  │  └── 📄 GeminiProvider.py
│  │  ├── 📂 templates
│  │  │  ├── 📂 locales
│  │  │  │  ├── 📂 ar
│  │  │  │  │  ├── 📄 __init__.py
│  │  │  │  │  ├── 📄 explain.py
│  │  │  │  │  ├── 📄 generate_title.py
│  │  │  │  │  ├── 📄 summarize_snippet.py
│  │  │  │  │  └── 📄 translate.py
│  │  │  │  ├── 📂 en
│  │  │  │  │  ├── 📄 __init__.py
│  │  │  │  │  ├── 📄 explain.py
│  │  │  │  │  ├── 📄 generate_title.py
│  │  │  │  │  ├── 📄 summarize_snippet.py
│  │  │  │  │  └── 📄 translate.py
│  │  │  │  └── 📄 __init__.py
│  │  │  ├── 📄 __init__.py
│  │  │  └── 📄 TemplateParser.py
│  │  ├── 📄 __init__.py
│  │  ├── 📄 LLMEnums.py
│  │  ├── 📄 LLMInterface.py
│  │  └── 📄 LLMProviderFactory.py
│  ├── 📂 routes
│  │  ├── 📄 __init__.py
│  │  ├── 📄 AI_Services.py
│  │  ├── 📄 Chat.py
│  │  ├── 📄 Data.py
│  │  ├── 📄 Healthy_Check.py
│  │  └── 📄 Search.py
│  ├── 📂 scheme
│  │  ├── 📄 __init__.py
│  │  ├── 📄 AI_Services.py
│  │  ├── 📄 Chat.py
│  │  ├── 📄 Data.py
│  │  └── 📄 Search.py
│  ├── 📂 vectordb
│  │  ├── 📂 providers
│  │  │  ├── 📄 __init__.py
│  │  │  └── 📄 QdrantProvider.py
│  │  ├── 📄 __init__.py
│  │  ├── 📄 VectorDBEnum.py
│  │  ├── 📄 VectorDBFactory.py
│  │  └── 📄 VectorDBInterface.py
│  ├── 📄 __init__.py
│  ├── 📄 .env
│  ├── 📄 .env.example
│  ├── 📄 main.py
│  └── 📄 requirements.txt
├── 📄 __init__.py
├── 📄 .gitignore
├── 📄 LICENSE
└── 📜 README.md

```

## Prerequisites

Before running the project, make sure you have the following installed:

- **Python 3.12+**
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
conda create -n env-name python=3.12
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
CONNECTION_URL = your_mongodb_connection_string
DATABASE_NAME = your_database_name
COHERE_API_KEY = your_api_key
GEMINI_API_KEY = your_api_key
QDRANT_URL = qdrant_connection_url
DISTANCE_METHOD = select_an_appropriate_method(Cosine, Dot)
TAVILY_API_KEY = your_api_key
GROQ_API_KEY = your_api_key
PADDLE_OCR_URL = paddle_ocr_connection_url
PADDLE_OCR_TOKEN = your_token
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

## 6- POST /chat/{user_id}/{thread_id}

### Description
Handle chat interactions including text messages, voice transcription, and image text extraction. Processes the input and streams the assistant's response.
### Method
`POST`
### Body
Form data with the following fields:
- `message` (optional): Text message from the user.
- `voice` (optional): Audio file for transcription.
- `image` (optional): Image file for text extraction [OCR only].

### Supported File Types and Size Limits

#### Image File Types
- **Allowed types:** `image/jpeg`, `image/png`, `image/webp`, `image/tiff`
- **Maximum size:** 5 MB

#### Voice/Audio File Types
- **Allowed types:** `audio/mpeg`, `audio/mp3`, `audio/mp4`, `audio/x-m4a`, `audio/wav`, `audio/webm`, `audio/ogg`, `audio/flac`
- **Maximum size:** 5 MB

### Success Response
Streaming response with the assistant's reply using Server-Sent Events (SSE) format.
**Media Type:** `text/event-stream`

**Status Code:** `200 OK`

#### Streaming Response Events

The response will contain multiple SSE events with the following structure:

**1. Metadata Event (for the first message only):**
```
data: {"type": "chat_title", "content": "Generated chat title"}

```

**2. Current Status (multiple events):**
```
data: {"type": "status", "content": "The current status of the model"}

```
**3. Model Answer Event:**
```
data: {"type": ""model_answer"", "content": "The final answer of the model"}

```

**4. Completion Event:**
```
data: {"type": "end", "content": "Streaming completed successfully."}

```

**5. Error Event (if an error occurs):**
```
data: {"type": "error", "content": "An error occurred during streaming."}

```


### Error Responses
```json
{
  "Response_signal": "No input provided. Please provide text, audio, or an image."
}
```
**Status Code:** `400 Bad Request`
```json
{
  "Response_signal": "Unsupported file format."
}
```
**Status Code:** `400 Bad Request`
```json
{
  "Response_signal": "File size exceeds the maximum limit."
}
```
**Status Code:** `400 Bad Request`
```json
{
  "Response_signal": "Failed to process the image for OCR."
}
```
**Status Code:** `400 Bad Request`
```json
{
  "Response_signal": "Failed to transcribe the audio file."
}
```
**Status Code:** `400 Bad Request`
```json
{
  "Response_signal": "Failed to generate chat title."
}
```
**Status Code:** `400 Bad Request`


## 7- POST /rename/chat

### Description
Rename the title of an existing chat thread.
### Method
`POST`
### Body
```json
{
  "thread_id": "thread_id_1",
  "new_title": "new_title",
  "user_id": "user_id_1"
}
```
### Success Response
```json
{
  "Response_signal": "Chat title renamed successfully."
}
```
**Status Code:** `200 OK`

### Error Responses
```json
{
  "Response_signal": "Failed to rename chat title."
}
```
**Status Code:** `400 Bad Request`

## 8- DELETE /temporary/chat

### Description
Delete a temporary chat thread by its thread ID.
### Method
`DELETE`
### Body
```json
{
  "thread_id": "thread_id_1"
}
```
### Success Response
```json
{
  "Response_signal": "Chat deleted successfully."
}
```
**Status Code:** `200 OK`

### Error Responses
```json
{
  "Response_signal": "Failed to delete chat."
}
```
**Status Code:** `400 Bad Request`

## 9- POST /AI/Services

### Description
Execute various AI services including explanation, translation, and summarization tasks.
### Method
`POST`
### Body
```json
{
  "service": "service_type",
  "input_text": "text_to_process",
  "target_language": "language_code"
}
```

**Parameters:**
- `service`: Type of AI service to execute ("explain", "summarize_snippet", "translate")
- `input_text`: The text content to be processed by the service.
- `target_language`(optional): Target language for translation task.

### Success Response
```json
{
  "answer": "generated_response"
}
```
**Status Code:** `200 OK`

### Error Responses
```json
{
  "answer": "Failed to generate a response."
}
```
**Status Code:** `400 Bad Request`


## Contributors

- [Salwa Mustafa](https://github.com/SalwaMustafa) 
- [Rawan Osama](https://github.com/Rawanelmoafy)