from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    weight = float(request.form['weight'])
    from_unit = request.form['from_unit']
    to_unit = request.form['to_unit']

    if from_unit == 'kg' and to_unit == 'lbs':
        converted_weight = weight * 2.20462
    elif from_unit == 'lbs' and to_unit == 'kg':
        converted_weight = weight / 2.20462
    else:
        converted_weight = weight

    return render_template('index.html', weight=weight, from_unit=from_unit, to_unit=to_unit, converted_weight=converted_weight)

if __name__ == '__main__':
    app.run(debug=True)
