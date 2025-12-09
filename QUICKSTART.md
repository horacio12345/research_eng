# 🚀 Guía Rápida de Uso (v2.0)

Este documento resume cómo usar tu sistema de investigación de ingeniería.

## 1. Cómo Ejecutarlo ▶️
Simplemente corre este comando en tu terminal (desde la carpeta del proyecto):

```bash
python run_research.py
```

## 2. Dónde están mis Resultados? 📂
Todos los archivos se guardan automáticamente en la carpeta `outputs/`.

Al terminar la ejecución, verás 3 archivos nuevos con la fecha y hora:

1. **Visor Interactivo** (`.html`): **¡El mejor para usar!**
   - Abre este archivo en Chrome, Safari o Edge.
   - Permite filtrar, buscar y ordenar resultados visualmente.
   
2. **Reporte de Lectura** (`.md`):
   - Archivo de texto para leer linealmente como un documento.
   
3. **Datos Crudos** (`.json`):
   - Solo para uso de programadores o integraciones.

## 3. Cómo Mejorar los Resultados ("Re-Act") ✨
Si el agente no está buscando lo que quieres, edita estos archivos de texto (prompts):

- **Para cambiar el filtro de relevancia:**
  `src/ai/prompts/relevance_analysis.txt`
  *(Dile al agente qué es importante y qué ignorar)*

- **Para cambiar el resumen:**
  `src/ai/prompts/summary_generation.txt`
  *(Dile si quieres resúmenes más técnicos, más cortos, etc.)*

## 4. Configurar Temas ⚙️
Para cambiar QUÉ buscar (temas), edita el archivo:
`config.yaml`
*(Busca la sección `topics` y añade o quita lo que necesites)*

---

**Nota:** Los archivos de más de 30 días se borran automáticamente cada vez que ejecutas el sistema.
