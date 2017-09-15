from os.path import dirname, join
import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import row, column,widgetbox
from bokeh.plotting import figure 
from bokeh.models import ColumnDataSource,Legend,LinearAxis,Range1d,LabelSet
from bokeh.models.widgets import PreText,Select,Slider
from bokeh.models.ranges import FactorRange
from bokeh.models.glyphs import VBar
import csv
from bokeh.settings import settings
import os

#set up widgets

DATA_DIR = join(dirname(__file__), 'labels1')

def returnList(file_dir):
	x_dir = join(DATA_DIR,file_dir)
	x_list = open(x_dir,encoding='utf-8').readlines()
	x_list = [x.strip() for x in x_list]
	return x_list

characters = returnList(file_dir='stats.txt')

yearTag, regionTag, categoryTag,typeTag = characters[1],characters[2],characters[3],characters[4]
dataTag1,countTag1,meanTag1,stdTag1 = characters[5],characters[6],characters[7],characters[8]
dataTag2,countTag2,meanTag2,stdTag2 = characters[9],characters[10],characters[11],characters[12]


data_list = returnList(file_dir='ylabel.txt')
year_list = returnList(file_dir='year.txt')
universities_list = returnList(file_dir='name.txt')
dataLabel_list = returnList(file_dir='DataLabel.txt')

sortLabel_list = returnList(file_dir='sortlabel.txt')
sortCriterion_list = returnList(file_dir='sortCriterion.txt')
uni_num_list = returnList(file_dir='uni_num.txt')


Unit_Dir = join(DATA_DIR,'labelUnit.csv')
csv_unit =  open(Unit_Dir,encoding='gbk')
lis = [i.strip() for i in csv_unit.readlines()]
dic_unit = {i.split(',')[0]:i.split(',')[1] for i in lis}


YEAR = Select(value=year_list[1],title=year_list[0],options=year_list[1:])
DATA_1 = Select(value=data_list[3],title=data_list[0],options=data_list[3:])
DATA_2 = Select(value=data_list[2],title=data_list[1],options=data_list[2:]) # 
LABEL_OPTION = Select(value=dataLabel_list[2],title=dataLabel_list[0],options=dataLabel_list[1:])
SORT_LABEL = Select(value=sortLabel_list[1],title=sortLabel_list[0],options=sortLabel_list[1:])
SORT_CRITERION = Select(value=sortCriterion_list[1],title=sortCriterion_list[0],options=sortCriterion_list[1:])
UNI_NUM = Slider(title=uni_num_list[0],value=10,start=10,end=76,step=10)


stats1 = PreText(text='',width=300,height=38)
stats2 = PreText(text='',width=300,height=38)

tools = 'pan,wheel_zoom,resize,reset,save'


def barPlot_xaxis_university(df_sorted,data1,data2,min1,min2,max1,max2):

	if DATA_2.value == data_list[2]:
		plot_title = YEAR.value + uni_num_list[1] + ' - ' +  DATA_1.value + ' - ' +  uni_num_list[2] + \
			     '(' + SORT_CRITERION.value + ')'  + ' - ' + uni_num_list[3] + ':' + str(UNI_NUM.value)
		df_sorted['dataText1'] =  [str(i) for i in df_sorted[data1]] 
	else:
		plot_title = YEAR.value + uni_num_list[1] + ' - ' +  DATA_1.value + ' vs ' +  DATA_2.value + ' - ' \
			     + uni_num_list[2] +  '(' + SORT_CRITERION.value + ')' +  ' - '\
			     + uni_num_list[3] + ':' + str(UNI_NUM.value)

		df_sorted['dataText1'] =  [str(i) for i in df_sorted[data1]] 
		df_sorted['dataText2'] =  [str(i) for i in df_sorted[data2]] 

	source = None
	if len(df_sorted) == 0: #
		return figure(400,400,tools='')

	elif len(df_sorted) <  10: #adjust the width of the window
		source = ColumnDataSource(df_sorted.to_dict(orient='list'))

		plot = figure(plot_width=750, plot_height=400,
			      x_range=FactorRange(factors=source.data['university']),
			      tools=[tools],title=plot_title)

		plot.vbar(x="university",width=0.3,top=data1,source=source)
		plot.xaxis.major_label_orientation = np.pi/4
		plot.yaxis.axis_label = data1+dic_unit[data1]

	elif len(df_sorted) <  31: #adjust the width of the window 
		
		width=1180 if LABEL_OPTION.value == str(dataLabel_list[2]) else 920
		
		df_sorted['dataText1'] = [str(i) for i in df_sorted[data1]]

		source = ColumnDataSource(df_sorted.to_dict(orient='list'))
		
		plot = figure(plot_width=width, plot_height=400,
					  x_range=FactorRange(factors=source.data['university']),
					  tools=[tools],title=plot_title,)

		plot.vbar(x="university",width=0.3,top=data1,source=source)
		plot.xaxis.major_label_orientation = np.pi/4
		plot.yaxis.axis_label = data1+dic_unit[data1]
	else:
		width= 2880 if LABEL_OPTION.value == str(dataLabel_list[2]) else 1280
		source = ColumnDataSource(df_sorted.to_dict(orient='list'))

		plot = figure(plot_width=width, plot_height=400,
					  x_range=FactorRange(factors=source.data['university']),
					  tools=[tools],title=plot_title)

		plot.vbar(x="university",width=0.3,top=data1,source=source)
		plot.xaxis.major_label_orientation = pd.np.pi / 3
		plot.yaxis.axis_label = data1+dic_unit[data1]

	plot = make_up(plot,df_sorted,data1,data2,min1,min2,max1,max2)
	return plot


