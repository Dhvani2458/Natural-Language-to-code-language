from flask import Flask, render_template, request, jsonify
from compiler import generate_code

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    user_input = data.get("code", "")
    
    try:
        output = generate_code(user_input)
        return jsonify({"success": True, "output": output})
    except Exception as e:
        return jsonify({"success": False, "output": str(e)})

if __name__ == '__main__':
    app.run(debug=True)