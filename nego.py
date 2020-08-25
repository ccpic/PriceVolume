# -*- coding: UTF-8 -*-
import numpy as np
import chardet
import pandas as pd
import calendar
import datetime
import time
import re
from chart_func import *


pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 5000)

df = pd.read_excel(open('降价品种销售表现.xlsx', 'rb'), sheet_name='CHPA')  #从Excel读取数

# new_products = ['信立坦', '瑞复美', '泽珂', '迈灵达', '爱谱沙']
# df = df[df['商品名'].isin(new_products)]
df.index = df['通用名']

d_eng = {
        '注射用重组人凝血因子VIIa': 'EPTACOG ALFA (activated)',
        '注射用童组人尿激酶原': 'SARUPLASE',
        '康柏西普眼用注射液': 'COMBERCEPT',
        '雷珠单抗注射液': 'RANIBIZUMAB',
        '喹硫平缓释片': 'QUETIAPINE',
        '替格瑞洛片': 'TICAGRELOR',
        '吗啉硝唑氯化钠注射液': 'MORINIDAZOLE+SODIUM',
        '重组人血管内皮抑制素注射液': 'HUMAN ENDOSTATIN',
        '阿利沙坦酯片': 'ALLISARTAN',
        '碳酸镧咀嚼片': 'LANTHANUM',
        '西达本胺片': 'TUCIDINOSTAT',
        '利妥昔单抗注射液': 'RITUXIMAB',
        '碳酸司维拉姆片': 'SEVELAMER',
        '甲磺酸阿帕替尼片': 'APATINIB',
        '依维莫司片': 'EVEROLIMUS',
        '尼妥珠单抗注射液': 'NIMOTUZUMAB',
        '托伐普坦片': 'TOLVAPUTAN',
        '甲苯磺酸拉帕替尼片': 'LAPATINIB',
        '泊沙康唑口服混悬液': 'POSACONAZOLE',
        '注射用重组人脑利钠肽': 'NESIRITIDE',
        '利拉鲁肽注射液': 'LIRAGLUTIDE',
        '甲苯碳酸索拉非尼片': 'SORAFENIB',
        '注射用硼替佐米': 'BORTEZOMIB',
        '醋酸阿比特龙片': 'ABIRATERONE',
        '氟维司群注射液': 'FULVESTRANT',
        '盐酸厄洛替尼片': 'ERLOTINIB',
        '来那度胺胶囊': 'LENALIDOMIDE',
        '贝伐珠单抗注射液': 'BEVACIZUMAB',
        '注射用曲妥珠单抗': 'TRASTUZUMAB',
        '利伐沙班': 'RIVAROXABAN',
        }

# d= {
#     '信立坦': '快速上量的新上市产品',
#     '爱谱沙': '快速上量的新上市产品',
#     '迈灵达': '快速上量的新上市产品',
# 
#     '泽珂': '爆发式增长的产品' ,
#     '瑞复美': '爆发式增长的产品' ,
#     '安维汀': '爆发式增长的产品' ,
#     '赫赛汀': '爆发式增长的产品' ,
#     '多吉美': '爆发式增长的产品' ,
#     '泰立沙': '爆发式增长的产品' ,
#     '芙仕得': '爆发式增长的产品' ,
#     '诺科飞': '爆发式增长的产品' ,
#     '福斯利诺': '爆发式增长的产品' ,
#     '诺维乐': '爆发式增长的产品' ,
#     '苏麦卡': '爆发式增长的产品' ,
#     '诺和力': '爆发式增长的产品' ,
# 
#     '倍林达': '可观增长的产品',
#     '诺适得': '可观增长的产品',
#     '泰欣': '可观增长的产品',
#     '飞尼妥': '可观增长的产品',
# 
#     '拜瑞妥': '销售量增长但未来拉动销售额的产品',
#     '万珂': '销售量增长但未来拉动销售额的产品',
#     '艾坦': '销售量增长但未来拉动销售额的产品',
#     '恩度': '销售量增长但未来拉动销售额的产品',
#     '特罗凯': '销售量增长但未来拉动销售额的产品',
#     '新活素': '销售量增长但未来拉动销售额的产品',
#     '朗沐': '销售量增长但未来拉动销售额的产品',
#     
#     '美罗华': '表现无起色甚至下滑的产品',
#     '诺其': '表现无起色甚至下滑的产品',
#     '思瑞康': '表现无起色甚至下滑的产品',
#     '普佑克': '表现无起色甚至下滑的产品',
# 
#     }

