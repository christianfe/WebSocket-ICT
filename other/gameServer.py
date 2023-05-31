import asyncio
import json
import logging
import websockets

logging.basicConfig()


class GameManager():
    __status = ["Aborted", "Waiting", "Started", "Ended"]
    __s = 1

    def __init__(self):
        self.RED = ""
        self.BLUE = ""
        self.MAP = {}
        self.__s = 1
        self.__match = self.getJSON("game", init=True)
        self.winner = ""

    def getJSON(self, type: str, msg="", ws: object = None, init=False, string=False):
        res = {}
        if type == "game":
            if init:
                res = {"ROUNDS": 5, "RED": {"score": 20, "force": 20, "round": 0}, "BLUE": {
                    "score": 20, "force": 20, "round": 0}}
            else:
                res = {"type": "gameInfo", "data": self.__match}
        elif type == "status":
            if self.__s == 3 or self.__s == 0:
                res = {"type": "gameStatus", "data": {"user": self.userStatus(
                    ws), "game": self.getStatus(), "users": len(self.MAP), "winner": self.winner}}
            else:
                res = {"type": "gameStatus", "data": {"user": self.userStatus(
                    ws), "game": self.getStatus(), "users": len(self.MAP)}}

        if string:
            return json.dumps(res)
        return res

    def getStatus(self):
        return self.__status[self.__s]

    def gameReady(self):
        return (not self.RED == "") and (not self.BLUE == "")

    async def newUser(self, websocket):
        id = str(websocket.id)
        self.MAP[id] = websocket
        if self.RED == "":
            self.RED = id
        elif self.BLUE == "":
            self.BLUE = id
            await self.startGame()
        await websocket.send(GAME.getJSON("status", ws=websocket, string=True))

    def userLeft(self, websocket):
        id = str(websocket.id)
        if id == self.RED:
            self.RED = ""
            self.winner = "BLUE"
        elif id == self.BLUE:
            self.BLUE = ""
            self.winner = "RED"
        del self.MAP[id]
        self.__s = 0

    def userStatus(self, websocket, more=False):
        if str(websocket.id) == self.RED:
            if more:
                return "RED", "BLUE"
            else:
                return "Red Player"

        if str(websocket.id) == self.BLUE:
            if more:
                return "BLUE", "RED"
            else:
                return "Blue Player"
        if more:
            return "", "Watcher"
        else:
            return "Watcher"

    async def startGame(self):
        self.__s = 2
        for ws in list(self.MAP.values()):
            await ws.send(self.getJSON("game", ws=ws, string=True))

    async def playerAction(self, ws, attack):
        team, opponent = self.userStatus(ws, more=True)
        if not self.__s == 2:
            await ws.send(json.dumps({"error": "game not started"}))
            return
        if team == "":
            await ws.send(json.dumps({"error": "you are not a player"}))
            return
        if self.__match[team]["force"] < attack:
            await ws.send(json.dumps({"error": "not enought points"}))
            return
        if self.__match[team]["round"] >= self.__match["ROUNDS"]:
            await ws.send(json.dumps({"error": "No more rounds available"}))
            return
        self.__match[team]["force"] -= attack
        self.__match[team]["round"] += 1
        self.__match[opponent]["score"] -= attack + (0.1 * attack)
        if not await self.isGameEnded():
            for ws in list(self.MAP.values()):
                await ws.send(self.getJSON("game", ws=ws, string=True))

    async def isGameEnded(self):
        winner = ""
        if self.__match["RED"]["score"] <= 0:
            winner = "BLUE"
        elif self.__match["BLUE"]["score"] <= 0:
            winner = "RED"
        if winner == "":
            return False
        self.__s = 3
        self.winner = winner
        for ws in list(self.MAP.values()):
            await ws.send(self.getJSON("status", ws=ws, string=True))
        return True


GAME = GameManager()


async def handler(websocket):
    global GAME
    try:
        await GAME.newUser(websocket)

        async for message in websocket:
            event = json.loads(message)
            if event["action"] == "status":
                await websocket.send(GAME.getJSON("status", ws=websocket, string=True))
            elif event["action"] == "attack":
                await GAME.playerAction(websocket, event['force'])
            else:
                logging.error("unsupported event: %s", event)
    finally:
        GAME.userLeft(websocket)


async def main():
    async with websockets.serve(handler, "localhost", 9001):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
