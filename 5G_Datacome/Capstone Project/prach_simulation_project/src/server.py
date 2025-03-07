from flask import Flask, request, jsonify, send_from_directory
import prach_simulation
import os

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))  # Use absolute path

@app.route('/')
def home():
    return app.send_static_file('input.html')

@app.route('/run_test', methods=['POST'])
def run_test():
    data = request.get_json()
    loads = data.get('loads', [10, 100, 500])  # Default loads
    results = prach_simulation.run_test_cases(loads)
    prach_simulation.save_results(results, os.path.join(output_dir, "prach_results.json"))
    prach_simulation.generate_graphical_report(results)
    return jsonify({"status": "success"})

@app.route('/results.html')
def results():
    return app.send_static_file('results.html')

@app.route('/PRACH_Success_Rate.html')
def prach_success_rate():
    return app.send_static_file('PRACH_Success_Rate.html')

@app.route('/output/<path:filename>')
def serve_output(filename):
    return send_from_directory(output_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)