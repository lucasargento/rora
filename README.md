# R.O.R.A: Operations Research Reasoning Agent

> **Resumen**  
>
> Como parte de un trabajo de investigación de la mateira Investigación Operativa Superior de la Facultad de Ingeniería de Buenos Aires, este trabajo analiza el desempeño de una arquitectura de agentes de inteligencia artificial, impulsada por grandes modelos del lenguaje (LLMs, por sus siglas en inglés) con capacidad de razonamiento, sobre ejemplos validados de los datasets de Investigación Operativa **Text2Zinc** y **NLP4LP**.  
>
> Se consideraron tanto problemas de **satisfacción** como de **optimización** para las evaluaciones. Se presenta la solución de alrededor de **120 problemas** provenientes de los conjuntos de datos mencionados (incluyendo descripciones de los problemas, implementaciones de código y soluciones).  
>
> A partir de este trabajo, se apunta a contribuir con las comunidades de **Investigación Operativa (IO)** e **Inteligencia Artificial (IA)** mediante un análisis del desempeño en IO de los enfoques de IA de última generación, así como con la creación de nuevos puntos de datos de entrenamiento para futuros esfuerzos de _fine-tuning_ en IO.

### Estructura

- **notebooks (`*.ipynb`)**: ejemplos de como buildear el agente y probarlo sobre nuevos problemas de optimizacion.
- **`src/`**: código fuente del agente y utilidades (p. ej., `src/agent/agent.py`, `src/agent/gates/`, `src/agent/nodes/`). Definen toda estructura modular del agente y permiten extenderlo/ utilizarlo a partir de la funcion build_agent().
- **`paper/`**: documento que explica la metodologia, el diseño del agente y los resultados sobre los datasets de evaluacion.
- **`outputs/`**: salidas generadas por corridas de razonamiento y registros asociados generados al correr el agente sobre los datasets de evaluación..
