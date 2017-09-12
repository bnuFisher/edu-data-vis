from os.path import dirname, join
import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import row, column,widgetbox
from bokeh.models import ColumnDataSource,Legend,HoverTool,LinearAxis,Range1d,LabelSet,Label
from bokeh.models.widgets import Select
from bokeh.plotting import figure
import csv

#limts = 8 sub-categories
COLORS = ['#FF4500','#6666FF','#3CB371','#FFA500','#FF1493','#800080','#808080','#000000']


#set up widgets
DATA_DIR = join(dirname(__file__), 'labels2')

data = join(DATA_DIR,'ylabel.txt')
data_list=open(data,encoding='utf-8').readlines()
data_list = [x.strip() for x in data_list]

universities = join(DATA_DIR,'name.txt')
universities_list = open(universities,encoding='utf-8').readlines()
universities_list = [x.strip() for x in universities_list]

title_list = open(join(DATA_DIR,'plot_title.txt'),encoding='utf-8').readlines()
title_tag1 = title_list[0]
title_tag2 = title_list[1]

Unit_Dir = join(DATA_DIR,'labelUnit.csv')
csvfile = open(Unit_Dir,'r',encoding='gbk')
reader = list(csv.reader(csvfile))
yLabel = [row[0] for row in reader]
yUnit  = [row[1] for row in reader]
secondClass = [row[2] for row in reader]
secondTag   = [row[3] for row in reader]

dic_unit = {lable:unit for lable,unit in zip(yLabel,yUnit)}
dic_second = {first:second for first,second in zip(yLabel,secondClass) if second!= ''}
dic_second_tag = {first:second for first,second in zip(yLabel,secondTag) if second!= ''}


LIS1 = [i.split(',') for i in secondClass if i != '']
full_name = [i for item in LIS1 for i in item]

LIS3 = [i.split(',') for i in secondTag if i != '']
short_name = [i for item in LIS3 for i in item]

dic_tag = {full:short for full,short in zip(full_name,short_name)}

DATA_1 = Select(value=str(data_list[3]),title=str(data_list[0]),options=data_list[3:])
DATA_2 = Select(value=str(data_list[2]),title=str(data_list[1]),options=data_list[2:]) # 

Uni_Name = Select(value=str(universities_list[1]),
				  title=str(universities_list[0]),
				  options=universities_list[1:])


def SetMinMax(df,column):
	minVal = min(df[column])
	maxVal = max(df[column])
	if maxVal > 0:
		maxVal = maxVal * 1.1
	else:
		maxVal = maxVal * 0.9
	if minVal >0:
		minVal = minVal * 0.9
	else:
		minVal = minVal *1.1
	if minVal == maxVal:
		minVal,maxVal = 0,1
	return minVal,maxVal


tools = 'pan,wheel_zoom,reset,resize,save'

def create_figure():

	DATA_csv = join(dirname(__file__), r'time')
	uni_name = Uni_Name.value

	data1 = DATA_1.value
	data2 = DATA_2.value

	if data2 != str(data_list[2]) and data1 != data2:
		df = pd.read_csv(join(DATA_csv,'%s.csv'%uni_name),encoding='gbk',
						 engine='python',usecols=['year',data1,data2]).dropna(axis=0,how='any')

		min1,max1 = SetMinMax(df,data1)
		min2,max2 = SetMinMax(df,data2)
		title  =  uni_name+' - '+ data1 +'  vs  ' + data2 +' - '+title_tag1

	else:
		df = pd.read_csv(join(DATA_csv,'%s.csv'%uni_name),encoding='gbk',engine='python',
						 usecols=['year',data1]).dropna(axis=0,how='any')
		min1,max1 = SetMinMax(df,data1)
		min2,max2 = None,None
		title = uni_name+' - '+ data1 +' - '+title_tag1

	y_axis = list(df[data1])
	x_axis = list(df['year'])
	x_axis = [str(i) for i in x_axis]
	df['year'] = x_axis	

	y_axis = [float(i) for i in y_axis]

	df['text1'] = ['{:.2f}'.format(i)  if float(i) > 1 else '{:.3f}'.format(i)  for i in  list(df[data1])]
	dataSource = ColumnDataSource(df)

	plot = figure(plot_width=1000, plot_height=250,x_range=x_axis,title=title,tools=[tools],toolbar_location="above")
	p1 = plot.line(x_axis,y_axis, line_width=4,line_dash='solid',line_alpha=0.8)
	p2 = plot.circle(x_axis,y_axis,line_width=3,color='#386CB0')

	label1 = LabelSet(x='year', y=data1, text='text1', x_offset=-1, y_offset=6,
					  source=dataSource,text_font_size="0.1pt",
					  text_align='right',text_color='#3288bd')

	plot.add_layout(label1)
	plot = make_up(plot,df,data1,data2,min1,min2,max1,max2,p1,p2)

	return plot


