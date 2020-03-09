#!/usr/bin/env ipython3
# coding: utf-8

# ## 试用pandas＋bokeh分析服务器性能信息

# In[1]:


# 读取csv数据
get_ipython().run_line_magic('matplotlib', 'inline')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['figure.figsize'] = (15, 5)
df = pd.read_csv('sample.csv',header=0,parse_dates=True, index_col='date',                   names=['date','ip','cpuidle','memtotal','memused','rx','tx','rootrate','ioawait','ioutil'])
df.dropna(axis=0)
df[:3]


# In[2]:


#  df的列里面不包括索引列date
df.columns


# In[3]:


# 数据类型
df.dtypes


# In[4]:


df.index[:5]


# In[5]:


# info最后一行显示了df的大小
df.info


# In[6]:


## 加一列内存使用率memutils，存到df3
memutils_df=pd.DataFrame(df['memused']/df['memtotal']*100).round(2)
memutils_df.columns=['memutils']
memutils_df[:5]
df3=pd.merge(df,memutils_df,how='right',left_index=True,right_index=True)


# In[7]:


df3[:3]


# In[8]:


## 单独画一个ip的cpuidle图，用resample改时间间隔重取数据
df.loc[(df['ip']=='192.168.10.171'),['cpuidle']][:5]


# In[9]:


#单个ip的cpuidle曲线图，数据太密了，没法看
df.loc[(df['ip']=='192.168.10.171'),['cpuidle']].plot()

df.loc[(df['ip']=='192.168.10.171' ),['cpuidle']].resample('120min').mean().plot()
df.loc[(df['ip']=='192.168.10.171' ),['cpuidle']].resample('D').mean().plot()
#df.groupby('ip')['cpuidle'].resample('D').mean().groupby('ip').plot()

#用resample重新采样


# In[11]:


#按天采样再画


# In[12]:


## 按ip分组，显示cpuidle变化曲线，只是没法标出label，不大好：（


# In[13]:


##  加上label，语法麻烦点
dfg=df.groupby('ip')['cpuidle'].resample('D').mean().reset_index().set_index('date')
ips=dfg['ip'].unique()
fig, ax = plt.subplots()
for ip in ips:
    dftmp=dfg[(dfg['ip']==ip)]['cpuidle'].reset_index()
    ax.plot(dftmp['date'],dftmp['cpuidle'],label=ip)
    legend = ax.legend(loc='upper right',  fontsize='x-large')

plt.show()


# ### plot用法参考：https://matplotlib.org/3.1.3/api/_as_gen/matplotlib.pyplot.plot.html#matplotlib.pyplot.plot  

# In[14]:


## 把四个用百分比表示的列画在一起，限定ip
df3.loc[(df3['ip']=='192.168.10.171' ),['cpuidle','rootrate','ioutil','memutils']].resample('120min').mean().plot()


# In[15]:




# In[17]:


## bokeh 画图
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.palettes import Spectral10
from bokeh.io import output_notebook, push_notebook
output_notebook()
output_file('example.html')


# ### 官网参考：https://docs.bokeh.org/en/latest/docs/user_guide/interaction/legends.html

# In[18]:


df[:5]


# In[19]:


#单个ip的cpuidle：
grouped=df.loc[(df['ip']=='192.168.10.171' ),['cpuidle']].resample('D').mean().reset_index()
source = ColumnDataSource(grouped)
grouped[:4]


# In[20]:


p = figure(x_axis_type='datetime')
p.line(x='date', y='cpuidle', line_width=2, source=source, legend_label='171')
p.yaxis.axis_label = 'cpuidle'
show(p)


# In[21]:


#所有ip的cpuidle：
ips=df['ip'].unique()
p = figure(x_axis_type='datetime')
i=0
for ip in ips:
    i=i+1
    grouped=df.loc[(df['ip']==ip ),['cpuidle']].resample('D').mean().reset_index()
    source = ColumnDataSource(grouped)
    p.line(x='date', y='cpuidle', line_width=2, source=source, color=Spectral10[i%9], legend_label=ip)

p.yaxis.axis_label = 'cpuidle'
show(p)


# In[22]:


# interactive 交互选择ip或项目，得到相应曲线
from ipywidgets import interact
import numpy as np
from bokeh.io import push_notebook, show, output_notebook
from bokeh.plotting import figure
from bokeh.palettes import brewer
output_notebook()


# In[23]:


def update(ip,item):
    p = figure(x_axis_type='datetime')
    p.yaxis.axis_label = item
    grouped=df.loc[(df['ip']==ip ),[item]].resample('D').mean().reset_index()
    source = ColumnDataSource(grouped)
    p.line(x='date', y=item, line_width=2, source=source, legend_label=ip+item)
    show(p, notebook_handle=True)
    push_notebook()


