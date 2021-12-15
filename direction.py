import math

def degree2motor(degree, max, force = 1):
    distvr1 = abs( 45 - degree )
    distvl1 = abs( 135 - degree )
    disthl1 = abs( 225 - degree )
    disthr1 = abs( 315 - degree )
    distvr2 = abs( 360 - distvr1 )
    distvl2 = abs( 360 - distvl1 )
    disthl2 = abs( 360 - disthl1 )
    disthr2 = abs( 360 - disthr1 )
    if distvr1 > distvr2 : distvr1 = distvr2
    if distvl1 > distvl2 : distvl1 = distvl2
    if disthl1 > disthl2 : disthl1 = disthl2
    if disthr1 > disthr2 : disthr1 = disthr2

    return {
        "vr": f(distvr1, max) * force,
        "vl": f(distvl1, max) * force,
        "hl": f(disthl1, max) * force,
        "hr": f(disthr1, max) * force
    }

def f(x, max): 
    return math.floor((max / 180) * x)

def normalize(motor):
    sum = motor["vl"] + motor["vr"] + motor["hl"] + motor["hr"]
    x = math.floor(sum / 4)

    return {
        "vr": motor["vr"] - x,
        "vl": motor["vl"] - x,
        "hl": motor["hl"] - x,
        "hr": motor["hr"] - x
    }