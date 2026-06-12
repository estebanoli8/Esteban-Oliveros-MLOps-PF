# Esteban Oliveros - Proyecto Final MLOps

## Sistema de despliegue automático de un modelo ML en ambientes DEV y PROD

Este repositorio contiene el proyecto final de MLOps para el despliegue automático de un modelo de Machine Learning en la nube, usando **GitHub Actions**, **Docker**, **Google Cloud Run**, **Artifact Registry** y **Cloud Storage**.

El sistema implementado es un **clasificador y recomendador de mensajes ciudadanos para la Política de la Felicidad**. A partir de un texto ingresado por un usuario, el modelo identifica la categoría más cercana, calcula un puntaje de similitud, entrega una recomendación operativa y sugiere una ruta organizacional.

---

## 1. Resumen ejecutivo

Este proyecto demuestra un flujo MLOps completo:

```text
código fuente
→ control de versiones en GitHub
→ ramas dev y prod
→ pipeline CI/CD
→ pruebas automáticas
→ descarga de artefactos externos
→ construcción de imagen Docker
→ publicación en Artifact Registry
→ despliegue en Cloud Run
→ endpoint de inferencia
→ registro de predicciones en Cloud Storage
```

El sistema recibe mensajes como:

```json
{
  "text": "Quiero aprender sobre SECOP y contratación pública"
}
```

Y responde con una predicción estructurada:

```json
{
  "input_text": "Quiero aprender sobre SECOP y contratación pública",
  "category": "ESTADO_CONTROL_PUBLICO",
  "score": 0.9015,
  "recommendation": "Ofrecer ruta de formación sobre Estado, contratación pública, SECOP, veeduría y control político.",
  "route": "Módulo Estado y control público + formación SECOP + veeduría ciudadana.",
  "model_type": "onnx",
  "environment": "prod"
}
```

La solución tiene dos ambientes separados:

```text
dev  → pf-recommender-dev  → /predict-dev  → predicciones_dev.txt
prod → pf-recommender-prod → /predict-prod → predicciones_prod.txt
```

---

## 2. Relación con la consigna de la asignación

La consigna solicitaba desarrollar un sistema de despliegue automático de un modelo ML existente en producción, usando un repositorio con CI/CD, ramas `dev` y `prod`, endpoints separados, artefactos externos y registro de predicciones.

Este proyecto implementa esa consigna de la siguiente manera:

| Requisito de la asignación | Implementación en este proyecto | Estado |
|---|---|---|
| Repositorio en GitHub | `Esteban-Oliveros-MLOps-PF` | Cumplido |
| Rama `dev` | Rama `dev` con despliegue automático a Cloud Run DEV | Cumplido |
| Rama `prod` | Rama `prod` con despliegue automático a Cloud Run PROD | Cumplido |
| Endpoint para `dev` | `/predict-dev` en `pf-recommender-dev` | Cumplido |
| Endpoint para `prod` | `/predict-prod` en `pf-recommender-prod` | Cumplido |
| Pipeline en GitHub Actions | `.github/workflows/ci-cd.yml` | Cumplido |
| Ejecución en push a `dev` | Test + build + deploy DEV | Cumplido |
| Ejecución en push a `prod` | Test + build + deploy PROD | Cumplido |
| Etapa de test | `pytest` + descarga de modelo y datos externos | Cumplido |
| Etapa build/promote | Docker + Artifact Registry + Cloud Run | Cumplido |
| Modelo en formato ONNX | `model.onnx` basado en `Xenova/all-MiniLM-L6-v2` | Cumplido |
| Modelo fuera del repo | Cloud Storage `models/minilm/model.onnx` | Cumplido |
| Datos de prueba fuera del repo | Cloud Storage `test_data/test_messages.json` | Cumplido |
| Registro de predicciones DEV | `logs/predicciones_dev.txt` | Cumplido |
| Registro de predicciones PROD | `logs/predicciones_prod.txt` | Cumplido |

