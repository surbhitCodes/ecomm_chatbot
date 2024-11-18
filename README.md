# Arbor Test Project

## Project Overview

An LLM-powered assistant designed for contractors and builders to aid in decision-making regarding building materials.

## Features

- Intelligent Material Queries
- Project Planning Assistant
- Technical Support

## Technologies Used

- **Backend**: FastAPI, LangChain, Chroma
- **Frontend**: Flutter
- **Database**: SQLite (via Chroma)

## Project Structure

```asciidoc
arbor-test/
├── backend/
│   |
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── queries.py
│   │   │   ├── project_planning.py
│   │   │   └── technical_support.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── llm.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── prompt_builder.py
│   │   ├── vector_db.py
│   │   └── conversation.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── chat_schemas.py
│   └── data/
│       ├── __init__.py
│       └── helpers.py
├──arbor_app/lib/   [Flutter Project Files]
|   ├── pages/
│   │   ├── project_planning.dart
│   │   ├── queries.dart
│   │   ├── technical_support.dart
|   ├── main.dart
|   └── styles.dart
├──requirements.txt    
└── README.md
```

## Project Architecture



## Setup Instructions

### Backend Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv arbor_env
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env`.

4. Populate the vector database:

```bash
python main.py
```

5. Run the backend server:

```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Navigate to the Flutter project directory:

```bash
cd arbor_app
```

2. Install dependencies:

```bash
flutter pub get
```

3. Run the Flutter app:

```bash
flutter run
```

## API Endpoints

- **POST /queries/**: Submit a natural language query about materials.
- **POST /project-planning/estimate**: Submit a project description to receive material estimates.
- **POST /technical-support/**: Ask technical questions regarding materials, installation, etc.

## Testing

Run tests using pytest:

```bash
pytest

Copyright (c) 2024 Surbhit Kumar

All rights reserved.

This work is the property of Surbhit and is protected under copyright law.
Unauthorized copying, distribution, or use of this code, in whole or in part, is strictly prohibited.

For inquiries, contact: me@surbhitkumar.com
```
