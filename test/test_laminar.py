from multiprocessing import Queue, Process, cpu_count

from context import laminar
from context import laminar_examples as le


def test_converter():
    queue = Queue()

    def sum_func(sum_list):
        return sum(sum_list)

    laminar.__converter("test12", sum_func, [2, 4, 6, 8], queue, [], {})

    q = queue.get()

    assert q[0] == "test12"
    assert q[1] == 20


def test_iter_flow():
    result = laminar.iter_flow(le.single_total, le.laminar_df['Col1'])

    assert result == {
                        'data[0-5]': 17,
                        'data[12-17]': 60,
                        'data[18-23]': 86,
                        'data[24-29]': 115,
                        'data[30-34]': 105,
                        'data[35-39]': 120,
                        'data[40-44]': 135,
                        'data[6-11]': 37,
                        }

    def sum_func(sum_list):
        return sum(sum_list)

    short_list = [1, 2, 3]

    result = laminar.iter_flow(sum_func, short_list, cores=4)

    assert result == {
                        'data[2-2]': 3,
                        'data[0-0]': 1,
                        'data[1-1]': 2
                        }

    result = laminar.iter_flow(sum_func, short_list, cores=9)

    assert result == {
                        'data[2-2]': 3,
                        'data[0-0]': 1,
                        'data[1-1]': 2
                        }

def test_list_flow():
    result = laminar.list_flow(le.single_total, [le.laminar_df[col] for col in le.laminar_df.columns])

    assert result == {
                        'data_position_0': 675,
                        'data_position_1': 1800,
                        'data_position_2': 2925,
                        }

    def sum_func(sum_list):
        return sum(sum_list)

    multi_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    result = laminar.list_flow(sum_func, multi_list, cores=9)

    assert result == {
                        'data_position_0': 6,
                        'data_position_1': 15,
                        'data_position_2': 24
                        }
