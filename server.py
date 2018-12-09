import asyncio
import websockets
import random
import webbrowser

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


# creates a chatbot object trained on math, time, and english conversations...
def createChatBot():
    chatbot = ChatBot('Barnard King', storage_adapter='chatterbot.storage.SQLStorageAdapter',
                      logic_adapters=[
                          {
                              "import_path": "chatterbot.logic.BestMatch",
                              "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
                              "response_selection_method": "chatterbot.response_selection.get_first_response",
                              "threshold": 0.65,
                              "default_response": 'I am sorry, but I do not understand.'
                          },
                          "chatterbot.logic.MathematicalEvaluation",
                          "chatterbot.logic.TimeLogicAdapter"
                      ],
                      )
    chatbot.set_trainer(ChatterBotCorpusTrainer)
    chatbot.train("chatterbot.corpus.english")
    return chatbot


# coroutine handler the server runs until forced to quit
async def chat(websocket, path):
    global chatbot  # make global since param cannot accept chatbot and load chatbot happens outside this function
    try:
        # first grab name from client and set conversation stamps
        name = await websocket.recv()
        print(f"< {name}")

        greeting = f"<b>Barnard:</b> Hello {name}! My name is Barnard. Let's chat!"
        await websocket.send(greeting)

        while True:
            # begin receiving messages to process a response for and send
            message = await websocket.recv()
            format_message = "<b>{}:</b> {}".format(name, message)
            await websocket.send(format_message)
            message = chatbot.get_response(message)
            bot_message = "<b>Barnard:</b> {}".format(message)
            await websocket.send(bot_message)
    except:
        # catch if a connection was closed either by closing page/quitting, exit server after
        print("connection was closed")
        exit(1)


start_server = websockets.serve(chat, 'localhost', 5678)
chatbot = createChatBot()
print ("finished training!")
# open chatbot after the bot has been trained
webbrowser.open("chatbot.html")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
