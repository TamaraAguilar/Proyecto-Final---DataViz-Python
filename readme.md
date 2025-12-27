# 📊 Estudio de Indicadores de Gobierno Digital 2023

Dashboard interactivo para visualizar datos sobre nivel de educación y género en la industria de tecnologías de información del gobierno chileno.

## 🚀 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 📦 Instalación

### 1. Clonar el proyecto

```bash
git clone https://github.com/tu-usuario/tu-proyecto.git
cd tu-proyecto

```

### 2. Crear un entorno virtual (recomendado)

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🏃 Ejecutar la Aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador

## 📁 Estructura del Proyecto

```
proyecto/
├── .streamlit/
│   └── config.toml          # Configuración de tema y colores
├── app.py                   # Archivo principal de la aplicación
├── requirements.txt         # Dependencias del proyecto
├── README.md               # Este archivo
└── .gitignore              # Archivos ignorados por git
```

## 📊 Fuente de Datos

- **Dataset**: Estudio de indicadores de gobierno digital 2023
- **Fuente**: [datos.gob.cl](https://datos.gob.cl/dataset/estudio-de-indicadores-2023)
- **API**: Los datos se obtienen directamente desde la API pública de datos.gob.cl

## 📝 Dependencias

- `streamlit` - Framework para aplicaciones web
- `pandas` - Manipulación de datos
- `requests` - Peticiones HTTP a la API
- `matplotlib` - Visualización de gráficos

## 👤 Autor

**Tamara Aguilar**  
Diciembre 2025

## 📄 Licencia

Este proyecto utiliza datos públicos del Gobierno de Chile bajo licencia abierta.

## 🔗 Enlaces Útiles

- [Documentación de Streamlit](https://docs.streamlit.io)
- [Dataset Original](https://datos.gob.cl/dataset/estudio-de-indicadores-2023)
- [Portal de Datos Abiertos](https://datos.gob.cl)

---
