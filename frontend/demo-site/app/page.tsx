"use client";

import { FormEvent, useMemo, useState } from "react";

type ClientType = "new" | "latido";

type Message = {
  from: "client" | "atlas";
  text: string;
  meta?: string;
};

type Session = {
  flow: "quote" | "order" | null;
  step: string | null;
  data: Record<string, string>;
};

const address = "Cra 39 # 15 - 56, Barrio Villa Aurora II, Acacias, Meta";

const initialMessages: Message[] = [
  {
    from: "atlas",
    text:
      "Esta es una demo temporal para que Rosa Pistacho revise textos, letras y flujo de conversacion antes de conectar WhatsApp real.",
    meta: "Prueba remota para Acacias",
  },
];

function normalize(value: string) {
  return value.toLowerCase().trim();
}

function isGreeting(message: string) {
  return ["hola", "buenas", "buen dia", "buenas tardes", "buenas noches"].some(
    (item) => message.includes(item),
  );
}

function isThanks(message: string) {
  return ["gracias", "muchas gracias", "mil gracias", "listo gracias"].some(
    (item) => message.includes(item),
  );
}

function mainMenu() {
  return (
    "¡Hola! 🌸✨ Que alegria tenerte aqui. Bienvenido(a) a Rosa Pistacho. " +
    "Estamos felices de acompañarte y ayudarte a encontrar justo lo que buscas. " +
    "¿En que podemos ayudarte hoy?\n\n" +
    "Deseas:\n" +
    "1. Cotizar una torta personalizada\n" +
    "2. Realizar un pedido\n" +
    "3. Catalogo\n" +
    "4. Consultar un pedido\n" +
    "5. Conocer horarios\n" +
    "6. Quiero que mi cafe sea cliente frecuente"
  );
}

function unknownMenu() {
  return (
    "Gracias por escribir a Rosa Pistacho. Para ayudarte mejor, responde con una opcion:\n\n" +
    "1. Cotizar una torta personalizada\n" +
    "2. Realizar un pedido\n" +
    "3. Ver catalogo\n" +
    "4. Consultar un pedido\n" +
    "5. Conocer horarios\n" +
    "6. Informacion para cafes frecuentes"
  );
}

function catalogReply() {
  return (
    "Claro. Puedes consultar el catalogo de Rosa Pistacho en este PDF:\n\n" +
    `${window.location.origin}/catalogo-rosa-pistacho.pdf\n\n` +
    "Las tortas personalizadas se cotizan segun el diseño."
  );
}

function getLatidoReply(message: string) {
  if (isThanks(message)) {
    return {
      text:
        "Gracias a ustedes, Latidos. Nos alegra mucho que sigan eligiendo a Rosa Pistacho. Dejamos la informacion registrada para continuar con el proceso.",
      meta: "Cliente frecuente",
    };
  }

  if (message === "1" || message === "2" || isGreeting(message)) {
    return {
      text:
        "Buen dia, Latidos. Que gusto atenderlos nuevamente. Por favor envianos el pedido con los productos y cantidades que necesitan. Por ejemplo: 2 tortas de chocolate, 18 brownies y 12 galletas NY Oreo.",
      meta: "Cliente frecuente",
    };
  }

  if (
    message.includes("torta") ||
    message.includes("brownie") ||
    message.includes("galleta")
  ) {
    return {
      text:
        "Perfecto, Latidos. Este es el resumen de tu pedido:\n\n" +
        "- 2 x Torta de Chocolate: $108.000 COP\n" +
        "- 18 x Brownie: $144.000 COP\n" +
        "- 12 x Galleta NY Oreo: $54.000 COP\n\n" +
        "Total: $306.000 COP\n\n" +
        "Registraremos el pedido para preparacion segun las condiciones acordadas con Rosa Pistacho.",
      meta: "Pedido frecuente",
    };
  }

  return {
    text:
      "Por favor envianos el pedido con productos y cantidades. Por ejemplo: 2 tortas de chocolate, 18 brownies y 12 galletas NY Oreo.",
    meta: "Cliente frecuente",
  };
}

