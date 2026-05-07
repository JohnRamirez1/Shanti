# Agente Ayurveda 🌿
## Loto de los Andes · Dra. Paula Diez Carreño

### Instalación y ejecución

1. Instala las dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecuta la aplicación:
```bash
streamlit run app.py
```

3. Abre tu navegador en `http://localhost:8501`

### Despliegue en Streamlit Cloud (gratis)

1. Sube el archivo `app.py` y `requirements.txt` a un repositorio GitHub
2. Ve a https://share.streamlit.io
3. Conecta tu repositorio
4. ¡Listo! Tendrás una URL pública para compartir con pacientes

### Flujo de la aplicación

```
Registro del paciente
    ↓
Test Prakriti (57 preguntas) — se realiza UNA SOLA VEZ
    ↓
Resultado Prakriti + interpretación IA
    ↓
Test Vikriti (27 preguntas) — repetir cada 3 MESES
    ↓
Resultado Vikriti + interpretación IA
    ↓
Plan alimenticio personalizado:
  • Cálculo de macronutrientes (Harris-Benedict + factor actividad)
  • Recetas Ayurvédicas del libro de cocina (Vata/Pitta/Kapha)
  • Alimentos favorables y a evitar
  • Plan personalizado generado por IA
```

### Estructura del agente

- **Diagnóstico Prakriti**: 57 afirmaciones extraídas del Test Prakriti (Dra. Paula Diez)
- **Diagnóstico Vikriti**: 27 preguntas sobre síntomas de los últimos 3 meses
- **Recetas integradas**: Libros de cocina Ayurvédica (Vata, Pitta, Kapha)
- **Nutrición**: Cálculo Harris-Benedict con ajuste por dosha y actividad física
- **IA**: Claude claude-sonnet-4-20250514 para interpretaciones y planes personalizados

### Migración futura a LangGraph

Cuando quieras escalar, el flujo de estados actual puede migrarse fácilmente a:
```python
from langgraph.graph import StateGraph
# Nodos: registro → prakriti → vikriti → dieta
```

