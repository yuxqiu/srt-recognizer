# srt-recognizer
<p align="center">
  <a href="https://github.com/qyxtim/srt-recognizer/blob/master/LICENSE">
    <img height="18px" alt="License" src="https://img.shields.io/github/license/qyxtim/srt-recognizer">
  </a>
  <a href="https://github.com/qyxtim/modern-poetry/graphs/contributors">
    <img height="18px" alt="Contributors" src="https://img.shields.io/github/contributors/qyxtim/srt-recognizer.svg">
  </a>
  <a href="https://github.com/qyxtim/modern-poetry/graphs/contributors">
    <img height="18px" alt="Contributors" src="https://img.shields.io/badge/PR-welcome-green">
  </a>
</p>

srt-recognizer是一个基于cnOCR的硬字幕提取软件，可以将硬字幕导出为纯文本文件和srt文件。

## 项目优点

1. 本地识别：不需要申请额外的API，也不需要安装其它的软件
2. 大小适中：相比其他项目，模型加上软件大小约为130M
3. 准确度较好：cnOCR的识别率能够达到95%左右

## 获取方式

1. 可执行文件：

2. 手动配置：如果你是Mac无法使用exe文件或者是想自己配置的话，可以采用如下的配置方法。

	1. 安装python
	2. 安装cnocr库: `pip install cnocr `
	3. 安装cv2: `pip install cv2`
	4. 愉快使用吧！

## 使用教程

1. 是否需要多行识别？

	如果需要识别带有多行的字幕，建议开启这个功能。如果不需要，可以关闭。关闭之后可以提升识别速度。

2. 是否需要导出为srt

	如果需要导出为srt字幕文件，选择这项功能。如果不需要，软件将默认到处字母内容为txt文件

3. 输入文件地址

	输入文件地址即可，需要加入后缀名

4. 选择字幕区域：在ocr字幕内容之前，软件会打开一个窗口让您选择字幕的区域，为此软件提供了两种框选方式。
	1. 矩形选择
		1. 矩形选择需要左键点击字幕的左上角，右键点击字幕的右下角
		2. 因为不好确定最长的字幕的左上角和右下角位置，使用这项功能有一定几率会导致后面的字幕无法准确识别
	2. 非矩形选择
		1. 左键点击字幕的最上方，右键点击字幕的最下方
		2. 该功能可以准确框选字幕，但有可能会导致识别的字幕带有一些干扰信息。
		3. 推荐使用非矩形选择！
	3. 如果弹出窗口没有字幕，可以按空格跳转到下一帧。选择完成之后按空格键退出选择窗口。
