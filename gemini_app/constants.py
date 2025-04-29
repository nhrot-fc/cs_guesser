# Constantes principales (MAYÚSCULAS por convención [3][10])
PROMPTO_BASE = """Genera una pregunta de trivia sobre {tema} con 6 pistas de difícil a fácil."""

EXTENSION_= """Incluir resumen con referencias académicas
Nivel de dificultad: {diccionario_caracteristicas['dificultad']['default']}"""

PISTAS = {
    "estructura": "Ordenadas de abstractas a concretas",
    "ejemplo": "Primera pista: concepto teórico, última: término específico"
}

FORMATO_JSON = """{
  "topic": str, 
  "question": str,
  "clues": [str x5],
  "answer": str,
  "options": [str x5]
}"""

EJEMPLO = '''{
  "Topic": "Algoritmos", 
  "question": "¿Qué estructura usa LIFO?",
  "clues": ["...", "...", "Stack"],
  "answer": "Stack"
}'''


diccionario_caracteristicas = {
    "resumen": {
        "descripcion": "Texto introductorio antes de la pregunta",
        "template": "Resumen: {texto}\nReferencias: {fuentes}",
        "ejemplo": "Resumen: Las estructuras LIFO...\nReferencias: Cormen et al. (2009)"
    },
    "referencias": {
        "campos": ["textbook", "pagina", "autor"],
        "ejemplo": {"textbook": "Introduction to Algorithms", "pagina": 102}
    },
    "temario": {
        "secciones": ["Matemática", "Algoritmos", "Bases de Datos"],
        "niveles": ["básico", "intermedio", "avanzado"]
    }
}
