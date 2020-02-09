"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
import FlaskWebTest.views
if __name__ == '__main__':
   app.run(threaded=True)