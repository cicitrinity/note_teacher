import requests
from PIL import Image
import io
import os

def download_and_process_clefs():
    # 创建resources目录（如果不存在）
    os.makedirs('resources', exist_ok=True)
    
    # 下载图片
    urls = {
        'treble': 'https://musescore.org/sites/musescore.org/files/treble_clef.png',
        'bass': 'https://musescore.org/sites/musescore.org/files/bass_clef.png'
    }
    
    for clef_type, url in urls.items():
        try:
            # 下载图片
            response = requests.get(url)
            img = Image.open(io.BytesIO(response.content))
            
            # 转换为RGBA（如果不是）
            img = img.convert('RGBA')
            
            # 调整大小
            if clef_type == 'treble':
                img = img.resize((60, 120))
            else:
                img = img.resize((40, 80))
            
            # 保存处理后的图片
            img.save(f'resources/{clef_type}_clef.png')
            print(f"Successfully processed {clef_type} clef")
            
        except Exception as e:
            print(f"Error processing {clef_type} clef: {e}")

if __name__ == "__main__":
    download_and_process_clefs() 