import math


def perpendicular_coords(aX, aY, bX, bY, length):
    vX = bX - aX
    vY = bY - aY

    if vY == 0:
       return aX, aY - length, bX, bY - length, bX, bY + length, aX, aY + length

    if vX == 0:
       return aX - length, aY, bX - length, bY, bX + length, bY, aX + length, aY

    mag = math.sqrt(vX * vX + vY * vY)
    vX = vX / mag
    vY = vY / mag
    temp = vX
    vX = 0 - vY
    vY = temp
    cX = bX + vX * length
    cY = bY + vY * length
    dX = bX - vX * length
    dY = bY - vY * length

    c1X = aX + vX * length
    c1Y = aY + vY * length
    d1X = aX - vX * length
    d1Y = aY - vY * length
    return [(int(cX), int(cY)), (int(dX), int(dY)), (int(d1X), int(d1Y)), (int(c1X), int(c1Y))]
