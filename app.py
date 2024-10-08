import sys
import argparse as argp
import PySimpleGUI as sg
from process import Sim, Graph, Astar


class App:
    def __init__(self):
        prsr = argp.ArgumentParser()
        prsr.add_argument('-f', required=True, help='input file path of map data')
        prsr.add_argument('-s', required=True, help='input pos of start')
        prsr.add_argument('-g', required=True, help='input pos of goal')
        prsr.add_argument('--no_app', action='store_false', help='do not run application mode')
        prsr.add_argument('--no_route', action='store_false', help='do not show route on the sim')
        prsr.add_argument('--no_anime', action='store_false', help='disable animation')
        prsr.add_argument('--no_plus_score', action='store_false', help='disable new feature')
        
        if len(sys.argv) <= 1:
            self.WIDTH:int = 1600
            self.HEIGHT:int = 900

            left_frame = sg.Frame('', [[sg.Text('test')], [sg.Canvas(size=(self.WIDTH*(2/3), self.HEIGHT), key='-CANVAS-', background_color='#FFFFFF')]], size=(self.WIDTH*(2/3), self.HEIGHT), relief=sg.RELIEF_FLAT)
            right_frame = sg.Frame('', [[sg.Text('test')], [sg.Canvas(size=(self.WIDTH*(1/3), self.HEIGHT), key='-CANVAS-', background_color='#FFFFFF')]], size=(self.WIDTH*(1/3), self.HEIGHT), relief=sg.RELIEF_FLAT)

            layout:list = [[left_frame, right_frame]]
            self.window:PySimpleGUI.PySimpleGUI.Window = sg.Window('path_planning_sim', layout, size=(self.WIDTH, self.HEIGHT))

        if len(sys.argv) > 1:
            self.args = prsr.parse_args()

            dta:str = ''
            ext:str = self.args.f.split('.')[1]
            start:tuple = tuple([ int(p) for p in self.args.s.split(',') ])
            goal:tuple = tuple([ int(p) for p in self.args.g.split(',') ])

            with open(self.args.f, 'r') as dta:
                f_data:list = dta.readlines()
                if ext == 'txt':
                    self.map_data = [ line.replace('\n', '') for line in f_data ]
                elif ext == 'pgm' and f_data[0].replace('\n', '') == 'P2':
                    size:tuple = tuple([ int(s) for s in f_data[2].replace('\n', '').split(' ') ])
                    pxls:list = f_data[4:]
                    self.map_data:list = [ [ int(pxl.replace('\n', '')) for line in [ pxls for i in range(size[0] * size[1]) ] for pxl in line ][size[0]*i:size[0]*(i+1)] for i in range(size[1]) ]
                else:
                    print('\033[31m[ERROR]\033[0m INVALID FILE TYPE!')
                    sys.exit(1)

            self.sim:process.sim.Sim = Sim(self.map_data, start, goal)
            self.graph:process.graph.Graph = Graph(self.map_data)
            self.a_star = Astar()


    def main(self):
        if len(sys.argv) > 1:
            graph:dict = self.graph.create_graph(self.args.no_plus_score)
            route:list = self.a_star.a_star(graph, self.sim.start, self.sim.goal)

            if self.args.no_app == False:
                self.sim.show_graph(route=route, show_route=self.args.no_route, animation=self.args.no_anime, graph=(graph if self.args.no_anime and self.args.no_plus_score else self.graph.create_graph(not self.args.no_plus_score) if self.args.no_anime and not self.args.no_plus_score else {}), mode=self.args.no_plus_score)
        if len(sys.argv) <=1 or self.args.no_app:
            event:str = ''
            values:list = []

            while True:
                event, values = self.window.read()
                if event == sg.WIN_CLOSED:
                    break



if __name__ == '__main__':
    app = App()
    app.main()
