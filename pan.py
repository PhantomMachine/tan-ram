from flask import Flask, request, jsonify
import time
import pantilthat

app = Flask(__name__)

pos = (0, 0)
pantilthat.pan(0)
pantilthat.tilt(0)

def pantilt(pan, tilt, steps=100):
    if steps <= 0:
        return

    dx = pan-pos[0]
    dy = tilt-pos[1]

    for step in range(0, steps):
        dstep = step / steps
        pantilthat.pan(pos[0]+dstep*dx)
        pantilthat.tilt(pos[1]+dstep*dy)
        time.sleep(0.02)
    return

def pan_camera(frm, to, step=1):
    global pos
    step = -1 * step if to < frm else step
    for degree in range(frm, to, step):
        # smooth transition from current position to new position
        pantilthat.pan(degree)
        time.sleep(0.02)
    return

@app.route('/position', methods=['GET', 'POST'])
def Pan():
    if request.method == 'GET':
        return jsonify({'pan': pos[0], 'tilt': -pos[1]})
        
    global pos
    # read JSON from body
    pan = request.json['pan']
    tilt = request.json['tilt']

    # validate
    if pan < -90 or pan > 90:
        message = {
            "error": "value out of range. Can only pan -90 to 90 degrees"
        }
        return jsonify(message)

    if tilt < -90 or tilt > 90:
        message = {
            "error": "value out of range. Can only tilt -90 to 90 degrees"
        }
        return jsonify(message)

    tilt = -tilt # note(andrew): implicit -1 multiplication. A positive tilt points the camera towards the table/ground.
    
    # actually do the panning
    pantilt(pan, tilt)
    pos = (pan, tilt)
    # respond
    return jsonify({"message": "Success"})

if __name__ == "__main__":
    app.run(host='127.0.0.1')