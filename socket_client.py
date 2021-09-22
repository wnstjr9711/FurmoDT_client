# -*-coding: utf-8 -*-

import websockets
import json


async def conn(main):
    # "ws://4.tcp.ngrok.io:12958" tcp 주소 예
    async with websockets.connect("ws://127.0.0.1:9998") as websocket:
        while True:
            await websocket.send(json.dumps(main.client))
            if main.client['create_project']:
                main.client['create_project'].clear()
            ret = await websocket.recv()
            main.refresh(json.loads(ret))  # receive 값에 맞게 작업 새로고침
            print(ret)
