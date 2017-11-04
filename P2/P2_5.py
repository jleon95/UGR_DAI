# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
import random as r
app = Flask(__name__)

@app.route('/')
def show_svg():
    rnd_list = [str(r.randint(1,80)) for x in range(11)]
    color_list = ["black","blue","yellow","gold","lawngreen","royalblue","chocolate","slategrey","plum","peru","lightpink"]
    r.shuffle(color_list)
    rectangle = '<rect x="{}%" y="{}%" width="{}%" height="{}%" stroke="{}" stroke-width="5" style="fill:{}" />'.format(*rnd_list[0:4],color_list[0],color_list[1])
    circle = '<circle cx="{}%" cy="{}%" r="{}%" stroke="{}" stroke-width="5" style="fill:{}" />'.format(rnd_list[4],rnd_list[5],str(int(rnd_list[6])/4),color_list[2],color_list[3])
    ellipse = '<ellipse cx="{}%" cy="{}%" rx="{}%" ry="{}%" stroke="{}" stroke-width="5" style="fill:{}"/>'.format(rnd_list[7],rnd_list[8],str(int(rnd_list[9])/4),str(int(rnd_list[10])/4),color_list[4],color_list[5])
    return '''
            <?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
                {}
                {}
                {}
            </svg>
            '''.format(rectangle,circle,ellipse)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
