from os.path import dirname,join
import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import row,column,widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import PreText,Select,MultiSelect,Slider,Paragraph
from bokeh.plotting import figure
from bkcharts import Donut
import csv

#set up widgets
#loading data
DATA_DIR = join(dirname(__file__), 'labels3')
DATA_CSV = join(dirname(__file__),'data')

def returnList(file_dir):
	x_dir = join(DATA_DIR,file_dir)
	x_list = open(x_dir,encoding='utf-8').readlines()
	x_list = [x.strip() for x in x_list]
	return x_list

year_list = returnList(file_dir='year.txt')
uni_list =  returnList(file_dir='name.txt')

#used for create_figure_individually
info0    =  returnList(file_dir='textInfo0.txt')
title_for_DATA   = info0[0]
yearTitle     = info0[1]
dataTitle     = info0[0]
subclassTitle = info0[2]
universityTitle = info0[3]
dataUnit1      = info0[4]
missing_data   = info0[5]
missing_data_2 = info0[6]

#used for create_figure_interschool
info1  = returnList(file_dir='textInfo1.txt')
baseTitle = info1[0]
other_universities = info1[1]
universityName     = info1[2]
dataUnit2          = info1[3]
dataLabel2         = info1[4]

switch_list = returnList(file_dir='switch.txt')
rangeSlider_list = returnList(file_dir='rangeSlider.txt')
sort_list = returnList(file_dir='sortCriterion.txt')
title_list = returnList(file_dir='plotTitle.txt')

plot_title_part0 = title_list[0] 
plot_title_part1 = title_list[1] 
etc              = title_list[2]
plot_title_part2 = title_list[3]
plot_title_part3 = title_list[4]
plot_title_part4 = title_list[5]
plot_title_part5 = title_list[6]

weizhi = sort_list[4]
Fetch1 = sort_list[5]

DATA_label = join(DATA_DIR,'dataTotal.csv')
csvfile = open(DATA_label,'r',encoding="gbk")
reader = list(csv.reader(csvfile))
ydata = [row[0] for row in reader]
ydata_second  = [row[2] for row in reader]
ydata_second_tag = [row[3] for row in reader]
second_data_dict = {i:j for i,j in zip(ydata,ydata_second)}
second_dataTag_dic = {i:j for i,j in zip(ydata,ydata_second_tag)}

YEAR = Select(value=year_list[1],title=str(year_list[0]),options=year_list[1:])
DATA = Select(value=ydata[0],title=title_for_DATA,options=ydata)
SWITCH = Select(value=switch_list[1],title=switch_list[0],options=switch_list[1:])
Sorting = Select(value=sort_list[1],title=sort_list[0],options=sort_list[1:3])
Sort_slider = Slider(title=sort_list[3],value=5,start=5,end=15,step=5)
MULTI_SELECT = MultiSelect(title='',value=[uni_list[1]],options=uni_list[1:],size=20)

stats0 = PreText(text='',width=250,height=90)
stats1 = PreText(text='',width=250,height=90)

text = returnList('text.txt')
text = ''.join(line for line in text)

paragraph = Paragraph(text = text,width=380,sizing_mode='fixed')
tools = 'pan,wheel_zoom,resize,reset,save'
width,height= 480,450


def sub_list(sublist):
	for item in sublist:
		yield '{item}\n\n'.format(item=item)

def statistics_inner(data_value,sublist_title,sublist_value):
	
	text_info0 = '\n{yearTitle}{yearVal}\n\n{dataTitle}\n\n{dataValue}\n\n'.\
		format(yearTitle=yearTitle,yearVal=YEAR.value,dataTitle=dataTitle,dataValue=DATA.value)

	text_info0 = text_info0 + ''.join(sub_list(sublist_title))

	text_info1 = '\n{universityTitle}{universityVal}\n\n{dataUnit1}\n\n{data}\n\n'.\
		         format(universityTitle=universityTitle,universityVal=MULTI_SELECT.value[0],
						dataUnit1=dataUnit1,data=data_value)

	text_info1 = text_info1 + ''.join(sub_list(sublist_value))

	return text_info0,text_info1


