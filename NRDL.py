# -*- coding: UTF-8 -*-
import numpy as np
import chardet
import pandas as pd
import calendar
import datetime
import time
import re
from chart_func import *
from data_func import *
import seaborn as sns

plt.rcParams.update(plt.rcParamsDefault)

from matplotlib.font_manager import FontProperties
myfont=FontProperties(fname=r'C:\Windows\Fonts\simhei.ttf',size=14)
sns.set(font=myfont.get_name())
mpl.rcParams['axes.unicode_minus'] = False

pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 5000)

df = pd.read_excel(open('2017医保目录新进分子.xlsx', 'rb'), sheet_name='Raw Data')  #从Excel读取数
df.index = df['通用名']


df_value = df.filter(regex=("Value.*"))
df_volume = df.filter(regex=("Volume.*"))
tsValue = tsMatrix(df_value)
tsVolume = tsMatrix(df_volume)
df_value.columns = df_value.columns.str[-4:]
df_volume.columns = df_volume.columns.str[-4:]
df_price = df_value/df_volume
df_price.replace([np.inf, -np.inf], np.nan, inplace=True)
df['单价'] = df_price.mean(axis=1)

df1 = pd.read_excel(open('降价品种销售表现.xlsx', 'rb'), sheet_name='Raw Data')  #从Excel读取数
df1.index = df1['通用名']
df1_value = df1.filter(regex=("Value.*"))
df1_volume = df1.filter(regex=("Volume.*"))
tsValue1 = tsMatrix(df1_value)
tsVolume1 = tsMatrix(df1_volume)


# 总体销售趋势双柱状图
df_total_value = df_value.sum().to_frame('销售额')
df_total_value = df_total_value/1000000000
df_total_value.index = df_total_value.index.str[-4:]
df_total_volume = df_volume.sum().to_frame('销售量')
df_total_volume = df_total_volume/1000000
df_total_volume.index = df_total_volume.index.str[-4:]
title_text = ['医保新列名品种总体销售额趋势', '医保新列名品种总体销售量趋势']
print(df_total_value.iloc[:,0])
plot_dual_bar(df1=df_total_value, df2=df_total_volume,savefile='plots/医保新列名品种总体销售趋势（季度）.png',
          xlabelrotation=90, ylabelperc=False,
          title=title_text, ytitle=['季度销售额（十亿）','季度销售量（百万）'])


