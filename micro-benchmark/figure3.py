import matplotlib.pyplot as plt
import numpy as np

# 数据
categories = ['Xiaomi Miio', 'Broadlink', 'Kasa Smart', 'Ring', 'Blink', 
              'WiZ', 'Amcrest', 'VeSync', 'Homematic', 'Magic Home',
              'Lutron Caseta', 'SmartThings', 'Yeelight', 'EZVIZ', 'Neato Botvac',
              'WLED', 'SwitchBot Bluetooth', 'Tado', 'Philips Hue', 'deCONZ',
              'AVM FRITZ', 'ecobee', 'Environment Canada', 'Vera', 'Reolink IP',
              'Overkiz', 'RFLink', 'Leviton Decora', 'Shelly', 'Home Connect',
              'Rheem EcoNet', 'Universal Devices', 'August', 'Elgato Light', 'motionEye',
              'Hive', 'Netatmo', 'IP Webcam', 'Philips TV', 'ONVIF',
              'myStrom', 'LIFX', 'Telldus Live', 'Sensibo', 'Twinkly',]

categories2 = ['1.Xiaomi Miio', '2.Broadlink', '3.Kasa Smart', '4.Ring', '5.Blink', 
              '6.WiZ', '7.Amcrest', '8.VeSync', '9.Homematic', '10.Magic Home',
              '11.Lutron Caseta', '12.SmartThings', '13.Yeelight', '14.EZVIZ', '15.Neato Botvac',
              '16.WLED', '17.SwitchBot Bluetooth', '18.Tado', '19.Philips Hue', '20.DeCONZ',
              '21.AVM FRITZ', '22.Ecobee', '23.Environment Canada', '24.Vera', '25.Reolink IP',
              '26.Overkiz', '27.RFLink', '28.Leviton Decora', '29.Shelly', '30.Home Connect',
              '31.Rheem EcoNet', '32.Universal Devices', '33.August', '34.Elgato Light', '35.MotionEye',
              '36.Hive', '37.Netatmo', '38.IP Webcam', '39.Philips TV', '40.ONVIF',
              '41.myStrom', '42.LIFX', '43.Telldus Live', '44.Sensibo', '45.Twinkly',]

categories.reverse()
categories2.reverse()

values_left1 = [0.842105263, 1, 0.888888889, 1, 0.875, 
          0.888888888888888, 1, 0.769230769230769, 0.888888888888888,
          1, 1, 0.954545454545454, 0.777777777777777, 0.565217391304347, 
          1, 1, 0.833333333333333, 1,
          0.666666666666666, 0.8, 1, 1, 0.75, 
          0.666666666666666, 0.956521739130434, 1, 1,
          1, 1, 1, 0.666666666666666, 0.763157894736842, 
          0.913043478260869, 1, 1, 1,
          0.8, 1, 0.878048780487804, 1, 0.9375, 
          0.909090909090909, 0.583333333333333, 1, 1]



values_left2 = [0.8, 1, 0.347826086956521, 0.916666666666666, 0.96551724137931, 
          0.888888888888888, 0.692307692307692, 0.625, 1,
          0.947368421052631, 0.833333333333333, 0.378378378378378, 0.28, 0.866666666666666, 
          0.904761904761904, 0.785714285714285, 0.5, 0.945205479452054,
          0.75, 0.8, 0.9, 0.966666666666666, 1, 
          0.769230769230769, 0.515625, 1, 1,
          1, 0.8125, 1, 0.25, 0.935483870967741, 
          1, 0.727272727272727, 1, 0.642857142857142,
          0.666666666666666, 0.684210526315789, 0.486486486486486, 0.888888888888888, 0.88235294117647, 
          1, 0.583333333333333, 1, 0.863636363636363]


values_right1 = [0.756756756756756, 1, 1, 0, 0, 
          0.85, 1, 0.916666666666666, 0.888888888888888,
          1, 0, 0, 0.875, 0.1, 
          1, 1, 0, 1,
          0, 0, 1, 1, 0.75, 
          0.625, 0.956521739130434, 1, 0,
          0, 0, 1, 0, 0, 
          1, 0.916666666666666, 1, 1,
          0, 0, 0.981818181818181, 0.941176470588235, 0.888888888888888, 
          0, 0, 0, 1]