def statistics_inter(data_value,sublist_university,sublist_value):
	text_info0 = '\n{yearTitle}{yearVal}\n\n{universityName}\n\n{universityTotal}\n\n'.\
		format(universityTotal=baseTitle,yearTitle=yearTitle,
			   yearVal=YEAR.value,universityName=universityName)
	text_info0 = text_info0 + ''.join(sub_list(sublist_university))
	text_info1 = '\n{dataUnit2}{data_tag}\n\n{dataLabel2}\n\n{dataValue}\n\n'.\
		format(dataUnit2=dataUnit2,dataLabel2=dataLabel2,dataValue=data_value,data_tag=DATA.value)
	text_info1 = text_info1 + ''.join(sub_list(sublist_value))

	return text_info0,text_info1


def statistics_inter_sorting(data_value,sublist_university,sublist_value):	
	text_info0 = '\n{yearTitle}{yearVal}\n\n{sortTag}:{sortCriterion}\n\n{universityName}' \
				 '\n\n{universityTotal}\n\n'.format(universityTotal=baseTitle,yearTitle=yearTitle,
				  yearVal=YEAR.value,universityName=universityName,
				  sortTag=sort_list[0],sortCriterion=Sorting.value)
	sublist_university = [str(index) + '.' + university for index,university in
						  zip(range(1,Sort_slider.value+1),sublist_university)]
	sublist_university.append(other_universities)
	text_info0 = text_info0 + ''.join(sub_list(sublist_university))
	text_info1 = '\n{dataUnit2}{data_tag}\n\n{Fetch_decending} {num} {weizhi}\n\n' \
				 '{dataLabel2}\n\n{dataValue}\n\n'.format(dataUnit2=dataUnit2,
				  dataLabel2=dataLabel2,dataValue=data_value,data_tag=DATA.value,
				  Fetch_decending=Fetch1,num=Sort_slider.value,weizhi=weizhi)
	text_info1 = text_info1 + ''.join(sub_list(sublist_value))
	return text_info0,text_info1


def append_to_df(data):
	second_data_list = second_data_dict[data].split(',')
	return second_data_list

def find_tags(data):
	second_dataTag_list = second_dataTag_dic[data].split(',')
	return second_dataTag_list


def create_figure_individul():

	data_value = DATA.value
	year = YEAR.value
	append_list = append_to_df(data_value)
	data_tags   = find_tags(data_value)
	df = pd.read_csv(join(DATA_CSV,'%stotal.csv'%year),encoding='gbk',
					 engine='python',usecols=['university',data_value]+append_list)
	university = MULTI_SELECT.value[0]
	df = df.loc[df['university'] == university]
	null_set = {i for item in  pd.isnull(df.values) for i in item}
	df_col = df[append_list]
	values = [val for item in df_col.values for val in item]
	data_value_for_text = (df[data_value].iloc[0])
	dic_for_sorting = {col:val for col,val in zip(data_tags,values)}
	dic_for_text    = {col:val for col,val in zip(append_list,values)}
	sorted_tuple = sorted(dic_for_sorting.items(), key=lambda d: d[1],reverse=True)
	sorted_tuple_text = sorted(dic_for_text.items(), key=lambda d: d[1],reverse=True)
	df_col = [i[0] for i in sorted_tuple] 
	df_col_for_text =  [i[0] for i in sorted_tuple_text]  # for stats_text
	values = [i[1] for i in sorted_tuple]
	values_percent = [i/sum(values) for i in values]
	valPercent_for_text = [("{:1}".format(val)+" ({:.2%})".format(per)) for val,per in
							zip(values,values_percent)]

	stats0.text,stats1.text = statistics_inner(data_value_for_text,df_col_for_text,valPercent_for_text)
	count = [i if i<0.01 else 0 for i in values_percent]
	tag_count = '{:.2%}'.format(sum(count))

	for val,index in zip(values_percent,range(len(df_col))):
		if val < 0.01:
			df_col[index] = '***  ' + tag_count
		else:
			df_col[index] = df_col[index] + "  {:.2%}".format(val)

	data_pie = pd.Series(values,index=df_col)
	title = str(YEAR.value) + plot_title_part0 + ' - '+ \
		    university + ' - ' + DATA.value + ' - ' + plot_title_part1

	pie_chart = Donut(data_pie,width=width,height=width,tools=tools,toolbar_location="right",
			  		  text_font_size='0.01pt',title=title,hover_tool=False)

	pie_chart.toolbar.logo=None
	pie_chart.outline_line_alpha = 0

	return pie_chart