---

## 3. Caso de uso

El sistema está diseñado para apoyar la clasificación inicial de mensajes ciudadanos dentro de una organización política o social.

Una persona puede enviar mensajes como:

```text
Quiero denunciar una obra abandonada en mi municipio.
Quiero aprender sobre SECOP.
Quiero ayudar como voluntario.
Quiero aprender comunicación política.
Quiero formar un equipo territorial.
Quiero diseñar servicios para mi comunidad.
```

El sistema analiza semánticamente el mensaje y responde:

1. Categoría más probable.
2. Score de similitud.
3. Recomendación operativa.
4. Ruta organizacional sugerida.
5. Tipo de modelo usado.
6. Ambiente donde se ejecutó la predicción.
7. Top 3 categorías más cercanas.

---

## 4. Categorías del modelo

El sistema clasifica los mensajes en siete categorías:

```text
LIDERAZGO_VOLUNTARIADO
CONTROL_POLITICO_OBRA_PUBLICA
ESCUELA_INNOVACION_POLITICA_FELICIDAD
COMUNICACION_NARRATIVA
ESTADO_CONTROL_PUBLICO
DESARROLLO_DE_EQUIPO
DISENO_DE_SERVICIOS
```

Cada categoría tiene:

- Frases de referencia.
- Una recomendación.
- Una ruta organizacional sugerida.

Ejemplo:

```text
Categoría:
ESTADO_CONTROL_PUBLICO

Recomendación:
Ofrecer ruta de formación sobre Estado, contratación pública, SECOP, veeduría y control político.

Ruta:
Módulo Estado y control público + formación SECOP + veeduría ciudadana.
```

---

## 5. Descripción técnica del modelo

El proyecto usa un modelo de embeddings en formato ONNX:

```text
Xenova/all-MiniLM-L6-v2
```

Archivo principal:

```text
model.onnx
```

Este sistema no entrena un clasificador supervisado desde cero. En su lugar, implementa un **clasificador semántico basado en embeddings**.

El flujo de predicción es:

```text
Texto del usuario
→ tokenización
→ embedding con modelo ONNX
→ comparación contra frases de referencia
→ cálculo de similitud coseno
→ selección de la categoría con mayor similitud
→ generación de recomendación y ruta
```

La similitud coseno permite comparar qué tan cercano está el mensaje del usuario frente a las frases de referencia de cada categoría.

---

## 6. Almacenamiento externo del modelo

El modelo no está almacenado en GitHub.

Está ubicado en Google Cloud Storage:

```text
gs://esteban-mlops-pf-artifacts/models/minilm/model.onnx
```

Además del archivo ONNX, se almacenan los archivos necesarios para el tokenizer:

```text
gs://esteban-mlops-pf-artifacts/models/minilm/config.json
gs://esteban-mlops-pf-artifacts/models/minilm/tokenizer.json
gs://esteban-mlops-pf-artifacts/models/minilm/tokenizer_config.json
gs://esteban-mlops-pf-artifacts/models/minilm/special_tokens_map.json
gs://esteban-mlops-pf-artifacts/models/minilm/vocab.txt
```

El repositorio excluye explícitamente archivos ONNX y artefactos temporales mediante `.gitignore`:

```text
*.onnx
model.onnx
models/
tmp_artifacts/
runtime_artifacts/
```

Esto demuestra que el pipeline no depende de que el modelo esté versionado en el repositorio.

---

## 7. Datos de prueba externos

Los datos de prueba tampoco están almacenados en GitHub.

Están ubicados en Cloud Storage:

```text
gs://esteban-mlops-pf-artifacts/test_data/test_messages.json
```

Durante el pipeline, GitHub Actions descarga este archivo y lo usa para ejecutar pruebas automáticas.

Esto permite validar que el proceso de CI/CD puede consumir datos externos, como ocurriría en un escenario real con un bucket, base de datos, data warehouse o repositorio de artefactos.