def make_up(plot,df,data1,data2,Min1,Min2,Max1,Max2,p1,p2):
	
	plot.xaxis.axis_label = None
	plot.yaxis.axis_label = data1+dic_unit[data1]
	plot.ygrid.grid_line_alpha = 0.8
	plot.title.text_color = "black"
	plot.title.text_font = "times"
	plot.title.text_font_style = "bold"
	plot.title.text_font_size = "10pt"
	plot.y_range = Range1d(Min1, Max1)
	plot.toolbar.logo=None

	#add right axis
	if  data2 != str(data_list[2]) and data1 != data2:
		#having the same unit
		if dic_unit[data1] == dic_unit[data2]:
			start,end = min(Min1,Min2), max(Max1,Max2)
			plot.y_range = Range1d(start, end)
		else:
			start,end = Min2,Max2
		plot.extra_y_ranges = {"right_axis": Range1d(start=start, end=end)}  
		p3 = plot.line(list(range(1,len(df)+1)), list(df[data2]), line_width=4,alpha=0.8,
					   y_range_name="right_axis",color="#FB8072",line_dash='solid')

		p4 = plot.circle(list(range(1,len(df)+1)), list(df[data2]),
						 line_width=3,y_range_name="right_axis",color="#FB8072")

		plot.add_layout(LinearAxis(y_range_name="right_axis", axis_label=data2+dic_unit[data2]), 'right')
		
		df['text2'] = ['{:.2f}'.format(i)  if float(i) > 1 else '{:.3f}'.format(i)  for i in  list(df[data2])]

		dataSource = ColumnDataSource(df)

		label2 = LabelSet(x='year', y=data2, text='text2', x_offset=-3, y_offset=2,
						  source=dataSource,text_font_size="0.05pt", text_align='right',
						  text_color='#FB8072',y_range_name='right_axis')

		plot.add_layout(label2)

		legend = Legend(items=[
				(data1,[p1,p2]),
				(data2,[p3,p4])
				],location=(0, -30))

		plot.add_layout(legend,'right')
		plot.legend.click_policy="hide"
		plot.legend.label_text_font_size = '10pt'

		return plot
	
	legend = Legend(items=[(data1,[p1,p2]),],location=(0, -30))

	plot.add_layout(legend,'right')
	plot.legend.click_policy="hide"
	plot.legend.label_text_font_size = '10pt'

	return plot


