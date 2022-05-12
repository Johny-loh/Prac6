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
            passenger = await STATIONS[self.station][self.direction]['q'].get()
            self.capacity.append(passenger)

        await sleep((DELAY - (time() - parking)) * S)

    async def crossing(self):
        while 1:
            await self.landing()

            for _ in range(STATIONS[self.station][self.direction]['t']):
                self.pos += 1 - 2 * (self.direction == 'l')
                await sleep(S * 60)

            self.station += 1 - 2 * (self.direction == 'l')
            self.change_direction()

    def change_direction(self):
        if self.station == len(STATIONS):
            self.direction = 'l'

        elif self.station == 1:
            self.direction = 'r'