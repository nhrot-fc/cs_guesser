# CS Quiz Project - Computer Science Learning Tool

A Django-based web application that leverages Google's Gemini API to generate interactive Computer Science quizzes with progressive hints to help students prepare for exams.

## Project Overview

CS Quiz is designed to help Computer Science students prepare for exams like POSTCOM (Post-Comprehensive) by generating topic-specific questions with a series of hints that progressively reveal the answer. The application uses Google's Gemini 2.0 AI model to create relevant, challenging questions across various CS domains.

## Features

- Generate CS trivia questions with 6 progressive hints (from difficult to easy)
- Questions cover multiple CS topics including Algorithms, Data Structures, Mathematics, and Databases
- Customizable difficulty levels (basic, intermediate, advanced)
- Academic references included with questions
- JSON-formatted responses for easy integration with frontend applications

## Technical Architecture

The project is built with:
- **Backend**: Django & Django REST Framework
- **AI Integration**: Google Gemini 2.0 API
- **Database**: SQLite (development)
- **Environment Management**: Conda & pip

## Getting Started

### Prerequisites

- Python 3.11+
- Conda (recommended for environment management)
- Google Gemini API key

### Environment Setup

```bash
# Create and activate conda environment
conda create -n django_gemini python=3.11
conda activate django_gemini

# Install dependencies
conda install -c conda-forge django djangorestframework python-dotenv
# Or with pip
pip install django djangorestframework python-dotenv google-genai
```

### Configuration

1. Clone the repository
2. Create a `.env` file in the project root with your Google Gemini API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
3. Run database migrations:
   ```
   python manage.py migrate
   ```

### Running the Application

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

## API Usage

The main endpoint for quiz generation is:

```
GET /gemini/
```

Example response:
```json
{
  "topic": "Algorithms", 
  "question": "¿Qué estructura usa LIFO?",
  "clues": [
    "Este concepto pertenece a las estructuras de datos fundamentales",
    "Se utiliza para el manejo temporal de información en memoria",
    "Opuesto conceptualmente a una cola (Queue)",
    "Se utiliza en la implementación de la recursividad",
    "Sigue el principio: último en entrar, primero en salir",
    "Stack"
  ],
  "answer": "Stack",
  "options": [
    "Queue",
    "Heap",
    "Stack",
    "Tree",
    "Linked List"
  ]
}
```

## Project Structure

```
cs_quiz_project/
├── cs_quiz/              # Django project settings
├── gemini_app/           # Main application
│   ├── constants.py      # Prompt templates and configuration
│   ├── models.py         # Data models
│   └── views.py          # API endpoints
├── manage.py             # Django management script
└── .env                  # Environment variables (API keys)
```

## Future Enhancements

- User authentication and quiz history
- Topic selection and customization
- Enhanced frontend with progressive hint revelation
- Scoring system based on how many hints were needed
- Additional question types and formats

## License

[MIT License](LICENSE)

## Acknowledgements

- Google Gemini API for AI-powered question generation
- Django community for the robust web framework
