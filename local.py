import asyncio
from engine import Engine

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    queue_suma=asyncio.Queue()
    queue_resta=asyncio.Queue()
    a=2
    b=3
    w=.05
    engine=Engine(a=a,b=b,w=w)
    engine.suma_task(queue_suma)
    engine.resta_task(queue_resta)
    engine.seno_task(queue_suma,queue_resta)
    loop.run_forever()
