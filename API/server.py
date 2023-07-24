import asyncio
import json
import websockets


USERS = {}


async def handler(websocket):
    global USERS
    id = str(websocket.id)
    try:

        # print("new connection:", id)
        await websocket.send(json.dumps({"hi": id, "connected": (len(USERS)+1)}))
        websockets.broadcast(USERS.values(), json.dumps(
            {"join": id, "connected": (len(USERS)+1)}))
        USERS[id] = websocket

        async for message in websocket:
            # print(message)
            event = json.loads(message)
            print(event)
            if event == "":
                continue
            if event["action"] == "msg":
                if event["admin"] == "1":
                    websockets.broadcast(USERS.values(), json.dumps(
                        {"sender": id, "msg": event["msg"], "admin": "1", "secret": "something very secret"}))
                else:
                    websockets.broadcast(USERS.values(), json.dumps(
                        {"sender": id, "msg": event["msg"], "admin": "0"}))
            else:
                print("unsupported event: ", event)
    except Exception:
        print("error")
    finally:
        del USERS[id]
        websockets.broadcast(USERS.values(), json.dumps(
            {"left": id, "connected": len(USERS)}))


async def main():
    async with websockets.serve(handler, "localhost", 9001):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
