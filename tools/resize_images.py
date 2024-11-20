from PIL import Image
import os
from pathlib import Path

def resize_image(image_path, target_size=(120, 120)):
    """调整图片大小到指定尺寸，小图等比放大，大图等比缩小"""
    try:
        with Image.open(image_path) as img:
            # 转换图片模式为 RGBA，保持透明度
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # 获取原始尺寸
            width, height = img.size
            
            # 计算缩放比例
            scale = min(target_size[0] / width, target_size[1] / height)
            
            # 如果图片小于目标尺寸，则放大；如果大于目标尺寸，则缩小
            new_width = int(width * scale)
            new_height = int(height * scale)
            
            # 使用LANCZOS算法进行缩放（放大或缩小）
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 创建完全透明背景的新图片
            new_img = Image.new('RGBA', target_size, (255, 255, 255, 0))
            
            # 计算居中位置
            pos_x = (target_size[0] - new_width) // 2
            pos_y = (target_size[1] - new_height) // 2
            
            # 将调整后的图片粘贴到新图片中心
            new_img.paste(resized_img, (pos_x, pos_y), resized_img)
            
            # 保存图片，覆盖原文件
            new_img.save(image_path, 'PNG')
            print(f"成功处理: {image_path} (原始尺寸: {width}x{height} -> 新尺寸: {new_width}x{new_height})")
            
    except Exception as e:
        print(f"处理失败 {image_path}: {str(e)}")

def process_directory(directory):
    """处理指定目录下的所有图片文件"""
    # 支持的图片格式
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
    
    # 确保目录存在
    directory = Path(directory)
    if not directory.exists():
        print(f"目录不存在: {directory}")
        return
    
    # 遍历目录下的所有文件
    count = 0
    for file_path in directory.glob('*'):
        if file_path.suffix.lower() in image_extensions:
            resize_image(file_path)
            count += 1
    
    print(f"\n处理完成！共处理 {count} 个图片文件")

def main():
    # 指定要处理的图片目录
    image_dir = "themes/WebStack-Hugo/static/assets/images/logos"
    process_directory(image_dir)

if __name__ == "__main__":
    main()