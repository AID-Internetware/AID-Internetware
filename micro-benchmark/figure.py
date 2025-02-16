import numpy as np
import matplotlib.pyplot as plt

# 假设你有两个工具在不同条件下的准确率数据，构造一个示例数据集
# 这里使用随机生成的数据
PyDEcg_precision = np.random.rand(5, 9)  # 生成一个 5x5 的随机准确率矩阵
Pycg_precision = np.random.rand(5, 9)  # 生成一个 5x5 的随机准确率矩阵
PyDEcg_recall = np.random.rand(5, 9)  # 生成一个 5x5 的随机准确率矩阵
PyCG_recall = np.random.rand(5, 9)  # 生成一个 5x5 的随机准确率矩阵

values = [0.842105263, 1, 0.888888889, 1, 0.875, 
          0.888888888888888, 1, 0.769230769230769, 0.888888888888888]
# 循环赋值
for i, value in enumerate(values):
    PyDEcg_precision[0, i] = value

values = [1, 1, 0.954545454545454, 0.777777777777777, 0.565217391304347, 
          1, 1, 0.833333333333333, 1]
# 循环赋值
for i, value in enumerate(values):
    PyDEcg_precision[1, i] = value

values = [0.666666666666666, 0.8, 1, 1, 0.75, 
          0.666666666666666, 0.956521739130434, 1, 1]
# 循环赋值
for i, value in enumerate(values):
    PyDEcg_precision[2, i] = value

values = [1, 1, 1, 0.666666666666666, 0.763157894736842, 
          0.913043478260869, 1, 1, 1]
# 循环赋值
for i, value in enumerate(values):
    PyDEcg_precision[3, i] = value

values = [0.8, 1, 0.878048780487804, 1, 0.9375, 
          0.909090909090909, 0.583333333333333, 1, 1]
# 循环赋值
for i, value in enumerate(values):
    PyDEcg_precision[4, i] = value





values = [0.756756756756756, 1, 1, 0, 0, 
          0.85, 1, 0.916666666666666, 0.888888888888888]
# 循环赋值
for i, value in enumerate(values):
    Pycg_precision[0, i] = value

values = [1, 0, 0, 0.875, 0.1, 
          1, 1, 0, 1]
# 循环赋值
for i, value in enumerate(values):
    Pycg_precision[1, i] = value

values = [0, 0, 1, 1, 0.75, 
          0.625, 0.956521739130434, 1, 0]
# 循环赋值
for i, value in enumerate(values):
    Pycg_precision[2, i] = value

values = [0, 0, 1, 0, 0, 
          1, 0.916666666666666, 1, 1]
# 循环赋值
for i, value in enumerate(values):
    Pycg_precision[3, i] = value

values = [0, 0, 0.981818181818181, 0.941176470588235, 0.888888888888888, 
          0, 0, 0, 1]
# 循环赋值
for i, value in enumerate(values):
    Pycg_precision[4, i] = value



values = [0.8, 1, 0.347826086956521, 0.916666666666666, 0.96551724137931, 
          0.888888888888888, 0.692307692307692, 0.625, 1]
# 循环赋值
for i, value in enumerate(values):
    PyDEcg_recall[0, i] = value

values = [0.947368421052631, 0.833333333333333, 0.378378378378378, 0.28, 0.866666666666666, 
          0.904761904761904, 0.785714285714285, 0.5, 0.945205479452054]
# 循环赋值
for i, value in enumerate(values):
    PyDEcg_recall[1, i] = value

values = [0.75, 0.8, 0.9, 0.966666666666666, 1, 
          0.769230769230769, 0.515625, 1, 1]
# 循环赋值
for i, value in enumerate(values):
    PyDEcg_recall[2, i] = value

values = [1, 0.8125, 1, 0.25, 0.935483870967741, 
          1, 0.727272727272727, 1, 0.642857142857142]
# 循环赋值
for i, value in enumerate(values):
    PyDEcg_recall[3, i] = value

values = [0.666666666666666, 0.684210526315789, 0.486486486486486, 0.888888888888888, 0.88235294117647, 
          1, 0.583333333333333, 1, 0.863636363636363]
# 循环赋值
for i, value in enumerate(values):
    PyDEcg_recall[4, i] = value






values = [0.7, 1, 0.347826086956521, 0, 0, 
          0.944444444444444, 0.692307692307692, 0.6875, 0.888888888888888]
# 循环赋值
for i, value in enumerate(values):
    PyCG_recall[0, i] = value

values = [0.947368421052631, 0, 0, 0.28, 0.0666666666666667, 
          0.904761904761904, 0.785714285714285, 0, 0.945205479452054]
# 循环赋值
for i, value in enumerate(values):
    PyCG_recall[1, i] = value

values = [0, 0, 0.9, 0.933333333333333, 1, 
          0.769230769230769, 0.515625, 0.677419354838709, 0]
# 循环赋值
for i, value in enumerate(values):
    PyCG_recall[2, i] = value

values = [0, 0, 1, 0, 0, 
          1, 1, 1, 0.464285714285714]
# 循环赋值
for i, value in enumerate(values):
    PyCG_recall[3, i] = value

values = [0, 0, 0.729729729729729, 0.888888888888888, 0.470588235294117, 
          0, 0, 0, 0.863636363636363]
# 循环赋值
for i, value in enumerate(values):
    PyCG_recall[4, i] = value








# 创建热力图
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 12))

# 工具1的热力图
heatmap1 = ax1.imshow(PyDEcg_precision, cmap='Oranges', vmin=0, vmax=1)

# 工具2的热力图
heatmap2 = ax2.imshow(Pycg_precision, cmap='Oranges', vmin=0, vmax=1)

# 工具3的热力图
heatmap3 = ax3.imshow(PyDEcg_recall, cmap='Oranges', vmin=0, vmax=1)

# 工具4的热力图
heatmap4 = ax4.imshow(PyCG_recall, cmap='Oranges', vmin=0, vmax=1)

# 添加标题
ax1.set_title('Precision of PyDECG')
ax2.set_title('Precision of PyCG')
ax3.set_title('Recall of PyDECG')
ax4.set_title('Recall of PyCG')

# 添加颜色条
#plt.colorbar(heatmap1, ax=ax1, orientation='vertical', label='Accuracy', shrink=0.5)
#plt.colorbar(heatmap2, ax=ax2, orientation='vertical', label='Accuracy', shrink=0.5)
#plt.colorbar(heatmap3, ax=ax3, orientation='vertical', label='Accuracy', shrink=0.5)
#plt.colorbar(heatmap4, ax=ax4, orientation='vertical', label='Accuracy', shrink=0.5)
plt.colorbar(heatmap1, ax=ax1, orientation='vertical', label='Precision', shrink=0.5)
plt.colorbar(heatmap2, ax=ax2, orientation='vertical', label='Precision', shrink=0.5)
plt.colorbar(heatmap3, ax=ax3, orientation='vertical', label='Recall', shrink=0.5)
plt.colorbar(heatmap4, ax=ax4, orientation='vertical', label='Recall', shrink=0.5)

# 显示热力图
plt.tight_layout()
plt.show()