---

## 8. Arquitectura general

```text
GitHub Repository
├── rama dev
└── rama prod

        ↓ push

GitHub Actions
├── test
│   ├── checkout del repositorio
│   ├── instalación de Python
│   ├── instalación de dependencias
│   ├── autenticación con Google Cloud
│   ├── descarga del modelo ONNX desde Cloud Storage
│   ├── descarga de datos de prueba desde Cloud Storage
│   └── ejecución de pytest
│
└── build-and-deploy
    ├── construcción de imagen Docker
    ├── autenticación con Artifact Registry
    ├── publicación de imagen Docker
    └── despliegue en Cloud Run

        ↓

Google Cloud Run
├── pf-recommender-dev
└── pf-recommender-prod

        ↓

Cloud Storage
├── models/minilm/
├── test_data/test_messages.json
└── logs/
    ├── predicciones_dev.txt
    └── predicciones_prod.txt
```

---

## 9. Servicios usados en Google Cloud

### 9.1 Cloud Storage

Bucket:

```text
esteban-mlops-pf-artifacts
```

Contenido principal:

```text
models/minilm/
test_data/test_messages.json
logs/predicciones_dev.txt
logs/predicciones_prod.txt
```

Cloud Storage cumple tres funciones:

1. Almacenar el modelo ONNX.
2. Almacenar datos de prueba externos.
3. Registrar logs de predicciones por ambiente.

### 9.2 Artifact Registry

Repositorio Docker:

```text
pf-recommender
```

Imagen:

```text
pf-api
```

Artifact Registry almacena las imágenes Docker construidas automáticamente por GitHub Actions.

### 9.3 Cloud Run

Servicios desplegados:

```text
pf-recommender-dev
pf-recommender-prod
```

Cloud Run ejecuta los contenedores de la API sin necesidad de administrar servidores.

Se configuró con:

```text
--min-instances 0
--max-instances 1
--memory 1Gi
--cpu 1
```

Esto permite controlar costos durante la demostración académica.

---

## 10. Ramas y ambientes

El repositorio tiene tres ramas principales:

```text
main
dev
prod
```

La consigna se implementa principalmente con:

```text
dev
prod
```

La lógica del pipeline es:

```text
push a dev
→ test
→ build
→ deploy a pf-recommender-dev
→ endpoint /predict-dev
→ logs/predicciones_dev.txt
```

```text
push a prod
→ test
→ build
→ deploy a pf-recommender-prod
→ endpoint /predict-prod
→ logs/predicciones_prod.txt
```

La rama determina automáticamente el ambiente de despliegue.

---

## 11. Endpoints desplegados

### 11.1 Ambiente DEV

Health:

```text
https://pf-recommender-dev-217415234348.us-central1.run.app/health
```

Predicción:

```text
https://pf-recommender-dev-217415234348.us-central1.run.app/predict-dev
```

### 11.2 Ambiente PROD

Health:

```text
https://pf-recommender-prod-217415234348.us-central1.run.app/health
```

Predicción:

```text
https://pf-recommender-prod-217415234348.us-central1.run.app/predict-prod
```

---

## 12. Prueba de health

Ejemplo para PROD:

```bash
curl "https://pf-recommender-prod-217415234348.us-central1.run.app/health"
```

Respuesta esperada:

```json
{
  "status": "ok",
  "environment": "prod",
  "model_ready": true,
  "model_type": "onnx"
}
```

Interpretación:

```text
status: ok              → la API está disponible.
environment: prod       → se está consultando producción.
model_ready: true       → el modelo fue cargado correctamente.
model_type: onnx        → se está usando el modelo ONNX real.
```

---

## 13. Prueba de predicción en PROD

Comando recomendado para ver la respuesta con formato legible y tildes correctas:

