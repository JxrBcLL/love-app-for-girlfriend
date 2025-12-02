import tkinter as tk
from tkinter import messagebox
import random
import time
from math import sin, cos, pi

####




class LoveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("邀约小程序")
        self.root.geometry("600x650")
        self.root.configure(bg="#FFE4E1")

        # 逃跑模式计数器
        self.escape_mode = False
        self.escape_count = 0

        # 动画效果相关
        self.animating = False
        self.animation_id = None

        self.create_main_question()

    def create_main_question(self):
        # 清除所有现有组件
        for widget in self.root.winfo_children():
            widget.destroy()

        # 重置逃跑模式
        self.escape_mode = False
        self.escape_count = 0
        self.animating = False

        # 主内容框架
        main_frame = tk.Frame(self.root, bg="#FFE4E1")
        main_frame.pack(fill="both", expand=True)

        # 标题
        title_label = tk.Label(
            main_frame,
            text="我问你答",
            font=("Arial", 28, "bold"),
            fg="#FF69B4",
            bg="#FFE4E1"
        )
        title_label.pack(pady=25)

        # 问题
        question_label = tk.Label(
            main_frame,
            text="这周五下班后要不要和我一起吃饭？",
            font=("Arial", 20),
            fg="#333333",
            bg="#FFE4E1",
            wraplength=500
        )
        question_label.pack(pady=40)

        # 添加一些装饰爱心
        hearts_frame = tk.Frame(main_frame, bg="#FFE4E1")
        hearts_frame.pack()
        for _ in range(5):
            heart = tk.Label(hearts_frame, text="🐶", font=("Arial", 16), bg="#FFE4E1", fg="#FF69B4")
            heart.pack(side="left", padx=5)

        # 同意按钮
        self.yes_button = tk.Button(
            main_frame,
            text="同意 🐶",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#FF69B4",
            command=self.show_dog_image,
            width=16,
            height=2,
            relief=tk.RAISED,
            borderwidth=3,
            cursor="heart"
        )
        self.yes_button.pack(pady=30)

        # 不同意按钮 - 使用place布局以便移动
        self.no_button = tk.Button(
            main_frame,
            text="不同意",
            font=("Arial", 18),
            fg="white",
            bg="#808080",
            command=self.move_no_button_with_effects,
            width=16,
            height=2,
            cursor="pirate"
        )
        # 初始位置
        self.no_button.place(x=200, y=350)

        # 记录按钮初始位置
        self.button_x = 200
        self.button_y = 350

        # 逃跑次数显示
        self.escape_counter = tk.Label(
            main_frame,
            text="",
            font=("Arial", 14),
            fg="#FF1493",
            bg="#FFE4E1"
        )
        self.escape_counter.pack(pady=5)

        # ========== 底部提示区域 ==========
        # 创建底部框架专门放提示
        bottom_hint_frame = tk.Frame(self.root, bg="#FFE4E1", height=60)
        bottom_hint_frame.pack(side="bottom", fill="x")

        # 底部提示标签
        self.hint_label = tk.Label(
            bottom_hint_frame,
            text="提示：点击'同意'我就告诉你你的圣诞礼物是啥～",
            font=("Arial", 16, "italic"),
            fg="#FF69B4",
            bg="#FFE4E1"
        )
        self.hint_label.pack(pady=15)

    def move_no_button_with_effects(self):
        """移动不同意按钮并添加动画效果"""
        # 增加逃跑次数
        self.escape_count += 1

        # 更新逃跑次数显示
        if self.escape_count == 1:
            self.escape_counter.config(text="不点同意吗")
        elif self.escape_count == 3:
            self.escape_counter.config(text=f"已经不同意{self.escape_count}次了！")
        elif self.escape_count >= 5:
            self.escape_counter.config(text=f"坚持不懈地不同意了{self.escape_count}次！")

        # 如果逃跑太多次，进入"疯狂模式"
        if self.escape_count >= 8 and not self.escape_mode:
            self.escape_mode = True
            self.start_crazy_mode()
            return

        # 获取窗口尺寸
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        if window_width <= 1:
            window_width = 600
            window_height = 650

        # 计算安全区域（避开同意按钮）
        yes_button_info = self.yes_button.winfo_geometry()
        yes_x = self.yes_button.winfo_x()
        yes_y = self.yes_button.winfo_y()
        yes_width = self.yes_button.winfo_width()
        yes_height = self.yes_button.winfo_height()

        # 生成随机位置，避开同意按钮区域
        while True:
            new_x = random.randint(20, window_width - 140)
            new_y = random.randint(150, window_height - 80)

            # 检查是否与同意按钮重叠
            if not (new_x + 140 > yes_x and new_x < yes_x + yes_width and
                    new_y + 60 > yes_y and new_y < yes_y + yes_height):
                break

        # 添加逃跑动画效果
        self.animate_movement(new_x, new_y)

        # 更改按钮文本
        self.update_no_button_text()

        # 增强同意按钮的吸引力
        self.enhance_yes_button()

        # 添加音效提示（文本形式）
        self.show_escape_effect()

    def animate_movement(self, target_x, target_y):
        """添加平滑移动动画"""
        if self.animating:
            return

        self.animating = True
        start_x = self.button_x
        start_y = self.button_y

        steps = 20
        dx = (target_x - start_x) / steps
        dy = (target_y - start_y) / steps

        # 添加弹跳效果
        self.bounce_animation(start_x, start_y, dx, dy, steps, 0)

    def bounce_animation(self, x, y, dx, dy, steps, current_step):
        """弹跳动画效果"""
        if current_step <= steps:
            # 计算弹跳高度
            bounce_height = 0
            if current_step < steps / 2:
                bounce_height = -20 * (current_step / (steps / 2))
            else:
                bounce_height = -20 * ((steps - current_step) / (steps / 2))

            new_x = x + dx * current_step
            new_y = y + dy * current_step + bounce_height

            # 移动按钮
            self.no_button.place(x=new_x, y=new_y)

            # 记录当前位置
            self.button_x = new_x
            self.button_y = new_y - bounce_height  # 实际位置

            # 继续动画
            self.animation_id = self.root.after(10,
                                                lambda: self.bounce_animation(x, y, dx, dy, steps, current_step + 1))
        else:
            self.animating = False

    def update_no_button_text(self):
        """更新不同意按钮的文本"""
        responses = [
            ("不同意", "#808080"),
            ("才不要", "#FF4500"),
            ("再想想", "#FF8C00"),
            ("跑掉啦", "#32CD32"),
            ("抓不到", "#1E90FF"),
            ("就不点", "#8A2BE2"),
            ("别跑了", "#FF1493"),
            ("抓不到我的", "#00CED1"),
            ("偏不点", "#DC143C"),
            ("嘿嘿嘿", "#FFD700")
        ]

        # 根据逃跑次数选择不同的文本
        if self.escape_count < 3:
            text, color = responses[0]
        elif self.escape_count < 5:
            text, color = random.choice(responses[1:4])
        elif self.escape_count < 8:
            text, color = random.choice(responses[4:7])
        else:
            text, color = random.choice(responses[7:])

        # 添加一些特效
        font_size = 16
        if self.escape_count > 5:
            font_size = 14 + self.escape_count % 3

        self.no_button.config(
            text=text,
            bg=color,
            font=("Arial", font_size, "bold" if self.escape_count > 3 else "normal"),
            fg="white"
        )

    def enhance_yes_button(self):
        """增强同意按钮的吸引力"""
        if self.escape_count < 3:
            self.yes_button.config(
                bg="#FF69B4",
                text="同意 🐶"
            )
        elif self.escape_count < 5:
            self.yes_button.config(
                bg="#FF1493",
                text="同意 🐶️（点这里！）",
                font=("Arial", 18, "bold")
            )
        elif self.escape_count < 8:
            self.yes_button.config(
                bg="#FF00FF",
                text="同意 🐶️（点！！）",
                font=("Arial", 19, "bold"),
                width=18
            )
        else:
            # 添加闪烁效果
            self.yes_button.config(
                bg="#FF1493",
                text="同意 🐶（拜托点我~）",
                font=("Arial", 20, "bold"),
                width=20
            )
            self.blink_yes_button()

    def blink_yes_button(self):
        """让同意按钮闪烁"""
        current_color = self.yes_button.cget("bg")
        new_color = "#FFD700" if current_color == "#FF1493" else "#FF1493"
        self.yes_button.config(bg=new_color)

        if self.escape_count >= 8:
            self.root.after(500, self.blink_yes_button)

    def show_escape_effect(self):
        """显示逃跑效果的文字提示 - 随机位置显示，停留时间更长"""
        effects = [
            "跑掉了！",
            "哦豁，没抓到！",
            "nonono",
            "啊哈",
            "抓不到我吧！",
            "哦莫",
            "差点被点到！",
            "闪！",
            "哈哈，没点到！",
            "你抓不到我！",
            "nonono",
            "又跑了！",
            "啊哈",
            "哦莫",
            "哦豁，没抓到！"
        ]

        # 获取窗口尺寸
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        if window_width <= 1 or window_height <= 1:
            window_width = 600
            window_height = 650

        # 随机选择显示位置
        # 确保文字不会显示在窗口外
        # 假设文字标签大概宽120，高35
        label_width = 120
        label_height = 35

        # 计算可用的随机位置范围
        # 避免太靠近边缘（留出30像素的边距）
        min_x = 30
        max_x = max(min_x, window_width - label_width - 30)
        min_y = 80  # 避免被标题挡住
        max_y = max(min_y, window_height - label_height - 100)  # 避免被底部提示挡住

        # 确保范围有效
        if max_x > min_x and max_y > min_y:
            random_x = random.randint(min_x, max_x)
            random_y = random.randint(min_y, max_y)
        else:
            # 如果计算有问题，使用安全位置
            random_x = 150
            random_y = 250

        # 随机选择效果文本
        effect_text = random.choice(effects)

        # 随机颜色方案 - 更鲜艳的颜色
        color_schemes = [
            {"fg": "#FF4500", "bg": "#FFFFE0"},  # 橙红/淡黄
            {"fg": "#FF1493", "bg": "#FFE4E1"},  # 深粉/浅粉
            {"fg": "#32CD32", "bg": "#F0FFF0"},  # 亮绿/蜜瓜绿
            {"fg": "#1E90FF", "bg": "#F0F8FF"},  # 道奇蓝/爱丽丝蓝
            {"fg": "#8A2BE2", "bg": "#F8F8FF"},  # 蓝紫/幽灵白
            {"fg": "#DC143C", "bg": "#FFF0F5"},  # 深红/薰衣草红
            {"fg": "#FF8C00", "bg": "#FFFAF0"},  # 深橙/花白
            {"fg": "#2E8B57", "bg": "#F5FFFA"},  # 海绿/薄荷糖
            {"fg": "#D2691E", "bg": "#FFF8DC"},  # 巧克力/蛋壳白
            {"fg": "#9932CC", "bg": "#F8F0FF"},  # 深紫罗兰/淡紫
            {"fg": "#FFD700", "bg": "#FFFACD"},  # 金色/柠檬绸
            {"fg": "#00CED1", "bg": "#E0FFFF"},  # 深青/淡青
            {"fg": "#FF6347", "bg": "#FFE4E1"},  # 番茄色/浅粉
            {"fg": "#6A5ACD", "bg": "#E6E6FA"},  # 板岩蓝/薰衣草紫
            {"fg": "#FF69B4", "bg": "#FFB6C1"},  # 热粉/浅粉红
        ]

        colors = random.choice(color_schemes)

        # 随机字体样式
        font_styles = ["bold", "italic", "bold italic", "normal"]
        font_style = random.choice(font_styles)

        # 随机字体大小 - 稍微大一点
        font_size = random.randint(12, 18)

        # 随机边框样式
        border_styles = [tk.RAISED, tk.SUNKEN, tk.GROOVE, tk.RIDGE]
        border_style = random.choice(border_styles)
        border_width = random.randint(1, 3)

        # 创建临时效果标签 - 使用更明显的样式
        effect_label = tk.Label(
            self.root,
            text=effect_text,
            font=("Arial", font_size, font_style),
            fg=colors["fg"],
            bg=colors["bg"],
            relief=border_style,
            borderwidth=border_width,
            padx=random.randint(8, 15),
            pady=random.randint(3, 7)
        )

        # 在随机位置显示
        effect_label.place(x=random_x, y=random_y)

        # 随机选择动画效果类型
        animation_types = ["long_fade", "gentle_float", "slow_shake", "smooth_zoom"]
        animation_type = random.choice(animation_types)

        # 执行不同的动画效果 - 所有动画都延长持续时间
        if animation_type == "long_fade":
            self.long_fade_effect(effect_label, random_x, random_y, 0)
        elif animation_type == "gentle_float":
            self.gentle_float_effect(effect_label, random_x, random_y, 0)
        elif animation_type == "slow_shake":
            self.slow_shake_effect(effect_label, random_x, random_y, 0)
        elif animation_type == "smooth_zoom":
            self.smooth_zoom_effect(effect_label, random_x, random_y, 0)

    def gentle_float_effect(self, label, start_x, start_y, step):
        """缓慢上浮效果 - 持续时间更长"""
        if step < 25:  # 增加到25步，让动画更慢
            # 缓慢向上移动，轻微左右摇摆
            new_y = start_y - step * 2  # 每次只上浮2像素，更慢

            # 更平缓的左右摇摆
            swing = int(sin(step * pi / 6) * 6)  # 减小摇摆幅度
            new_x = start_x + swing

            label.place(x=new_x, y=new_y)

            # 更缓慢地变淡
            if step > 15:  # 延迟开始变淡
                # 计算透明度
                alpha = 1.0 - (step - 15) / 10.0  # 更平缓的透明度变化
                # 获取当前颜色
                fg_color = label.cget("fg")
                bg_color = label.cget("bg")
                # 让颜色变淡
                label.config(
                    fg=self.lighten_color(fg_color, alpha),
                    bg=self.lighten_color(bg_color, alpha)
                )

            # 继续动画 - 增加延迟时间
            self.root.after(80, lambda: self.gentle_float_effect(label, start_x, start_y, step + 1))  # 80ms
        else:
            # 最后停留一下再消失
            self.root.after(300, label.destroy)  # 停留300ms再销毁

    def slow_shake_effect(self, label, start_x, start_y, step):
        """缓慢抖动效果"""
        if step < 20:  # 增加到20步
            # 缓慢左右抖动
            shake_x = int(sin(step * pi) * 8)  # 减小抖动幅度
            shake_y = int(sin(step * pi / 3) * 4)  # 上下轻微浮动

            label.place(x=start_x + shake_x, y=start_y + shake_y)

            # 每隔更多步改变颜色
            if step % 4 == 0:  # 每4步改变一次
                colors = [
                    ("#FF4500", "#FFFFE0"),
                    ("#1E90FF", "#F0F8FF"),
                    ("#32CD32", "#F0FFF0"),
                    ("#FF1493", "#FFE4E1"),
                    ("#FFD700", "#FFFACD"),
                    ("#00CED1", "#E0FFFF")
                ]
                fg, bg = random.choice(colors)
                label.config(fg=fg, bg=bg)

            # 继续动画 - 增加延迟时间
            self.root.after(100, lambda: self.slow_shake_effect(label, start_x, start_y, step + 1))  # 100ms
        else:
            # 抖动结束后停留一下
            self.root.after(400, label.destroy)  # 停留400ms

    def smooth_zoom_effect(self, label, start_x, start_y, step):
        """平滑缩放效果 - 持续时间更长"""
        if step < 15:  # 增加到15步
            # 更平缓的缩放
            scale = 1.0 + sin(step * pi / 7.5) * 0.3  # 减小缩放幅度

            # 获取当前字体大小
            current_font = label.cget("font")
            font_parts = current_font.split()
            base_size = int(font_parts[1])

            # 计算新字体大小
            new_size = max(10, min(22, int(base_size * scale)))

            # 更新标签
            new_font = ("Arial", new_size, font_parts[2] if len(font_parts) > 2 else "normal")
            label.config(font=new_font)

            # 调整位置保持居中
            label_width = label.winfo_reqwidth()
            label_height = label.winfo_reqheight()
            new_x = start_x - (label_width - 100) // 2
            new_y = start_y - (label_height - 30) // 2

            label.place(x=new_x, y=new_y)

            # 继续动画 - 增加延迟时间
            self.root.after(80, lambda: self.smooth_zoom_effect(label, start_x, start_y, step + 1))  # 80ms
        else:
            # 缩放结束后停留一下
            self.root.after(500, label.destroy)  # 停留500ms

    def long_fade_effect(self, label, start_x, start_y, step):
        """长时间淡出效果"""
        if step < 20:  # 增加到20步，让淡出更慢
            # 缓慢向上移动
            new_y = start_y - step * 2  # 每次上浮2像素

            # 轻微左右漂移
            drift = int(sin(step * pi / 5) * 4)  # 减小漂移幅度
            new_x = start_x + drift

            label.place(x=new_x, y=new_y)

            # 更缓慢地降低颜色饱和度
            if step >= 8:  # 延迟开始变淡
                # 获取当前颜色
                fg_color = label.cget("fg")
                bg_color = label.cget("bg")

                # 计算淡化因子
                fade_factor = 1.0 - (step - 7) / 13.0  # 更平缓的淡化

                # 应用淡化
                label.config(
                    fg=self.lighten_color(fg_color, fade_factor),
                    bg=self.lighten_color(bg_color, fade_factor)
                )

            # 继续动画 - 增加延迟时间
            self.root.after(80, lambda: self.long_fade_effect(label, start_x, start_y, step + 1))  # 80ms
        else:
            # 淡出结束后停留一下再消失
            self.root.after(300, label.destroy)  # 停留300ms

    def lighten_color(self, hex_color, factor=0.5):
        """让颜色变淡（模拟透明度）"""
        try:
            # 确保颜色格式正确
            hex_color = hex_color.lstrip('#')
            if len(hex_color) != 6:
                return hex_color

            # 将十六进制颜色转换为RGB
            rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

            # 向白色靠近（增加亮度）
            new_rgb = tuple(int(255 - (255 - c) * factor) for c in rgb)

            # 转换回十六进制
            return '#%02x%02x%02x' % tuple(min(255, max(0, c)) for c in new_rgb)
        except:
            return hex_color

    def start_crazy_mode(self):
        """启动疯狂模式"""
        self.hint_label.config(text="别挣扎了，点同意吧")

        # 更改不同意按钮
        self.no_button.config(
            text="抓到我算你厉害",
            bg="#FF0000",
            font=("Arial", 14, "bold"),
            fg="white"
        )

        # 开始自动逃跑
        self.crazy_escape()

    def crazy_escape(self):
        """疯狂模式下的自动逃跑"""
        if self.escape_mode and not self.animating:
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()

            if window_width <= 1:
                window_width = 600
                window_height = 650

            # 更随机的移动
            new_x = random.randint(10, window_width - 130)
            new_y = random.randint(100, window_height - 70)

            # 添加更快的动画
            self.animate_crazy_movement(new_x, new_y)

            # 继续疯狂模式
            self.root.after(1500, self.crazy_escape)

    def animate_crazy_movement(self, target_x, target_y):
        """疯狂模式的动画"""
        start_x = self.button_x
        start_y = self.button_y

        # 创建更快的动画
        steps = 10
        dx = (target_x - start_x) / steps
        dy = (target_y - start_y) / steps

        self.crazy_animation(start_x, start_y, dx, dy, steps, 0)

    def crazy_animation(self, x, y, dx, dy, steps, current_step):
        """疯狂动画效果"""
        if current_step <= steps:
            # 更疯狂的弹跳
            bounce = sin(current_step * pi / steps) * 30

            new_x = x + dx * current_step
            new_y = y + dy * current_step + bounce

            # 随机改变颜色
            colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
            self.no_button.config(bg=random.choice(colors))

            self.no_button.place(x=new_x, y=new_y)
            self.button_x = new_x
            self.button_y = new_y - bounce

            self.root.after(20,
                            lambda: self.crazy_animation(x, y, dx, dy, steps, current_step + 1))

    def show_dog_image(self):
        """显示小狗图片和么么哒"""
        # 停止所有动画
        if self.animation_id:
            self.root.after_cancel(self.animation_id)

        # 清除所有现有组件
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#FFE4E1")

        # 胜利标题
        title_label = tk.Label(
            self.root,
            text="耶耶耶！！你终于同意了！",
            font=("Arial", 24, "bold"),
            fg="#FF69B4",
            bg="#FFE4E1"
        )
        title_label.pack(pady=20)

        # 显示逃跑统计
        if self.escape_count > 0:
            stats_label = tk.Label(
                self.root,
                text=f"你让按钮逃跑了 {self.escape_count} 次才同意！",
                font=("Arial", 14),
                fg="#FF4500",
                bg="#FFE4E1"
            )
            stats_label.pack(pady=10)
        else:
            stats_label = tk.Label(
                self.root,
                text=f"居然直接同意了！！太好了！",
                font=("Arial", 14),
                fg="#FF4500",
                bg="#FFE4E1"
            )
            stats_label.pack(pady=10)

        # 创建小狗显示
        self.create_animated_dog()

        # 重新开始按钮
        restart_button = tk.Button(
            self.root,
            text="再玩一次",
            font=("Arial", 16),
            fg="white",
            bg="#FF69B4",
            command=self.create_main_question,
            width=15,
            height=2,
            cursor="hand2"
        )
        restart_button.pack(pady=30)

        # 退出按钮
        exit_button = tk.Button(
            self.root,
            text="退出",
            font=("Arial", 14),
            fg="white",
            bg="#808080",
            command=self.root.quit,
            width=12,
            height=1
        )
        exit_button.pack(pady=10)

    def create_animated_dog(self):
        """创建动画小狗"""
        # 使用更复杂的ASCII艺术
        dog_frames = [
            """
              / \\__
             (    @\\___
             /         O
            /   (_____/
           /_____/   U
            """,
            """
              / \\__
             (    @\\___
             /         O
            /   (_____/
           /_____/   U
            🐾
            """,
            """
              / \\__
             (    @\\___
             /         O
            /   (_____/
           /_____/   U
              🐾 🐾
            """
        ]

        # 创建小狗显示区域
        dog_container = tk.Frame(self.root, bg="#FFE4E1")
        dog_container.pack(pady=20)

        self.dog_label = tk.Label(
            dog_container,
            text=dog_frames[0],
            font=("Courier", 16),
            fg="#8B4513",
            bg="#FFE4E1"
        )
        self.dog_label.pack()

        # 添加小狗动画
        self.animate_dog(dog_frames, 0)

        # 么么哒文字
        love_label = tk.Label(
            self.root,
            text="周五见！️下班我来接你！",
            font=("Arial", 22, "bold"),
            fg="#FF1493",
            bg="#FFE4E1"
        )
        love_label.pack(pady=20)

        # 底部信息
        info_label = tk.Label(
            self.root,
            text="凭借密码：\njiangjiang0927\n领取圣诞礼物",
            font=("Arial", 16),
            fg="#333333",
            bg="#FFE4E1",
            wraplength=500
        )
        info_label.pack(pady=20)

    def animate_dog(self, frames, index):
        """小狗动画"""
        self.dog_label.config(text=frames[index % len(frames)])
        self.root.after(500, lambda: self.animate_dog(frames, index + 1))


def main():
    root = tk.Tk()
    app = LoveApp(root)

    # 设置窗口居中
    window_width = 600
    window_height = 650
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # 禁止调整窗口大小
    root.resizable(False, False)

    # 设置窗口图标（如果有）
    try:
        root.iconbitmap('heart.ico')
    except:
        pass

    # 运行应用程序
    root.mainloop()


if __name__ == "__main__":
    main()
