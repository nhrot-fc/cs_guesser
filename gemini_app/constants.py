# constants.py
# Temario y estructura curricular
SYLLABUS = {
  "Álgebra Lineal": [
    "Espacios Vectoriales, Subespacios",
    "Independencia Lineal, Bases, Dimensión",
    "Transformaciones Lineales, Núcleo, Imagen",
    "Representación Matricial Transformaciones Lineales",
    "Matrices: Operaciones, Inversa, Determinante",
    "Sistemas Ecuaciones Lineales, Solución",
    "Valores, Vectores Propios (Autovalores)",
    "Diagonalización Matrices, Forma Jordan",
    "Producto Interno, Ortogonalidad, Gram-Schmidt",
    "Descomposiciones Matriciales (LU, QR, SVD)",
    "Aplicaciones: Mínimos Cuadrados, Markov, PCA"
  ],
  "Cálculo Diferencial e Integral": [
    "Límites, Continuidad, Diferenciabilidad (Varias)",
    "Derivación, Parciales, Direccional, Gradiente",
    "Teorema Función Implícita/Explícita",
    "Optimización, Lagrange, Puntos Críticos",
    "Series Taylor y Maclaurin",
    "Integrales, Teorema Fundamental Cálculo",
    "Teoremas Vectoriales: Green, Stokes, Gauss",
    "Ecuaciones Diferenciales Ordinarias (EDO)"
  ],
  "Probabilidad y Estadística": [
    "Teoría Probabilidad, Axiomas",
    "Probabilidad Condicional, Bayes, Independencia",
    "Variables Aleatorias (Discretas/Continuas), FDA/FDP",
    "Distribuciones Notables (Normal, Poisson...)",
    "Esperanza, Varianza, Momentos, Correlación",
    "Distribuciones Conjuntas, Marginales, Condicionales",
    "Funciones Generadoras de Momentos",
    "Estadística Descriptiva, Medidas",
    "Procesos Estocásticos, Cadenas Markov",
    "Inferencia Bayesiana"
  ],
  "Matemáticas Discretas": [
    "Lógica Proposicional, Predicados, Demostraciones",
    "Teoría Conjuntos, Operaciones, Cardinalidad",
    "Relaciones, Equivalencia, Orden Parcial",
    "Funciones: Tipos, Composición, Inversa",
    "Principios Fundamentales Conteo",
    "Combinatoria, Binomio, Inclusión-Exclusión, Palomar",
    "Relaciones Recurrencia, Resolución",
    "Teoría Grafos, Definiciones, Representaciones",
    "Recorridos Grafos: Euler, Hamilton",
    "Conectividad, Componentes, Grafos Bipartitos",
    "Árboles, Propiedades, Recorridos, MST",
    "Planaridad, Coloración Grafos",
    "Teoría Números: Divisibilidad, Congruencias"
  ],
  "Teoría de Autómatas y Lenguajes Formales": [
    "Jerarquía Chomsky, Clasificación Lenguajes",
    "Lenguajes Regulares, Autómatas Finitos, Regex",
    "Lenguajes Libres Contexto (LLC), GLC",
    "Autómatas Pila (AP), Equivalencia GLC",
    "Lenguajes Sensibles Contexto (LSC)",
    "Máquinas Turing (MT), Universalidad",
    "Tesis Church-Turing"
  ],
  "Computabilidad y Decidibilidad": [
    "Problemas de Decisión",
    "Decidibilidad, Problemas Indecidibles",
    "Problema Parada (Halting Problem)",
    "Reducciones entre Problemas",
    "Otros Problemas Indecidibles (PCP)",
    "Teorema de Rice",
    "Funciones Recursivas, Calculabilidad"
  ],
  "Teoría de la Complejidad Computacional": [
    "Medición Complejidad (Tiempo/Espacio)",
    "Clases Tiempo Determinista (P, EXPTIME)",
    "Clases Tiempo No Determinista (NP)",
    "NP-Completitud, Reducciones, Cook-Levin",
    "Clases Espacio (PSPACE, L, NL)",
    "Teorema de Savitch",
    "Jerarquías Tiempo y Espacio",
    "Complejidad Parametrizada (Intro)",
    "Complejidad Aproximación, Clases APX",
    "Complejidad Aleatorizada (BPP, RP)"
  ],
  "Arquitectura de Computadoras": [
    "Representación Datos (Enteros, Flotantes)",
    "Lógica Digital, Circuitos Comb/Sec",
    "ISA (RISC/CISC), Instrucciones, Direccionamiento",
    "Organización CPU: Datapath, Control",
    "Rendimiento: Métricas, Ley Amdahl",
    "Pipelining: Concepto, Riesgos, Soluciones",
    "Paralelismo Instrucción (ILP)",
    "Jerarquía Memoria: Caché, Virtual",
    "Sistemas E/S, Transferencia, DMA",
    "Arquitecturas Paralelas (Flynn, Multicore, GPU)"
  ],
  "Sistemas Operativos": [
    "Conceptos SO, Abstracciones, Estructura",
    "Gestión Procesos, Hilos, Planificación",
    "Concurrencia, Sincronización (Mutex, Semáforos)",
    "Deadlocks: Caracterización, Prevención, Evitación",
    "Gestión Memoria Principal: Paginación, Segmentación",
    "Memoria Virtual, Reemplazo Páginas (LRU)",
    "Gestión Discos, Sistemas Archivos (FS)",
    "Sistemas E/S: Hardware, Software",
    "Protección, Seguridad SO, Control Acceso",
    "Sistemas Distribuidos (Conceptos SO)",
    "Virtualización: Hipervisores, VMs, Contenedores"
  ],
  "Redes de Computadoras e Internet": [
    "Introducción, Modelos Capas (OSI/TCP)",
    "Capa Física: Medios, Codificación, Multiplexación",
    "Capa Enlace: Errores, MAC, Switches",
    "Capa Red: IP (v4/v6), Enrutamiento",
    "Capa Transporte: TCP, UDP, Congestión",
    "Capa Aplicación: Protocolos (HTTP, DNS...)",
    "Seguridad Redes: Cripto, Amenazas, Firewalls",
    "Redes Inalámbricas, Móviles (WiFi, Celular)",
    "Multimedia en Red",
    "SDN, NFV (Conceptos)"
  ],
  "Algoritmos y Estructuras de Datos": [
    "Análisis Algoritmos: Complejidad, Recurrencias",
    "Estructuras Lineales: Listas, Pilas, Colas",
    "Árboles: BST, AVL, B-Trees",
    "Heaps: Binarios, Fibonacci",
    "Tablas Hash, Resolución Colisiones",
    "Conjuntos Disjuntos (Union-Find)",
    "Grafos: Representación, Recorridos (BFS/DFS)",
    "Algoritmos Ordenamiento (Merge, Quick, Radix)",
    "Algoritmos Búsqueda (Secuencial, Binaria)",
    "Técnicas Diseño Algoritmos",
    "Algoritmos Grafos Avanzados (Caminos, Flujo)",
    "Algoritmos Cadenas (KMP, Distancia Edición)",
    "Geometría Computacional (Convex Hull)",
    "Algoritmos Aleatorizados",
    "Algoritmos Aproximación (NP-Hard)"
  ],
  "Lenguajes de Programación y Compiladores": [
    "Lenguajes Programación: Principios, Paradigmas",
    "Sintaxis: Gramáticas, Análisis Léxico/Sintáctico",
    "Semántica: Estática, Dinámica (Conceptos)",
    "Nombres, Ámbitos, Enlaces (Bindings)",
    "Tipos Datos, Sistemas Tipos",
    "Expresiones, Asignaciones, Control",
    "Subprogramas: Parámetros, Alcance, Stack",
    "POO: Clases, Herencia, Polimorfismo",
    "Programación Funcional: Funciones Orden Superior",
    "Gestión Memoria: Stack, Heap, GC",
    "Concurrencia Lenguaje: Hilos, Sincronización",
    "Compilador: Fases, Tabla Símbolos",
    "Generación Código Intermedio (AST)",
    "Optimización Código (Local, Global)",
    "Generación Código Final, Registros",
    "Intérpretes vs Compiladores, JIT"
  ],
  "Ingeniería de Software": [
    "Procesos Desarrollo: Ciclo Vida, Ágil",
    "Ingeniería Requisitos: Elicitación, Especificación",
    "Diseño Software: Principios, Arquitectura, Patrones",
    "Construcción: Codificación, Refactorización, CI",
    "Pruebas Software: Niveles, Técnicas, TDD",
    "Calidad Software: Métricas, SQA",
    "Gestión Proyectos: Estimación, Planificación",
    "Gestión Configuración (SCM), Git",
    "Mantenimiento Software: Tipos",
    "Ética Profesional, Aspectos Legales"
  ],
  "Bases de Datos": [
    "Conceptos BD, Modelo ANSI-SPARC",
    "Modelo Relacional, Claves, Integridad",
    "Álgebra Relacional, Cálculo Relacional",
    "SQL: DDL, DML, Consultas Complejas",
    "Diseño BD: Modelo ER/EER, Mapeo",
    "Normalización: Dependencias Funcionales, Formas Normales",
    "Optimización Consultas: Costos, Planes",
    "Transacciones: ACID, Estados",
    "Control Concurrencia: Bloqueos, Timestamping, MVCC",
    "Recuperación BD: Logs, Checkpointing, ARIES",
    "Seguridad BD: Autenticación, Autorización",
    "BD Distribuidas: Arquitecturas, 2PC",
    "Data Warehousing, Modelado Dimensional, OLAP",
    "Minería Datos (Data Mining): KDD, Tareas",
    "BD NoSQL: CAP, Tipos",
    "Indexación Física: B+-Trees, Hash"
  ],
  "Inteligencia Artificial y Aprendizaje Automático": [
    "Introducción IA, Agentes Inteligentes",
    "Resolución Problemas: Búsqueda",
    "Representación Conocimiento, Razonamiento",
    "Planificación (Clásica, Jerárquica)",
    "Paradigmas Aprendizaje Automático",
    "Arquitecturas de Redes Neuronales",
    "Procesamiento Lenguaje Natural (NLP)",
    "Visión por Computadora (CV)",
    "Aprendizaje Refuerzo (MDP, Q-Learning)",
  ],
  "Gráficos por Computadora": [
    "Introducción, Pipeline Gráfico, Rasterización",
    "Coordenadas, Transformaciones 2D/3D",
    "Proyecciones (Paralela, Perspectiva)",
    "Rasterización: Líneas, Polígonos",
    "Recorte (Clipping) Líneas, Polígonos",
    "Visibilidad, Z-Buffer",
    "Modelado Geométrico: Curvas, Superficies",
    "Iluminación, Sombreado (Phong, Gouraud)",
    "Mapeo Texturas, Filtrado, Mipmapping",
    "Renderizado Realista (Ray/Path Tracing)",
    "Animación: Keyframing, Cinemática",
    "GPU, Shaders (Vertex, Fragment)"
  ],
  "Interacción Humano-Computador (HCI)": [
    "Principios Diseño Interfaces",
    "Modelos Interacción (WIMP, Táctil...)",
    "Diseño Centrado Usuario, Prototipado",
    "Evaluación Usabilidad: Métodos, Métricas",
    "Accesibilidad (WCAG), Diseño Universal"
  ],
  "Computación de Alto Rendimiento (HPC)": [
    "Arquitecturas Paralelas (Memoria, Interconexión)",
    "Programación Paralela (MPI, OpenMP)",
    "Diseño Algoritmos Paralelos",
    "Métricas Rendimiento Paralelo (Speedup...)",
    "Balanceo Carga",
    "Programación GPUs (CUDA/OpenCL)"
  ],
  "Criptografía y Seguridad Computacional": [
    "Fundamentos Criptografía, Ataques",
    "Criptografía Simétrica (AES, Modos)",
    "Criptografía Asimétrica (RSA, ECC)",
    "Funciones Hash (SHA-2, SHA-3)",
    "Autenticación Mensajes (MACs, HMAC)",
    "Firmas Digitales (RSA, DSA)",
    "Infraestructura Clave Pública (PKI, CA)",
    "Protocolos Criptográficos (TLS, IPsec)",
    "Seguridad Software: Vulnerabilidades, Análisis",
    "Seguridad SO: Control Acceso, Sandboxing",
    "Seguridad Redes: Firewalls, IDS/IPS, WiFi",
    "Análisis Malware: Tipos, Técnicas",
    "Privacidad: Anonimización, Diferencial"
  ]
}

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
    "topic": "Algoritmos",
    "subtopic": "Sorting",
    "difficulty": 4,
    "tags": ["sorting", "divide-and-conquer", "algorithms"]
  },
  "summary": "El algoritmo MergeSort utiliza la técnica de divide y vencerás para ordenar listas. Divide la lista en mitades, ordena cada mitad y luego combina los resultados.",
  "references": [
    {
      "type": "book",
      "title": "Introduction to Algorithms third edition",
      "authors": "Cormen, Leiserson, Rivest, Stein",
    },
    {
      "type": "paper",
      "title": "A Fast Merge Sort Algorithm",
      "authors": "John Doe, Jane Smith",
    },
    {
      "type": "website",
      "title": "GeeksforGeeks - Merge Sort",
      "authors": "GeeksforGeeks",
    }
  ]
}"""
