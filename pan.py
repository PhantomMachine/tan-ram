from flask import Flask, request, jsonify
import time
import pantilthat

app = Flask(__name__)

pos = 0
pantilthat.pan(0)
pantilthat.tilt(0)

def pan_camera(frm, to, step=1):
    global pos
    step = -1 * step if to < frm else step
    for degree in range(frm, to, step):
        # smooth transition from current position to new position
        pantilthat.pan(degree)
        time.sleep(0.02)
    return

@app.route('/pan', methods=['POST'])
def Pan():
    global pos
    # read JSON from body
    content = request.json
    print(content['pan'])
    pan = content['pan']
    # validate
    if pan < -90 or pan > 90:
        message = {
            "error": "value out of range. Can only pan -90 to 90 degrees"
        }
        return jsonify(message)
    
    # actually do the panning
    pan_camera(pos, pan)
    pos = pan
    # respond
    return jsonify({"message": "Success"})

if __name__ == "__main__":
    app.run(host='127.0.0.1')
