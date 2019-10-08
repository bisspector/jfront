from app import app
from flask import jsonify, render_template, request, Response
import math
from app import alg

def formRJSON(message: str, status: int):
    return jsonify({
        "status": status,
        "message": message
    })

A_uav = alg.DroneAlgo()

@app.route("/api/v1/sendUavInfo")
def sendUavInfo():
    inp = request.get_json()
    
    try:
        global battery
        global photo

        angle, height, ratio, ov_ratio = inp[0], inp[1], inp[2], inp[3] 
        battery, photo = inp[4], inp[5]

        A_uav.lx = (2 * height * math.tan(angle / 360 * 3.1415926))
        A_uav.ly = A_uav.lx / ratio
        A_uav.lx *= (1 - ov_ratio)
        A_uav.ly *= (1 - ov_ratio)

        return formRJSON(A_uav.lx, 200)
    except:
        return formRJSON("Invalid Input", 400)

@app.route("/api/v1/sendUavHomeLoc")
def sendUavHomeLoc():
    location = request.get_json()

    try:
        A_uav.get_dps(location)
        return formRJSON(location, 200)
    except:
        return formRJSON("Invalid Input", 400)

@app.route("/api/v1/sendUavProblem")
def sendUavProblem():
    inp = request.get_json()
    
    try:
        A_uav.points = inp
        print(A_uav.points)
        A_uav.get_distance()
        A_uav.solve()
        can = 1
        if A_uav.cur_ans / 1000 * photo > battery:
            can = 0
        data = []
        print(A_uav.ans_points)
        data.append(A_uav.ans_points)
        data.append(can)
        print(data)

        return formRJSON(data, 200)
    except:
        return formRJSON("Invalid Input", 400)

@app.route("/")
def index():
    return render_template("index.html")