# df['表现'] = df['商品名'].map(d)
# for category in ['快速上量的新上市产品', '爆发式增长的产品', '可观增长的产品', '销售量增长但未来拉动销售额的产品', '表现无起色甚至下滑的产品']:

df_value = df.filter(regex=("Value.*"))
df_value = df_value.astype('float')
df_value.columns = df_value.columns.str[-4:]
df_value_gr = df_value.pct_change(axis=1, periods=4)
df_value_gr.dropna(how='all', axis=1, inplace=True)
df_value.fillna(0, inplace=True)
df_value_diff = df_value.diff(axis=1, periods=4)

df_volume = df.filter(regex=("Volume.*"))
df_volume = df_volume.astype('float')
df_volume.columns = df_volume.columns.str[-4:]
df_volume_gr = df_volume.pct_change(axis=1,periods=4)
df_volume_gr.dropna(how='all', axis=1, inplace=True)
df_volume.fillna(0, inplace=True)
df_volume_diff = df_volume.diff(axis=1,periods=4)



for i in range(0, len(df_value.index)):
    df_value.iloc[i] = df_value.iloc[i].rolling(window=4).sum()
df_value = df_value.iloc[:, 4:]
for i in range(0, len(df_volume.index)):
    df_volume.iloc[i] = df_volume.iloc[i].rolling(window=4).sum()
df_volume = df_volume.iloc[:, 4:]

# 总体销售趋势双柱状图
df_total_value = df_value.sum().to_frame('销售额')
df_total_value = df_total_value/1000000000
df_total_value.index = df_total_value.index.str[-4:]
df_total_volume = df_volume.sum().to_frame('销售量')
df_total_volume = df_total_volume/1000000
df_total_volume.index = df_total_volume.index.str[-4:]
print(df_total_value)
print(df_total_volume)
title_text = ['降价品种总体销售额趋势', '降价品种总体销售量趋势']
plot_dual_bar(df1=df_total_value, df2=df_total_volume,savefile='plots/降价品种总体销售趋势（滚动年）.png',
          xlabelrotation=90, ylabelperc=False,
          title=title_text, ytitle=['滚动年销售额（十亿）','滚动年销售量（百万）'])

# # 总体销售增长率趋势折线图
# df_total_value_gr = df_total_value.pct_change(periods=4)
# df_total_volume_gr = df_total_volume.pct_change(periods=4)
#
# df_total_gr = pd.concat([df_total_value_gr,df_total_volume_gr],axis=1)
# df_total_gr.dropna(how='all', inplace=True)
# df_total_gr.columns = ['Value Sales\nGR(y-1)', 'Volume Sales\nGR(y-1)']
# title_text = 'YoY sales growth trend of drugs that participate NRDL price-cut negotiation'
# plot_line(df=df_total_gr,savefile='plots/'+title_text+'.png',
#           xlabelrotation=90, ylabelperc=True,
#           title=title_text, ytitle='% GR(y-1)')


# #销售额增长率趋势矩阵图
# df_value = df_value.sort_values('Value18Q3', ascending=False)
# df_value_gr = df_value.pct_change(axis=1,periods=4)
# df_value_gr = df_value_gr.iloc[:,-11:]
# df_value_gr.columns = df_value_gr.columns.str[-4:]
# print(df_value_gr)
# 
# brand_list = df_value_gr.index.tolist()
# 
# fig, axes = plt.subplots(nrows=6, ncols=5, sharex=True, figsize=(13, 6))
# plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.1, hspace=0.4)
# 
# for i, brand in enumerate(brand_list):
# 
#     df = df_value_gr.loc[brand,:].T.to_frame(brand)
#     print(df)
# 
#     ax = plt.subplot(6, 5, i+1)
# 
#     for column in df:
#         linewidth = 1
#         ax.plot(df.index, df[column], color='teal', linewidth=linewidth , label=column)
# 
# 
#     ax.grid(which='major', linestyle=':', linewidth='0.5', color='grey')
#     ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
#     ax.set_title(brand, fontproperties=myfont, fontsize=9)
#     ax.set_yticklabels([])
#     ax.axvline('17Q2', linestyle='--', linewidth=1, color='crimson')
# 
#     plt.tick_params(
#         axis='x',  # changes apply to the x-axis
#         which='both',  # both major and minor ticks are affected
#         bottom='off',  # ticks along the bottom edge are off
#         top='off',  # ticks along the top edge are off
#         left='off',
#         labelbottom='off',
#         labelleft = 'off')
# 
# # Save
# 
# # handles, labels = ax.get_legend_handles_labels()
# # fig.legend(handles, labels,  loc='center right', prop=myfont)
# plt.suptitle('各降价品牌降价前后一年销售额增长率趋势（季度）', fontproperties=myfont, fontsize=20)
# fig.text(0.5, 0.05, '降价前后一年销售额增长率趋势对比', ha='center', fontproperties=myfont, fontsize=16)
# fig.text(0.05, 0.5, '销售额同比增长率', va='center', rotation='vertical', fontproperties=myfont, fontsize=16)
# 
# plt.savefig('plots/销售额增长率趋势矩阵图.png', format='png', bbox_inches='tight', dpi=600)
# 
# # Close
# plt.clf()
# plt.cla()
# plt.close()