#add data-label
def make_up(plot,df_sorted,data1,data2,Min1,Min2,Max1,Max2):

	plot.xaxis.axis_label = None
	plot.ygrid.grid_line_alpha = 0.8
	plot.legend.orientation = "horizontal"
	plot.toolbar_location = 'above'
	plot.toolbar.logo=None
	plot.y_range = Range1d(Min1, Max1)
	plot.xgrid.grid_line_color = None
	plot.ygrid.grid_line_alpha = 0.8
	plot.ygrid.grid_line_dash = [6,4]
	plot.title.text_font_size = '11pt'

	#add right axis
	if data2 != str(data_list[2]) and data1 != data2:
		#having the same unit
		if dic_unit[data1] == dic_unit[data2]:
			start,end = min(Min1,Min2), max(Max1,Max2)
			plot.y_range = Range1d(start, end)
		else:
			start,end = Min2,Max2
		plot.extra_y_ranges = {"right_axis": Range1d(start=start, end=end)}  

		plot.line(list(range(1,len(df_sorted)+1)), list(df_sorted[data2]), line_width=3, alpha=0.8,
				  y_range_name="right_axis",color="red",line_dash='dashed',legend=data2)

		plot.circle(list(range(1,len(df_sorted)+1)), list(df_sorted[data2]), line_width=2, alpha=0.6,
					y_range_name="right_axis",color="red",legend=data2)

		plot.add_layout(LinearAxis(y_range_name="right_axis", axis_label=data2+dic_unit[data2]), 'right') #ok!
		plot.legend.click_policy="hide"

	# add value label
	if LABEL_OPTION.value == str(dataLabel_list[2]):
		df_copy = df_sorted.copy() #key point! 
		df_sorted['text'] = ['{:.1f}'.format(i)  if float(i) > 1 else '{:.3f}'.format(i)
							  for i in  list(df_sorted[data1])]

		dataSource = ColumnDataSource(df_sorted)
		labels = LabelSet(x='university', y=data1, text='text', x_offset=0, y_offset=7,
						  source=dataSource,text_font_size="0.5pt",
						  text_align='center',text_color='#3288bd')

		plot.add_layout(labels)

		if data2 != str(data_list[2]) and data1 != data2:
			df_copy['text2'] = ['{:.1f}'.format(i) if float(i) > 1 else '{:.3f}'.format(i)
								for i in  list(df_copy[data2])]

			dataSource = ColumnDataSource(df_copy)
			labels = LabelSet(x='university', y=data2, text='text2', x_offset=0, y_offset=1,
							  source=dataSource,text_font_size="0.5pt", text_align='center',
							  text_color='black',y_range_name='right_axis')

			plot.add_layout(labels)
			
	return plot


