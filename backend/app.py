from flask import Flask, request, jsonify
from main import perform_scrape  # Ensure your main.py file has perform_scrape function

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    job_type = data['job_type']
    keywords = data['keywords']
    results = perform_scrape(job_type, keywords)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/test', methods=['GET'])
def test():
    return jsonify([
        ("Software Engineer Intern", "https://example.com"),
        ("Data Scientist Intern", "https://example.com")
    ])

