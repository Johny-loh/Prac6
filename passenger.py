from const import *
from random import choices

# class Passenger:
#     def __init__(self, start, end, dir):
#         self.start = start
#         self.end = end
#         self.dir = dir

async def generate_pass(stat):
    coefficients = [0.25 * (stat != st) for st in STATIONS.keys()]

    while True:
        if time() - START > 19 * 60 * S:
            station = choices(list(STATIONS.keys()), coefficients)[0]

            direction = 'r'
            if station < stat:
                direction = 'l'

            await STATIONS[stat][direction]['q'].put([stat, station, direction])
            await sleep(S)