# #销售量增长率趋势矩阵图
# df_volume = df.sort_values('Value18Q3', ascending=False).filter(regex=("Volume.*"))
# df_volume_gr = df_volume.pct_change(axis=1,periods=4)
# df_volume_gr = df_volume_gr.iloc[:,-11:]
# df_volume_gr.columns = df_volume_gr.columns.str[-4:]
# print(df_volume_gr)
#
# brand_list = df_volume_gr.index.tolist()
#
# fig, axes = plt.subplots(nrows=6, ncols=5, sharex=True, figsize=(13, 6))
# plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.1, hspace=0.4)
#
# for i, brand in enumerate(brand_list):
#
#     df = df_volume_gr.loc[brand,:].T.to_frame(brand)
#     print(df)
#
#     ax = plt.subplot(6, 5, i+1)
#
#     for column in df:
#         linewidth = 1
#         ax.plot(df.index, df[column], color='teal', linewidth=linewidth , label=column)
#
#
#     ax.grid(which='major', linestyle=':', linewidth='0.5', color='grey')
#     ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
#     ax.set_title(brand, fontproperties=myfont, fontsize=9)
#     ax.set_yticklabels([])
#     ax.axvline('17Q2', linestyle='--', linewidth=1, color='crimson')
#
#     plt.tick_params(
#         axis='x',  # changes apply to the x-axis
#         which='both',  # both major and minor ticks are affected
#         bottom='off',  # ticks along the bottom edge are off
#         top='off',  # ticks along the top edge are off
#         left='off',
#         labelbottom='off',
#         labelleft = 'off')
#
# # Save
#
# # handles, labels = ax.get_legend_handles_labels()
# # fig.legend(handles, labels,  loc='center right', prop=myfont)
# plt.suptitle('各降价品牌降价前后一年销售量增长率趋势（季度）', fontproperties=myfont, fontsize=20)
# fig.text(0.5, 0.05, '降价前后一年销售量增长率趋势对比', ha='center', fontproperties=myfont, fontsize=16)
# fig.text(0.05, 0.5, '销售量同比增长率', va='center', rotation='vertical', fontproperties=myfont, fontsize=16)
#
# plt.savefig('plots/销售量增长率趋势矩阵图.png', format='png', bbox_inches='tight', dpi=600)
#
# # Close
# plt.clf()
# plt.cla()
# plt.close()

# #降价后各品种销售额 Uplift vs 增长率变化气泡图
# df_value_gr = df_value.pct_change(axis=1,periods=4)
# df_value_gr.fillna(0, inplace=True)
# df_value_gr_diff = df_value_gr.loc[:,'18Q3'] - df_value_gr.loc[:,'17Q2']
# df_value_diff = df_value.loc[:,'18Q3'] - df_value.loc[:,'17Q2']
# df_size = df_value.loc[:,'18Q3']/100000
# df_total_value_gr =  df_value.sum().pct_change(periods=4)
# labels = df_value_gr.index.str.replace('|', '\n')
# avggrdiff = df_total_value_gr.loc['18Q3'] - df_total_value_gr.loc['17Q2']
# title_text = '降价后各品种销售额 Uplift vs 增长率变化'
# 
# 
# 
# plot_bubble_m(x=df_value_diff, y=df_value_gr_diff, z=df_size, avggr=avggrdiff, width=15, height=8, labels=labels, xfmt='{:,.0f}',
#               ylabel='平均增长率\n变化', savefile='plots/' + title_text + '气泡图.png',
#               title=title_text, xtitle='降价后销售额Uplift', ytitle='降价后销售额增长率变化')


