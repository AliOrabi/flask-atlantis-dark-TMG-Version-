# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present TMGROUP
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import folium
import pandas as pd

def find_top_flow(n = 7):

  points_df=pd.read_csv("data/dataset.csv")
  by_point = points_df.groupby('City').sum()[['Points', 'C2 Flow (4-20) (FLOW )', 'C1 Pressure (PRESSURE)']]
  cdf = by_point.nlargest(n, 'Points')[['Points']]
  return cdf


cdf=find_top_flow()
pairs=[(City,Points) for City, Points in zip(cdf.index,cdf['Points'])]



points_df = pd.read_csv("data/dataset.csv")
points_df=points_df[['Lat','Long_','Points']]
points_df=points_df.dropna()

m=folium.Map(location=[30.0561,31.2394],
            tiles='Stamen toner',
            zoom_start=8)

def circle_maker(x):
    folium.Circle(location=[x[0],x[1]],
                 radius= x[2],
                 color="red",
                 popup= 'City:\n' + ('Points:{}').format(x[2])).add_to(m)
points_df.apply(lambda x:circle_maker(x),axis=1)

html_map=m._repr_html_()

@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index', table=cdf, cmap=html_map, pairs=pairs)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
