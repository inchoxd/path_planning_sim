import argparse as argp
from process import Sim, Graph


class App:
    def __init__(self):
        prsr = argp.ArgumentParser()
        prsr.add_argument('-f', required=True)
        args = prsr.parse_args()

        ld_map = args.f
        ext = ld_map.split('.')[1]
        with open(args.f, 'r') as dta:
            if ext == 'txt':
                self.map_data = [ line.replace('\n', '') for line in dta.readlines() ]

        self.sim:process.sim.Sim = Sim(self.map_data)
        self.graph:process.graph.Graph = Graph(self.map_data)


    def main(self):
        graph = self.graph.create_graph()
        self.sim.show_graph()


if __name__ == '__main__':
    app = App()
    app.main()

