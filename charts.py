import random

from bokeh.embed import components
from bokeh.plotting import figure


def create_figure(rows):
    dates = []
    totals = []
    for row in rows:
        dt, total = row
        dates.append(dt)
        totals.append(total)

    # Creating Plot Figure
    p = figure(
        x_range=dates,
        height=330,
        title="Aplicações nos últimos 7 dias",
        sizing_mode="stretch_width",
        y_range=(0, max(totals)),
    )

    # Defining Plot to be a Vertical Bar Plot
    p.vbar(x=dates, top=totals, width=0.5)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    return p