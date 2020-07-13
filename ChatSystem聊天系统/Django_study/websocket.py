async def websocket_application(scope, receive, send):
    while True:
        event = await receive()
        print('[event]', event)

        # 收到建立webScoket连接的消息
        if event['type'] == 'webscoket.connect':
            send({'type': 'webscoket_accept'})

        # 收到中断webScoket连接的消息
        elif event['type'] == 'webscoket.disconnect':
            break

        # 其他情况，正常的webscoket连接
        elif event['type'] == 'webscoket.receive':
            if event['text'] == 'ping':
                await send({
                    'type': 'webscoket.send',
                    'text': 'pong'
                })
        else:
            pass
    print("[disconnect]")