# #降价后各品种销售量 Uplift vs 增长率变化气泡图
# df_volume_gr = df_volume.pct_change(axis=1,periods=4)
# df_volume_gr.fillna(0, inplace=True)
# df_volume_gr_diff = df_volume_gr.loc[:,'18Q3'] - df_volume_gr.loc[:,'17Q2']
# df_volume_diff = df_volume.loc[:,'18Q3'] - df_volume.loc[:,'17Q2']
# df_size = df_volume.loc[:,'18Q3']/1000
# df_total_volume_gr =  df_volume.sum().pct_change(periods=4)
# labels = df_volume_gr.index.str.replace('|', '\n')
# avggrdiff = df_total_volume_gr.loc['18Q3'] - df_total_volume_gr.loc['17Q2']
# title_text = '降价后各品种销售量 Uplift vs 增长率变化'
#
#
#
# plot_bubble_m(x=df_volume_diff, y=df_volume_gr_diff, z=df_size, avggr=avggrdiff, width=15, height=8, labels=labels, xfmt='{:,.0f}',
#               ylabel='平均增长率\n变化', savefile='plots/' + title_text + '气泡图.png',
#               title=title_text, xtitle='降价后销售量Uplift', ytitle='降价后销售量增长率变化')

# #降价后各品种销售量uplift vs 销售额uplift
#
# df_volume_gr.fillna(0, inplace=True)
# df_volume_gr_diff = df_volume_gr.loc[:,'18Q3'] - df_volume_gr.loc[:,'17Q2']
# df_value_gr.fillna(0, inplace=True)
# df_value_gr_diff = df_value_gr.loc[:,'18Q3'] - df_value_gr.loc[:,'17Q2']
# df_size = df_value.loc[:,'18Q3']/200000
# labels = df_volume_gr_diff.index.str.replace('|', '\n')
# df_total_volume_gr = df_volume.sum().pct_change(periods=4)
# df_total_value_gr = df_value.sum().pct_change(periods=4)
# avg_volume_gr_diff= df_total_volume_gr.loc['18Q3'] - df_total_volume_gr.loc['17Q2']
# avg_value_gr_diff = df_total_value_gr.loc['18Q3'] - df_total_value_gr.loc['17Q2']
# title_text = '降价后各品种销售量增长率变化 vs 销售额增长率变化'
#
# plot_bubble_m(x=df_volume_gr_diff, y=df_value_gr_diff, z=df_size, avggr=avg_value_gr_diff, width=15, height=8,
#               labels=labels, xfmt='{:+.0%}',ylabel='销售额增长率\n平均变化',
#               xavgline=True, avgms=avg_volume_gr_diff, xlabel='销售量增长率\n平均变化',
#               savefile='plots/' + title_text + '气泡图.png',
#               title=title_text, xtitle='降价后销售量增长率变化', ytitle='降价后销售额增长率变化')


# # #降价后各品种销售额增长率 vs 增长率和降价前的变化
# df_value_gr_diff = df_value_gr.loc[:,'18Q3']/df_value_gr.loc[:,'17Q2']
# df_size = df_value.loc[:,'18Q3']/200000
# df_total_value_gr = df_value.sum().pct_change(periods=4)
# avg_value_gr = df_total_value_gr.loc['18Q3']
# avg_value_gr_diff = df_total_value_gr.loc['18Q3'] - df_total_value_gr.loc['17Q2']
# title_text = '降价后各品种销售额增长率 vs 增长率和降价前的变化'
#
# df_value_gr_diff.drop('西达本胺片|微芯生物', inplace=True)
# df_size.drop('西达本胺片|微芯生物', inplace=True)
# df_value_gr.drop('西达本胺片|微芯生物', inplace=True)
# labels = df_value_gr_diff.index.str.replace('|', '\n')
#
# plot_bubble_m(x=df_value_gr.loc[:,'18Q3'] , y=df_value_gr_diff, z=df_size, avggr=avg_value_gr_diff, width=15, height=8,
#               labels=labels, xfmt='{:+.0%}',yfmt='{:,.1f}', ylabel='平均',
#               xavgline=True, avgms=avg_value_gr, xlabel='平均',
#               savefile='plots/' + title_text + '气泡图.png',
#               title=title_text, xtitle='销售额增长率(18Q3)', ytitle='销售额增长率变化(18Q3 vs 17Q2)')


