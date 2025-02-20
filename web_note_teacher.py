import tkinter as tk
from tkinter import ttk, messagebox
import random

class NoteStudyHelper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("五线谱音符学习助手")
        self.root.geometry("1000x900")
        
        # 音符数据
        self.notes_data = {
            '高音谱号': {
                '第一线': {'音名': 'E4', '位置': 130, '钢琴键': 40},
                '第一间': {'音名': 'F4', '位置': 120, '钢琴键': 41},
                '第二线': {'音名': 'G4', '位置': 110, '钢琴键': 43},
                '第二间': {'音名': 'A4', '位置': 100, '钢琴键': 45},
                '第三线': {'音名': 'B4', '位置': 90, '钢琴键': 47},
                '第三间': {'音名': 'C5', '位置': 80, '钢琴键': 48},
                '第四线': {'音名': 'D5', '位置': 70, '钢琴键': 50},
                '第四间': {'音名': 'E5', '位置': 60, '钢琴键': 52},
                '第五线': {'音名': 'F5', '位置': 50, '钢琴键': 53}
            },
            '低音谱号': {
                '第一线': {'音名': 'G2', '位置': 130, '钢琴键': 31},
                '第一间': {'音名': 'A2', '位置': 120, '钢琴键': 33},
                '第二线': {'音名': 'B2', '位置': 110, '钢琴键': 35},
                '第二间': {'音名': 'C3', '位置': 100, '钢琴键': 36},
                '第三线': {'音名': 'D3', '位置': 90, '钢琴键': 38},
                '第三间': {'音名': 'E3', '位置': 80, '钢琴键': 40},
                '第四线': {'音名': 'F3', '位置': 70, '钢琴键': 41},
                '第四间': {'音名': 'G3', '位置': 60, '钢琴键': 43},
                '第五线': {'音名': 'A3', '位置': 50, '钢琴键': 45}
            }
        }
        
        # 钢琴键数据
        self.piano_keys = {
            'G2': 31, 'A2': 33, 'B2': 35,
            'C3': 36, 'D3': 38, 'E3': 40, 'F3': 41, 'G3': 43, 'A3': 45, 'B3': 47,
            'C4': 48, 'D4': 50, 'E4': 52, 'F4': 53, 'G4': 55, 'A4': 57, 'B4': 59,
            'C5': 60, 'D5': 62, 'E5': 64, 'F5': 65
        }
        
        self.current_clef = '高音谱号'  # 当前谱号
        self.current_position = None    # 当前位置
        self.create_ui()
        
    def create_ui(self):
        # 创建五线谱显示区域
        self.staff_frame = ttk.LabelFrame(self.root, text="五线谱", padding="10")
        self.staff_frame.pack(fill="x", padx=10, pady=5)
        
        self.staff_canvas = tk.Canvas(self.staff_frame, width=900, height=400, bg='white')
        self.staff_canvas.pack(pady=5)
        
        # 创建问题标签
        self.question_label = ttk.Label(self.root, text="请选择这个音符的音名：", font=("Arial", 14))
        self.question_label.pack(pady=10)
        
        # 创建选项按钮区域
        self.options_frame = ttk.Frame(self.root)
        self.options_frame.pack(pady=10)
        
        # 创建钢琴键盘显示区域
        self.piano_frame = ttk.LabelFrame(self.root, text="钢琴键盘", padding="10")
        self.piano_frame.pack(fill="x", padx=10, pady=5)
        
        self.piano_canvas = tk.Canvas(self.piano_frame, width=900, height=150, bg='white')
        self.piano_canvas.pack(pady=5)
        
        # 开始练习按钮
        ttk.Button(self.root, text="下一题", command=self.generate_question).pack(pady=10)
        
        # 初始化显示
        self.draw_staff()
        self.draw_piano()
        self.generate_question()
    
    def draw_staff(self):
        self.staff_canvas.delete("all")
        
        # 绘制两组五线谱
        y_starts = [50, 250]
        
        for y_start in y_starts:
            # 绘制五条线
            for i in range(5):
                y = y_start + i * 20
                self.staff_canvas.create_line(50, y, 850, y, width=1)
        
        try:
            # 使用正确的 Unicode 编码绘制谱号
            treble_clef = chr(0x1D11E)  # 高音谱号
            bass_clef = chr(0x1D122)    # 低音谱号
            
            # 尝试使用不同的字体显示谱号
            fonts_to_try = [
                ("Segoe UI Symbol", 70),  # 减小高音谱号字体大小
                ("Arial Unicode MS", 70),
                ("Times New Roman", 70)
            ]
            
            for font_name, size in fonts_to_try:
                try:
                    # 绘制高音谱号
                    self.staff_canvas.create_text(
                        80, y_starts[0] + 35,
                        text=treble_clef,
                        font=(font_name, size)
                    )
                    # 绘制低音谱号 - 调整位置
                    self.staff_canvas.create_text(
                        80, y_starts[1] +23,  # 改回原来的位置
                        text=bass_clef,
                        font=(font_name, 53)  # 低音谱号使用更小的字号
                    )
                    break
                except:
                    continue
                    
        except:
            # 如果 Unicode 显示失败，使用备用方案
            self.staff_canvas.create_text(80, y_starts[0] + 40, text="G", font=("Arial", 36, "bold"))
            self.staff_canvas.create_text(80, y_starts[1] - 80, text="F", font=("Arial", 36, "bold"))
        
        # 如果当前有音符要显示，在对应的五线谱上绘制
        if self.current_position:
            y_offset = 0 if self.current_clef == '高音谱号' else 200
            y_position = self.notes_data[self.current_clef][self.current_position]['位置'] + y_offset
            self.draw_note(y_position)
            
            # 只在需要时绘制加线
            if self.current_clef == '低音谱号':
                note_x = 200  # 音符的x位置
                if self.current_position == '下加一线':
                    y = y_starts[1] + 5 * 20 + 10
                    self.staff_canvas.create_line(note_x - 10, y, note_x + 10, y, width=1)
                elif self.current_position == '上加一线':
                    y = y_starts[1] - 10
                    self.staff_canvas.create_line(note_x - 10, y, note_x + 10, y, width=1)
                elif self.current_position == '上加二线':
                    y = y_starts[1] - 30
                    self.staff_canvas.create_line(note_x - 10, y, note_x + 10, y, width=1)
    
    def draw_note(self, y_position):
        x_position = 200
        self.staff_canvas.create_oval(x_position-6, y_position-6, 
                                    x_position+6, y_position+6, 
                                    fill='black')
        self.staff_canvas.create_line(x_position+6, y_position, 
                                    x_position+6, y_position-40, 
                                    width=1)
    
    def draw_piano(self, highlight_key=None):
        self.piano_canvas.delete("all")
        
        # 基本参数
        x_start = 50
        white_key_width = 40
        white_key_height = 120
        black_key_width = 26
        black_key_height = 80
        
        # 白键
        white_keys = list(self.piano_keys.keys())
        
        # 计算中央C的位置
        center_x = self.piano_canvas.winfo_reqwidth() / 2
        total_width = len(white_keys) * white_key_width
        x_start = center_x - (total_width / 2)
        
        # 绘制白键
        for i, note in enumerate(white_keys):
            x = x_start + i * white_key_width
            # 判断是否需要高亮
            current_note = self.notes_data[self.current_clef][self.current_position]['音名'] if self.current_position else None
            fill_color = 'yellow' if highlight_key and note == current_note else 'white'
            
            self.piano_canvas.create_rectangle(x, 10, 
                                             x + white_key_width, white_key_height,
                                             fill=fill_color, outline='black')
            self.piano_canvas.create_text(x + white_key_width/2, 
                                        white_key_height - 20,
                                        text=note)
            
            if note == 'C4':
                self.piano_canvas.create_text(x + white_key_width/2,
                                            white_key_height + 10,
                                            text="中央C",
                                            fill='red',
                                            font=('Arial', 10, 'bold'))
        
        # 绘制黑键
        for i, note in enumerate(white_keys[:-1]):  # 最后一个白键后面不需要黑键
            current_note = note
            next_note = white_keys[i + 1]
            
            # 检查是否需要绘制黑键
            if abs(self.piano_keys[next_note] - self.piano_keys[current_note]) == 2:
                x = x_start + i * white_key_width + white_key_width - black_key_width/2
                black_note = f"{current_note[0]}#{current_note[1]}"  # 例如：C4 -> C#4
                
                # 判断是否需要高亮
                fill_color = 'yellow' if highlight_key and black_note == current_note else 'black'
                
                self.piano_canvas.create_rectangle(x, 10, 
                                                 x + black_key_width, black_key_height,
                                                 fill=fill_color)
    
    def create_options(self, correct_answer):
        # 清除现有按钮
        for widget in self.options_frame.winfo_children():
            widget.destroy()
            
        # 获取当前谱号的所有音名
        all_notes = [data['音名'] for data in self.notes_data[self.current_clef].values()]
        all_notes.remove(correct_answer)
        options = random.sample(all_notes, 3)
        options.append(correct_answer)
        random.shuffle(options)
        
        for option in options:
            ttk.Button(self.options_frame, 
                      text=option,
                      width=10,
                      command=lambda o=option: self.check_answer(o)).pack(side=tk.LEFT, padx=5)
    
    def generate_question(self):
        # 随机选择谱号
        self.current_clef = random.choice(['高音谱号', '低音谱号'])
        
        # 随机选择一个位置
        positions = list(self.notes_data[self.current_clef].keys())
        self.current_position = random.choice(positions)
        
        # 重绘五线谱
        self.draw_staff()
        
        # 绘制音符
        y_position = self.notes_data[self.current_clef][self.current_position]['位置']
        y_offset = 0 if self.current_clef == '高音谱号' else 200
        self.draw_note(y_position + y_offset)
        
        # 创建选项按钮
        correct_answer = self.notes_data[self.current_clef][self.current_position]['音名']
        self.create_options(correct_answer)
        
        # 更新钢琴键盘显示
        self.draw_piano()
    
    def check_answer(self, user_answer):
        correct_answer = self.notes_data[self.current_clef][self.current_position]['音名']
        if user_answer == correct_answer:
            messagebox.showinfo("正确", 
                              f"回答正确！\n这个音符是{correct_answer}，位于{self.current_clef}的{self.current_position}")
        else:
            messagebox.showerror("错误", 
                               f"回答错误。\n正确答案是：{correct_answer}\n位于{self.current_clef}的{self.current_position}")
        
        # 高亮显示正确的钢琴键
        self.draw_piano(highlight_key=True)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = NoteStudyHelper()
    app.run()