import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)
xAxisStart = -10
xAxisEnd = 10
yAxisStart = -10
yAxisEnd = 10
ax.set_xlim(xAxisStart, xAxisEnd)
ax.set_ylim(yAxisStart, yAxisEnd)

trailorW = 2
trailorH = 1
headW = 0.5
headH = 0.5
startPointX = -5
startPointY = -8
lineW = 0.2
lineH = 0.5

assert startPointX >= xAxisStart, "The start point is out of the x axis. Try to change the inputs"
assert startPointY >= yAxisStart, "The start point is out of the y axis. Try to change the inputs"

totalLength = trailorW + lineW + headW
assert (totalLength + startPointX) < xAxisEnd, "The vehicle is out of the x axis. Try to change the inputs"

totalHeight = trailorH
assert (totalHeight + startPointY) < yAxisEnd, "The vehicle is out of the y axis. Try to change the inputs"

middleOfTrailor = (trailorH / 2) + startPointY

trailor = plt.Rectangle((startPointX, startPointY), trailorW, trailorH, fc='r')
plt.gca().add_patch(trailor)

line = plt.Line2D(((trailorW + startPointX), (trailorW + startPointX + lineW)), (middleOfTrailor, middleOfTrailor),
                  lineH)
plt.gca().add_line(line)

yPositionForHead = (trailorH / 2) - (headH / 2) + startPointY
rectangle2 = plt.Rectangle((trailorW + startPointX + lineW, yPositionForHead), headW, headH, fc='r')
plt.gca().add_patch(rectangle2)

plt.show()