# # 总体销售净增长双柱状图
# df_total_value = df_value.sum().diff(periods=4).to_frame('销售额')
# df_total_value = df_total_value/1000000000
# df_total_value.index = df_total_value.index.str[-4:]
# df_total_volume = df_volume.sum().diff(periods=4).to_frame('销售量')
# df_total_volume = df_total_volume/1000000
# df_total_volume.index = df_total_volume.index.str[-4:]
# title_text = ['医保新列名品种总体销售额净增长趋势', '医保新列名品种总体销售量净增长趋势']
# print(df_total_value.iloc[:,0])
# plot_dual_bar(df1=df_total_value, df2=df_total_volume,savefile='plots/医保新列名品种总体销售净增长趋势（季度）.png',
#           xlabelrotation=90, ylabelperc=False,
#           title=title_text, ytitle=['季度销售额净增长（十亿）','季度销售量净增长（百万）'])
#
#
# # 总体销售增长率趋势折线图
# df_total_value_gr = tsValue.toTotalGR()
# df_total_volume_gr = tsVolume.toTotalGR()
# df_total_gr = pd.concat([df_total_value_gr,df_total_volume_gr],axis=1)
# df_total_gr.dropna(how='all', inplace=True)
# df_total_gr.columns = ['销售额\n增长率', '销售量\n增长率']
# title_text = '医保新列名品种总体销售增长率趋势（季度）'
# plot_line(df=df_total_gr,savefile='plots/'+title_text+'.png',
#           xlabelrotation=90, ylabelperc=True,
#           title=title_text, ytitle='同比增长率')
#
# # 医保新列名品种分治疗大类销售额增长率趋势
# df_value_grouped = df.filter(regex=("Value.*")).groupby(df['治疗大类']).sum().sort_values('Value18Q3', ascending=False)
# df1 = tsMatrix(df_value_grouped).toGR()
# title_text = '医保新列名品种分治疗大类销售额增长率趋势（季度）'
# plot_line(df=df1.T,savefile='plots/'+title_text+'.png',
#           xlabelrotation=90, ylabelperc=True,
#           title=title_text, ytitle='同比增长率')
#
# #医保新列名后净增长Top10品种
# df2 = tsValue.toBaseDiff(head=10)/1000000
# print(df2)
# title_text = '医保新列名后净增长Top10品种'
# plot_line(df=df2.T,savefile='plots/'+title_text+'.png', width=14, height=8,
#           xlabelrotation=0, ylabelperc=False, colorscheme='loop',hasLabel=False,
#           title=title_text, ytitle='销售额净增长（vs 17Q1, 百万元）')
#
# #医保新列名后净增长Bottom10品种
# df2 = tsValue.toBaseDiff(head=10, sort_ascending=True)/1000000
# print(df2)
# title_text = '医保新列名后净增长Bottom10品种'
# plot_line(df=df2.T,savefile='plots/'+title_text+'.png', width=14, height=8,
#           xlabelrotation=0, ylabelperc=False, colorscheme='loop', hasLabel=False,
#           title=title_text, ytitle='销售额净增长（vs 17Q1, 百万元）')
#
# #医保新列名后净增长Top10品种
# df2 = tsValue.toBaseGR(head=10)
# print(df2)
# title_text = '医保新列名后增长率Top10品种'
# plot_line(df=df2.T,savefile='plots/'+title_text+'.png', width=14, height=8,
#           xlabelrotation=0, ylabelperc=True, colorscheme='loop',hasLabel=False,
#           title=title_text, ytitle='销售额增长率（vs 17Q1, %）')
#
# #医保新列名后净增长Bottom10品种
# df2 = tsValue.toBaseGR(head=10, sort_ascending=True)
# print(df2)
# title_text = '医保新列名后增长率Bottom10品种'
# plot_line(df=df2.T,savefile='plots/'+title_text+'.png', width=14, height=8,
#           xlabelrotation=0, ylabelperc=True, colorscheme='loop',hasLabel=False,
#           title=title_text, ytitle='销售额增长率（vs 17Q1, %）')
#
#
# #分布图
# latest_value_GR = tsValue.toGR().iloc[:,-1] - tsValue.toGR().iloc[:,-7]
# latest_value_GR.dropna(inplace=True)
# latest_value_Diff = tsValue.toDiff().iloc[:,-1]
# sns.distplot(latest_value_GR, color="m")
# plt.show()
#
# # 进医保后销售额净增长和单价的关系
# value_baseDiff = tsValue.toBaseDiff().iloc[:,-1]
# df2 = pd.concat([np.log(value_baseDiff),np.log(df['单价']),df['治疗大类'],df_value.iloc[:,-1]],axis=1)
# df2.columns = ['log(进入医保后销售额净增长)', 'log(单价)', '治疗大类', '销售额规模']
# print(df2)
#
# fig = plt.figure(figsize=(14,9))
# colors = iter(['navy', 'teal', 'crimson', 'darkorange', 'darkgreen', 'sienna', 'olivedrab',
#                'deepskyblue', 'pink', 'purple', 'dimgray', 'orchid', 'saddlebrown', ])
# sns.set(style='white', font='simhei')
#
# ax = sns.scatterplot(x='log(单价)', y='log(进入医保后销售额净增长)',
#                      hue='治疗大类', size='销售额规模',
#                      sizes=(100, 3000), palette = colors, legend='brief',
#                      data=df2)
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,frameon=False, labelspacing=1.5)
# plt.savefig('plots/进医保后销售额净增长和单价的关系.png',
#             format='png', bbox_inches='tight', transparent=True, dpi=600)
#
#
# # 进医保后销售额增长率和单价的关系
# value_baseGR = tsValue.toBaseGR().iloc[:,-1]
# df2 = pd.concat([np.log(value_baseGR),np.log(df['单价']),df['治疗大类'],df_value.iloc[:,-1]],axis=1)
# df2.columns = ['log(进入医保后销售额增长率)', 'log(单价)', '治疗大类', '销售额规模']
# print(df2)
#
# fig = plt.figure(figsize=(14,9))
# colors = iter(['navy', 'teal', 'crimson', 'darkorange', 'darkgreen', 'sienna', 'olivedrab',
#                'deepskyblue', 'pink', 'purple', 'dimgray', 'orchid', 'saddlebrown', ])
# sns.set(style='white', font='simhei')
#
# ax = sns.scatterplot(x='log(单价)', y='log(进入医保后销售额增长率)',
#                      hue='治疗大类', size='销售额规模',
#                      sizes=(100, 3000), palette = colors, legend='brief',
#                      data=df2)
#
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,frameon=False, labelspacing=1.5)
# plt.savefig('plots/进医保后销售额增长率和单价的关系.png',
#             format='png', bbox_inches='tight', transparent=True, dpi=600)
#
# # 医保新列名品种分治疗大类销售额净增长趋势
# df_value_grouped = df.filter(regex=("Value.*")).groupby(df['治疗大类']).sum().sort_values('Value18Q3', ascending=False)
# df2 = tsMatrix(df_value_grouped).toBaseDiff()/1000000
# title_text = '医保新列名品种分治疗大类净增长'
# plot_line(df=df2.T, savefile='plots/'+title_text+'.png', width=14, height=8,
#           xlabelrotation=0, ylabelperc=False, colorscheme='loop', hasLabel=False,
#           title=title_text, ytitle='销售额净增长（vs 17Q1, 百万元）')
#
# # 医保新列名品种分治疗大类销售额增长率趋势
# df_value_grouped = df.filter(regex=("Value.*")).groupby(df['治疗大类']).sum().sort_values('Value18Q3', ascending=False)
# df2 = tsMatrix(df_value_grouped).toBaseGR()
# title_text = '医保新列名品种分治疗大类增长率'
# plot_line(df=df2.T, savefile='plots/'+title_text+'.png', width=14, height=8,
#           xlabelrotation=0, ylabelperc=True, colorscheme='loop', hasLabel=False,
#           title=title_text, ytitle='销售额增长率（vs 17Q1, %）')
#
# #医保非谈判新列名品种 versus 谈判品种 销售额增长率趋势（季度）
# df_total_value_gr = tsValue.toTotalGR()
# df_total_value_gr1 = tsValue1.toTotalGR()
# df_total_gr = pd.concat([df_total_value_gr, df_total_value_gr1],axis=1)
# df_total_gr.dropna(how='all', inplace=True)
# df_total_gr.columns = ['非谈判新列名品种\n增长率', '谈判列名品种\n增长率']
# title_text = '医保非谈判新列名品种 versus 谈判列名品种 销售额增长率趋势（季度）'
# plot_line(df=df_total_gr,savefile='plots/'+title_text+'.png',
#           xlabelrotation=90, ylabelperc=True,
#           title=title_text, ytitle='销售额同比增长率')
#
# #医保非谈判新列名品种 versus 谈判品种 销售量增长率趋势（季度）
# df_total_volume_gr = tsVolume.toTotalGR()
# df_total_volume_gr1 = tsVolume1.toTotalGR()
# df_total_gr = pd.concat([df_total_volume_gr, df_total_volume_gr1],axis=1)
# df_total_gr.dropna(how='all', inplace=True)
# df_total_gr.columns = ['非谈判新列名品种\n增长率', '谈判列名品种\n增长率']
# title_text = '医保非谈判新列名品种 versus 谈判列名品种 销售量增长率趋势（季度）'
# plot_line(df=df_total_gr,savefile='plots/'+title_text+'.png',
#           xlabelrotation=90, ylabelperc=True,
#           title=title_text, ytitle='销售量同比增长率')
#
# # 进医保后销售额净增长和单价的关系
# value_baseDiff = tsValue.toBaseDiff().iloc[:,-1]
# value_baseGR = tsValue.toBaseGR().iloc[:,-1]
# df_nego = pd.concat([np.log(value_baseDiff),np.log(value_baseGR),df_value.iloc[:,-1]],axis=1)
# df_nego['是否谈判品种'] = '非谈判品种'
# df_nego.columns = ['log(进入医保后销售额净增长)', 'log(进入医保后销售额增长率)', '销售额规模', '是否谈判品种']
#
# value_baseDiff1 = tsValue1.toBaseDiff().iloc[:,-1]
# value_baseGR1 = tsValue1.toBaseGR().iloc[:,-1]
# df_normal = pd.concat([np.log(value_baseDiff1),np.log(value_baseGR1),df1_value.iloc[:,-1]],axis=1)
# df_normal['是否谈判品种'] = '谈判品种'
# df_normal.columns = ['log(进入医保后销售额净增长)', 'log(进入医保后销售额增长率)', '销售额规模', '是否谈判品种']
#
# df_combined = pd.concat([df_nego,df_normal], axis=0)
# print(df_combined)
#
# fig = plt.figure(figsize=(14,9))
# colors = iter(['teal', 'crimson', ])
# sns.set(style='white', font='simhei')
#
# ax = sns.scatterplot(x='log(进入医保后销售额净增长)', y='log(进入医保后销售额增长率)',
#                      hue='是否谈判品种', size='销售额规模',
#                      sizes=(100, 3000), palette = colors, legend='brief',
#                      data=df_combined)
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,frameon=False, labelspacing=1.5)
# plt.savefig('plots/进医保后销售表现（谈判 versus 非谈判品种）.png',
#             format='png', bbox_inches='tight', transparent=True, dpi=600)
#
#
# #医保非谈判新列名品种（不同价格） versus 谈判品种 销售额增长率趋势（季度）
# tsValue_hp = tsMatrix(df[df['单价'] >= 1500].filter(regex=("Value.*")))
# tsValue_mp = tsMatrix(df[df['单价'].between(100, 1500)].filter(regex=("Value.*")))
# tsValue_lp = tsMatrix(df[df['单价'] < 100].filter(regex=("Value.*")))
# df_totalhp_value_gr = tsValue_hp.toTotalGR()
# df_totalmp_value_gr = tsValue_mp.toTotalGR()
# df_totallp_value_gr = tsValue_lp.toTotalGR()
# df_total_value_gr1 = tsValue1.toTotalGR()
# df_total_gr = pd.concat([df_totalhp_value_gr, df_totalmp_value_gr, df_totallp_value_gr, df_total_value_gr1],axis=1)
# df_total_gr.dropna(how='all', inplace=True)
# df_total_gr.columns = ['非谈判新列名品种\n（单价>=1500元）', '非谈判新列名品种\n（单价>=100元且<1500元）', '非谈判新列名品种\n（单价<100元）', '谈判列名品种']
# title_text = '医保非谈判新列名品种（不同价格） versus 谈判列名品种 销售额增长率趋势（季度）'
# plot_line(df=df_total_gr,savefile='plots/'+title_text+'.png',
#           xlabelrotation=90, ylabelperc=True,
#           title=title_text, ytitle='销售额同比增长率')
#
# #医保非谈判新列名品种（不同品类） versus 谈判品种 销售额增长率趋势（季度）
# tsValue_oc = tsMatrix(df[df['治疗大类'] == '抗肿瘤药及免疫调节剂'].filter(regex=("Value.*")))
# tsValue_noc = tsMatrix(df[df['治疗大类'] != '抗肿瘤药及免疫调节剂'].filter(regex=("Value.*")))
# tsValue_oc1 = tsMatrix(df1[df1['治疗大类'] == '抗肿瘤药及免疫调节剂'].filter(regex=("Value.*")))
# tsValue_noc1 = tsMatrix(df1[df1['治疗大类'] != '抗肿瘤药及免疫调节剂'].filter(regex=("Value.*")))
# df_totaloc_value_gr = tsValue_oc.toTotalGR()
# df_totalnoc_value_gr = tsValue_noc.toTotalGR()
# df_totaloc_value_gr1 = tsValue_oc1.toTotalGR()
# df_totalnoc_value_gr1 = tsValue_noc1.toTotalGR()
# df_total_gr = pd.concat([df_totaloc_value_gr, df_totalnoc_value_gr, df_totaloc_value_gr1, df_totalnoc_value_gr1],axis=1)
# df_total_gr.dropna(how='all', inplace=True)
# df_total_gr.columns = ['非谈判新列名品种\n（抗肿瘤药及免疫调节剂）', '非谈判新列名品种\n（其他治疗大类）',
#                        '谈判列名品种\n（抗肿瘤药及免疫调节剂）',  '谈判新列名品种\n（其他治疗大类）']
# title_text = '医保非谈判新列名品种（不同治疗大类） versus 谈判列名品种 销售额增长率趋势（季度）'
# plot_line(df=df_total_gr,savefile='plots/'+title_text+'.png',
#           xlabelrotation=90, ylabelperc=True,
#           title=title_text, ytitle='销售额同比增长率')

