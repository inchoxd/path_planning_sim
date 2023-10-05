import argparse as argp
from process import Sim


class App:
    def __init__(self):
        prsr = argp.ArgumentParser()
        prsr.add_argument('-f', required=True)
        args = prsr.parse_args()

        ld_map = args.f
        ext = ld_map.split('.')[1]
        with open(args.f, 'r') as dta:
            if ext == 'txt':
                self.map_data = [ line for line in dta.readlines() ]

        self.sim:process.sim.Sim = Sim(self.map_data)


if __name__ == '__main__':
    App()
