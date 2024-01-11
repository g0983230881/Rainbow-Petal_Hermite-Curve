# 匯入必要的函式庫
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# 定義一個函數，計算 Hermite 基底函數在給定參數 t 時的值
def hermite_basis(t):
    """計算在給定參數 t 時的 Hermite 基底函數"""
    h00 = 2 * t**3 - 3 * t**2 + 1
    h10 = t**3 - 2 * t**2 + t
    h01 = -2 * t**3 + 3 * t**2
    h11 = t**3 - t**2
    return h00, h10, h01, h11

# 定義一個函數，根據給定的控制點和切線計算 Hermite Spline 上的點
def hermite_spline(p0, p1, v0, v1, num_points=100):
    """根據給定的控制點和切線計算 Hermite Spline 上的點"""
    t = np.linspace(0, 1, num_points)
    h00, h10, h01, h11 = hermite_basis(t)
    spline_points = \
    h00[:, None] * p0 + h10[:, None] * v0 + h01[:, None] * p1 + h11[:, None] * v1
    return spline_points


# 使用十六進位顏色碼，將值傳遞給 Matplotlib 的 fill 函數。
# Matplotlib 預期十六進位顏色碼前面有 '#' 符號。
# 修改 rotate_and_plot_petals 函數接受十六進位顏色碼。

def rotate_and_plot_petals(spline_base, spline_left, center_point, num_petals, hex_colors, ax):
    """
    根據花瓣的數量和以十六進位格式指定的顏色，繪製繞中心點旋轉的 Hermite spline 花瓣。

    :param spline_base: 花瓣基底 spline 的點。
    :param spline_left: 花瓣左側的點。
    :param center_point: 繞其旋轉花瓣的中心點 (x, y)。
    :param num_petals: 要生成的花瓣數量。
    :param hex_colors: 用於填充花瓣的顏色列表，每個以十六進位字符串指定。
    :param ax: Matplotlib Axes 物件以進行繪製。
    """
    angle_increment = 360 / num_petals  # 計算每個花瓣之間的角度

    # 定義旋轉函數
    def rotate_around_point(xy, radians, origin=(0, 0)):
        x, y = xy
        ox, oy = origin
        px, py = x - ox, y - oy
        qx = np.cos(radians) * px - np.sin(radians) * py
        qy = np.sin(radians) * px + np.cos(radians) * py
        return qx + ox, qy + oy
    
    # 對每個點應用旋轉並繪製花瓣
    for i, angle in enumerate(np.arange(0, 360, angle_increment)):
        radians = np.deg2rad(angle)  # 將角度轉換為弧度
        rotated_spline_base = np.array([rotate_around_point(point, radians, center_point) for point in spline_base])
        rotated_spline_left = np.array([rotate_around_point(point, radians, center_point) for point in spline_left])

        # 合併旋轉後的 spline 點
        combined_rotated_x = np.concatenate((rotated_spline_base[:, 0], rotated_spline_left[::-1, 0]))
        combined_rotated_y = np.concatenate((rotated_spline_base[:, 1], rotated_spline_left[::-1, 1]))

        # 用列表中的顏色填充旋轉後的花瓣
        color = hex_colors[i % len(hex_colors)]  # 循環使用顏色列表
        ax.fill(combined_rotated_x, combined_rotated_y, color=f'#{color}')
        ax.plot(rotated_spline_base[:, 0], rotated_spline_base[:, 1], 'k')  # 以黑色繪製輪廓以增加可見性
        ax.plot(rotated_spline_left[:, 0], rotated_spline_left[:, 1], 'k')  


def main():
    # 調整切線向量以使 spline 曲線更自然
    new_tangents_adjusted = np.array([
        [1, 2],    # 底部的切線，水平方向使底部變寬
        [0, -1]    # 頂部的切線，向上方向增加曲率
    ])

    # 調整底部控制點的位置至 y 軸 1.0
    new_points_adjusted = np.array([
        [0, 1.3],   # 底部移到 y 軸 1.0
        [0, 1.5]    # 頂部保持不變
    ])

    # 使用調整後的控制點和切線重新計算 Hermite Spline
    new_spline_adjusted_base = hermite_spline(new_points_adjusted[0], new_points_adjusted[1], new_tangents_adjusted[0], new_tangents_adjusted[1])

    # 為了將 spline 鏡射到左側，我們可以反射 spline 點的 x 座標
    new_spline_adjusted_left = np.copy(new_spline_adjusted_base)
    new_spline_adjusted_left[:, 0] *= -1  # 反射 x 座標

    # 使用此函數繪製帶有自訂十六進位顏色的花瓣
    custom_hex_colors = [
        'EF5350',
        'EC407A',
        'AB47BC',
        '7E57C2',  
        '26C6DA',
        '9CCC65',
        'FFEE58',
        'FFA726',
        '8D6E63',
    ]

    def update_petals(value):
       num_petals = int(value)
       ax.clear()
       rotate_and_plot_petals(new_spline_adjusted_base, new_spline_adjusted_left, new_points_adjusted[0], num_petals, custom_hex_colors, ax)
       ax.plot(new_points_adjusted[0, 0], new_points_adjusted[0, 1], 'go')  # 中心點
       ax.invert_yaxis()  # 反轉 y 軸以匹配圖像座標系統
       ax.set_aspect('equal', adjustable='box')
       ax.set_title(f'Hermite Spline Rainbow Petal')
       ax.set_xlabel('X axis')
       ax.set_ylabel('Y axis')
       canvas.draw()


    # 創建主視窗
    root = tk.Tk()
    root.title("自訂花瓣設定")

    # 添加標籤、拉桿和按鈕
    label = tk.Label(root, text="調整花瓣數量:")
    label.pack(pady=10)

    # 控制花瓣最大最小數量並動態更新花瓣數
    petal_scale = tk.Scale(root, from_=1, to=9, orient=tk.HORIZONTAL, command=lambda value: update_petals(value))
    petal_scale.set(5)  # 初始花瓣數
    petal_scale.pack(pady=10)

    # 創建 Matplotlib 圖形
    fig, ax = plt.subplots(figsize=(8, 8))
    rotate_and_plot_petals(new_spline_adjusted_base, new_spline_adjusted_left, new_points_adjusted[0], 5, custom_hex_colors, ax)
    ax.plot(new_points_adjusted[0, 0], new_points_adjusted[0, 1], 'go')  # 中心點
    ax.invert_yaxis()  # 反轉 y 軸以匹配圖像座標系統
    ax.set_aspect('equal', adjustable='box')
    ax.set_title(f'Hermite Spline Rainbow Petal')
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')

    # 在 Tkinter 視窗中添加 Matplotlib 圖形
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # 啟動主迴圈
    root.mainloop()

if __name__ == "__main__":
    main()
