# -*-coding: utf-8 -*-

import websockets
import json


async def conn(main):
    while True:
        # "ws://4.tcp.ngrok.io:12958" tcp 주소 예
        async with websockets.connect("ws://127.0.0.1:5000") as websocket:
            await websocket.send(json.dumps(main.client))
            if main.client['create_project']:
                main.client['create_project'].clear()
            ret = await websocket.recv()
            # main.client[str(a[0])] = str(b[0])
            print(ret)
            main.refresh()  # receive 값에 맞게 작업 새로고침
