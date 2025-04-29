# constants.py
from enum import Enum

class QuestionType(Enum):
    UNIQUE_ANSWER = "unique_answer"
    MULTIPLE_ANSWERS = "multiple_answers"

# Estructura principal del prompt
PROMPT_BASE = """\
Genera una pregunta de examen de admisión de posgrado en Computer Science con los siguientes parámetros:
- Tema principal: {topic}
- Subtema: {subtopic}
- Nivel de dificultad: {difficulty}/5
"""

# Plantillas de características extensibles
FEATURE_TEMPLATES = {
    "core": {
        "description": "Estructura básica de la pregunta",
        "template": """\
{context}
Requisitos:
- Las pistas deben ordenarse de abstractas a concretas
- Las opciones deben incluir distracciones plausibles
- Incluir referencias académicas relevantes"""
    },
    "metadata": {
        "description": "Metadatos para clasificación",
        "fields": {
            "topic": "str",
            "subtopic": "str",
            "curriculum_tags": "list[str]"
        }
    },
    "references": {
        "description": "Sistema de referencias académicas",
        "template": """\
Referencias requeridas:
- Libro de texto principal
- 2 papers seminales
- Páginas relevantes del libro"""
    },
    "pedagogy": {
        "description": "Elementos pedagógicos",
        "components": {
            "learning_objective": "str",
            "common_misconceptions": "list[str]"
        }
    }
}

# Esquema de validación JSON
JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "question": {"type": "string"},
        "clues": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 5,
            "maxItems": 5
        },
        "type": {
            "type": "string",
            "enum": [t.value for t in QuestionType]
        },
        "options": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "label": {"type": "string"},
                    "answer": {"type": "boolean"}
                },
                "required": ["label", "answer"]
            }
        },
        "metadata": {
            "type": "object",
            "properties": {
                "topic": {"type": "string"},
                "subtopic": {"type": "string"},
                "difficulty": {"type": "number", "minimum": 1, "maximum": 5}
            }
        },
        "references": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["book", "paper"]},
                    "citation": {"type": "string"},
                    "pages": {"type": "string"}
                }
            }
        }
    },
    "required": ["question", "clues", "type", "options"]
}

# Temario y estructura curricular
SYLLABUS = {
    "core_topics": {
        "Matemática": [
            "Álgebra Lineal",
            "Análisis Combinatorio",
            "Cálculo Diferencial e Integral",
            "Geometría Analítica",
            "Lógica Matemática",
            "Matemática Discreta",
            "Probabilidad y Estadística",
            # Subtemas de Álgebra Lineal
            "Sistemas de Ecuaciones Lineales",
            "Espacios Vectoriales",
            "Transformaciones Lineales",
            "Autovalores/Autovectores",
            "Teorema Espectral",
            # Subtemas de Cálculo
            "Límites y Continuidad",
            "Derivadas y Aplicaciones",
            "Integración Numérica",
            "Funciones Multivariadas",
            "Optimización con Lagrange"
        ],
        "Algoritmos": [
            "Análisis de Complejidad",
            "Teoría de Grafos",
            "Programación Dinámica",
            "Análisis Asintótico",
            "Notación Big O/Omega/Theta",
            "Algoritmos Recursivos e Iterativos"
        ],
        "Sistemas": [
            "Sistemas Operativos",
            "Arquitectura de Computadoras",
            "Sistemas Distribuidos",
            "Circuitos Digitales",
            "Redes de Computadoras",
            # Subtemas de Arquitectura
            "Memorias y Procesadores",
            "Lenguaje de Ensamblador",
            "Arquitecturas RISC/CISC",
            "Paralelismo y Pipeline",
            # Subtemas de Redes
            "Protocolos de Comunicación",
            "Arquitectura de Redes",
            "Seguridad y Autenticación",
            "Desempeño de Redes"
        ],
        "IA/ML": [
            "Aprendizaje Supervisado",
            "Redes Neuronales",
            "Procesamiento de Lenguaje Natural",
            "Lógica Difusa"
        ],
        "Bases de Datos": [
            "Modelado de Datos",
            "Arquitectura de SGBD",
            "Bases de Datos Distribuidas",
            "Minería de Datos"
        ],
        "Ingeniería de Software": [
            "Ciclo de Vida del Software",
            "Ingeniería de Requisitos",
            "Garantía de Calidad",
            "Pruebas y Validación"
        ],
        "Teoría de la Computación": [
            "Lenguajes Formales",
            "Autómatas y Computabilidad",
            "Complejidad Computacional",
            "Problemas NP-Completos"
        ]
    }
}

# Ejemplo completo
FULL_EXAMPLE = """\
{
  "question": "¿Qué algoritmo utiliza divide y vencerás para ordenar con complejidad O(n log n)?",
  "clues": [
    "No es estable",
    "Usa recursión",
    "Divide el array en mitades",
    "Combina resultados ordenados",
    "No requiere espacio adicional"
  ],
  "type": "unique_answer",
  "options": [
    {"label": "QuickSort", "answer": false},
    {"label": "MergeSort", "answer": true},
    {"label": "BubbleSort", "answer": false},
    {"label": "HeapSort", "answer": false},
    {"label": "InsertionSort", "answer": false}
  ],
  "metadata": {
    "topic": "Algorithms",
    "subtopic": "Sorting",
    "difficulty": 4
  },
  "summary" : "El algoritmo MergeSort utiliza la técnica de divide y vencerás para ordenar listas. Divide la lista en mitades, ordena cada mitad y luego combina los resultados.",
  "references": [
    {
      "type": "book",
      "citation": "Cormen, T. H., et al. 'Introduction to Algorithms, 3rd ed'",
      "pages": "30-35"
    }
  ]
}"""
