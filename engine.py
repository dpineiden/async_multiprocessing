import asyncio
import functools
import math
from networktools.time import timestamp
from networktools.colorprint import gprint, bprint, rprint
from tasktools.taskloop import coromask, renew, simple_fargs, simple_fargs_out

def read_queue(queue):
    result=[]
    if not queue.empty():
        for m in range(queue.qsize()):
            result.append(queue.get())
        queue.task_done()
    return result

async def co_read_queue(queue):
    result=[]
    if not queue.empty():
        for m in range(queue.qsize()):
            result.append(await queue.get())
        queue.task_done()
    return result

def suma_fargs(_in, obtained):
    b=_in[0]+.1
    _out=[b,_in[1]]
    return _out

def resta_fargs(_in, obtained):
    b=_in[0]+.1
    _out=[b,_in[1]]
    return _out

class Engine(object):
    def __init__(self, *args, **kwargs):
        self.a=kwargs['a']
        self.b=kwargs['b']
        self.w=kwargs['w']
        self.mode=kwargs['mode']

    #colores::::
    #red: suma
    #blue: resta
    #green: seno

    async def suma(self, delta, queue):
        result=self.a+delta
        bprint(result)
        await asyncio.sleep(2)
        if not self.mode=='mprocess':
            await queue.put(result)
        else:
            queue.put(result)
        return result

    async def resta(self, delta, queue):
        result=self.b-delta
        rprint(result)
        await asyncio.sleep(2)
        if not self.mode=='mprocess':
            await queue.put(result)
        else:
            queue.put(result)
        return result

    async def seno(self, queue_suma, queue_resta):
        if not self.mode=='mprocess':
            r=await co_read_queue(queue_resta)
            s=await co_read_queue(queue_suma)
        else:
            r=read_queue(queue_resta)
            s=read_queue(queue_suma)
        result=0
        print(r)
        print(s)
        if s and r:
            amplitude=s[0]/r[0]
            ts=timestamp()
            result = amplitude * math.sin(self.w*ts)
            gprint(result)
        await asyncio.sleep(2)
        return result

    def suma_task(self, queue):
        loop=asyncio.get_event_loop()
        rprint("Iniciando tarea para Suma")
        delta=.3
        args= [delta, queue]
        # Create instances
        task=loop.create_task(
            coromask(
                self.suma,
                args,
                suma_fargs)
        )
        task.add_done_callback(
            functools.partial(
                renew,
                task,
                self.suma,
                suma_fargs)
        )
        if not loop.is_running() and self.mode=='mprocess':
            loop.run_forever()
            pass


    def resta_task(self, queue):
        loop=asyncio.get_event_loop()
        bprint("Iniciando tarea para resta")
        delta=.3
        args= [delta, queue]
        # Create instances
        task=loop.create_task(
            coromask(
                self.resta,
                args,
                resta_fargs)
        )
        task.add_done_callback(
            functools.partial(
                renew,
                task,
                self.resta,
                resta_fargs)
        )
        if not loop.is_running() and self.mode=='mprocess':
            loop.run_forever()
            pass




    def seno_task(self, queue_suma, queue_resta):
        loop=asyncio.get_event_loop()
        gprint("Iniciando tarea para seno")
        delta=.3
        args= [queue_suma, queue_resta]
        # Create instances
        task=loop.create_task(
            coromask(
                self.seno,
                args,
                simple_fargs)
        )
        task.add_done_callback(
            functools.partial(
                renew,
                task,
                self.seno,
                simple_fargs)
        )
        if not loop.is_running() and self.mode=='mprocess':
            loop.run_forever()
            pass