def create_figure2():
	
	if DATA_1.value not in dic_second:

		text = open(join(DATA_DIR,'info_text.txt'),encoding='utf-8').readlines()

		plot = figure(width=1000,height=200,tools='',toolbar_location='left')
		info1 = Label(x=100, y=130,text=text[0],text_font_size='11pt',x_units='screen', y_units='screen',
                 	      border_line_color='white', border_line_alpha=0.1,
                 	      background_fill_color='white', background_fill_alpha=1.0)

		info2 = Label(x=100, y=100,text=text[1],text_font_size='9pt',x_units='screen', y_units='screen',
                 	      border_line_color='white', border_line_alpha=0.1,
                 	      background_fill_color='white', background_fill_alpha=1.0)

		plot.add_layout(info1)
		plot.add_layout(info2)
		plot.toolbar.logo=None

		return plot

	DATA_csv = join(dirname(__file__), r'time')
	uni_name = Uni_Name.value
	data1 = DATA_1.value
	
	lis_second = dic_second[DATA_1.value].split(',')
	lis_second = [i.strip() for i in lis_second]

	lis_second_tag = dic_second_tag[DATA_1.value].split(',')
	lis_second_tag = [i.strip() for i in lis_second_tag]
	
	df_second = pd.read_csv(join(DATA_csv,'%s.csv'%uni_name),encoding='gbk', #文件名不含中文的话用默认的engine即可
				engine='python',usecols=['year']+lis_second).dropna(axis=0,how='any')

	for i,j in zip(lis_second,lis_second_tag):
		df_second[j] = df_second[i]

	dict_for_label = df_second.iloc[-1].to_dict()
	del dict_for_label['year']
	for i in lis_second:
		del dict_for_label[i]

	dict_for_label = sorted(dict_for_label.items(), key=lambda x: x[1],reverse=True)
	hover_text_lis = [i[0] for i in dict_for_label]

	df_second['Year'] = [str(val) for val in df_second['year']]
	text_lis = ["datatext%s"%i for i in range(1,len(lis_second_tag)+1)]
	
	for i,j  in zip(hover_text_lis,text_lis):
		df_second[j] = [str(val) for val in df_second[i]]
	
	title  =  uni_name+' - '+ data1 + ' - ' + title_tag2 + ' - ' + title_tag1
	
	x_axis = df_second['Year'].tolist()

	plot = figure(plot_width=1000,plot_height=250,x_range=x_axis,
		      title=title,tools=tools,toolbar_location="above")
	
	def add_hover():
			datatext = ['@datatext%s'%i for i in range(1,len(hover_text_lis)+1)]
			hover = HoverTool(tooltips=[("Year","@Year")] + [(i,j) for i,j in zip(hover_text_lis,datatext)])
			plot.add_tools(hover)
			
	def make_plot():
		for index,column,color in zip(range(len(lis_second)),hover_text_lis,COLORS):
			source = ColumnDataSource(df_second)
			yield plot.line("Year",column, line_width=4,line_dash='solid',
							color=color,line_alpha=0.8,source=source)

	add_hover()

	legend = Legend(items=[(column,[plot]) for column,plot in zip(hover_text_lis,make_plot())],location=(0,-30))
	
	plot.add_layout(legend,'right')
	
	plot.xaxis.axis_label = None
	plot.xaxis.major_label_orientation = "horizontal"
	plot.yaxis.axis_label = data1+dic_unit[data1]
	plot.legend.click_policy="hide"
	plot.legend.label_text_font_size = '10pt'
	plot.legend.spacing = 6
	plot.title.text_color = "black"
	plot.title.text_font = "times"
	plot.title.text_font_style = "bold"
	plot.title.text_font_size = "10pt"
	plot.toolbar.logo=None
	
	return plot


def update(attr,old,new):
	layout.children[1:3] = create_figure(),create_figure2()


selects = [DATA_1,DATA_2,Uni_Name]
for select in selects:
	select.on_change('value',update) 

#set up layout

lis1 = [DATA_1]
lis2 = [DATA_2]
lis3 = [Uni_Name]

control1 = widgetbox(children=lis1,width=390,sizing_mode='scale_width')
control2 = widgetbox(children=lis2,width=390,sizing_mode='scale_width')
control3 = widgetbox(children=lis3,width=180,sizing_mode='scale_width')

layout = column(row(control1,control2,control3),create_figure(),create_figure2())

curdoc().add_root(layout)
curdoc().title='TimeSeries'
