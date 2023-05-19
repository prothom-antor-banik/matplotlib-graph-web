from flask import Flask, render_template, request, send_file
from io import BytesIO
import matplotlib.pyplot as plt


app = Flask(__name__)


### Route -> home
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')

    global datapoint
    datapoint = int(request.form.get('datapoint'))

    uid_x = [f"x{i}" for i in range(datapoint)]
    uid_y = [f"y{i}" for i in range(datapoint)]

    return render_template('input.html', datapoint=datapoint, xid=uid_x, yid=uid_y)

### Route -> user input
@app.route('/data', methods=['GET', 'POST'])
def data():
    global x_data, y_data
    x_data, y_data = [], []

    global xlimits, ylimits
    xlimits, ylimits = [], []

    global Title, x_label, y_label
    Title = []
    x_label = []
    y_label = []

    if request.method == 'POST':
        for i in range(datapoint):
            x = request.form.get(f"x{i}").replace(" ", "")
            y = request.form.get(f"y{i}").replace(" ", "")

            x_data.append([eval(i) for i in x.split(',')])
            y_data.append([eval(i) for i in y.split(',')])

        global option
        option = request.form.get('opt')

        return render_template('graph.html')
    else: return None

### Route -> generate graph
@app.route('/graph')
def graph():
    plt.switch_backend("AGG")
    plt.style.use(option)

    if len(xlimits) > 0 and len(ylimits) > 0:
        plt.xlim(xlimits[0], xlimits[1])
        plt.ylim(ylimits[0], ylimits[1])

    if len(Title) and len(x_label) and len(y_label) :
        plt.title(Title[0])
        plt.xlabel(x_label[0])
        plt.ylabel(y_label[0])

    for i in range(datapoint):
        plt.plot(x_data[i], y_data[i], '-o')

    plt.savefig('image.jpg', dpi=1000)

    Title.clear()
    x_label.clear()
    y_label.clear()
    xlimits.clear()
    ylimits.clear()

    img = BytesIO()
    plt.savefig(img, format='jpg')
    img.seek(0)
    return send_file(img, mimetype='img/jpg')

### Route -> adjust axis
@app.route('/axis', methods=['GET', 'POST'])
def axis():
    if request.method == 'GET':
        return render_template('axis.html')
    else:
        xlim = request.form.get('xlimit').replace(" ", "")
        ylim = request.form.get('ylimit').replace(" ", "")

        xlim = [eval(i) for i in xlim.split(',')]
        ylim = [eval(i) for i in ylim.split(',')]

        for i in range(2):
            xlimits.append(xlim[i])
            ylimits.append(ylim[i])

        Title.append(request.form.get('title'))
        x_label.append(request.form.get('x-label'))
        y_label.append(request.form.get('y-label'))

        return render_template('graph.html')

### Route -> download the image
@app.route('/download')
def download():
    return send_file('../image.jpg', as_attachment=True)

### Route -> entering user name
@app.route('/name', methods=['GET', 'POST'])
def name():
    if request.method == 'GET':
        return render_template('name.html', list_user=None)
    else:
        userList = {}

        with open('name.txt', 'r') as file:
            lines = file.read()
            lines = [line for line in lines.split("\n")]
            for line in lines:
                if line == "": continue
                userList[line] = True

        userName = request.form.get('user-name')
        if userName not in userList.keys():
            with open('name.txt', 'a') as file:
                userList[userName] = True
                file.write(userName + "\n")

        userList = list(userList)

        return render_template('name.html', list_user=userList)


if __name__ == '__main__':
    app.run(debug=True, port=8888)
