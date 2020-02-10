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
import concurrent.futures

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


@app.route('/testA',methods=['GET', 'POST'])
def testA():
    c = int(request.values['count'])
    FIBS = [28, 10, 20, 20, 23, 30, 10, 30]
    result=[]
    print('start')
    with concurrent.futures.ProcessPoolExecutor() as executor:
       for number, fib_value in zip(FIBS, executor.map(fib, FIBS)):
            print("%d's fib number is %d" % (number, fib_value))
    return str(result)

@app.route('/testB',methods=['GET', 'POST'])
def testB():
    c = int(request.values['count'])
    FIBS = [28, 10, 20, 20, 23, 30, 10, 30]
    result=[]
    print('start')
    for i in range(len(FIBS)):
        print('{0}s fib number is {1}'.format(str(FIBS[i]), str(fib(FIBS[i]))))
    return str(result)
    
def fib(n):
    if n < 2:
        return 1
    return fib(n - 1) + fib(n - 2)
