from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if request.method == 'POST':
        weight = float(request.form['weight'])
        unit = request.form['unit']
        converted_weight = convert_weight(weight, unit)
        return render_template('result.html', weight=weight, unit=unit, converted_weight=converted_weight)

def convert_weight(weight, unit):
    if unit == 'kg':
        return weight * 2.20462  # Convert kg to pounds
    elif unit == 'lbs':
        return weight * 0.453592  # Convert pounds to kg
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
