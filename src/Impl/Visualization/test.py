from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import math
from Impl.ClusterEngine.DataStructure import DataStructure
import time
import multiprocessing as mp
import numpy as np

class ProcessPlotter(object):
    def __init__(self):
        self.x = []
        self.y = []

    def terminate(self):
        plt.close('all')

    def call_back(self):
        while self.pipe.poll():
            plt.cla()
            L = self.pipe.recv()
            # print("Receiving centers: ", L.centers)
            if L is None:
                self.terminate()
                return False
            else:
                m = Basemap(projection='mill', llcrnrlat=-90, urcrnrlat=90, 
                            llcrnrlon=-180, urcrnrlon=180, resolution='c')
                m.drawcoastlines()
                m.fillcontinents(color='#d1d1d1', lake_color='#FFFFFF')
                m.drawmapboundary(color='#FFFFFF')
                x, y = m([p.x*360/(2*math.pi) for p in L.centers], [p.y*360/(2*math.pi) for p in L.centers])
                objs = m.plot(x, y, 'r.', markersize=5, zorder=pow(2,32))
                for cluster in L.Clusters:
                    x, y = m([p.x*360/(2*math.pi) for p in cluster.points], [p.y*360/(2*math.pi) for p in cluster.points])
                    objs += m.plot(x, y, 'g.', markersize=1, alpha=.5)
                self.fig.canvas.draw()
        self.fig.canvas.draw()
        return True

    def __call__(self, pipe):
        print('starting plotter...')

        self.pipe = pipe
        self.fig, self.ax = plt.subplots()
        timer = self.fig.canvas.new_timer(interval=1000)
        timer.add_callback(self.call_back)
        timer.start()
        print('...done')
        plt.show()


class Plotter(object):
    def __init__(self):
        self.plot_pipe, plotter_pipe = mp.Pipe()
        self.plotter = ProcessPlotter()
        self.plot_process = mp.Process(
            target=self.plotter, args=(plotter_pipe,), daemon=True)
        self.plot_process.start()

    def plot(self, L:DataStructure, finished=False):
        send = self.plot_pipe.send
        if finished:
            send(None)
        else:
            # print("sending centers: ", L.centers)
            send(L)


# if __name__ == '__main__':
#     if plt.get_backend() == "MacOSX":
#         mp.set_start_method("forkserver")
#     main()





# class Plotter():
#     def __init__(self):
#         self.m = Basemap(projection='mill', llcrnrlat=-90, urcrnrlat=90, 
#                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
#         self.m.drawcoastlines()
#         self.m.fillcontinents(color='#d1d1d1', lake_color='#FFFFFF')
#         self.m.drawmapboundary(color='#FFFFFF')

#     def plot(self, L:DataStructure):
#         centers = L.centers
#         x, y = self.m([p.x*360/(2*math.pi) for p in centers], [p.y*360/(2*math.pi) for p in centers])
#         objs = self.m.plot(x, y, 'r.', markersize=5, zorder=pow(2,32))
#         for cluster in L.Clusters:
#             x, y = self.m([p.x*360/(2*math.pi) for p in cluster.points], [p.y*360/(2*math.pi) for p in cluster.points])
#             objs += self.m.plot(x, y, 'g.', markersize=1, alpha=.5)
        
#         plt.title('Geo Plotting')
#         plt.show()
#         for obj in objs:
#             obj.remove()
#         plt.close()
#         return
        
        
