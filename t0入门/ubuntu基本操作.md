# ubuntu 基本操作

##路径

	cd - 	//表示 换回上前一次文件夹
	cd ..  	//表示 换回上一级文件夹
	cd ~ 	//表示 换回当前用户更目录
	cd / 	//表示 进入用户权限的根目录下（最大的更目录。）
	在文件资源管理器中 Ctrl+L获取文件路径

## ubuntu 文件的颜色
使用Ubuntu的ls命令时候，常常会出现各种颜色的文件名及文件夹名，大家记住常用的几个就OK了，具体的查看的话可以使用命令"dircolors -p"来输出所有配色代表的意义。

- 蓝 色：文件夹 
- 红色：压缩文件  
- 绿色：可执行文件  
- 白色：文本文件
- 红色闪烁：错误的符号链接
- 淡蓝色：符号链接
- 黄色：设备文件
- 灰色:其它文件

## 文件夹tree
使用tree前需要安装

	sudo apt install tree

常用命令：

	tree -L 1	//只显示1级目录
	tree -L 2	//只显示2级以上目录
	tree -L 3 
