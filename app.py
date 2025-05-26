from flask import Flask, jsonify, send_from_directory, request
import scanner

app = Flask(__name__, static_folder='')

@app.route('/')
def serve_index():
    return send_from_directory('', 'index.html')

@app.route('/api/scan')
def api_scan():
    # Get URL parameter from query string
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({'result': 'Error: No URL parameter provided.'})
    try:
        result = scanner.run_scan(target_url)
    except Exception as e:
        result = f"Error running scan: {e}"
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
