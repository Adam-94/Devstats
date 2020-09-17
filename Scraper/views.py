from flask import Flask, render_template, jsonify, session, url_for
from flask import request, send_file, make_response, Response, send_from_directory
from bs4 import BeautifulSoup
from Scraper import app, tasks

import json
import os

@app.route('/')
def index():
      return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
      return send_from_directory(os.path.join(app.root_path, 'static'),
                                 'favicon.ico', mimetype='B:\\Desktop\\Programming\\Indeed Scraper V2\\Scraper\\static\\favicon.ico')

@app.route('/logo')
def logo():
      return send_from_directory(os.path.join(app.root_path, 'static'),
                                 'logo.png', mimetype='B:\\Desktop\\Programming\\Indeed Scraper V2\\Scraper\\static\\logo.png')

@app.route('/city_selection', methods=['POST'])
def get_city():
      if request.method == 'POST':
            print('Incoming...')
            selections = request.get_json()
            city = selections['options'][0]
            stats = selections['options'][1]
            print('City', selections['options'][0])
            print('Stats', selections['options'][1])
            chart_data = tasks.get_statistics(stats, city)
      return jsonify(chart_data)