def create_figure_interSchool():
	
	data_value = DATA.value
	year = YEAR.value
	universities = MULTI_SELECT.value # a list

	df = pd.read_csv(join(DATA_CSV,'%stotal.csv'%year),
					 encoding='gbk',engine='python',usecols=['university',data_value])
	baseTitle_info2 = baseTitle 
	baseSeries = df.loc[df['university'] == baseTitle_info2]
	basevalue = baseSeries[data_value].iloc[0]
	basevalue = '{:2}'.format(basevalue)
	df = df[df['university'].isin(universities)] #isin, fliter multiple rows by a value
	index_list_for_pie = list(df['university'])
	value_list_for_pie = list(df[data_value])
	dic_for_text = {university:value for university,value in
					zip(index_list_for_pie,value_list_for_pie)}
	
	if baseTitle in dic_for_text:
		del dic_for_text[baseTitle]
	
	sorted_dic_for_text = sorted(dic_for_text.items(), key=lambda d: d[1],reverse=True)
	tags_for_text   =  [i[0] for i in sorted_dic_for_text] 
	values_for_text =  ['{:.1f}'.format(i[1]) for i in sorted_dic_for_text]
	tags_for_plot   = tags_for_text   + [other_universities]
	values_for_plot = [float(i) for i in values_for_text + [basevalue]]
	values_for_plot[-1] = '{:1f}'.format(values_for_plot[-1] - sum(values_for_plot[:-1]))
	values_for_plot[-1] = float(values_for_plot[-1])
	percent_for_plot = ['{:.4f}'.format(i/sum(values_for_plot)) for i in values_for_plot]
	percent_for_text = ['{:.2%}'.format(float(i)) for i in percent_for_plot]

	tuple_for_text =sorted([(val,per,tag) for val,per,tag in
			       zip(values_for_plot,percent_for_text,tags_for_plot)],reverse=True)

	sublist_university = [item[2] for item in tuple_for_text]
	sublist_value      = [str(item[0]) + ' ' + '('+str(item[1]) + ')' for item in tuple_for_text]

	count = [float(i) if float(i) < 0.01 else 0 for i in percent_for_plot]
	tag_count = '{:.2%}'.format(sum(count))

	for index,val in zip(range(len(tags_for_plot)),percent_for_plot):
		if float(val) < 0.01:
			tags_for_plot[index] = '***  ' + tag_count
		else:
			tags_for_plot[index] = tags_for_plot[index] + "  {:.2%}".format(float(val))

	tags_university = [i.split()[0] for i in tags_for_plot]
	tags_percent    = [i.split()[1] for i in tags_for_plot]
	tags_value      = [float(i) for i in percent_for_plot]
	tags_university = [i+ ' ' +j for i,j in zip(tags_university,tags_percent)]
	tags_num = list(range(1,len(tags_university)+1))
	tags_num[-1] = 0

	for index in range(len(tags_value)):
		if tags_value[index] < 0.01:
			tags_num[index] = 100

	dic_for_pie =  {'university':tags_university,'num':tags_num,'value':tags_value}

	stats0.text,stats1.text = statistics_inter(basevalue,sublist_university,sublist_value)
	df_pie = pd.DataFrame(dic_for_pie)
	title = str(YEAR.value) + plot_title_part0 + ' - '+ MULTI_SELECT.value[1] + etc +' - ' \
			+ DATA.value + ' - ' + plot_title_part2

	pie_chart = Donut(df_pie,label=['num','university'],values='value',
			  		  width=width,height=height,tools=tools,toolbar_location="right",
			  		  text_font_size='0.01pt',title=title,hover_tool=False)
	
	pie_chart.toolbar.logo=None
	pie_chart.outline_line_alpha = 0

	return pie_chart


