import pandas as pd
import numpy as np

df_o = pd.read_csv('sample.csv',header=0,parse_dates=True, index_col='date',\
                   names=['date','ip','cpuidle','memtotal','memused','rx','tx','rootrate','ioawait','ioutil'])
df_o.dropna(axis=0)

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
from bokeh.server.server import Server
from bokeh.themes import Theme


def bkapp(doc):
    df = df_o.loc[(df_o['ip']=='192.168.10.171' ),['cpuidle']].copy()
    source = ColumnDataSource(data=df)

    plot = figure(x_axis_type='datetime', y_range=(0, 100), y_axis_label='Cpuidle',
                  title="Cpuidle 10.171")
    plot.line('date', 'cpuidle', source=source)

    def callback(attr, old, new):
        if new == 0:
            data = df
        else:
            data = df.rolling('{0}min'.format(new)).mean()
        source.data = ColumnDataSource.from_df(data)

    slider = Slider(start=5, end=1440, value=5, step=5, title="Smoothing by N minute")
    slider.on_change('value', callback)

    doc.add_root(column(slider, plot))

    doc.theme = Theme(filename="theme.yaml")

# Setting num_procs here means we can't touch the IOLoop before now, we must
# let Server handle that. If you need to explicitly handle IOLoops then you
# will need to use the lower level BaseServer class.
server = Server({'/': bkapp}, num_procs=4)
server.start()

if __name__ == '__main__':
    print('Opening Bokeh application on http://localhost:5006/')

    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()
