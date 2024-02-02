from flask import Flask, render_template, request, jsonify
import json

# Setup
app = Flask(__name__, template_folder='template', static_folder='static')

# Schedule Processing
current_schedule = []
def process_schedule(data):
    global current_schedule
    data = data.decode('utf8').replace("'", '"')
    data = json.loads(data)
    current_schedule = []
    current_schedule += [format_schedule([[data.get("A1"), data.get("B1"), data.get("C1")],
                                     [data.get("A2"), data.get("B2"), data.get("C2")],
                                     [data.get("A3"), data.get("B3"), data.get("C3")],
                                     [data.get("Notes")]])]
    for i in range(1,11):
        current_schedule += [format_schedule([[data.get("{}A1".format(i)), data.get("{}B1".format(i)), data.get("{}C1".format(i))],
             [data.get("{}A2".format(i)), data.get("{}B2".format(i)), data.get("{}C2".format(i))],
             [data.get("{}A3".format(i)), data.get("{}B3".format(i)), data.get("{}C3".format(i))],
             [data.get("{}Notes".format(i))]])]

def format_schedule(res):
    for row in res[:-1]:
        i = -1
        for cell in row:
            i += 1
            if cell.lower().strip() == "x":
                row[i] = "";

    letters = []
    for row in res[:-1]:
        for cell in row:
            for char in cell:
                if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and not char in letters:
                    letters += char

    letters.sort()

    # Check for empty schedules
    if len(letters) == 0:
        # such an efficient if statement i know
        res[0][0] = "N/A"
        res[0][1] = "N/A"
        res[1][0] = "N/A"
        res[1][1] = "N/A"
        res[2][0] = "N/A"
        res[2][1] = "N/A"

        res[3] = [res[3], "N/A", "N/A"]
        return res.copy()


    block1letter = letters[0]
    block2letter = letters[1]
    print(block1letter, block2letter)

    for row in res[:-1]:
        while None in row:
            row.remove(None)
        while "" in row:
            row.remove("")

        # Check row status
        if len(row) == 0:
            row.append("")
            row.append("")
        elif len(row) == 3:
            print("WHAT THE FLIP WHAT THE FUDGE THIS IS VERY BAD ABORT")
        elif len(row) == 1:
            # bruh ( Usually the forbidden AB case >:( )
            culprit = row[0]
            row.remove(culprit)
            # confirm worst fears
            s_type = culprit[-2:]
            if s_type == block1letter + block2letter:
                room = culprit[:-3]
                row.append(room + " " + block1letter)
                row.append(room + " " + block2letter)
            else:
                print("WDYM ITS NOT AN AB!!!! ABORT ABORT ABORT!!!")

    for row in res[:-1]:
        if len(row) != 2 and len(row) != 0:
            # oh noes! abort processing
            print("Processing Aborted")
            return

    if block2letter in res[0][0]:
        res[0] = res[0][::-1]
    res[0][0] = res[0][0][:-2]
    res[0][1] = res[0][1][:-2]

    if "→" in res[1][0]:
        blockA = ["", ""]
        blockB = ["", ""]
        if res[1][0].index(block1letter) < res[1][0].index(block2letter):
            res[1][0] = res[1][0][:-4]
            blockA[0] = res[1][0]
            blockB[1] = res[1][0]

            res[1][1] = res[1][1][:-4]
            blockA[1] = res[1][1]
            blockB[0] = res[1][1]
        else:
            res[1][0] = res[1][0][:-4]
            blockA[1] = res[1][0]
            blockB[0] = res[1][0]

            res[1][1] = res[1][1][:-4]
            blockA[0] = res[1][1]
            blockB[1] = res[1][1]

        res[1][0] = " → ".join(blockA)
        res[1][1] = " → ".join(blockB)
    else:
        if block2letter in res[1][0]:
            res[1] = res[1][::-1]
        res[1][0] = res[1][0][:-2]
        res[1][1] = res[1][1][:-2]


    if block2letter in res[2][0]:
        res[2] = res[2][::-1]
    res[2][0] = res[2][0][:-2]
    res[2][1] = res[2][1][:-2]

    # Fix Empty Schedules
    if res[0][0] == "" and res[0][1] == "" and res[1][0] == "" and res[1][1] == "" and res[2][0] == "" and res[2][1] == "":
        # such an efficient if statement i know
        res[0][0] = "N/A"
        res[0][1] = "N/A"
        res[1][0] = "N/A"
        res[1][1] = "N/A"
        res[2][0] = "N/A"
        res[2][1] = "N/A"

    res[3] = [res[3], block1letter, block2letter]
    return res.copy()


# Handling POST Requests
@app.route('/', methods=['POST'])
def handle_post():
    print("Received a POST!")
    if request.method == 'POST':
        username = request.headers['username']
        password = request.headers['password']
        if username == "pilliam" and password == "TV Timeout (Not the real password, nice try!)":
            data = request.data
            process_schedule(data)
            return "Success!"
            # Do something with the data
        else:
            return "Failure!"

# Handling GET Requests
@app.route('/', methods=['GET'])
def handle_get():
    print("Received a GET!")
    response = jsonify({'body': current_schedule})
    response.headers.add('Access-Control-Allow-Origin', '*')
    print(response)
    return response

# Webapp
@app.route('/')
def index():
    return render_template('index.html')

def run():
    app.run(host='0.0.0.0',port=8080)
