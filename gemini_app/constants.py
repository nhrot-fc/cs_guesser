# constants.py
from enum import Enum

class DifficultyLevel(Enum):
    BASIC = 1
    INTERMEDIATE = 3
    ADVANCED = 5

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
            "Álgebra Linear",
            "Análise Combinatória",
            "Cálculo Diferencial e Integral",
            "Geometria Analítica",
            "Lógica Matemática",
            "Matemática Discreta",
            "Probabilidade e Estatística"
        ],
        "Algorithms": [
            "Complexity Analysis",
            "Graph Theory",
            "Dynamic Programming",
            "Análise Assintótica",
            "Notación Big O/Omega/Theta",
            "Algoritmos Recursivos e Iterativos"
        ],
        "Sistemas": [
            "Operating Systems",
            "Computer Architecture",
            "Distributed Systems",
            "Arquitetura de Computadores",
            "Circuitos Digitais",
            "Redes de Computadores"
        ],
        "AI/ML": [
            "Supervised Learning",
            "Neural Networks",
            "Natural Language Processing",
            "Lógica Fuzzy",
            "Redes Neurais",
            "Processamento de Linguagem Natural"
        ],
        "Bases de Datos": [
            "Modelagem de Dados",
            "SGBD Arquitetura",
            "Bancos Distribuídos",
            "Mineração de Dados"
        ],
        "Engenharia de Software": [
            "Ciclo de Vida de Software",
            "Engenharia de Requisitos",
            "Garantia de Qualidade",
            "Testes e Validação"
        ],
        "Teoria da Computação": [
            "Linguagens Formais",
            "Autômatos e Computabilidade",
            "Complexidade Computacional",
            "Problemas NP-Completos"
        ]
    },
    "subtopics_detail": {
        "Álgebra Linear": [
            "Sistemas de Equações Lineares",
            "Espaços Vetoriais",
            "Transformações Lineares",
            "Autovalores/Autovetores",
            "Teorema Espectral"
        ],
        "Cálculo Diferencial e Integral": [
            "Limites e Continuidade",
            "Derivadas e Aplicações",
            "Integração Numérica",
            "Funções Multivariadas",
            "Otimização com Lagrange"
        ],
        "Arquitetura de Computadores": [
            "Memórias e Processadores",
            "Linguagem de Montagem",
            "Arquiteturas RISC/CISC",
            "Paralelismo e Pipeline"
        ],
        "Redes de Computadores": [
            "Protocolos de Comunicação",
            "Arquitetura de Redes",
            "Segurança y Autenticación",
            "Desempenho de Redes"
        ]
    },
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
  "references": [
    {
      "type": "book",
      "citation": "Cormen, T. H., et al. 'Introduction to Algorithms, 3rd ed'",
      "pages": "30-35"
    }
  ]
}"""
