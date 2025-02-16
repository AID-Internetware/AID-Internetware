import matplotlib.pyplot as plt

# 数据
labels = ['Docs', 'Guide', 'Null']
sizes = [21.88, 61.87, 16.25]
colors = ['#444444', '#777777', '#999999']  # 使用更深的黑色和更亮的灰色
explode = (0, 0.1, 0.1)  # 将"guide"和"null"一起突出显示

# 自定义百分比显示函数，包括设置字体大小
def my_autopct(pct):
    return '%1.2f%%' % pct

# 创建饼状图
plt.figure(figsize=(8, 6))
_, _, autotexts = plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=my_autopct, shadow=True, startangle=140, textprops={'color': 'black', 'fontsize': 14})  # 调整标签字体大小
plt.axis('equal')  # 使得饼状图是正圆形

# 增大百分比字体大小
for autotext in autotexts:
    autotext.set_fontsize(18)  # 设置字体大小

# 添加图例
plt.legend(loc='upper right', labels=['%s: %.2f %%' % (l, s) for l, s in zip(labels, sizes)], fontsize=10)

# 去除边框
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# 显示图形
plt.show()