#
# #各产品表现双图
# for brand in df_value.index.tolist():
#     df_sales = pd.concat([df_value.loc[brand,:], df_volume.loc[brand,:]], axis=1)
#     df_sales.columns = ['销售额', '销售量']
#     df_sales = df_sales.iloc[-11:,:]
#     df_gr = pd.concat([df_value_gr.loc[brand,:] , df_volume_gr.loc[brand,:]], axis=1)
#     df_gr.columns = ['销售额\n增长率', '销售量\n增长率']
#     df_gr = df_gr.iloc[-11:,:]
#
#     title_text = ['销售表现趋势', '销售增长率变化趋势']
#     fig_title = brand + '降价前后销售表现\n降价幅度（'+"{:+.1%}".format(df.loc[brand, '实际降价幅度']) + '）'
#     plot_bar_line(df1=df_sales,df2=df_gr,savefile='plots/分产品/'+brand.replace('|', '_')+'.png',
#               xlabelrotation=90, title=title_text, ytitle=['销售额','同比增长率'], fig_title=fig_title)
#     print(brand)


# #各大类销售增长率趋势
# 
#     df_total_value = df_value.sum()
#     df_total_value_gr = df_total_value.pct_change(periods=4)
# 
#     df_total_volume = df_volume.sum()
#     df_total_volume_gr = df_total_volume.pct_change(periods=4)
# 
#     df_total_gr = pd.concat([df_total_value_gr,df_total_volume_gr],axis=1)
#     df_total_gr.dropna(how='all', inplace=True)
#     df_total_gr.columns = ['销售额\n增长率', '销售量\n增长率']
#     title_text = category+'销售增长率趋势'
#     plot_line(df=df_total_gr,savefile='plots/'+title_text+'.png',
#               xlabelrotation=90, ylabelperc=True,
#               title=title_text, ytitle='同比增长率')

# #降价前各品种体量 vs 增长率变化气泡图
# df_value_gr.fillna(0, inplace=True)
# df_value_gr_diff = df_value_gr.loc[:,'18Q3'] - df_value_gr.loc[:,'17Q2']
# print(df_value_gr_diff)
# df_size_before = df_value.loc[:,'17Q2']
# df_size = df_value.loc[:,'18Q3']/100000
# labels = df_value_gr.index.str.replace('|', '\n')
# title_text = '降价前产品规模 vs 降价后增长率变化'
#
# plot_bubble_m(x=df_size_before, y=df_value_gr_diff , z=df_size,  width=15, height=8, labels=labels,  xfmt='{:,.0f}',
#                savefile='plots/' + title_text + '气泡图.png', yavgline=True, yavg=0,
#               title=title_text, xtitle='降价前产品单季销售额', ytitle='降价后销售额增长率变化')


# #降价前各品种体量 vs 销售额Uplift变化气泡图
# df_value_diff_diff = df_value_diff.loc[:,'18Q3'] - df_value_diff.loc[:,'17Q2']
# print(df_value_diff_diff)
# df_size_before = df_value.loc[:,'17Q2']
# df_size = df_value.loc[:,'18Q3']/100000
# labels = df_value_gr.index.str.replace('|', '\n')
#
# title_text = '降价前产品规模 vs 降价后Uplift变化'
#
# plot_bubble_m(x=df_size_before, y=df_value_diff_diff , z=df_size,  width=15, height=8, labels=labels,
#               yfmt = '{:+,.0f}', xfmt='{:,.0f}',
#               savefile='plots/' + title_text + '气泡图.png', yavgline=True, yavg=0,
#               title=title_text, xtitle='降价前产品单季销售额', ytitle='降价后销售额Uplift变化')


# # 上市年份 vs 增长率变化气泡图
# df_value_gr.fillna(0, inplace=True)
# df_value_gr_diff = df_value_gr.loc[:,'18Q3'] - df_value_gr.loc[:,'17Q2']
# print(df_value_gr_diff)
# df_launch_year = df['上市年份']
# df_size = df_value.loc[:,'18Q3']/100000
# labels = df_value_gr.index.str.replace('|', '\n')
# title_text = '上市年份 vs 降价后增长率变化'
#
# plot_bubble_m(x=df_launch_year, y=df_value_gr_diff , z=df_size,  width=15, height=8, labels=labels,  xfmt='{:.0f}',
#                savefile='plots/' + title_text + '气泡图.png', yavgline=True, yavg=0,
#               title=title_text, xtitle='上市年份', ytitle='降价后销售额增长率变化')


