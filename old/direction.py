import math

direction = {
    'right': "right",
    'left': "left",
    'up': "up",
    'down': "down"
}

def direction2spin(x,y,angle, step = 5, quotient = 3):
    quot = math.floor(step / quotient)
    if x == direction['right'] and y == direction['up']   and angle == direction['up']:    return {'vl': quot,  'vr': 0,    'hl': step, 'hr': step}
    if x == direction['right'] and y == direction['up']   and angle == direction['right']: return {'vl': step,  'vr': 0,    'hl': step, 'hr': quot}
    if x == direction['right'] and y == direction['down'] and angle == direction['right']: return {'vl': step,  'vr': quot, 'hl': step, 'hr': 0}
    if x == direction['right'] and y == direction['down'] and angle == direction['down']:  return {'vl': step,  'vr': step, 'hl': quot, 'hr': 0}
    if x == direction['left']  and y == direction['down'] and angle == direction['down']:  return {'vl': step,  'vr': step, 'hl': 0,    'hr': quot}
    if x == direction['left']  and y == direction['down'] and angle == direction['left']:  return {'vl': quot,  'vr': step, 'hl': 0,    'hr': step}
    if x == direction['left']  and y == direction['up']   and angle == direction['left']:  return {'vl': 0,     'vr': step, 'hl': quot, 'hr': step}
    if x == direction['left']  and y == direction['up']   and angle == direction['up']:    return {'vl': 0,     'vr': quot, 'hl': step, 'hr': step}
    return {'vl': 0, 'vr': 0, 'hl': 0, 'hr': 0}

