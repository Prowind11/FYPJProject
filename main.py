from flask import Flask

import sap_hana_data as data

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

    
if __name__ == '__main__':
    app.run(debug=True)
