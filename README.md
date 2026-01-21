# Intelligent Data Room

A full-stack AI-powered data analysis application that allows users to upload datasets (CSV/Excel) and chat with them using natural language.

## Basic Architecture

The application follows a client-server architecture:
- **Frontend**: A React application that provides a chat interface. It handles file uploads (converting Excel to CSV if necessary), manages conversation history, and displays results (text or generated charts).
- **Backend**: A FastAPI server that integrates with PandasAI. It uses a "Plan-and-Execute" pattern where user prompts are first converted into a logical execution plan by an LLM, and then executed against the loaded dataframe.

## Tech Stack

### Frontend
- **Framework**: React (Vite) + TypeScript
- **Styling**: Tailwind CSS + Shadcn UI
- **HTTP Client**: Axios

### Backend
- **Framework**: FastAPI
- **AI/ML**: PandasAI, LiteLLM (Google Gemini)
- **Data Processing**: Pandas

## Exposed API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload` | Upload a CSV file. Returns a unique `dataframe_id`. |
| `POST` | `/generate-plan` | Accepts `dataframe_id` and `prompt`. Returns a generated execution plan. |
| `POST` | `/execute-plan` | Accepts `dataframe_id` and `plan`. Executes the plan and returns result (Text or Base64 Image). |

## Pages

- **AI Chat** (`/`): The main workspace.
  - Initial state: File upload dropzone.
  - Active state: Chat interface with "Thinking" indicator, Plan visualization (Reasoning), and Multi-turn conversation context (last 5 messages).
- **Challenge Description** (`/challenge`): Displays the project requirements doc.

## Key Components

- `DataChat`: The main container managing application state.
- `ChatMessages`: Renders the conversation list, including user queries, AI text responses, and generated charts. Handles the "Thinking..." animation and "Reasoning" collapsible.
- `ChatInput`: Handles file inputs (Dropzone) and text inputs. Logic includes auto-conversion of `.xlsx` -> `.csv`.
- `Navbar`: Simple navigation menu using Shadcn components.

## How to Run

### Backend
1. Navigate to the backend directory:
   ```bash
   cd intelligent-data-room-be
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables (API keys for Gemini).
    ```env
    MODEL_NAME=gemini-2.5-flash # or any other Gemini model
    GEMINI_API_KEY=your_gemini_api_key_here
    ```
4. Run the server:
   ```bash
   fastapi dev main.py
   ```
   Server runs at `http://127.0.0.1:8000`.

### Frontend
1. Navigate to the frontend directory:
   ```bash
   cd intelligent-data-room-fe
   ```
2. Change the base API URL in `src\components\custom\chat-handlers.ts` if necessary.
3. Install dependencies:
   ```bash
   npm install
   ```
4. Run the development server:
   ```bash
   npm run dev
   ```
   App runs at `http://localhost:5173`.
