from pyecharts import Bar,Pie,Style
import pandas as pd


#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100)


df = pd.read_excel('lagou.xls')


#薪资对比
salary_list = ['10k-20k','12k-20k','15k-25k','15k-30k','20k-40k','25k-50k']
df_python = df[(df['职位类型']=='python')&(df['薪资'].isin (salary_list))].groupby(['薪资'],as_index=False)['职位类型'].size().reset_index(name='count')
df_java = df[(df['职位类型']=='java')&(df['薪资'].isin (salary_list))].groupby(['薪资'],as_index=False)['职位类型'].size().reset_index(name='count')
df_go = df[(df['职位类型']=='go')&(df['薪资'].isin (salary_list))].groupby(['薪资'],as_index=False)['职位类型'].size().reset_index(name='count')



# bar = Bar("薪资分布图", "数量")
# bar.add("python薪资分布", df_python['薪资'], df_python['count'], is_more_utils=True)
# bar.add("java薪资分布", df_java['薪资'], df_java['count'], is_more_utils=True)
# bar.add("go薪资分布", df_go['薪资'], df_go['count'], is_more_utils=True)
# # bar.print_echarts_options() # 该行只为了打印配置项，方便调试时使用
# bar.render('薪资分布图.html')  # 生成本地 HTML 文件



#学历对薪资的影响
salary_list = ['10k-20k','12k-20k','15k-25k','15k-30k','20k-40k','25k-50k']
df_Bachelor  = df[(df['学历要求']=='本科')&(df['薪资'].isin (salary_list))].groupby(['薪资'],as_index=False)['职位类型'].size().reset_index(name='count')
df_junior = df[(df['学历要求']=='大专')&(df['薪资'].isin (salary_list))].groupby(['薪资'],as_index=False)['职位类型'].size().reset_index(name='count')
df_master = df[(df['学历要求']=='硕士')&(df['薪资'].isin (salary_list))].groupby(['薪资'],as_index=False)['职位类型'].size().reset_index(name='count')
df_other = df[(df['学历要求']=='不限')&(df['薪资'].isin (salary_list))].groupby(['薪资'],as_index=False)['职位类型'].size().reset_index(name='count')

print(df_Bachelor,df_junior,df_master,df_other)


#职位总需求量
city_list = ['北京', '上海', '深圳', '成都', '广州', '杭州', '武汉', '南京', '苏州', '郑州','西安']
df_python_pos = df[(df['职位类型']=='python')&(df['城市'].isin (city_list))].groupby(['城市'],as_index=False)['职位类型'].size().reset_index(name='count')
df_java_pos = df[(df['职位类型']=='java')&(df['城市'].isin (city_list))].groupby(['城市'],as_index=False)['职位类型'].size().reset_index(name='count')
df_go_pos = df[(df['职位类型']=='go')&(df['城市'].isin (city_list))].groupby(['城市'],as_index=False)['职位类型'].size().reset_index(name='count')


# bar = Bar("职位需求量分布图", "数量")
# bar.add("python需求量分布", df_python_pos['城市'], df_python_pos['count'], is_more_utils=True)
# bar.add("java需求量分布", df_java_pos['城市'], df_java_pos['count'], is_more_utils=True)
# bar.add("go需求量分布", df_go_pos['城市'], df_go_pos['count'], is_more_utils=True)
# # bar.print_echarts_options() # 该行只为了打印配置项，方便调试时使用
# bar.render('各大城市职位需求量大致分布图.html')  # 生成本地 HTML 文件

#学历要求
df_python_education = df[(df['职位类型']=='python')].groupby(['学历要求'],as_index=False)['职位类型'].size().reset_index(name='count')
df_java_education = df[(df['职位类型']=='java')].groupby(['学历要求'],as_index=False)['职位类型'].size().reset_index(name='count')
df_go_education = df[(df['职位类型']=='go')].groupby(['学历要求'],as_index=False)['职位类型'].size().reset_index(name='count')
# print(df_python_education)
# print(df_python_education['count'].values.tolist())


# pie = Pie("各类职位中学历所占的比例", title_pos='center')
# pie.add(
#     "python",
#     df_python_education['学历要求'],
#     df_python_education['count'],
#     center=[50, 70],
#     radius=[20, 30],
#     label_text_color=None,
#     is_label_show=True,
#     legend_orient="vertical",
#     legend_pos="left",
# )
#
# pie.add(
#     "",
#     df_java_education['学历要求'],
#     df_java_education['count'],
#     center=[70, 70],
#     radius=[20, 30],
#     label_text_color=None,
#     is_label_show=True,
#     legend_orient="vertical",
#     legend_pos="left",
# )
#
# pie.add(
#     "",
#     df_go_education['学历要求'],
#     df_go_education['count'],
#     center=[90, 70],
#     radius=[20, 30],
#     label_text_color=None,
#     is_label_show=True,
#     legend_orient="vertical",
#     legend_pos="left",
# )
#
# pie.render('python学历要求分布.html')