# #上市年份 vs 销售额Uplift变化气泡图
# df_value_diff_diff = df_value_diff.loc[:,'18Q3'] - df_value_diff.loc[:,'17Q2']
# print(df_value_diff_diff)
# df_launch_year = df['上市年份']
# df_size = df_value.loc[:,'18Q3']/100000
# labels = df_value_gr.index.str.replace('|', '\n')
#
# title_text = '上市年份 vs 降价后Uplift变化'
#
# plot_bubble_m(x=df_launch_year, y=df_value_diff_diff , z=df_size,  width=15, height=8, labels=labels,
#               yfmt = '{:+,.0f}', xfmt='{:.0f}',
#               savefile='plots/' + title_text + '气泡图.png', yavgline=True, yavg=0,
#               title=title_text, xtitle='上市年份', ytitle='降价后销售额Uplift变化')


# # 降价百分比 vs 增长率变化气泡图
# df_value_gr.fillna(0, inplace=True)
# df_value_gr_diff = df_value_gr.loc[:,'18Q3'] - df_value_gr.loc[:,'17Q2']
#
# df_price_cut_rate = df['实际降价幅度']
# df_size = df_value.loc[:,'18Q3']/100000
# labels = df_value_gr.index.str.replace('|', '\n').tolist()
# labels_eng = []
# for label in labels:
#         labels_eng.append(d_eng[label])
# title_text = 'Price-cut Ratio versus Sales Performance after NRDL listing'
#
# plot_bubble_m(x=df_price_cut_rate, y=df_value_gr_diff , z=df_size,  width=15, height=8, labels=labels_eng,  xfmt='{:+.1%}',
#                savefile='plots/' + title_text + '气泡图.png', yavgline=True, yavg=0,
#               title=title_text, xtitle='% Price-cut Ratio', ytitle='% YoY Growth Change after NRDL listing')


# #降价百分比 vs 销售额Uplift变化气泡图
# df_value_diff_diff = df_value_diff.loc[:,'18Q3'] - df_value_diff.loc[:,'17Q2']
# print(df_value_diff_diff)
# df_price_cut_rate = df['实际降价幅度']
# df_size = df_value.loc[:,'18Q3']/100000
# labels = df_value_gr.index.str.replace('|', '\n')
#
# title_text = '降价百分比 vs 降价后Uplift变化'
#
# plot_bubble_m(x=df_price_cut_rate, y=df_value_diff_diff , z=df_size,  width=15, height=8, labels=labels,
#               yfmt = '{:+,.0f}', xfmt='{:+.1%}',
#               savefile='plots/' + title_text + '气泡图.png', yavgline=True, yavg=0,
#               title=title_text, xtitle='降价百分比', ytitle='降价后销售额Uplift变化')


# # 降价幅度绝对值 vs 增长率变化气泡图
# df_value_gr.fillna(0, inplace=True)
# df_value_gr_diff = df_value_gr.loc[:,'18Q3'] - df_value_gr.loc[:,'17Q2']
# print(df_value_gr_diff)
# df_price_diff = df['谈判前三年均价'] * df['实际降价幅度']
# df_size = df_value.loc[:,'18Q3']/100000
# labels = df_value_gr.index.str.replace('|', '\n')
# title_text = '降价幅度绝对值 vs 降价后增长率变化'
#
# plot_bubble_m(x=df_price_diff, y=df_value_gr_diff , z=df_size,  width=15, height=8, labels=labels,  xfmt='{:+,.0f}',
#                savefile='plots/' + title_text + '气泡图.png', yavgline=True, yavg=0,
#               title=title_text, xtitle='降价幅度绝对值', ytitle='降价后销售额增长率变化')
#
#
# #降价幅度绝对值 vs 销售额Uplift变化气泡图
# df_value_diff_diff = df_value_diff.loc[:,'18Q3'] - df_value_diff.loc[:,'17Q2']
# print(df_value_diff_diff)
# df_price_diff = df['谈判前三年均价'] * df['实际降价幅度']
# df_size = df_value.loc[:,'18Q3']/100000
# labels = df_value_gr.index.str.replace('|', '\n')
#
# title_text = '降价幅度绝对值 vs 降价后Uplift变化'
#
# plot_bubble_m(x=df_price_diff, y=df_value_diff_diff , z=df_size,  width=15, height=8, labels=labels,
#               yfmt = '{:+,.0f}', xfmt='{:+,.0f}',
#               savefile='plots/' + title_text + '气泡图.png', yavgline=True, yavg=0,
#               title=title_text, xtitle='降价幅度绝对值', ytitle='降价后销售额Uplift变化')