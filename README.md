# R.O.R.A: Operations Research Reasoning Agent

> **Resumen**  
>
> Dentro del marco de la materia de Investigación Operativa Superior de la Facultad de Ingeniería de Buenos Aires, este trabajo analiza el desempeño de una arquitectura de agentes de inteligencia artificial, impulsada por grandes modelos del lenguaje (LLMs, por sus siglas en inglés) con capacidad de razonamiento, sobre ejemplos validados de los datasets de Investigación Operativa **Text2Zinc** y **NLP4LP**.  
>
> Se consideraron tanto problemas de **satisfacción** como de **optimización** para las evaluaciones. Se presenta la solución de alrededor de **120 problemas** provenientes de los conjuntos de datos mencionados (incluyendo descripciones de los problemas, implementaciones de código y soluciones).  
>
> A partir de este trabajo, se apunta a contribuir con las comunidades de **Investigación Operativa (IO)** e **Inteligencia Artificial (IA)** mediante un análisis del desempeño en IO de los enfoques de IA de última generación, así como con la creación de nuevos puntos de datos de entrenamiento para futuros esfuerzos de _fine-tuning_ en IO.

### Estructura

- **notebooks (`*.ipynb`)**: ejemplos de como buildear el agente y probarlo sobre nuevos problemas de optimizacion.
- **`src/`**: código fuente del agente y utilidades (p. ej., `src/agent/agent.py`, `src/agent/gates/`, `src/agent/nodes/`). Definen toda estructura modular del agente y permiten extenderlo/ utilizarlo a partir de la funcion build_agent().
- **`paper/`**: documento que explica la metodologia, el diseño del agente y los resultados sobre los datasets de evaluacion.
- **`outputs/`**: salidas generadas por corridas de razonamiento y registros asociados generados al correr el agente sobre los datasets de evaluación..

### Cómo Probarlo

1. **Cloná este repositorio** (o descargalo y ubicáte en la raíz):

   ```bash
   git clone <url-del-repo>
   cd <carpeta-del-repo>
   ```

2. **Creá y activá un entorno virtual (recomendado):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # En Linux/Mac
   # .\venv\Scripts\activate     # En Windows
   ```

3. **Instalá las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutá el frontend (app de Streamlit):**

   ```bash
   streamlit run src/frontend/main.py
   ```

5. **Configurá tu clave de OpenAI API:**
   - Ingresala en la barra lateral de la app cuando se te solicite (`sk-...`).

¡Listo! Ahora podés testear el agente desde el navegador, interactuando con problemas de investigación operativa de manera conversacional.
