#
# NB I know nothing about seeds or farms -- this is just
# a rough sketch of how a farming simulation might work!
#
import os
import csv
import pickle
import time

class Seed:
    """Seed - a seed which grows at a particular rate
    """

    def __init__(self, name, growth_rate, ready_for_harvest_cm):
        self.name = name
        self.growth_rate = float(growth_rate)
        self.ready_for_harvest_cm = float(ready_for_harvest_cm)
        self.current_size = 0
        self.condition = "Seed"

    def grow(self, sunlight_lumens, rain_cm, temperature_celsius):
        """Grow for one turn

        Crudely, we just multiply the factors together and add that
        to the size. Obviously should do something more sophisticated!

        Keep track of what status we're in by checking our current size
        (This could be used to change what image is on display)
        """
        growth_spurt = sunlight_lumens * rain_cm * temperature_celsius * self.growth_rate
        self.current_size += growth_spurt
        if self.current_size > self.ready_for_harvest_cm:
            self.condition = "Overripe"
        elif self.current_size == self.ready_for_harvest_cm:
            self.condition = "Ripe"
        elif 0 < self.current_size < self.ready_for_harvest_cm:
            self.condition = "Growing"
        elif self.current_size == 0:
            self.condition = "Seed"
        else:
            raise RuntimeError("Shouldn't get here!")


class Farm:

    def __init__(self):
        self.seeds = {}
        self.planted = []
        with open("seeds.csv", newline="") as f:
            for row in csv.reader(f):
                name, growth_rate, ready_for_harvest_cm = row
                self.seeds[name] = Seed(name, growth_rate, ready_for_harvest_cm)

    def plant(self, seed_name, quantity):
        seed = self.seeds[seed_name]
        for n in range(quantity):
            self.planted.append(seed)

    def show_status(self):
        for planted in self.planted:
            print("%s - %s (%scm)" % (planted.name, planted.condition, planted.current_size))

    def run(self):
        while True:
            self.show_status()
            for p in self.planted:
                p.grow(1, 1, 1)
            time.sleep(1)

if __name__ == '__main__':
    SAVED_FILENAME = "farm.saved"
    if os.path.exists(SAVED_FILENAME):
        with open(SAVED_FILENAME, "rb") as f:
            farm = pickle.loads(f.read())
    else:
        farm = Farm()
        farm.plant("Turnip", 12)
        farm.plant("Barley", 10)

    try:
        farm.run()
    except KeyboardInterrupt:
        with open(SAVED_FILENAME, "wb") as f:
            f.write(pickle.dumps(farm))

