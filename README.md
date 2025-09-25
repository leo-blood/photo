# 图片水印添加程序使用说明

## 功能描述
这个程序可以读取图片的EXIF信息中的拍摄时间，并将其作为水印添加到图片上。

## 安装依赖
```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法
```bash
python photo_watermark.py "图片目录路径"
```

### 高级用法
```bash
python photo_watermark.py "图片目录路径" --font-size 30 --color red --position top-left
```

## 参数说明

- `input_dir`: 输入图片目录路径（必需）
- `--font-size`: 字体大小，默认24
- `--color`: 水印颜色，默认white
- `--position`: 水印位置，可选值：
  - `top-left`: 左上角
  - `top-right`: 右上角
  - `bottom-left`: 左下角
  - `bottom-right`: 右下角（默认）
  - `center`: 居中
  - `top-center`: 顶部居中
  - `bottom-center`: 底部居中

## 支持的图片格式
- JPG/JPEG
- PNG
- TIFF/TIF
- BMP

## 输出说明
- 处理后的图片会保存在 `原目录名_watermark` 子目录中
- 水印文本格式为：`YYYY年MM月DD日`
- 如果图片没有EXIF拍摄时间信息，会使用文件修改时间
- 水印会添加阴影效果以提高可读性

## 示例
```bash
# 处理D:\photos目录下的所有图片，使用默认设置
python photo_watermark.py "D:\photos"

# 处理图片，字体大小30，红色水印，位置在左上角
python photo_watermark.py "D:\photos" --font-size 30 --color red --position top-left
```
