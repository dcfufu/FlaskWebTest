"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,request
from FlaskWebTest import app
import time
import json
import threading
import random
from queue import Queue

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template('index.html',
        title='Home Page',
        year=datetime.now().year,)

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template('contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.')

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.')

@app.route('/getData',methods=['GET', 'POST'])
def getData():
    #get count value c from request get
    c = int(request.values['count'])

    #Queue
    q = Queue()

    #result list
    datas = []

    #thread list
    threads = []

    #create multi thread to process job and add to Queue
    for i in range(c):
        threads.append(threading.Thread(target = setJob, args = (i,q)))
        threads[i].start()
        
    #whait all of the thread to complete job
    for thread in threads:
        thread.join()

    #get data form queue
    for _ in range(c):
        datas += q.get()

    return json.dumps(datas)

def setJob(count,q):
    temp = []
    temp.append(str(count))
    time.sleep(random.randint(1,5))
    print('{0}*****OK'.format(str(count)))
    q.put(temp)
