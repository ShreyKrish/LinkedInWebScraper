from flask import Flask, render_template, request
from scraper import perform_scrape  # Import the scraper function
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    job_type = request.form['job_type']
    keywords = request.form['keywords']
    try:
        results = perform_scrape(job_type, keywords)
        return render_template('results.html', results=results)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
