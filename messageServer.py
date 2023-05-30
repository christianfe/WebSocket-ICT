import asyncio
import json
import logging
import websockets

logging.basicConfig()

USER_A = None
USER_B = None


async def handler(websocket):
    global USER_A, USER_B
    id = str(websocket.id)
    try:
        if USER_A == None:
            USER_A = websocket
        elif USER_B == None:
            USER_B = websocket
        else:
            return
        print("new connection:", id)
        await websocket.send(json.dumps({"hi": id}))

        async for message in websocket:
            event = json.loads(message)
            if event == "":
                continue
            if event["action"] == "status":
                if USER_A == None or USER_B == None:
                    await websocket.send(json.dumps({"you": id}))
                else:
                    if id == str(USER_A.id):
                        await websocket.send(json.dumps({"you": id, "someone": str(USER_B.id)}))
                    elif id == str(USER_B.id):
                        await websocket.send(json.dumps({"you": id, "someone": str(USER_A.id)}))
            elif event["action"] == "msg":
                if USER_A.id == websocket.id:
                    await USER_A.send(json.dumps({"mine": True, "msg": event["msg"]}))
                    await USER_B.send(json.dumps({"mine": False, "msg": event["msg"]}))
                elif USER_B.id == websocket.id:
                    await USER_B.send(json.dumps({"mine": True, "msg": event["msg"]}))
                    await USER_A.send(json.dumps({"mine": False, "msg": event["msg"]}))
            else:
                logging.error("unsupported event: %s", event)
    finally:
        if USER_A.id == websocket.id:
            USER_A = None
        elif USER_B.id == websocket.id:
            USER_B = None


async def main():
    async with websockets.serve(handler, "localhost", 9001):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