#stats
def Statistics(stats_list1,stats_list2):

	text_info1 = '{dataTag}{dataVal}\n\n{countTag}' \
				 '{countVal}\n\n{meanTag}{meanVal:.3f}\n\n{stdTag}{stdVal:.3f}'.format(
		dataTag=dataTag1,dataVal=DATA_1.value,countTag=countTag1,countVal=int(float(stats_list1[2])),
		meanTag=meanTag1,meanVal=float(stats_list1[4]),stdTag=stdTag1,stdVal=float(stats_list1[6]))

	text_info2 = '{dataTag}{dataVal}\n\n{countTag}{countVal}\n\n{meanTag}' \
		     '{meanVal}\n\n{stdTag}{stdVal}'.format(
		      dataTag=dataTag2,dataVal=str(data_list[2]),countTag=countTag2,countVal=None,
		      meanTag=meanTag2,meanVal=None,stdTag=stdTag2,stdVal=None)

	if stats_list2 != None:
		text_info2 = '{dataTag}{dataVal}\n\n{countTag}{countVal}\n\n{meanTag}' \
			     '{meanVal:.3f}\n\n{stdTag}{stdVal:.3f}'.format(
			      dataTag=dataTag2,dataVal=DATA_2.value,countTag=countTag2,
			      countVal=int(float(stats_list2[2])),meanTag=meanTag2,meanVal=float(stats_list2[4]),
			      stdTag=stdTag2,stdVal=float(stats_list2[6]))
		
		return text_info1,text_info2

	return text_info1,text_info2


#set up plot
def create_figure():

	_year = YEAR.value
	_data_1 = DATA_1.value
	_data_2 = DATA_2.value

	DATA_Dir = join(dirname(__file__), 'data')

	if _data_2 != str(data_list[2]) and _data_1 != _data_2:
		df_copy =  pd.read_csv(join(DATA_Dir,'%stotal.csv'%_year),encoding='gbk',
							        usecols=['university',_data_1,_data_2])
		df_copy = df_copy.drop(df_copy.index[-1])
		min1,max1 = SetMinMax(df_copy,_data_1)
		min2,max2 = SetMinMax(df_copy,_data_2)
		sort_by = _data_1 if SORT_LABEL.value == sortLabel_list[1] else _data_2
		ascending = False if SORT_CRITERION.value == sortCriterion_list[1] else True
		df_sorted = df_copy.sort_values(by=sort_by, axis=0, ascending=ascending)
		df_sorted = df_sorted[:UNI_NUM.value]
	else:
		df_copy = pd.read_csv(join(DATA_Dir,'%stotal.csv'%_year),encoding='gbk',
							       usecols=['university',_data_1])
		df_copy = df_copy.drop(df_copy.index[-1])
		min1,max1 = SetMinMax(df_copy,_data_1)
		min2,max2 = None,None
		ascending = False if SORT_CRITERION.value == sortCriterion_list[1] else True
		df_sorted = df_copy.sort_values(by=_data_1, axis=0, ascending=ascending)
		df_sorted = df_sorted[:UNI_NUM.value]


	stats1.text = str(df_sorted[[_data_1]].describe())
	stats_list1 = list(stats1.text.split())

	stats_list2 = None
	stats1.text, stats2.text = Statistics(stats_list1,stats_list2)

	if DATA_2.value != str(data_list[2]):
		stats2.text = str(df_sorted[[_data_2]].describe())
		stats_list2 = list(stats2.text.split())	
		stats1.text, stats2.text = Statistics(stats_list1,stats_list2)

	plot = barPlot_xaxis_university(df_sorted,_data_1,_data_2,min1,min2,max1,max2)
	
	return plot


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

	return minVal,maxVal


def update(attr,old,new):
	layout.children[1] = create_figure()


selects = [YEAR,DATA_1,DATA_2,LABEL_OPTION,SORT_LABEL,SORT_CRITERION,UNI_NUM]
for select in selects:
	select.on_change('value',update) 


#set up layout
lis1 = [YEAR]
lis5 = [DATA_1]
lis6 = [DATA_2]
lis7 = [LABEL_OPTION]
lis8 = [SORT_LABEL]
lis9 = [SORT_CRITERION]
lis10 = [UNI_NUM]

control1 = widgetbox(children=lis1,width=180,sizing_mode='scale_width')
control5 = widgetbox(children=lis5,width=320,sizing_mode='scale_width')
control6 = widgetbox(children=lis6,width=320,sizing_mode='scale_width')
control7 = widgetbox(children=lis7,width=180,sizing_mode='scale_width')
control8 = widgetbox(children=lis8,width=180,sizing_mode='scale_width')
control9 = widgetbox(children=lis9,width=180,sizing_mode='scale_width')
control10 = widgetbox(children=lis10,width=310,sizing_mode='scale_width')

layout = column(row(column(row(row(control1,control7)),row(row(control8,control9)),row(row(control10))),
		    column(control5,stats1),
		    column(control6,stats2)),
		    create_figure())

curdoc().add_root(layout)
curdoc().title='dataINDEX'
