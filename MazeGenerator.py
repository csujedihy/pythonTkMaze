import Tkinter
import tkMessageBox
import random

class UnionFind():
    def __init__(self, m, n):
        self.dad = [i for i in xrange(0, m*n)]
        self.rank = [0 for i in xrange(0, m*n)]
        self.m = m
        self.n = n
    
    def find(self, x):
        dad = self.dad
        if dad[x] != x:
            dad[x] = self.find(dad[x])
        return dad[x]
    
    def union(self, xy):
        dad = self.dad
        rank = self.rank
        x, y = map(self.find, xy)
        if x == y:
            return False
        if rank[x] > rank[y]:
            dad[y] = x
        else:
            dad[x] = y
            if rank[x] == rank[y]:
                rank[y] += 1
        return True

class Maze(object):
    def __init__(self, mazeWidth, mazeHeight, canvasWidth, canvasHeight):
        self.mazeWidth, self.mazeHeight = mazeWidth, mazeHeight
        self.canvasWidth, self.canvasHeight = canvasWidth, canvasHeight
        self.cellWidth, self.cellHeight = canvasWidth / mazeWidth, canvasHeight / mazeHeight
        self.maze = None
        self.top = Tkinter.Tk()
        self.pad = pad = 5
        windowWidth = self.top.winfo_screenwidth()
        windowHeight = self.top.winfo_screenheight()
        self.canvas = Tkinter.Canvas(self.top, bg="white", height=canvasHeight + pad, width=canvasWidth + pad)
        self.canvas.pack()

    def generateMaze(self):
        m = self.mazeHeight
        n = self.mazeWidth
        uf = UnionFind(m, n)
        maze = [[15] * n for _ in xrange(0, m)]
        directions = [("u", -1, 0), ("d", 1, 0), ("l", 0, -1), ("r", 0, 1)]
        for i in xrange(0, m):
            for j in xrange(0, n):
                random.shuffle(directions)
                for d, di, dj in directions:
                    newi, newj = i + di, j + dj
                    if 0 <= newi < m and 0 <= newj < n:
                        if uf.union((i*n + j, newi * n + newj)):
                            if d == "u":
                                maze[i][j] &= 7
                                maze[newi][newj] &= 13
                            elif d == "d":
                                maze[i][j] &= 13
                                maze[newi][newj] &= 7
                            elif d == "l":
                                maze[i][j] &= 14
                                maze[newi][newj] &= 11
                            elif d == "r":
                                maze[i][j] &= 11
                                maze[newi][newj] &= 14
                            else:
                                return "error"
                            break
        self.maze = maze
        return self.maze
    
    def displayMazeByChar(self):
        if not self.maze:
            return
        maze = self.maze

        m = len(maze)
        n = len(maze[0])
        for i in xrange(0, m):
            up = ""
            down = ""
            mid = ""

            for j in xrange(0, n):
                up += " "
                down += " "
                if maze[i][j] & 8:
                    up += "-"
                else:
                    up += " "
                    
                if maze[i][j] & 2:
                    down += "-"
                else:
                    down += " "
                    
                if maze[i][j] & 1:
                    mid += "|"
                else:
                    mid += " "
                mid += " "
            if maze[i][-1] & 4:
                mid += "|"
                    
            print "".join(up)
            print "".join(["".join(d) for d in mid])
            print "".join(down)

    def displayMaze(self):
        if not self.maze:
            return
        maze = self.maze
        canvas = self.canvas
        pad = self.pad
        m = len(maze)
        n = len(maze[0])
        for i in xrange(0, m):
            for j in xrange(0, n):
                topLineY = i * self.cellHeight + pad
                botLineY = (i + 1) * self.cellHeight + pad
                startX = j * self.cellWidth + pad
                endX = (j + 1) * self.cellWidth + pad
                if maze[i][j] & 8:
                    canvas.create_line(startX, topLineY, endX, topLineY)
                if maze[i][j] & 2:
                    canvas.create_line(startX, botLineY, endX, botLineY)
                if maze[i][j] & 1:
                    canvas.create_line(startX, topLineY, startX, botLineY)
                if maze[i][j] & 4:
                    canvas.create_line(endX, topLineY, endX, botLineY)

        self.top.mainloop()

maze = Maze(10, 10, 800, 800)
maze.generateMaze()
maze.displayMazeByChar()
