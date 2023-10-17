import argparse as argp
from process import Sim, Graph, Astar


class App:
    def __init__(self):
        prsr = argp.ArgumentParser()
        prsr.add_argument('-f', required=True, help='input file path of map data')
        prsr.add_argument('--no_route', action='store_false', help='do not show route on the sim')
        args = prsr.parse_args()

        ld_map = args.f
        self.is_route_show = args.no_route
        ext = ld_map.split('.')[1]
        with open(args.f, 'r') as dta:
            if ext == 'txt':
                self.map_data = [ line.replace('\n', '') for line in dta.readlines() ]

        self.sim:process.sim.Sim = Sim(self.map_data)
        self.graph:process.graph.Graph = Graph(self.map_data)
        self.a_star = Astar()


    def main(self):
        graph:dict = self.graph.create_graph()
        route:list = self.a_star.a_star(graph, self.sim.start, self.sim.goal)
        self.sim.show_graph(route=(route if self.is_route_show else []))


if __name__ == '__main__':
    app = App()
    app.main()

