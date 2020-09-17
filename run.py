from Scraper import app

if __name__ == '__main__':
    app.run(host='192.168.0.23', port=5500, debug=True, threaded=True)