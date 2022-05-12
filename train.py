from const import *

class Train:
    def __init__(self, n):
        self.n = n
        self.station = 1
        self.capacity = []
        self.direction = 'r'
        self.pos = 0

    async def landing(self):
        self.capacity = list(filter(lambda x: x[1] != self.station, self.capacity))
        parking = time()

        while len(self.capacity) < TRAIN_MAX_CAPACITY and (time() - parking < DELAY * S):
            try:
                passenger = STATIONS[self.station][self.direction]['q'].get_nowait()
                self.capacity.append(passenger)
            except queues.QueueEmpty:
                pass

        await sleep((DELAY - (time() - parking)) * S)

    async def crossing(self):
        while 1:
            await self.landing()

            for _ in range(STATIONS[self.station][self.direction]['t'] * 60):
                if _ % 60 == 59:
                    self.pos += 1 - 2 * (self.direction == 'l')
                await sleep(S)

            self.station += 1 - 2 * (self.direction == 'l')
            self.change_direction()

    def change_direction(self):
        if self.station == len(STATIONS):
            self.direction = 'l'

        elif self.station == 1:
            self.direction = 'r'
