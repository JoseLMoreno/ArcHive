from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import sys, pickle
class GUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        self.setWindowTitle('Archive')
        self.socket = None
        self.centralWidget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.centralWidget)
        selection = Selection(self)
        selection.button[0].clicked.connect(self.Agent0)
        selection.button[1].clicked.connect(self.Agent1)
        self.centralWidget.addWidget(selection)
    
    def SetSocket(self,Socket):
        self.socket = Socket

    def Agent0(self, thing):
        self.socket.send(str(len("Sparse Agent")).encode())
        self.socket.send("Sparse Agent".encode())
        info_widget = AgentInfo(self)
        self.centralWidget.addWidget(info_widget)
        self.centralWidget.setCurrentWidget(info_widget)
        readSize = int(self.socket.recv(sys.getsizeof(int)))
        chunk = self.socket.recv(readSize)
        while (sys.getsizeof(chunk) < readSize):
            chunk += self.socket.recv(readSize)
        history = pickle.loads(chunk)
        info_widget.plot(history)
    
    def Agent1(self, thing):
        self.socket.send(str(len("QTable Agent")).encode())
        self.socket.send("QTable Agent".encode())
        info_widget = AgentInfo(self)
        self.centralWidget.addWidget(info_widget)
        self.centralWidget.setCurrentWidget(info_widget)
        readSize = int(self.socket.recv(sys.getsizeof(int)))
        chunk = self.socket.recv(readSize)
        while (sys.getsizeof(chunk) < readSize):
            chunk += self.socket.recv(readSize)
        history = pickle.loads(chunk)
        info_widget.plot(history)

class Selection(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Selection, self).__init__(parent)
        self.setWindowTitle('Agent Selection')
        self.layout = QtWidgets.QVBoxLayout()
        self.button= []
        self.button.append(QtWidgets.QPushButton('Sparse Agent'))
        self.button.append(QtWidgets.QPushButton('QTable Agent'))
        for buttons in self.button:
            self.layout.addWidget(buttons)
        self.setLayout(self.layout)

class AgentInfo(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AgentInfo, self).__init__(parent)
        self.title = 'ArcHive'
  
        self.setWindowTitle(self.title)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        # self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.show()

    def plot(self, history):
        score = []
        length = []
        wins = []
        avg10games = []
        avgwin = []
        for games in history:
            score.append(games[5])
            length.append(games[6])
            if games[4] == 0:
                wins.append(0)
            elif games[4] == 1:
                wins.append(100)
            else:
                wins.append(50)
        for index,games in enumerate(wins):
            if index < 10:
                avg10games.append(sum(wins[index:index + 10])/10)
            elif index > len(wins)-10:
                avg10games.append(sum(wins[index-10:index])/10)
            else:
                avg10games.append(sum(wins[index-5:index+5])/len(wins[index-5:index+5]))
            if len(wins[:index]):
                avgwin.append(sum(wins[:index])/len(wins[:index]))


        # for games in history:
        #     data.append(games[4])
        plots = self.figure.subplots(nrows=2,ncols=2)
        self.figure.tight_layout()
        for row in plots:
            for column in row:
                column.clear()
   
        plots[0][0].plot(score, '*-', label = "Score", color="red")
        plots[0][0].legend(loc='best')
        plots[0][1].plot(length, '.-', label = "Frames Per Game", color="green")
        plots[0][1].legend(loc='best')
        plots[1][0].plot(avg10games, '--', label = "Average win percentage over 10 games", color="blue")
        plots[1][0].legend(loc='best')
        plots[1][1].plot(avgwin, '--', label = "Average win percentage overall", color="purple")
        plots[1][1].legend(loc='best')

        self.canvas.draw()