values_right2 = [0.7, 1, 0.347826086956521, 0, 0, 
          0.944444444444444, 0.692307692307692, 0.6875, 0.888888888888888,
          0.947368421052631, 0, 0, 0.28, 0.0666666666666667, 
          0.904761904761904, 0.785714285714285, 0, 0.945205479452054,
          0, 0, 0.9, 0.933333333333333, 1, 
          0.769230769230769, 0.515625, 0.677419354838709, 0,
          0, 0, 1, 0, 0, 
          1, 1, 1, 0.464285714285714,
          0, 0, 0.729729729729729, 0.888888888888888, 0.470588235294117, 
          0, 0, 0, 0.863636363636363]

values_left1.reverse()
values_left2.reverse()
values_right1.reverse()
values_right2.reverse()

values_left1 = [x * 100  for x in values_left1]
values_left2 = [x * 100  for x in values_left2]
values_right1 = [x * 100  for x in values_right1]
values_right2 = [x * 100  for x in values_right2]


# 创建画布和子图
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(10, 6))  # 调整画布大小

# 设置柱状图位置和宽度
bar_width = 0.35
index = np.arange(len(categories))

# 绘制左侧柱状图
bars1 = ax1.barh(index + bar_width/2, values_left1, bar_width, color='0', align='center', label='Precision')
bars2 = ax1.barh(index - bar_width/2, values_left2, bar_width, color='1', align='center', label='Recall')

for bar in bars1:
    ax1.add_patch(plt.Rectangle((0, bar.get_y()), bar.get_width(), bar.get_height(), fill=False, edgecolor='black', linewidth=1))

for bar in bars2:
    ax1.add_patch(plt.Rectangle((0, bar.get_y()), bar.get_width(), bar.get_height(), fill=False, edgecolor='black', linewidth=1))

# 绘制右侧柱状图
bars3 = ax2.barh(index + bar_width/2, values_right1, bar_width, color='0', align='center', label='Precision')
bars4 = ax2.barh(index - bar_width/2, values_right2, bar_width, color='1', align='center', label='Recall')

for bar in bars3:
    ax2.add_patch(plt.Rectangle((0, bar.get_y()), bar.get_width(), bar.get_height(), fill=False, edgecolor='black', linewidth=1))

for bar in bars4:
    ax2.add_patch(plt.Rectangle((0, bar.get_y()), bar.get_width(), bar.get_height(), fill=False, edgecolor='black', linewidth=1))

# 设置y轴标签
ax1.set_yticks(index)
ax1.set_yticklabels(categories2)
ax1.invert_xaxis()

ax2.set_yticks(index)
ax2.set_yticklabels(categories2)

# 设置y轴标签在右侧
ax1.tick_params(axis='y', labelleft=False, labelright=False, left=False, right=True)
ax2.tick_params(axis='y', labelleft=True, labelright=False)
#ax2.set_yticklabels(categories, horizontalalignment='center')
ax2.set_yticklabels([label + '                                      'for label in categories2], horizontalalignment='center', fontsize=12, fontname='Times New Roman')  # 添加左侧空格使标签居中对齐

# 创建自定义图例
custom_legend = [
    plt.Rectangle((0, 0), 1, 1, fc='0', ec='black', lw=1),
    plt.Rectangle((0, 0), 1, 1, fc='1', ec='black', lw=1),
]
legend_labels = ['Precision', 'Recall']


# 将自定义图例添加到图中
#fig.legend(custom_legend, legend_labels, loc='lower center', ncol=2)
#fig.legend(custom_legend, legend_labels, loc='lower center', ncol=2, edgecolor='black', fancybox=True)
fig.legend(custom_legend, legend_labels, loc='lower center', ncol=2, edgecolor='black', fancybox=True)

a, *b, c = [1,2,3,4]


# 获取当前的X轴刻度标签
xticks = ax2.get_xticklabels()

# 修改刻度标签，在每个标签后面加上'%'
new_xticks = [tick.get_text() + '%' for tick in xticks]

# 设置新的X轴刻度标签
ax1.set_xticklabels(new_xticks)
ax2.set_xticklabels(new_xticks)


ax1.set_title('AID', fontname='Times New Roman', fontweight = 'bold',fontsize=16)
ax2.set_title('AID-PyCG', fontname='Times New Roman', fontweight = 'bold',fontsize=16)

# 添加标题
#fig.suptitle('Left vs Right Comparison')

# 设置y轴标签居中
#fig.text(0.05, 0.5, 'Categories', va='center', rotation='vertical')
# 调整子图布局使其居中
plt.subplots_adjust(wspace=0.5)


# 显示图表
plt.show()
