# -*-coding: utf-8 -*-

import websockets
import websockets.client
import json
import config


async def conn(main):
    # "ws://4.tcp.ngrok.io:12958" tcp 주소 예
    async with websockets.connect(f"ws://{config.SERVER}/ws") as websocket:
        while True:
            await websocket.send(json.dumps(main.client))
            if main.client['POST']:
                main.setdefault_client()
            ret = await websocket.recv()
            main.refresh(json.loads(ret))  # receive 값에 맞게 작업 새로고침
