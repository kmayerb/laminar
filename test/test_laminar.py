from multiprocessing import Queue, Process, cpu_count

from context import laminar
from context import laminar_examples as le


def test_converter():
    queue = Queue()

    laminar.__converter("test12", lambda x: sum(x), [2, 4, 6, 8], queue)

    q = queue.get()
    print(q)
    assert q[0] == "test12"
    assert q[1] == 10
