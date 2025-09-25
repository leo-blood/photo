#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片水印添加程序
读取图片EXIF信息中的拍摄时间，并将其作为水印添加到图片上
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
import datetime
from pathlib import Path
import argparse


class PhotoWatermark:
    def __init__(self):
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp'}
        
    def get_exif_data(self, image_path):
        """获取图片的EXIF数据"""
        try:
            with Image.open(image_path) as image:
                exif_data = image._getexif()
                if exif_data is not None:
                    exif_dict = {}
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        exif_dict[tag] = value
                    return exif_dict
        except Exception as e:
            print(f"读取EXIF数据时出错 {image_path}: {e}")
        return None
    
    def get_shooting_date(self, exif_data):
        """从EXIF数据中提取拍摄日期"""
        if not exif_data:
            return None
            
        # 尝试不同的日期字段
        date_fields = ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized']
        
        for field in date_fields:
            if field in exif_data:
                try:
                    date_str = exif_data[field]
                    # 解析日期字符串 (格式通常是 "YYYY:MM:DD HH:MM:SS")
                    if isinstance(date_str, str) and len(date_str) >= 10:
                        date_part = date_str.split(' ')[0]  # 取日期部分
                        date_obj = datetime.datetime.strptime(date_part, '%Y:%m:%d')
                        return date_obj.strftime('%Y年%m月%d日')
                except Exception as e:
                    print(f"解析日期时出错: {e}")
                    continue
        
        return None
    
    def get_watermark_text(self, image_path):
        """获取水印文本（拍摄日期）"""
        exif_data = self.get_exif_data(image_path)
        shooting_date = self.get_shooting_date(exif_data)
        
        if shooting_date:
            return shooting_date
        else:
            # 如果没有找到拍摄日期，使用文件修改时间
            try:
                file_time = os.path.getmtime(image_path)
                date_obj = datetime.datetime.fromtimestamp(file_time)
                return date_obj.strftime('%Y年%m月%d日')
            except:
                return datetime.datetime.now().strftime('%Y年%m月%d日')
    
    def calculate_position(self, image_size, text_size, position):
        """计算水印文本的位置"""
        img_width, img_height = image_size
        text_width, text_height = text_size
        
        # 添加一些边距
        margin = 20
        
        if position == 'top-left':
            return (margin, margin)
        elif position == 'top-right':
            return (img_width - text_width - margin, margin)
        elif position == 'bottom-left':
            return (margin, img_height - text_height - margin)
        elif position == 'bottom-right':
            return (img_width - text_width - margin, img_height - text_height - margin)
        elif position == 'center':
            return ((img_width - text_width) // 2, (img_height - text_height) // 2)
        elif position == 'top-center':
            return ((img_width - text_width) // 2, margin)
        elif position == 'bottom-center':
            return ((img_width - text_width) // 2, img_height - text_height - margin)
        else:
            return (margin, margin)  # 默认左上角
    
    def add_watermark(self, image_path, output_path, font_size=24, color='white', position='bottom-right'):
        """为单张图片添加水印"""
        try:
            # 打开图片
            with Image.open(image_path) as image:
                # 转换为RGB模式（如果需要）
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # 创建绘图对象
                draw = ImageDraw.Draw(image)
                
                # 获取水印文本
                watermark_text = self.get_watermark_text(image_path)
                
                # 尝试加载字体
                try:
                    # 尝试使用系统字体
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    try:
                        # 尝试使用其他常见字体
                        font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", font_size)  # 微软雅黑
                    except:
                        try:
                            font = ImageFont.truetype("C:/Windows/Fonts/simsun.ttc", font_size)  # 宋体
                        except:
                            # 使用默认字体
                            font = ImageFont.load_default()
                
                # 获取文本尺寸
                bbox = draw.textbbox((0, 0), watermark_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                # 计算位置
                text_position = self.calculate_position(image.size, (text_width, text_height), position)
                
                # 添加文本阴影效果（可选）
                shadow_offset = 2
                shadow_color = 'black'
                
                # 绘制阴影
                shadow_position = (text_position[0] + shadow_offset, text_position[1] + shadow_offset)
                draw.text(shadow_position, watermark_text, font=font, fill=shadow_color)
                
                # 绘制主文本
                draw.text(text_position, watermark_text, font=font, fill=color)
                
                # 保存图片
                image.save(output_path, quality=95)
                print(f"已处理: {os.path.basename(image_path)} -> {os.path.basename(output_path)}")
                
        except Exception as e:
            print(f"处理图片时出错 {image_path}: {e}")
    
    def process_directory(self, input_dir, font_size=24, color='white', position='bottom-right'):
        """批量处理目录中的所有图片"""
        input_path = Path(input_dir)
        
        if not input_path.exists():
            print(f"错误: 目录不存在 {input_dir}")
            return
        
        # 创建输出目录
        output_dir = input_path.parent / f"{input_path.name}_watermark"
        output_dir.mkdir(exist_ok=True)
        
        print(f"输入目录: {input_dir}")
        print(f"输出目录: {output_dir}")
        print(f"字体大小: {font_size}")
        print(f"颜色: {color}")
        print(f"位置: {position}")
        print("-" * 50)
        
        # 查找所有支持的图片文件
        image_files = []
        for ext in self.supported_formats:
            image_files.extend(input_path.glob(f"*{ext}"))
            image_files.extend(input_path.glob(f"*{ext.upper()}"))
        
        if not image_files:
            print("未找到支持的图片文件")
            return
        
        print(f"找到 {len(image_files)} 个图片文件")
        
        # 处理每个图片文件
        for image_file in image_files:
            output_file = output_dir / image_file.name
            self.add_watermark(str(image_file), str(output_file), font_size, color, position)
        
        print(f"\n处理完成！共处理 {len(image_files)} 个文件")
        print(f"输出目录: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description='图片水印添加程序')
    parser.add_argument('input_dir', help='输入图片目录路径')
    parser.add_argument('--font-size', type=int, default=24, help='字体大小 (默认: 24)')
    parser.add_argument('--color', default='white', help='水印颜色 (默认: white)')
    parser.add_argument('--position', 
                       choices=['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center', 'top-center', 'bottom-center'],
                       default='bottom-right', 
                       help='水印位置 (默认: bottom-right)')
    
    args = parser.parse_args()
    
    watermark_tool = PhotoWatermark()
    watermark_tool.process_directory(args.input_dir, args.font_size, args.color, args.position)


if __name__ == "__main__":
    main()
