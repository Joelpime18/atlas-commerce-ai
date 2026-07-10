# Conversacion Atlas - 2026-07-10

## Objetivo del proyecto

Atlas Commerce AI sera una plataforma SaaS para ayudar a negocios que venden por
WhatsApp. El Cliente Cero es Rosa Pistacho.

El objetivo inicial no es construir un chatbot avanzado. La version inicial debe
ser un capturador confiable de pedidos: responder rapido, guiar al cliente,
organizar la informacion y evitar que se pierdan solicitudes.

## Regla de trabajo

Cada funcionalidad debe cumplir tres condiciones:

- Funciona.
- Se puede probar con un cliente real.
- Aporta valor.

Si una funcionalidad no cumple las tres, no entra en la siguiente version.

## Decisiones tomadas

- El proyecto se llama Atlas Commerce AI.
- El repositorio es `Joelpime18/atlas-commerce-ai`.
- La rama principal es `main`.
- La rama de desarrollo sera `develop`.
- El backend se construye con Python, FastAPI, Pydantic y SQLAlchemy.
- La base de datos prevista es PostgreSQL.
- WhatsApp se conectara mas adelante mediante Meta Cloud API.
- OpenAI se conectara mas adelante.
- No se incluira analisis de imagenes en la version inicial.
- Rosa Pistacho revisara manualmente imagenes, disponibilidad, precio final y pagos.

## Estado actual

Ya existe una primera estructura del proyecto:

- Backend FastAPI.
- Ruta de prueba `GET /health`.
- Ruta principal `POST /webhook`.
- Servicio inicial del asistente.
- Identificacion simple del cliente por numero de telefono.
- Pruebas automatizadas.
- Documentacion inicial.

El servidor local ya fue probado en navegador usando:

```text
http://127.0.0.1:8000/docs
```

La prueba fue exitosa.

## Menu actual del asistente

Cuando el cliente escribe `Hola`, Atlas responde:

```text
¡Hola! 🌸✨ Qué alegría tenerte aquí. Bienvenido(a) a Rosa Pistacho. Estamos felices de acompañarte y ayudarte a encontrar justo lo que buscas. ¿En qué podemos ayudarte hoy?

Deseas:
1. Cotizar una torta
2. Realizar un pedido
3. Consultar un pedido
4. Conocer horarios
```

## Opcion 1 - Cotizar una torta

Atlas debe pedir:

- Para cuantas personas es la torta.
- Color o colores de la torta.
- Si tiene imagen de referencia.
- Si tiene imagen, pedir que la envie.

Tambien debe aclarar:

- Rosa Pistacho no trabaja con imagenes obscenas o contenido inapropiado.

## Opcion 2 - Realizar un pedido

Atlas debe pedir:

- Nombre completo.
- Fecha de entrega.
- Tipo de producto.
- Numero de personas.
- Si desea recoger o recibir a domicilio.
- Imagen de referencia de la torta.

Si el cliente indica que recogera la torta, Atlas debe enviar la direccion de
Rosa Pistacho.

La direccion real aun esta pendiente por confirmar.

## Opcion 3 - Consultar un pedido

Atlas debe solicitar:

- Numero de pedido.

En esta version todavia no existe busqueda real en base de datos. Eso vendra en
una siguiente fase.

## Opcion 4 - Conocer horarios

Atlas debe responder la consulta de horarios.

Los horarios reales de Rosa Pistacho aun estan pendientes por confirmar.

## Pruebas actuales

Las pruebas automatizadas pasan correctamente:

```text
10 passed
```

Esto confirma que:

- El saludo responde correctamente.
- El menu tiene las 4 opciones.
- La opcion de cotizacion pide los datos correctos.
- La opcion de pedido pide los datos correctos.
- La consulta de pedido solicita numero de pedido.
- La opcion de horarios responde.
- La recogida responde con mensaje de direccion pendiente.

## Proximo paso recomendado

El siguiente paso natural es guardar conversaciones y pedidos preliminares.

Eso permitira que Atlas no solo responda, sino que recuerde en que punto va cada
cliente y pueda capturar un pedido paso a paso.

Primer objetivo de esa fase:

- Crear una memoria simple de conversacion.
- Guardar el estado del cliente.
- Registrar un pedido preliminar con los datos disponibles.
- Mantener la conversacion ordenada hasta que una asesora humana revise el caso.
