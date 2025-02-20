import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import tkinter as tk
from tkinter import ttk, messagebox, Canvas
import pygame
import json
from datetime import datetime
import random
import time

class ScaleTrainer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("音阶学习器")
        self.root.geometry("1000x800")
        
        # 初始化音频
        pygame.mixer.init()
        
        # 初始化练习数据
        self.current_scale = None
        self.practice_count = 0
        self.correct_count = 0
        self.is_practicing = False
        
        # 音阶数据
        self.scales_data = {
            '初级': {
                'C大调': {'notes': ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']},
                'G大调': {'notes': ['G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F#5', 'G5']},
                'F大调': {'notes': ['F4', 'G4', 'A4', 'Bb4', 'C5', 'D5', 'E5', 'F5']}
            },
            '中级': {
                'D大调': {'notes': ['D4', 'E4', 'F#4', 'G4', 'A4', 'B4', 'C#5', 'D5']},
                'A大调': {'notes': ['A4', 'B4', 'C#5', 'D5', 'E5', 'F#5', 'G#5', 'A5']}
            },
            '高级': {
                '降B大调': {'notes': ['Bb4', 'C5', 'D5', 'Eb5', 'F5', 'G5', 'A5', 'Bb5']},
                '降E大调': {'notes': ['Eb4', 'F4', 'G4', 'Ab4', 'Bb4', 'C5', 'D5', 'Eb5']}
            }
        }
        
        # 加载用户数据
        self.load_user_data()
        
        # 创建界面
        self.create_ui()
        
    def create_ui(self):
        # 主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 难度选择区域
        self.create_difficulty_section()
        
        # 五线谱显示区域
        self.create_staff_section()
        
        # 练习控制区域
        self.create_practice_section()
        
        # 统计信息区域
        self.create_stats_section()
    
    def create_difficulty_section(self):
        difficulty_frame = ttk.LabelFrame(self.main_frame, text="难度设置", padding="10")
        difficulty_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
        
        ttk.Label(difficulty_frame, text="选择难度：").grid(row=0, column=0, padx=5)
        self.level_var = tk.StringVar(value=self.user_data['level'])
        self.level_combo = ttk.Combobox(difficulty_frame, 
                                       textvariable=self.level_var, 
                                       values=list(self.scales_data.keys()))
        self.level_combo.grid(row=0, column=1, padx=5)
        
        ttk.Label(difficulty_frame, text="练习次数：").grid(row=0, column=2, padx=5)
        self.practice_times_var = tk.StringVar(value="10")
        practice_times_entry = ttk.Entry(difficulty_frame, 
                                       textvariable=self.practice_times_var,
                                       width=5)
        practice_times_entry.grid(row=0, column=3, padx=5)
    
    def create_staff_section(self):
        self.staff_frame = ttk.LabelFrame(self.main_frame, text="五线谱", padding="10")
        self.staff_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.staff_canvas = Canvas(self.staff_frame, width=800, height=300, bg='white')
        self.staff_canvas.pack(pady=10)
        
        # 绘制五线谱
        self.draw_staff()
    
    def create_practice_section(self):
        practice_frame = ttk.LabelFrame(self.main_frame, text="练习控制", padding="10")
        practice_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.start_button = ttk.Button(practice_frame, 
                                     text="开始练习", 
                                     command=self.start_practice)
        self.start_button.pack(pady=5)
        
        self.next_button = ttk.Button(practice_frame, 
                                    text="下一个", 
                                    command=self.next_scale,
                                    state='disabled')
        self.next_button.pack(pady=5)
        
        self.scale_label = ttk.Label(practice_frame, 
                                    text="点击开始练习",
                                    font=('Arial', 24))
        self.scale_label.pack(pady=10)
    
    def create_stats_section(self):
        stats_frame = ttk.LabelFrame(self.main_frame, text="统计信息", padding="10")
        stats_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.streak_label = ttk.Label(stats_frame, 
                                    text=f"连续打卡：{self.user_data['streak']}天")
        self.streak_label.pack(side=tk.LEFT, padx=10)
        
        self.progress_label = ttk.Label(stats_frame, 
                                      text="正确率：0%")
        self.progress_label.pack(side=tk.LEFT, padx=10)
    
    def draw_staff(self):
        # 清除画布
        self.staff_canvas.delete("all")
        
        # 绘制五线谱线
        y_start = 100
        for i in range(5):
            y = y_start + i * 20
            self.staff_canvas.create_line(50, y, 750, y, width=1)
        
        # 绘制谱号
        self.staff_canvas.create_text(80, y_start + 40, 
                                    text="𝄞", 
                                    font=("Arial", 48))
        
        # 如果有当前音阶，绘制音符
        if self.current_scale and self.current_scale in self.scales_data[self.level_var.get()]:
            notes = self.scales_data[self.level_var.get()][self.current_scale]['notes']
            x_start = 150
            for i, note in enumerate(notes):
                x = x_start + i * 80
                y = self.get_note_position(note)
                # 绘制音符
                self.staff_canvas.create_oval(x-6, y-6, x+6, y+6, fill='black')
                # 绘制符干
                self.staff_canvas.create_line(x+6, y, x+6, y-40, width=1)
    
    def get_note_position(self, note):
        # 音符位置映射（简化版本）
        note_positions = {
            'C4': 180, 'D4': 170, 'E4': 160, 'F4': 150, 'G4': 140,
            'A4': 130, 'B4': 120, 'C5': 110, 'D5': 100, 'E5': 90,
            'F5': 80, 'G5': 70, 'A5': 60, 'B5': 50,
            'F#4': 150, 'G#4': 140, 'A#4': 130, 'B#4': 120,
            'C#5': 110, 'D#5': 100, 'E#5': 90, 'F#5': 80, 'G#5': 70,
            'Bb4': 130, 'Eb4': 160, 'Ab4': 140, 'Bb5': 50, 'Eb5': 90
        }
        return note_positions.get(note, 140)
    
    def start_practice(self):
        self.is_practicing = True
        self.practice_count = 0
        self.correct_count = 0
        self.next_button.config(state='normal')
        self.start_button.config(state='disabled')
        self.next_scale()
    
    def next_scale(self):
        if not self.is_practicing:
            return
            
        level = self.level_var.get()
        available_scales = list(self.scales_data[level].keys())
        self.current_scale = random.choice(available_scales)
        
        self.scale_label.config(text=self.current_scale)
        self.draw_staff()
        
        # 播放音频
        try:
            pygame.mixer.music.load(f"scales/{self.current_scale}.mp3")
            pygame.mixer.music.play()
        except:
            messagebox.showwarning("提示", "音频文件未找到")
        
        self.practice_count += 1
        max_practices = int(self.practice_times_var.get())
        
        # 更新进度
        self.progress_label.config(text=f"进度：{self.practice_count}/{max_practices}")
        
        # 检查是否完成练习
        if self.practice_count >= max_practices:
            self.finish_practice()
    
    def finish_practice(self):
        self.is_practicing = False
        self.next_button.config(state='disabled')
        self.start_button.config(state='normal')
        
        # 更新打卡记录
        today = datetime.now().strftime('%Y-%m-%d')
        if self.user_data['last_practice'] != today:
            self.user_data['streak'] += 1
            self.user_data['last_practice'] = today
            self.streak_label.config(text=f"连续打卡：{self.user_data['streak']}天")
        
        # 保存用户数据
        self.save_user_data()
        
        # 显示完成信息
        messagebox.showinfo("练习完成", 
                          f"本次练习完成！\n"
                          f"完成度：{self.practice_count}/{self.practice_times_var.get()}")
    
    def load_user_data(self):
        try:
            with open('user_data.json', 'r') as f:
                self.user_data = json.load(f)
        except FileNotFoundError:
            self.user_data = {
                'streak': 0,
                'last_practice': '',
                'level': '初级'
            }
    
    def save_user_data(self):
        with open('user_data.json', 'w') as f:
            json.dump(self.user_data, f)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ScaleTrainer()
    app.run()
    # 在 ScaleTrainer 类中添加以下方法，其他代码保持不变

def create_piano_section(self):
    self.piano_frame = ttk.LabelFrame(self.main_frame, text="钢琴键盘", padding="10")
    self.piano_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")
    
    self.piano_canvas = Canvas(self.piano_frame, width=800, height=150, bg='white')
    self.piano_canvas.pack(pady=10)
    
    # 初始绘制钢琴键盘
    self.draw_piano()

def draw_piano(self):
    # 清除画布
    self.piano_canvas.delete("all")
    
    # 钢琴键的基本尺寸
    white_key_width = 40
    white_key_height = 120
    black_key_width = 24
    black_key_height = 80
    
    # 白键位置数据
    white_keys = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    # 黑键位置数据（相对于白键的偏移）
    black_keys = [0, 1, 3, 4, 5]  # C#, D#, F#, G#, A#
    
    # 绘制两个八度的钢琴键
    for octave in range(2):  # 绘制两个八度
        x_offset = 50 + (octave * 7 * white_key_width)
        
        # 绘制白键
        for i, key in enumerate(white_keys):
            x = x_offset + (i * white_key_width)
            
            # 判断当前音符是否在演奏中
            is_active = False
            if self.current_scale:
                current_note = f"{key}{octave+4}"
                if current_note in self.scales_data[self.level_var.get()][self.current_scale]['notes']:
                    is_active = True
            
            # 绘制白键
            self.piano_canvas.create_rectangle(
                x, 20,
                x + white_key_width, 20 + white_key_height,
                fill='yellow' if is_active else 'white',
                outline='black'
            )
            
            # 添加音名标签
            self.piano_canvas.create_text(
                x + white_key_width/2, 
                20 + white_key_height - 20,
                text=f"{key}{octave+4}"
            )
        
        # 绘制黑键
        for i in black_keys:
            x = x_offset + (i * white_key_width) + (white_key_width - black_key_width/2)
            
            # 判断当前音符是否在演奏中
            is_active = False
            if self.current_scale:
                current_note = f"{white_keys[i]}#{octave+4}"
                if current_note in self.scales_data[self.level_var.get()][self.current_scale]['notes']:
                    is_active = True
            
            self.piano_canvas.create_rectangle(
                x, 20,
                x + black_key_width, 20 + black_key_height,
                fill='yellow' if is_active else 'black'
            )

# 在 create_ui 方法中添加钢琴键盘部分
def create_ui(self):
    # ... 现有的代码 ...
    
    # 添加钢琴键盘显示区域
    self.create_piano_section()

# 在 next_scale 方法中添加钢琴更新
def next_scale(self):
    # ... 现有的代码 ...
    self.draw_piano()  # 更新钢琴显示  