```bash
curl -s -X POST "https://pf-recommender-prod-217415234348.us-central1.run.app/predict-prod" \
  -H "Content-Type: application/json" \
  -d '{"text":"Quiero aprender sobre SECOP y contratación pública"}' \
  | python3 -c 'import sys,json; print(json.dumps(json.load(sys.stdin), indent=4, ensure_ascii=False))'
```

Respuesta obtenida:

```json
{
    "input_text": "Quiero aprender sobre SECOP y contratación pública",
    "category": "ESTADO_CONTROL_PUBLICO",
    "score": 0.9015,
    "recommendation": "Ofrecer ruta de formación sobre Estado, contratación pública, SECOP, veeduría y control político.",
    "route": "Módulo Estado y control público + formación SECOP + veeduría ciudadana.",
    "model_type": "onnx",
    "top_categories": [
        {
            "category": "ESTADO_CONTROL_PUBLICO",
            "score": 0.9015
        },
        {
            "category": "COMUNICACION_NARRATIVA",
            "score": 0.6935
        },
        {
            "category": "ESCUELA_INNOVACION_POLITICA_FELICIDAD",
            "score": 0.62
        }
    ],
    "environment": "prod"
}
```

---

## 14. Interpretación de resultados reales

### Caso 1

Input:

```text
Quiero aprender sobre SECOP y contratación pública
```

Resultado:

```text
Categoría: ESTADO_CONTROL_PUBLICO
Score: 0.9015
Modelo: onnx
Ambiente: prod
```

Interpretación:

El resultado es coherente porque el mensaje habla de SECOP y contratación pública, temas directamente relacionados con Estado, contratación, veeduría ciudadana y control público.

El score de 0.9015 indica una alta similitud semántica con las frases de referencia de la categoría `ESTADO_CONTROL_PUBLICO`.

### Caso 2

Input:

```text
Quiero aprende SECOP y contratación
```

Resultado:

```text
Categoría: ESTADO_CONTROL_PUBLICO
Score: 0.7762
Modelo: onnx
Ambiente: prod
```

Interpretación:

Aunque el texto tiene un error gramatical, el modelo conserva la clasificación correcta porque reconoce la intención general y las palabras clave `SECOP` y `contratación`.

El score baja frente al caso más completo porque el texto es menos claro.

### Caso 3

Input:

```text
Quiero aprende SECOP
```

Resultado:

```text
Categoría: ESTADO_CONTROL_PUBLICO
Score: 0.9558
Modelo: onnx
Ambiente: prod
```

Interpretación:

La palabra `SECOP` es muy distintiva para la categoría de Estado y control público. Por eso el sistema clasifica con alta confianza, incluso con un texto corto e imperfecto.

### Caso 4

Input:

```text
Quiero a SECOP
```

Resultado:

```text
Categoría: ESTADO_CONTROL_PUBLICO
Score: 0.8473
Modelo: onnx
Ambiente: prod
```

Interpretación:

El texto es incompleto, pero conserva una señal fuerte: `SECOP`. El modelo lo enruta correctamente hacia `ESTADO_CONTROL_PUBLICO`.

Sin embargo, en un sistema real, un mensaje tan corto debería generar una solicitud adicional de información antes de tomar una decisión operativa definitiva.

---

## 15. Registro de predicciones

Cada predicción realizada en los endpoints se registra en Cloud Storage.

Archivo de logs para DEV:

```text
gs://esteban-mlops-pf-artifacts/logs/predicciones_dev.txt
```

Archivo de logs para PROD:

```text
gs://esteban-mlops-pf-artifacts/logs/predicciones_prod.txt
```

Cada línea del archivo es un JSON independiente con:

```text
timestamp_utc
input_text
category
score
recommendation
route
model_type
top_categories
environment
```

Ejemplo de log en PROD:

```json
{
  "timestamp_utc": "2026-06-12T03:13:18.899619+00:00",
  "input_text": "Quiero aprender sobre SECOP y contratación pública",
  "category": "ESTADO_CONTROL_PUBLICO",
  "score": 0.9015,
  "recommendation": "Ofrecer ruta de formación sobre Estado, contratación pública, SECOP, veeduría y control político.",
  "route": "Módulo Estado y control público + formación SECOP + veeduría ciudadana.",
  "model_type": "onnx",
  "environment": "prod"
}
```

Esto demuestra trazabilidad de las inferencias.

---

## 16. Pipeline CI/CD

El pipeline está definido en:

```text
.github/workflows/ci-cd.yml
```

Se ejecuta automáticamente en:

```text
push a dev
push a prod
pull_request hacia dev
pull_request hacia prod
```

### 16.1 Etapa test

La etapa `test` realiza:

1. Checkout del repositorio.
2. Instalación de Python.
3. Instalación de dependencias.
4. Autenticación con Google Cloud.
5. Descarga del modelo ONNX desde Cloud Storage.
6. Descarga de los datos de prueba desde Cloud Storage.
7. Ejecución de pruebas con `pytest`.

Esta etapa valida que el sistema pueda usar artefactos externos y que la API responda correctamente.

### 16.2 Etapa build-and-deploy

La etapa `build-and-deploy` realiza:

1. Construcción de imagen Docker.
2. Autenticación contra Artifact Registry.
3. Publicación de la imagen Docker.
4. Despliegue automático en Cloud Run.

La rama define el ambiente:

```text
dev  → pf-recommender-dev
prod → pf-recommender-prod
```

---

## 17. Pruebas automáticas

Las pruebas están ubicadas en:

```text
tests/test_api.py
tests/test_external_artifacts.py
```

### 17.1 `test_health_endpoint_responds`

Valida que la API responda correctamente en `/health`.

### 17.2 `test_prediction_endpoint_responds_with_category`

Valida que el endpoint de predicción retorne:

```text
category
score
recommendation
route
```

### 17.3 `test_prediction_metric_threshold`

Valida que la predicción tenga un score mínimo aceptable.

Esto cumple la idea de verificar que no haya un cambio significativo en el comportamiento esperado del modelo.

### 17.4 `test_external_test_data_file_exists`

Valida que el archivo externo de datos de prueba haya sido descargado correctamente desde Cloud Storage.

### 17.5 `test_external_model_file_exists`

Valida que el modelo ONNX externo haya sido descargado correctamente desde Cloud Storage.

---

## 18. Resultado de pruebas

Ejecución local:

```bash
pytest -v
```

Resultado esperado:

```text
5 passed
```

En GitHub Actions, los tests también se ejecutan automáticamente antes del despliegue.

---

## 19. Estructura del repositorio

```text
.
├── app/
│   ├── __init__.py
│   ├── categories.py
│   ├── main.py
│   ├── recommender.py
│   ├── settings.py
│   └── storage.py
├── scripts/
│   └── download_artifacts.py
├── tests/
│   ├── test_api.py
│   └── test_external_artifacts.py
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── Dockerfile
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

---

## 20. Ejecución local

Crear ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalar dependencias:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Ejecutar pruebas:

```bash
pytest -v
```

Ejecutar API local en modo de prueba:

```bash
USE_FAKE_MODEL=true APP_ENV=dev GCP_BUCKET="" uvicorn app.main:app --reload --port 8000
```

Probar localmente:

```bash
curl -s -X POST "http://127.0.0.1:8000/predict-dev" \
  -H "Content-Type: application/json" \
  -d '{"text":"Quiero denunciar una obra pública abandonada en mi municipio"}' \
  | python3 -c 'import sys,json; print(json.dumps(json.load(sys.stdin), indent=4, ensure_ascii=False))'