# #各产品表现双图
# df2 = df.sort_values('单价', ascending=False).iloc[20:30,:]
# df_value_gr = tsValue.toGR()
# df_volume_gr = tsVolume.toGR()
# for brand in df2.index.tolist():
#     df_sales = pd.concat([df_value.loc[brand,:]/1000000, df_volume.loc[brand,:]/1000], axis=1)
#     df_sales.columns = ['销售额（百万元）', '销售量（千）']
#     df_sales = df_sales.iloc[-13:,:]
#     df_gr = pd.concat([df_value_gr.loc[brand,:] , df_volume_gr.loc[brand,:]], axis=1)
#     df_gr.columns = ['销售额\n增长率', '销售量\n增长率']
#     df_gr = df_gr.iloc[-13:,:]
#
#     title_text = ['销售表现趋势', '销售增长率变化趋势']
#     fig_title = brand + '列名医保后销售表现\n（单价：'+"{:.1f}".format(df.loc[brand, '单价']) + '元）'
#     plot_bar_line(df1=df_sales,df2=df_gr,savefile='plots/分产品/'+brand.replace('|', '_')+'.png',
#               xlabelrotation=90,  title=title_text, ytitle=['销售额（百万元）','同比增长率'], fig_title=fig_title)
#     print(brand)
