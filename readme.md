# Gadio Video

![sample](https://static.gcores.com/assets/25c9a8fc027ac16ba3e7fe996551f828.png)

|Platform|Test Result|
|:---:|:---:|
|Windows|[![Build status](https://rabbitism.visualstudio.com/GadioVideo/_apis/build/status/GadioVideo-Python%20Windows%20Test)](https://rabbitism.visualstudio.com/GadioVideo/_build/latest?definitionId=2)|
|macOS|[![Build status](https://rabbitism.visualstudio.com/GadioVideo/_apis/build/status/GadioVideo-Python%20macOS)](https://rabbitism.visualstudio.com/GadioVideo/_build/latest?definitionId=1)|

本脚本的作用是利用[机核网](https://www.gcores.com)的图文电台时间轴信息自动生成视频。

## 运行环境

python 3.11

## 使用说明

### 安装依赖

```bash
pip3 install -r requirements.txt
```

### 运行示例

以 `https://www.gcores.com/radios/107884` 中的电台为例：

如果想要生成视频可运行

```bash
# 直接生成最新一期电台的视频
python gcores.py
# 生成id为107884的电台的视频
python gcores.py 107884
# 跳过爬虫直接用已下载的图片生成107884的视频
python gcores.py 107884 -s

```

此外
如果想单独爬取文本和图片不生成视频，可运行

```bash
# 爬取id为107884的电台文本和图片
python crawler.py 107884
#只爬取文本 不下载图片
python crawler.py 107884 -t
```

图片/音频等暂存于`.\cache\107884\`中。图片的名称为图片在视频中最初出现的秒数。

生成的视频文件位于 `output` 文件夹内

### 更改配置

修改`config.py`中的参数可以修改如下配置

|参数|含义|示例|注释|
|:---:|:---|:---:|:---|
|fps|帧率|2|
|width|视频宽度|1920|
|height|视频高度|1080|
|title_font_size|标题字体大小|53|
|content_font_size|正文字体大小|36|
|gcores_title_color|标题字体颜色|(255,255,255,246)|
|gcores_content_color|正文字体颜色|(255,255,255,205)|
|background_color|背景颜色|#FFFFFF|
|title_font|标题字体|./gadio/utils/PingFang-Heavy.ttf|如果使用系统自带字体，直接写字体文件名|
|content_font|正文字体|./gadio/utils/PingFang-Medium.ttf|如果使用系统自带字体，直接写字体文件名|
|gcores_logo_name|logo图片|./gadio/utils/gcores.png|logo文件应放在utils文件夹下|
|test|测试模式|False|在测试模式下之生成前10段视频，最长不超过200秒|
|start_offset|片头偏移量|5|最终的文字时间轴偏移量|

尺寸和实例见下图

![sample](doc/sample1.png)
![sample](doc/sample2.png)
![sample](doc/sample3.png)

视频示例请参考

[哔哩哔哩](https://www.bilibili.com/video/av59856563)