function getReply(
  clientType: ClientType,
  rawMessage: string,
  session: Session,
): { reply: Message; nextSession: Session } {
  const message = normalize(rawMessage);

  if (clientType === "latido") {
    const latido = getLatidoReply(message);
    return {
      reply: { from: "atlas", text: latido.text, meta: latido.meta },
      nextSession: { flow: null, step: null, data: {} },
    };
  }

  if (isThanks(message)) {
    return {
      reply: {
        from: "atlas",
        text:
          "Gracias a ti por elegir a Rosa Pistacho. Nos alegra poder acompañarte y ayudarte con tu pedido.",
        meta: "Cierre amable",
      },
      nextSession: { flow: null, step: null, data: {} },
    };
  }

  if (session.flow === "quote" && session.step === "people") {
    return {
      reply: {
        from: "atlas",
        text:
          "Perfecto. ¿Tienes una imagen de referencia? Si la tienes, por favor enviala en este chat.\n\n" +
          "Ten presente que en Rosa Pistacho no trabajamos con imagenes obscenas o contenido inapropiado.",
        meta: "Cotizacion",
      },
      nextSession: {
        flow: "quote",
        step: "reference",
        data: { ...session.data, people: rawMessage },
      },
    };
  }

  if (session.flow === "quote" && session.step === "reference") {
    return {
      reply: {
        from: "atlas",
        text:
          "Gracias. Ya tenemos la informacion inicial para cotizar tu torta personalizada:\n\n" +
          `- Personas: ${session.data.people ?? "pendiente"}\n` +
          `- Imagen de referencia: ${rawMessage}\n\n` +
          "La pastelera de Rosa Pistacho revisara los detalles y te compartira la cotizacion.",
        meta: "Revision de pastelera",
      },
      nextSession: { flow: null, step: null, data: {} },
    };
  }

  if (session.flow === "order" && session.step === "name") {
    return {
      reply: {
        from: "atlas",
        text: "Gracias. ¿Para que fecha necesitas el pedido?",
        meta: "Pedido",
      },
      nextSession: {
        flow: "order",
        step: "date",
        data: { ...session.data, name: rawMessage },
      },
    };
  }

  if (session.flow === "order" && session.step === "date") {
    return {
      reply: {
        from: "atlas",
        text: "Perfecto. ¿Que tipo de producto necesitas?",
        meta: "Pedido",
      },
      nextSession: {
        flow: "order",
        step: "product",
        data: { ...session.data, date: rawMessage },
      },
    };
  }

  if (session.flow === "order" && session.step === "product") {
    return {
      reply: {
        from: "atlas",
        text: "Entendido. ¿Para cuantas personas es?",
        meta: "Pedido",
      },
      nextSession: {
        flow: "order",
        step: "people",
        data: { ...session.data, product: rawMessage },
      },
    };
  }

  if (session.flow === "order" && session.step === "people") {
    return {
      reply: {
        from: "atlas",
        text:
          "Gracias. Por favor envia la imagen de referencia de la torta o cuentanos si no tienes una.",
        meta: "Pedido",
      },
      nextSession: {
        flow: "order",
        step: "reference",
        data: { ...session.data, people: rawMessage },
      },
    };
  }

  if (session.flow === "order" && session.step === "reference") {
    return {
      reply: {
        from: "atlas",
        text:
          "Gracias. Ya tenemos la informacion inicial de tu pedido:\n\n" +
          `- Nombre: ${session.data.name ?? "pendiente"}\n` +
          `- Fecha de entrega: ${session.data.date ?? "pendiente"}\n` +
          `- Tipo de producto: ${session.data.product ?? "pendiente"}\n` +
          `- Personas: ${session.data.people ?? "pendiente"}\n` +
          `- Imagen de referencia: ${rawMessage}\n\n` +
          `Recuerda que los pedidos se recogen en: ${address}. Una asesora revisara la informacion y continuara el proceso.`,
        meta: "Revision humana",
      },
      nextSession: { flow: null, step: null, data: {} },
    };
  }

  if (isGreeting(message)) {
    return {
      reply: { from: "atlas", text: mainMenu(), meta: "Menu principal" },
      nextSession: { flow: null, step: null, data: {} },
    };
  }

  if (message === "1" || message.includes("cotizar")) {
    return {
      reply: {
        from: "atlas",
        text:
          "Perfecto, con gusto te ayudamos a cotizar tu torta personalizada. Para empezar: ¿para cuantas personas es la torta?",
        meta: "Cotizacion",
      },
      nextSession: { flow: "quote", step: "people", data: {} },
    };
  }

  if (message === "2" || message.includes("pedido")) {
    return {
      reply: {
        from: "atlas",
        text:
          "Listo. Para realizar tu pedido, empecemos por el nombre. ¿A nombre de quien registramos el pedido?\n\n" +
          `Importante: Rosa Pistacho no realiza domicilios. Los pedidos se recogen en: ${address}.`,
        meta: "Pedido",
      },
      nextSession: { flow: "order", step: "name", data: {} },
    };
  }

  if (message === "3" || message.includes("catalogo") || message.includes("precio")) {
    return {
      reply: { from: "atlas", text: catalogReply(), meta: "Catalogo PDF" },
      nextSession: { flow: null, step: null, data: {} },
    };
  }

  if (message === "4" || message.includes("consultar")) {
    return {
      reply: {
        from: "atlas",
        text: "Claro. Para consultar tu pedido, por favor enviame el numero de pedido.",
        meta: "Consulta de pedido",
      },
      nextSession: { flow: null, step: null, data: {} },
    };
  }

  if (message === "5" || message.includes("horario") || message.includes("domingo")) {
    return {
      reply: {
        from: "atlas",
        text:
          "Nuestro horario de atencion es:\n\nLunes a viernes: 9:00 a.m. a 12:00 p.m. y 2:00 p.m. a 6:00 p.m.\nSabados: 9:00 a.m. a 5:00 p.m.\nDomingos: cerrado.",
        meta: "Horarios",
      },
      nextSession: { flow: null, step: null, data: {} },
    };
  }

  if (message === "6" || message.includes("cliente frecuente")) {
    return {
      reply: {
        from: "atlas",
        text:
          "¡Nos encanta que quieras que tu cafe trabaje con Rosa Pistacho! Por favor dejanos el nombre del cafe, nombre de contacto y numero de telefono. Rosa Pistacho revisara la informacion y se pondra en contacto contigo.",
        meta: "Cafe frecuente",
      },
      nextSession: { flow: null, step: null, data: {} },
    };
  }

  if (message.includes("domicilio") || message.includes("domicilios")) {
    return {
      reply: {
        from: "atlas",
        text:
          "Rosa Pistacho no realiza domicilios.\n\n" +
          `Puedes recoger tu pedido en: ${address}.`,
        meta: "Domicilios",
      },
      nextSession: { flow: null, step: null, data: {} },
    };
  }

  return {
    reply: { from: "atlas", text: unknownMenu(), meta: "Guia" },
    nextSession: { flow: null, step: null, data: {} },
  };
}

