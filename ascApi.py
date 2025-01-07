from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/')
@app.route('/top10', methods=['GET'])
def get_events():
    with open('top10.json') as f:
        events = json.load(f)
    return jsonify(events)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8000, debug=True)

