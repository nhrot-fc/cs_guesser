# CS Quiz Project - Computer Science Learning Tool

A Django-based web application that leverages Google's Gemini API to generate interactive Computer Science quizzes with progressive hints to help students prepare for exams.

## Project Overview

CS Quiz is designed to help Computer Science students prepare for exams like POSTCOM (Post-Comprehensive) by generating topic-specific questions with a series of hints that progressively reveal the answer. The application uses Google's Gemini 2.0 AI model to create relevant, challenging questions across various CS domains.

## Features

- Generate CS trivia questions with 6 progressive hints (from difficult to easy)
- Questions cover multiple CS topics including Algorithms, Data Structures, Mathematics, and Databases
- Customizable difficulty levels (basic, intermediate, advanced)
- Streak counter and achievement system
- Real-time statistics for user performance
- Academic references included with questions
- Responsive design with Tailwind CSS
- JSON-formatted responses for easy integration with frontend applications

## Technical Architecture

The project is built with:
- **Backend**: Django & Django REST Framework
- **Frontend**: HTML, JavaScript with Tailwind CSS for styling
- **AI Integration**: Google Gemini 2.0 API
- **Database**: SQLite (development), PostgreSQL (production)
- **Environment Management**: Conda & pip
- **Deployment**: Configured for Heroku/Render/Railway

## Getting Started

### Prerequisites

- Python 3.11+
- Conda (recommended for environment management) or pip
- Node.js and npm (for Tailwind CSS)
- Google Gemini API key

### Environment Setup

```bash
# Create and activate conda environment
conda create -n django_gemini python=3.11
conda activate django_gemini

# Install dependencies
pip install -r requirements.txt

# Install frontend dependencies
npm install
```

### Configuration

1. Clone the repository
2. Create a `.env` file in the project root with your Google Gemini API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ALLOWED_HOSTS=localhost,127.0.0.1
   DEBUG=True
   ```
3. Run database migrations:
   ```
   python manage.py migrate
   ```
4. Compile the CSS (if making changes to the styling):
   ```
   npx tailwindcss -i gemini_app/static/input.css -o gemini_app/static/output.css --watch
   ```

### Running the Application

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

## Deployment

This project is configured for deployment to platforms like Heroku, Render, or Railway. The necessary files are already included:

- `Procfile`: Configures Gunicorn as the WSGI server
- `requirements.txt`: Lists all Python dependencies
- `runtime.txt`: Specifies the Python version (3.11)
- `package.json`: Manages Node.js dependencies (Tailwind CSS)

### Deployment Steps

1. Make sure your static files are collected:
   ```bash
   python manage.py collectstatic
   ```

2. Configure environment variables on your hosting platform:
   ```
   GOOGLE_API_KEY=your_api_key_here
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   SECRET_KEY=your_secret_key_here
   ```

3. For database configuration (if using PostgreSQL):
   ```
   DATABASE_URL=your_database_connection_string
   ```

4. Deploy to your chosen platform using their specific deployment methods.

5. Run migrations on the production server:
   ```
   python manage.py migrate
   ```

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
├── cs_quiz_project/        # Django project settings
├── gemini_app/             # Main application
│   ├── controllers/        # Quiz question generation controllers
│   ├── models/             # Data models and dataclasses
│   ├── static/             # CSS and static assets
│   ├── templates/          # HTML templates
│   ├── constants.py        # Prompt templates and configuration
│   └── views.py            # API endpoints
├── static/                 # Collected static files
├── manage.py               # Django management script
├── Procfile                # For deployment configuration
├── requirements.txt        # Python dependencies
├── runtime.txt             # Specifies Python version
├── package.json            # Node.js dependencies
└── .env                    # Environment variables (API keys)
```

## Future Enhancements

- User authentication and quiz history
- Topic selection and customization
- Enhanced frontend with progressive hint revelation
- Scoring system based on how many hints were needed
- Additional question types and formats
- Mobile application using React Native

## License

[MIT License](LICENSE)

## Acknowledgements

- Google Gemini API for AI-powered question generation
- Django community for the robust web framework
- Tailwind CSS for the responsive design system