export default function Home() {
  const [clientType, setClientType] = useState<ClientType>("new");
  const [input, setInput] = useState("Hola");
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [session, setSession] = useState<Session>({
    flow: null,
    step: null,
    data: {},
  });

  const subtitle = useMemo(() => {
    return clientType === "latido"
      ? "Modo cliente frecuente: Latido Coffee"
      : "Modo cliente nuevo";
  }, [clientType]);

  function sendMessage(event?: FormEvent) {
    event?.preventDefault();
    const clean = input.trim();
    if (!clean) return;

    const { reply, nextSession } = getReply(clientType, clean, session);
    setMessages((current) => [
      { from: "client", text: clean, meta: subtitle },
      reply,
      ...current,
    ]);
    setSession(nextSession);
    setInput("");
  }

  function useExample(text: string, type: ClientType = clientType) {
    setClientType(type);
    setInput(text);
  }

  function resetDemo() {
    setMessages(initialMessages);
    setSession({ flow: null, step: null, data: {} });
    setInput("Hola");
  }

  return (
    <main className="shell">
      <section className="hero">
        <div>
          <p className="eyebrow">Demo temporal publicada</p>
          <h1>Atlas para Rosa Pistacho</h1>
          <p className="subtitle">
            Prueba remota para revisar textos, letras y flujo de conversacion
            antes de conectar WhatsApp real.
          </p>
        </div>
        <div className="status">
          <span>Acacias</span>
          <strong>Validacion v0.1</strong>
          <span>Bogota</span>
        </div>
      </section>

      <section className="workspace" aria-label="Chat de prueba">
        <aside className="controls">
          <label htmlFor="client">Tipo de cliente</label>
          <select
            id="client"
            value={clientType}
            onChange={(event) => {
              setClientType(event.target.value as ClientType);
              setSession({ flow: null, step: null, data: {} });
            }}
          >
            <option value="new">Cliente nuevo</option>
            <option value="latido">Latido Coffee</option>
          </select>

          <div className="quick-actions" aria-label="Mensajes de prueba">
            <button type="button" onClick={() => useExample("Hola", "new")}>
              Saludo
            </button>
            <button type="button" onClick={() => useExample("1", "new")}>
              Cotizar
            </button>
            <button type="button" onClick={() => useExample("3", "new")}>
              Catalogo
            </button>
            <button
              type="button"
              onClick={() =>
                useExample(
                  "Necesitamos 2 tortas de chocolate, 18 brownies y 12 galletas NY Oreo",
                  "latido",
                )
              }
            >
              Latido
            </button>
            <button type="button" onClick={() => useExample("Gracias")}>
              Gracias
            </button>
          </div>

          <button className="secondary" type="button" onClick={resetDemo}>
            Reiniciar prueba
          </button>
        </aside>

        <section className="chat-panel">
          <form onSubmit={sendMessage} className="composer">
            <label htmlFor="message">Mensaje del cliente</label>
            <textarea
              id="message"
              value={input}
              onChange={(event) => setInput(event.target.value)}
              placeholder="Escribe como si fueras una cliente..."
            />
            <button type="submit">Enviar a Atlas</button>
          </form>

          <div className="conversation" aria-live="polite">
            {messages.map((message, index) => (
              <article className={`bubble ${message.from}`} key={`${index}-${message.text}`}>
                <p>{message.text}</p>
                {message.meta ? <span>{message.meta}</span> : null}
              </article>
            ))}
          </div>
        </section>
      </section>
    </main>
  );
}
