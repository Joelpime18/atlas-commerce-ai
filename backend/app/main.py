from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api.webhook import router as webhook_router
from app.config.settings import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(webhook_router)
app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.get("/demo", response_class=HTMLResponse)
def chat_demo() -> str:
    return """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Atlas Commerce AI - Prueba</title>
  <style>
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f7f2ef;
      color: #2f2725;
    }
    main {
      max-width: 760px;
      margin: 0 auto;
      padding: 24px;
    }
    h1 {
      margin: 0 0 8px;
      font-size: 30px;
    }
    .subtitle {
      margin: 0 0 20px;
      color: #6d5b56;
    }
    .panel {
      background: white;
      border: 1px solid #e2d8d2;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 16px;
    }
    label {
      display: block;
      font-weight: 700;
      margin-bottom: 8px;
    }
    select, textarea, button {
      width: 100%;
      box-sizing: border-box;
      font: inherit;
    }
    select, textarea {
      border: 1px solid #cdbeb8;
      border-radius: 8px;
      padding: 10px;
      background: #fff;
    }
    textarea {
      min-height: 96px;
      resize: vertical;
    }
    button {
      border: 0;
      border-radius: 8px;
      padding: 12px;
      margin-top: 12px;
      background: #8d4f48;
      color: white;
      cursor: pointer;
      font-weight: 700;
    }
    button:hover {
      background: #753f39;
    }
    .chat {
      display: grid;
      gap: 12px;
      margin-top: 16px;
    }
    .message {
      white-space: pre-wrap;
      border-radius: 8px;
      padding: 12px;
      line-height: 1.4;
    }
    .client {
      background: #efe5df;
    }
    .atlas {
      background: #fdf9f6;
      border: 1px solid #eaded7;
    }
    .meta {
      margin-top: 8px;
      color: #7a6861;
      font-size: 13px;
    }
    .examples {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 10px;
    }
    .example {
      width: auto;
      margin: 0;
      padding: 8px 10px;
      background: #e9d8d2;
      color: #382b28;
    }
  </style>
</head>
<body>
  <main>
    <h1>Atlas Commerce AI</h1>
    <p class="subtitle">Prueba de conversación para Rosa Pistacho</p>

    <section class="panel">
      <label for="client">Tipo de cliente</label>
      <select id="client">
        <option value="573001112233">Cliente nuevo</option>
        <option value="573009990001">Latido Coffee</option>
      </select>
    </section>

    <section class="panel">
      <label for="message">Mensaje del cliente</label>
      <textarea id="message">Hola</textarea>
      <div class="examples">
        <button class="example" type="button" onclick="setMessage('Hola')">Hola</button>
        <button class="example" type="button" onclick="setMessage('1')">Cotizar</button>
        <button class="example" type="button" onclick="setMessage('Hacen domicilios?')">Domicilios</button>
        <button class="example" type="button" onclick="latidoExample()">Pedido Latido</button>
      </div>
      <button type="button" onclick="sendMessage()">Enviar a Atlas</button>
    </section>

    <section class="panel">
      <strong>Conversación</strong>
      <div id="chat" class="chat"></div>
    </section>
  </main>

  <script>
    function setMessage(text) {
      document.getElementById("message").value = text;
    }

    function latidoExample() {
      document.getElementById("client").value = "573009990001";
      setMessage("Necesitamos 2 tortas de chocolate, 18 brownies y 12 galletas NY Oreo");
    }

    function addMessage(kind, text, meta) {
      const chat = document.getElementById("chat");
      const bubble = document.createElement("div");
      bubble.className = "message " + kind;
      bubble.textContent = text;

      if (meta) {
        const extra = document.createElement("div");
        extra.className = "meta";
        extra.textContent = meta;
        bubble.appendChild(extra);
      }

      chat.prepend(bubble);
    }

    async function sendMessage() {
      const phone = document.getElementById("client").value;
      const message = document.getElementById("message").value;

      addMessage("client", message);

      const response = await fetch("/webhook", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({from_phone: phone, message})
      });

      const data = await response.json();

      if (!response.ok) {
        addMessage("atlas", "No pude procesar el mensaje. Revisa el texto e intenta de nuevo.");
        return;
      }

      addMessage("atlas", data.reply, "Intención: " + data.intent + " | Etapa: " + data.stage);
    }
  </script>
</body>
</html>
"""
