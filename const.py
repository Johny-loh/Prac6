from asyncio import Queue, sleep, get_event_loop, queues
from time import time

TRAIN_MAX_CAPACITY = 400
STATIONS_MAX_CAPACITY = 1000

DELAY = 15
S = 10 ** -3
START = time()

TRAIN_COUNT = 5
TRAIN = '🚋'

HEADER = '  Рокоссовская            Соборная    Кристал      Заречная              Библиотека имени Пушкина'
OFFSET = [11, 19, 26, 34]

STATIONS = {
    1: {'l': {'t': 6, 'q': Queue()}, 'r': {'t': 6, 'q': Queue()}, 'n': 'Рокоссовская'},
    2: {'l': {'t': 6, 'q': Queue()}, 'r': {'t': 2, 'q': Queue()}, 'n': 'Соборная'},
    3: {'l': {'t': 2, 'q': Queue()}, 'r': {'t': 3, 'q': Queue()}, 'n': 'Кристал'},
    4: {'l': {'t': 3, 'q': Queue()}, 'r': {'t': 7, 'q': Queue()}, 'n': 'Заречная'},
    5: {'l': {'t': 7, 'q': Queue()}, 'r': {'t': 7, 'q': Queue()}, 'n': 'Библиотека имени Пушкина'},}

# MEASUREMENT_INTERVAL = 60 * S

number_people_train = []
number_people_stations = []
travel_time = []