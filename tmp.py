import itertools
import multiprocessing
from collections import deque
from multiprocessing.managers import BaseManager, MakeProxyType

class DequeManager(BaseManager):
   pass

BaseDequeProxy = MakeProxyType('BaseDequeProxy', (
    '__add__', '__contains__', '__delitem__', '__getitem__', '__len__',
    '__mul__', '__reversed__', '__rmul__', '__setitem__',
    'append', 'count', 'extend', 'extendleft', 'index', 'insert', 'pop', 
    'remove', 'reverse', 'sort', 'appendleft', 'popleft', 'rotate', 
    '__imul__'
    ))
class DequeProxy(BaseDequeProxy):
    def __iadd__(self, value):
        self._callmethod('extend', (value,))
        return self
    def __imul__(self, value):
        self._callmethod('__imul__', (value,))
        return self

DequeManager.register('deque', deque, DequeProxy)


cur_best = d_sol = d_names = None

def init_globals(best, sol, names):
    """ This will be called in each worker process. 

    A global variable (cur_best) will be created in each worker.
    Because it is a multiprocessing.Value, it will be shared
    between each worker, too.

    """
    global cur_best, d_sol, d_names
    cur_best = best
    d_sol = sol
    d_names = names

def calculate(vals):
    global cur_best
    sol = sum(int(x[2]) for x in vals)
    if sol > cur_best.value:
        cur_best.value = sol
        names = [x[0] for x in vals]
        print(", ".join(names) + " = " + str(cur_best.value))
        d_sol.append(cur_best.value)
        d_names.append(names)
    return sol

def process():
    global d_sol, d_names
    cur_best = multiprocessing.Value("I", 0)  # unsigned int

    m = DequeManager()
    m.start()
    d_sol = m.deque(maxlen=9)
    d_names = m.deque(maxlen=9)  

    pool = multiprocessing.Pool(processes=4, initializer=init_globals, 
                                initargs=(cur_best, d_sol, d_names))
    prod = itertools.product([x[2], x[4], x[10]] for x in Data1)
    result = pool.map(calculate, prod)  # map instead of map_async
    pool.close()
    pool.join()
    return result  # Result will be a list containing the value of `sol` returned from each worker call

if __name__ == "__main__":    
    print(process())