def create_figure_interSchool_sorting():
	data_value = DATA.value
	year = YEAR.value

	df = pd.read_csv(join(DATA_CSV,'%stotal.csv'%year),encoding='gbk',engine='python',
		             usecols=['university',data_value])

	baseSeries = df.loc[df['university'] == baseTitle]
	basevalue = baseSeries[data_value].iloc[0]
	basevalue = '{:2}'.format(basevalue)

	if Sorting.value ==sort_list[1]:
		df = df.sort_values(by=DATA.value,ascending=False)
		df = df[:Sort_slider.value+1]
	else:
		df = df.sort_values(by=DATA.value,ascending=True)
		df_last = df[-1:]
		df_last = df_last.append(df[:Sort_slider.value]) 
		df = df_last
	
	university_list = df['university'].tolist()
	university_list.append(other_universities)
	value_list      = df[DATA.value].tolist()
	value_list.append(float('{:.1f}'.format(value_list[0] - sum(value_list[1:]))))
	tags_university = [i for i in university_list[1:]]
	tags_percent_digital  = [i/value_list[0] for i in value_list[1:]]
	tags_percent = ['{:.1%}'.format(i/value_list[0]) for i in value_list[1:]]
	tags_university_for_plot = [i + ' ' + j for i,j in zip(tags_university,tags_percent)]
	tags_university_for_text = tags_university[:]
	tags_percent_for_text = tags_percent[:]
	tags_num = [i for i in range(1,len(tags_university)+1)]
	tags_num[-1] = 0

	count = [i if i<0.01 else 0 for i in tags_percent_digital]
	tag_count = '{:.2%}'.format(sum(count))

	for val,index in zip(tags_percent_digital,range(len(tags_university))):
		if val < 0.01:
			tags_university_for_plot[index] = '***  ' + tag_count

	tags_value = [i for i in value_list[1:]]

	for index in range(len(tags_num)):
		if tags_percent_digital[index] < 0.01:
			tags_num[index] = 100

	dic_for_pie =  {'university':tags_university_for_plot,'num':tags_num,'value':tags_value}

	df_pie = pd.DataFrame(dic_for_pie)

	sublist_value = [str(i)+' '+ '('+ j + ')' for i, j in zip(tags_value,tags_percent_for_text)]
	stats0.text,stats1.text = statistics_inter_sorting(basevalue,tags_university_for_text,sublist_value)

	title = str(YEAR.value) + plot_title_part0 + ' - '+ plot_title_part3 + ' - ' \
			 + DATA.value + ' - ' + plot_title_part4 + plot_title_part5
	pie_chart = Donut(df_pie,label=['num','university'],values='value',
				      width=width,height=height,tools=tools,toolbar_location="right",
				      text_font_size='0.01pt',title=title,hover_tool=False)

	pie_chart.toolbar.logo=None
	pie_chart.outline_line_alpha = 0
	
	return pie_chart


def create_figure():
	if SWITCH.value == switch_list[2]:
		plot = create_figure_interSchool_sorting()
	else:	
		if len(MULTI_SELECT.value) == 1:
			plot = create_figure_individul()
		else:
			plot = create_figure_interSchool()
	return plot


def update(attr,old,new):
	layout1.children[3].children[0] = create_figure()

selects = [YEAR,DATA,MULTI_SELECT,SWITCH,Sorting,Sort_slider]

for select in selects:
	select.on_change('value',update) 

lis2 = [YEAR]
lis3 = [DATA]
lis4 = [SWITCH]
lis5 = [Sorting]
lis6 = [Sort_slider]

control1 = widgetbox(MULTI_SELECT ,width=240,sizing_mode='scale_both')
control2 = widgetbox(children=lis2,width=250,height=10,sizing_mode='scale_both')
control3 = widgetbox(children=lis3,width=250,height=10,sizing_mode='scale_both')
control4 = widgetbox(children=lis4,width=240,height=10,sizing_mode='scale_both')
control5 = widgetbox(children=lis5,width=240,height=10,sizing_mode='scale_both')
control6 = widgetbox(children=lis6,width=240,height=10,sizing_mode='scale_both')

layout1 =  row(column(control1,control4,control5,control6),
	       column(control2,stats0),
	       column(control3,stats1),
	       column(create_figure(),paragraph))

curdoc().add_root(layout1)
curdoc().title='ratioAnalysis'