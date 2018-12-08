#!/usr/bin/env python

# WS server example

import asyncio
import websockets


async def hello(websocket, path):
    try:
        name = await websocket.recv()
        print(f"< {name}")

        greeting = f"<b>Barnard:</b> Hello {name}! My name is Barnard. Ask me something!"
        await websocket.send(greeting)

        while True:
            message = await websocket.recv()
            format_message = "<b>{}:</b> {}".format(name, message)
            await websocket.send(format_message)
            message = "my name is bot"
            bot_message = "<b>Barnard:</b> {}".format(message)
            await websocket.send(bot_message)
    except:
        print("connection was closed")
        exit(1)


start_server = websockets.serve(hello, 'localhost', 5678)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
