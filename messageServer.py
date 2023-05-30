import asyncio
import json
import logging
import websockets

logging.basicConfig()

USERS = {}


async def handler(websocket):
    global USERS
    id = str(websocket.id)
    try:

        print("new connection:", id)
        await websocket.send(json.dumps({"hi": id}))
        websockets.broadcast(USERS.values(), json.dumps({"join": id}))
        USERS[id] = websocket

        async for message in websocket:
            event = json.loads(message)
            if event == "":
                continue
            if event["action"] == "msg":
                websockets.broadcast(USERS.values(), json.dumps(
                    {"sender": id, "msg": event["msg"]}))
            else:
                logging.error("unsupported event: %s", event)
    finally:
        del USERS[id]
        websockets.broadcast(USERS.values(), json.dumps({"left": id}))


async def main():
    async with websockets.serve(handler, "localhost", 9001):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
