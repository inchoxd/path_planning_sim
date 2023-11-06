import argparse as argp
from process import Sim, Graph, Astar


class App:
    def __init__(self):
        prsr = argp.ArgumentParser()
        prsr.add_argument('-f', required=True, help='input file path of map data')
        prsr.add_argument('--no_route', action='store_false', help='do not show route on the sim')
        prsr.add_argument('--no_anime', action='store_false', help='disable animation')
        prsr.add_argument('--no_plus_score', action='store_false', help='disable new feature')
        self.args = prsr.parse_args()

        dta:str = ''
        ext:str = self.args.f.split('.')[1]
        with open(self.args.f, 'r') as dta:
            f_data:list = dta.readlines()
            if ext == 'txt':
                self.map_data = [ line.replace('\n', '') for line in f_data ]
            elif ext == 'pgm':
                size:tuple = tuple([ int(pos) if '\n' not in pos else int(pos.replace('\n', '')) for pos in f_data[2].split(' ') ])
                pxls:list = f_data[4:]
                self.map_data:list = [ [ int(pxl.replace('\n', '')) for line in [ pxls for i in range(size[0] * size[1]) ] for pxl in line ][17*i:17*(i+1)] for i in range(size[1]) ]

        self.sim:process.sim.Sim = Sim(self.map_data)
        self.graph:process.graph.Graph = Graph(self.map_data)
        self.a_star = Astar()


    def main(self):
        graph:dict = self.graph.create_graph(self.args.no_plus_score)
        route:list = self.a_star.a_star(graph, self.sim.start, self.sim.goal)
        self.sim.show_graph(route=route, show_route=(route if self.args.no_route else []), animation=self.args.no_anime)


if __name__ == '__main__':
    app = App()
    app.main()

