from passenger import generate_pass
from const import *
from train import Train
import signal
import matplotlib.pyplot as plt
import os

async def task():

    for t in range(TRAIN_COUNT):
        tr = Train(t + 1)
        loop.create_task(tr.crossing())
        trains.put_nowait(tr)
        await sleep(38 * 60 * S / TRAIN_COUNT)

    for st in STATIONS:
        loop.create_task(generate_pass(st))
        await sleep(0)

    loop.create_task(statistic())

async def statistic(mode=1):

    tr = [await trains.get() for _ in range(TRAIN_COUNT)]

    while 1:
        os.system('cls')
        print(f'''Time: {round(time() - START, 2)}''')

        number_people_train.append(0)
        number_people_stations.append(0)
        travel_time.append(0)

        for st in STATIONS:
            if mode:
                number_people_train[-1] += STATIONS[st]['l']['q'].qsize() + STATIONS[st]['r']['q'].qsize()
                print(f'''{STATIONS[st]['n']}: {STATIONS[st]['r']['q'].qsize() + STATIONS[st]['l']['q'].qsize()}''')

            if STATIONS[st]['r']['q'].qsize() + STATIONS[st]['l']['q'].qsize() >= STATIONS_MAX_CAPACITY:
                exit()

            await sleep(0)

        if mode:
            print(HEADER)
            t = 0
            for train in tr:
                if len(train.capacity):
                    measure = train.capacity[-1]

                    for ts in list(STATIONS)[min(measure[0] - 1, measure[1] - 1): max(measure[0] - 1, measure[1] - 1)]:
                        t += STATIONS[ts][measure[2]]['t']

                    travel_time[-1] += t
                else:
                    travel_time[-1] += 8.2

                number_people_stations[-1] += len(train.capacity)

                offset = OFFSET[train.station - 1 - 1 * (train.direction == 'l')] + train.pos * 2
                print(f'''{train.n}:{" " * offset}{TRAIN}''', len(train.capacity))

                await sleep(0)

            number_people_train[-1] /= TRAIN_COUNT
            number_people_stations[-1] /= 5
            travel_time[-1] /= 5

        await sleep(S)

def handler(*args, **kwargs):

    timer = [t / 60 for t in range(len(number_people_stations))]
    plt.plot(timer, number_people_train, 'red')
    plt.plot(timer, number_people_stations, 'blue')
    plt.plot(timer, travel_time, 'purple')
    print(travel_time)
    plt.show()
    exit(0)

signal.signal(signal.SIGINT, handler)
trains = Queue()

loop = get_event_loop()

loop.create_task(task())
loop.run_forever()