```

---

## 21. Variables y secretos de GitHub Actions

El proyecto usa GitHub Secrets para conectarse a Google Cloud.

Secrets configurados:

```text
GCP_PROJECT_ID
GCP_REGION
GCP_BUCKET
GCP_ARTIFACT_REPO
GCP_SERVICE_ACCOUNT_KEY
```

Estos valores no se almacenan en el código fuente.

---

## 22. Seguridad y buenas prácticas

El proyecto aplica las siguientes buenas prácticas:

- El modelo ONNX no se sube a GitHub.
- Los datos de prueba no se suben a GitHub.
- Las credenciales se almacenan como GitHub Secrets.
- Los artefactos temporales están excluidos por `.gitignore`.
- Los ambientes `dev` y `prod` tienen endpoints separados.
- Los ambientes `dev` y `prod` tienen archivos de logs separados.
- El pipeline automatiza test, build y deploy.
- Cloud Run se configuró con mínimo de instancias en cero para controlar costos.
- El ambiente `test` no escribe predicciones en los logs reales.

---

## 23. Limitaciones

Este proyecto fue desarrollado como demostración académica de MLOps. Algunas limitaciones son:

1. No se entrenó un clasificador supervisado propio.
2. La clasificación depende de frases de referencia.
3. El sistema usa similitud semántica, no aprendizaje supervisado con etiquetas históricas.
4. Los logs se escriben en archivos TXT mediante lectura y escritura simple.
5. Este mecanismo de logging es suficiente para una demo académica, pero no es ideal para alta concurrencia.
6. Se usó Service Account Key por simplicidad académica.
7. En producción real sería recomendable usar Workload Identity Federation.
8. Los textos muy cortos pueden ser clasificados correctamente, pero deberían generar solicitud de más información.

---

## 24. Mejoras futuras

Posibles mejoras:

- Agregar una regla para textos muy cortos o ambiguos.
- Crear un endpoint adicional con respuesta explicativa en texto plano.
- Reemplazar TXT por BigQuery o Cloud Logging para trazabilidad más robusta.
- Usar Workload Identity Federation en lugar de Service Account Key.
- Incorporar métricas históricas de calidad del modelo.
- Crear un dataset etiquetado propio.
- Entrenar un clasificador supervisado sobre embeddings.
- Agregar monitoreo de drift.
- Crear dashboards de predicciones por categoría.
- Incorporar revisión humana para casos de baja confianza.

---

## 25. Guía breve de sustentación

Este proyecto puede sustentarse como una demostración completa del ciclo MLOps:

```text
1. El código vive en GitHub.
2. Existen ramas dev y prod.
3. Cada rama dispara GitHub Actions.
4. El pipeline descarga modelo y datos externos desde Cloud Storage.
5. Se ejecutan pruebas automáticas.
6. Si las pruebas pasan, se construye una imagen Docker.
7. La imagen se publica en Artifact Registry.
8. La aplicación se despliega en Cloud Run.
9. Cada ambiente tiene su propio endpoint.
10. Cada predicción queda registrada en el archivo TXT correspondiente.
```

La idea central es que el despliegue no depende de acciones manuales después del push. El pipeline automatiza el paso desde código hasta endpoint funcional.

---

## 26. Evidencia de cumplimiento técnico

El sistema permite demostrar:

```text
push a dev
→ GitHub Actions
→ test
→ build
→ deploy Cloud Run DEV
→ /predict-dev
→ predicciones_dev.txt
```

Y también:

```text
push a prod
→ GitHub Actions
→ test
→ build
→ deploy Cloud Run PROD
→ /predict-prod
→ predicciones_prod.txt
```

Además, se evidencia que:

```text
modelo ONNX         → Cloud Storage
datos de prueba     → Cloud Storage
imagen Docker       → Artifact Registry
API                 → Cloud Run
logs dev/prod       → Cloud Storage
secrets             → GitHub Actions Secrets
```

---

## 27. Autor

```text
Esteban Oliveros Montoya
Maestría en Inteligencia Artificial Aplicada
Curso: MLOps
Proyecto final
```
