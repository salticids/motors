import graphics as g
def main():
    win = g.GraphWin('Stator Tooth', 100, 100)
    l1 = g.Line(g.Point(0, 0), g.Point(10, 10))
    c = g.Circle(g.Point(50, 50), 50)
    c.draw(win)
    win.getMouse()
    win.close()


main()
