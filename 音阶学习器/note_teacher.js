class NoteStudyHelper {
    constructor() {
        this.initData();
        this.initCanvas();
        this.addEventListeners();
        this.resizeHandler();
        this.generateQuestion();
    }

    initData() {
        this.notesData = {
            '高音谱号': {
                '第一线': { '音名': 'E4', '位置': 80, '钢琴键': 40 },
                '第一间': { '音名': 'F4', '位置': 70, '钢琴键': 41 },
                '第二线': { '音名': 'G4', '位置': 60, '钢琴键': 43 },
                '第二间': { '音名': 'A4', '位置': 50, '钢琴键': 45 },
                '第三线': { '音名': 'B4', '位置': 40, '钢琴键': 47 },
                '第三间': { '音名': 'C5', '位置': 30, '钢琴键': 48 },
                '第四线': { '音名': 'D5', '位置': 20, '钢琴键': 50 },
                '第四间': { '音名': 'E5', '位置': 10, '钢琴键': 52 },
                '第五线': { '音名': 'F5', '位置': 0, '钢琴键': 53 }
            },
            '低音谱号': {
                '第一线': { '音名': 'G2', '位置': 80, '钢琴键': 31 },
                '第一间': { '音名': 'A2', '位置': 70, '钢琴键': 33 },
                '第二线': { '音名': 'B2', '位置': 60, '钢琴键': 35 },
                '第二间': { '音名': 'C3', '位置': 50, '钢琴键': 36 },
                '第三线': { '音名': 'D3', '位置': 40, '钢琴键': 38 },
                '第三间': { '音名': 'E3', '位置': 30, '钢琴键': 40 },
                '第四线': { '音名': 'F3', '位置': 20, '钢琴键': 41 },
                '第四间': { '音名': 'G3', '位置': 10, '钢琴键': 43 },
                '第五线': { '音名': 'A3', '位置': 0, '钢琴键': 45 }
            }
        };

        this.pianoKeys = {
            'G2': 31, 'A2': 33, 'B2': 35,
            'C3': 36, 'D3': 38, 'E3': 40, 'F3': 41, 'G3': 43, 'A3': 45, 'B3': 47,
            'C4': 48, 'D4': 50, 'E4': 52, 'F4': 53, 'G4': 55, 'A4': 57, 'B4': 59,
            'C5': 60, 'D5': 62, 'E5': 64, 'F5': 65
        };

        this.currentClef = '高音谱号';
        this.currentPosition = null;
    }

    initCanvas() {
        this.staffCanvas = document.getElementById('staffCanvas');
        this.staffCtx = this.staffCanvas.getContext('2d');
        this.pianoCanvas = document.getElementById('pianoCanvas');
        this.pianoCtx = this.pianoCanvas.getContext('2d');
    }
    addEventListeners() {
        window.addEventListener('resize', () => this.resizeHandler());
        document.getElementById('nextBtn').addEventListener('click', () => this.generateQuestion());
    }
    resizeHandler() {
        const container = document.querySelector('.container');
        const containerWidth = container.clientWidth;
        const containerHeight = container.clientHeight;

        this.staffCanvas.width = containerWidth;
        this.staffCanvas.height = containerHeight * 0.5;

        this.pianoCanvas.width = containerWidth;
        this.pianoCanvas.height = containerHeight * 0.3;

        this.drawStaff();
        this.drawPiano();
    }
    drawStaff() {
        const ctx = this.staffCtx;
        ctx.clearRect(0, 0, this.staffCanvas.width, this.staffCanvas.height);

        // 调整两个谱表的起始位置，增加间距
        const yStarts = [this.staffCanvas.height * 0.15, this.staffCanvas.height * 0.6];
        
        // 绘制五线谱线条
        yStarts.forEach(yStart => {
            for (let i = 0; i < 5; i++) {
                const y = yStart + i * 20;
                ctx.beginPath();
                ctx.moveTo(50, y);
                ctx.lineTo(this.staffCanvas.width - 50, y);
                ctx.strokeStyle = 'black';
                ctx.stroke();
            }
        });

        // 调整谱号位置
        ctx.font = '70px Arial';
        ctx.fillText('𝄞', 60, yStarts[0] + 68);
        ctx.font = '53px Arial';
        ctx.fillText('𝄢', 60, yStarts[1] + 43);

        // 如果有当前音符，绘制它
        // 删除在画布上绘制问题文字的代码
        if (this.currentPosition) {
            const yStart = this.currentClef === '高音谱号' ? 
                          this.staffCanvas.height * 0.15 : 
                          this.staffCanvas.height * 0.6;
            const yPosition = yStart + this.notesData[this.currentClef][this.currentPosition]['位置'];
            this.drawNote(yPosition);
        }
    }
    generateQuestion() {
        this.currentClef = Math.random() < 0.5 ? '高音谱号' : '低音谱号';
        const positions = Object.keys(this.notesData[this.currentClef]);
        this.currentPosition = positions[Math.floor(Math.random() * positions.length)];
        this.currentNote = this.notesData[this.currentClef][this.currentPosition]['音名'];

        // 更新问题文字
        document.getElementById('question').textContent = '请选择这个音符的音名：';

        this.drawStaff();
        this.drawPiano();
        this.createOptions();
    }
    drawNote(yPosition) {
        const ctx = this.staffCtx;
        const xPosition = 200;
        const lineSpacing = 20; // 五线谱线间距
        
        // 判断音符是否在线上（通过位置计算）
        const isOnLine = (yPosition - 40) % lineSpacing === 0;
        
        if (isOnLine) {
            // 在线上时，音符大小稍小，确保线穿过音符中心
            const noteSize = lineSpacing * 0.7;
            ctx.beginPath();
            ctx.ellipse(xPosition, yPosition, noteSize/2, noteSize/2.5, Math.PI/4, 0, Math.PI * 2);
            ctx.fill();
        } else {
            // 在线间时，音符大小等于线间距
            const noteSize = lineSpacing;
            ctx.beginPath();
            ctx.ellipse(xPosition, yPosition, noteSize/2, noteSize/2.5, Math.PI/4, 0, Math.PI * 2);
            ctx.fill();
        }
        
        // 绘制音符竖线
        ctx.beginPath();
        ctx.lineWidth = 2;
        ctx.moveTo(xPosition + lineSpacing/2, yPosition);
        ctx.lineTo(xPosition + lineSpacing/2, yPosition - 60);
        ctx.stroke();
        ctx.lineWidth = 1;
    }
    drawPiano(highlightKey = null) {
        const ctx = this.pianoCtx;
        ctx.clearRect(0, 0, this.pianoCanvas.width, this.pianoCanvas.height);

        const whiteKeyWidth = Math.min(this.pianoCanvas.width / 21, 40);
        const whiteKeyHeight = this.pianoCanvas.height * 0.8;
        const blackKeyWidth = whiteKeyWidth * 0.65;
        const blackKeyHeight = whiteKeyHeight * 0.6;

        const totalWidth = whiteKeyWidth * Object.keys(this.pianoKeys).length;
        const startX = (this.pianoCanvas.width - totalWidth) / 2;

        // 绘制白键
        Object.entries(this.pianoKeys).forEach(([note, _], index) => {
            const x = startX + index * whiteKeyWidth;
            const isHighlighted = highlightKey && note === this.currentNote;
            
            ctx.fillStyle = isHighlighted ? 'yellow' : 'white';
            ctx.strokeStyle = 'black';
            ctx.fillRect(x, 0, whiteKeyWidth, whiteKeyHeight);
            ctx.strokeRect(x, 0, whiteKeyWidth, whiteKeyHeight);

            ctx.fillStyle = 'black';
            ctx.font = '12px Arial';
            ctx.fillText(note, x + whiteKeyWidth/4, whiteKeyHeight - 10);
        });

        // 绘制黑键
        Object.entries(this.pianoKeys).forEach(([note, keyNumber], index) => {
            if (index < Object.keys(this.pianoKeys).length - 1) {
                const nextNote = Object.entries(this.pianoKeys)[index + 1][0];
                const nextKeyNumber = this.pianoKeys[nextNote];
                
                if (nextKeyNumber - keyNumber === 2) {
                    const x = startX + index * whiteKeyWidth + whiteKeyWidth - blackKeyWidth/2;
                    const blackNote = `${note[0]}#${note[1]}`;
                    const isHighlighted = highlightKey && blackNote === this.currentNote;
                    
                    ctx.fillStyle = isHighlighted ? 'yellow' : 'black';
                    ctx.fillRect(x, 0, blackKeyWidth, blackKeyHeight);
                    ctx.strokeStyle = 'black';
                    ctx.strokeRect(x, 0, blackKeyWidth, blackKeyHeight);
                }
            }
        });

        // 标记中央C
        const centralCIndex = Object.keys(this.pianoKeys).indexOf('C4');
        if (centralCIndex !== -1) {
            const x = startX + centralCIndex * whiteKeyWidth;
            ctx.fillStyle = 'red';
            ctx.font = '10px Arial';
            ctx.fillText('中央C', x + whiteKeyWidth/4, whiteKeyHeight + 15);
        }
    }
    createOptions() {
        const optionsContainer = document.getElementById('options');
        optionsContainer.innerHTML = '';

        const allNotes = Object.values(this.notesData[this.currentClef]).map(data => data['音名']);
        const correctAnswer = this.currentNote;
        
        const options = allNotes.filter(note => note !== correctAnswer)
            .sort(() => Math.random() - 0.5)
            .slice(0, 3)
            .concat([correctAnswer])
            .sort(() => Math.random() - 0.5);
    
        options.forEach(option => {
            const button = document.createElement('button');
            button.className = 'option-btn';
            button.textContent = option;
            // 同时支持点击和触摸
            const handleSelect = () => this.checkAnswer(option);
            button.onclick = handleSelect;
            button.ontouchend = (e) => {
                e.preventDefault();
                handleSelect();
            };
            optionsContainer.appendChild(button);
        });
    }
    checkAnswer(userAnswer) {
        const isCorrect = userAnswer === this.currentNote;
        alert(isCorrect ? 
            `正确！\n这个音符是${this.currentNote}，位于${this.currentClef}的${this.currentPosition}` :
            `错误。\n正确答案是：${this.currentNote}\n位于${this.currentClef}的${this.currentPosition}`
        );
        this.drawPiano(true);
    }
}

// 初始化应用
window.onload = () => new NoteStudyHelper();