# In[24]:


interact(update, ip=df['ip'].unique(),  item=df.columns[1:])


# In[25]:


# 加个顔色,和采样周期
from bokeh.palettes import Spectral11

def update(ip,item,per):
    p = figure(x_axis_type='datetime')
    p.yaxis.axis_label = item
    grouped=df3.loc[(df3['ip']==ip ),[item]].resample(per).mean().reset_index()
    source = ColumnDataSource(grouped)
    p.line(x='date', y=item, line_width=2, source=source, color=Spectral11[ips.tolist().index(ip)],legend_label=ip+item)
    show(p, notebook_handle=True)
    push_notebook()

ips=df3['ip'].unique()
period=['5min','15min','60min','120min','D','2D','3D']
interact(update, ip=ips,  item=df3.columns[1:],per=period)


# In[29]:


df3[:5]


# In[34]:


#多图，选择一个ip，显示这个ip的所有数据
#选择采样间隔，数据图跟随变化
from bokeh.palettes import Spectral11
from bokeh.layouts import row
from bokeh.layouts import gridplot

def update(ip,per):
    p = figure(x_axis_type='datetime',plot_width=250, plot_height=250)
    p.yaxis.axis_label = 'cpuidle'
    grouped=df3.loc[(df3['ip']==ip ),['cpuidle']].resample(per).mean().reset_index()
    source = ColumnDataSource(grouped)
    p.line(x='date', y='cpuidle', line_width=1, source=source, color=Spectral11[ips.tolist().index(ip)],legend_label='cpuidle')

    p2 = figure(x_axis_type='datetime',plot_width=250, plot_height=250)
    p2.yaxis.axis_label = 'memutils'
    grouped2=df3.loc[(df3['ip']==ip ),['memutils']].resample(per).mean().reset_index()
    source2= ColumnDataSource(grouped2)
    p2.line(x='date', y='memutils', line_width=1, source=source2, color=Spectral11[ips.tolist().index(ip)],legend_label='memutils')

    p3 = figure(x_axis_type='datetime',plot_width=250, plot_height=250)
    p3.yaxis.axis_label = 'rootrate'
    grouped3=df3.loc[(df3['ip']==ip ),['rootrate']].resample(per).mean().reset_index()
    source3= ColumnDataSource(grouped3)
    p3.line(x='date', y='rootrate', line_width=1, source=source3, color=Spectral11[ips.tolist().index(ip)],legend_label='rootrate')
    
    p4 = figure(x_axis_type='datetime',plot_width=250, plot_height=250)
    p4.yaxis.axis_label = 'iotuil'
    grouped4=df3.loc[(df3['ip']==ip ),['ioutil']].resample(per).mean().reset_index()
    source4= ColumnDataSource(grouped4)
    p4.line(x='date', y='ioutil', line_width=1, source=source4, color=Spectral11[ips.tolist().index(ip)],legend_label='ioutil')
    
    p_rx = figure(x_axis_type='datetime',plot_width=250, plot_height=250)
    p_rx.yaxis.axis_label = 'rx'
    grouped_rx=df3.loc[(df3['ip']==ip ),['rx']].resample(per).mean().reset_index()
    source_rx= ColumnDataSource(grouped_rx)
    p_rx.line(x='date', y='rx', line_width=1, source=source_rx, color=Spectral11[ips.tolist().index(ip)],legend_label='rx')
    
    p_tx = figure(x_axis_type='datetime',plot_width=250, plot_height=250)
    p_tx.yaxis.axis_label = 'tx'
    grouped_tx=df3.loc[(df3['ip']==ip ),['tx']].resample(per).mean().reset_index()
    source_tx= ColumnDataSource(grouped_tx)
    p_tx.line(x='date', y='tx', line_width=1, source=source_tx, color=Spectral11[ips.tolist().index(ip)],legend_label='tx')
    
    #show(row(p,p2,p_rx), notebook_handle=True)
    #show(row(p3,p4,p_tx), notebook_handle=True)
    grid = gridplot([[p, p2,p_rx], [p3,p4, p_tx]], plot_width=250, plot_height=250)
    show(grid, notebook_handle=True)
    push_notebook()

ips=df3['ip'].unique()
period=['5min','15min','60min','120min','D','2D','3D']
interact(update, ip=ips,  per=period)

# make a grid
#grid = gridplot([s1, s2, s3], ncols=2, plot_width=250, plot_height=250)
#grid = gridplot([[s1, s2], [None, s3]], plot_width=250, plot_height=250)
#show(grid)






