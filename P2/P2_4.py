# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
import os
import time
import mandelbrot as mb
app = Flask(__name__)

def clean_cache(cache_dir,timespan):
    limit = time.time() - timespan
    for f in os.listdir(cache_dir):
        file_path = os.path.join(cache_dir,f)
        if os.path.getmtime(file_path) < limit:
            os.remove(file_path)
            print("Removing %s"%file_path)

@app.route('/')
def show_mandelbrot(): # Show a Mandelbrot set image
    x1 = request.args.get('x1') or -1
    x2 = request.args.get('x2') or 1
    y1 = request.args.get('y1') or -1
    y2 = request.args.get('y2') or 1
    width = request.args.get('width') or 300
    iters = request.args.get('iters') or 10
    c1 = request.args.get('c1',type=str) or "0-0-0"
    c2 = request.args.get('c2',type=str) or "255-255-0"
    c3 = request.args.get('c3',type=str) or "255-50-0"
    filename = "./static/mandelbrot_cache/f_P_%s_%s_%s_%s_W_%s_I_%s_C1_%s_C2_%s_C3_%s.png" % (x1,x2,y1,y2,width,iters,c1,c2,c3)
    clean_cache("./static/mandelbrot_cache/",86400) # Delete files more than a day older

    if not os.path.isfile(filename):
        c1 = tuple([int(x) for x in c1.split("-")])
        c2 = tuple([int(x) for x in c2.split("-")])
        c3 = tuple([int(x) for x in c3.split("-")])
        mb.renderizaMandelbrotBonito(float(x1),float(y1),float(x2),float(y2),int(width),int(iters),filename,[c1,c2,c3],3)

    return '''  <!DOCTYPE html>
                <head>
                  <link rel="stylesheet" type="text/css" href="/static/style.css">
                </head>
                <html>
                  <body>
                    <img src='%s'>
                  </body>
                </html>
                ''' % filename

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
