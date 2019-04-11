# Gadio Video Generator

本代码库的作用是利用gcores网站的图文电台时间轴信息自动生成视频。

## 使用说明

### 安装依赖包

```bash
pip install -r requirements.txt
```

### 运行示例

如果需要生成 https://www.gcores.com/radios/107884 中的电台的视频，在控制台中运行：

```bash
python main.py 107884
```
图片暂存于`.\resource\107884\`中，视频合成后会自动清除。图片的名称为图片在视频中最初出现的秒数。由于暂不支持gif图片，因此gif图片在视频合成后不会清除，请根据图片名添加到视频相应位置。

视频文件是`.\output\107884.mp4`

### 更改配置
修改`config.py`中的参数可以修改如下配置

|参数|含义|示例|
|:---:|:---|:---:|
|fps|帧率|3|
|width|视频宽度|1280|
|height|视频高度|720|
|picture_width|图片宽度（图片过高时会以高度为准）|400|
|title_font_size|标题字体大小| 48|
|content_font_size|正文字体大小| 28|
|margin|边界宽度|60|
|font|字体|msyh.ttc|

尺寸实例见下图

![sample](doc\Sample.jpg)

## TODO

* 支持 gif
* 合并音频