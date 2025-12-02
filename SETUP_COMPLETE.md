# RFP Document Manager - Quick Start Guide

## ✅ All Steps Completed!

Alle 12 Schritte der Anleitung aus `prompting-strategy.md` wurden erfolgreich ausgeführt.

## 📁 Erstellte Dateien

- `models.py` - Pydantic v2 Datenmodelle (RFPDocument, ChatMessage)
- `utils.py` - Utility-Funktionen (Storage, Markdown-Renderer, OpenAI-Client, Extraction, Function-Calling)
- `app.py` - Streamlit-Anwendung mit kompletter UI
- `.env.example` - Beispiel-Konfigurationsdatei für Azure OpenAI
- `.gitignore` - Git-Ignore-Datei für sensible Daten

## 🚀 Anwendung starten

### 1. Environment-Variablen konfigurieren

Erstellen Sie eine `.env`-Datei basierend auf `.env.example`:

```bash
cp .env.example .env
```

Tragen Sie Ihre Azure OpenAI-Credentials ein:
```
AZURE_OPENAI_API_KEY=ihr_api_key
AZURE_OPENAI_ENDPOINT=https://ihre-ressource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
```

### 2. Virtuelle Umgebung aktivieren

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Streamlit-App starten

```powershell
streamlit run app.py
```

Die Anwendung wird automatisch im Browser unter `http://localhost:8501` geöffnet.

## 📋 Funktionen

### Upload & Extraktion
- Laden Sie .txt-Dateien mit RFP-Inhalten hoch
- Die KI extrahiert automatisch strukturierte Informationen
- Dokumente werden in `rfp_documents.json` gespeichert

### Chat-Interface
- Stellen Sie Fragen zu den hochgeladenen RFP-Dokumenten
- Die KI kann Tool-Calls verwenden um:
  - Detaillierte Dokumentzusammenfassungen anzuzeigen
  - Dokumenttabellen zu erstellen
- Beantworten Sie allgemeine Fragen über mehrere Dokumente

### Verwaltung
- **Clear Chat**: Löscht die Chat-Historie
- **Clear Documents**: Löscht alle Dokumente und die JSON-Datei

## 🧪 Testdaten

Verwenden Sie die drei Test-RFP-Dateien im `test-data/` Ordner:
- `rfp-test_1.txt`
- `rfp-test_2.txt`
- `rfp-test_3.txt`

## 🔧 Technologie-Stack

- **Python 3.11+**
- **Streamlit** - Web-UI Framework
- **Pydantic v2** - Datenvalidierung
- **Azure OpenAI** - KI-Funktionalität mit Structured Outputs & Function Calling
- **python-dotenv** - Umgebungsvariablen-Management

## ✨ Implementierte Features

✅ Pydantic-Modelle mit Type Hints und Docstrings
✅ JSON-basierte persistente Speicherung
✅ Markdown-Renderer für Dokumentanzeige
✅ Azure OpenAI Client mit Environment Variables
✅ Structured Outputs für RFP-Extraktion
✅ Function Calling mit zwei Tools
✅ Chat-Completion mit Tool-Calling-Support
✅ Vollständige Streamlit-UI mit File Upload
✅ Session State Management
✅ Clear-State Controls
