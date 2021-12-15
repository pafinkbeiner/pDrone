import math

# Params: 
# x -> gyro x => -16000 < x < 16000
# y -> gyro y => -16000 < y < 16000
# base -> Calibrated base position of gyro
# max -> maximal delta possible

# 1. Get Distances 
# 2. Distances to motor drehzahl delta
# 4. return delta
# 3. Normalize motor drehzahl delta (after from direction)
def correct(x,y,base, max):
    distx = abs(base["x"] - x)
    disty = abs(base["y"] - y)

    dist = {
        "vl": 0,
        "vr": 0,
        "hl": 0,
        "hr": 0
    }

    # calc x achse
    if x < base["x"]: 
        # drone to the right
        dist.update({
            "vr": distx,
            "hr": distx
        })
    else: 
        # drone to the left
        dist.update({
            "vl": distx,
            "hl": distx
        })
    # cals y achse
    if y < base["y"]:
        # drone to the front
        dist.update({
            "vr": disty,
            "vl": disty
        })
    else:
        # drone to the back
        dist.update({
            "hr": disty,
            "hl": disty
        })

    return {
        "vl": f(dist["vl"], max),
        "vr": f(dist["vr"], max),
        "hl": f(dist["hl"], max),
        "hr": f(dist["hr"], max)
    }

# todo exponential formular for smoother stabilisation
def f(x, max):
    return math.floor((max/16000) * x)

