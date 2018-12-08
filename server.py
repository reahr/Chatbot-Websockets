#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import random

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

def createChatBot():
    chatbot = ChatBot('Barnard King', storage_adapter='chatterbot.storage.SQLStorageAdapter',
     logic_adapters=[
            "chatterbot.logic.MathematicalEvaluation",
            "chatterbot.logic.TimeLogicAdapter",
            {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": "chatterbot.response_selection.get_first_response",
            "threshold": 0.65,
            "default_response": 'I am sorry, but I d not understand.'
        }
        ]
    )
    chatbot.set_trainer(ChatterBotCorpusTrainer)
    chatbot.train("chatterbot.corpus.english")
    return chatbot

async def hello(websocket, path):
    try:
        chatbot = createChatBot()
        name = await websocket.recv()
        print(f"< {name}")

        greeting = f"<b>Barnard:</b> Hello {name}! My name is Barnard. Ask me something!"
        await websocket.send(greeting)

        while True:
            message = await websocket.recv()
            format_message = "<b>{}:</b> {}".format(name, message)
            await websocket.send(format_message)
            message = chatbot.get_response(message)
            bot_message = "<b>Barnard:</b> {}".format(message)
            await websocket.send(bot_message)
    except:
        print("connection was closed")
        exit(1)



start_server = websockets.serve(hello, 'localhost', 5678)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
