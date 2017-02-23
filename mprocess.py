import asyncio
import functools
import concurrent.futures
from engine import Engine
from multiprocessing import Manager, Queue


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    manager=Manager()
    queue_suma=manager.Queue()
    queue_resta=manager.Queue()
    a=2
    b=3
    w=.05
    engine=Engine(a=a,b=b,w=w, mode='mprocess')
    with concurrent.futures.ProcessPoolExecutor() as executor:
        def suma_process():
            print(engine)
            engine.suma_task(queue_suma)

        def resta_process():
            print(engine)
            engine.resta_task(queue_resta)

        def seno_process():
            print(engine)
            engine.seno_task(queue_suma,queue_resta)

        loop.run_in_executor(
                executor,
                #functools.partial(engine.suma_task,queue_suma)
                suma_process
        )
        loop.run_in_executor(
            executor,
            resta_process
        )
        loop.run_in_executor(
            executor,
            seno_process
        )
            #await engine.resta_task(queue_resta)
            #await engine.seno_task(queue_suma, queue_resta)
        loop.run_forever()
        
