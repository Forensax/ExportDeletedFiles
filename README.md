# ExportDeletedFiles

基于SleuthKit套件的删除文件恢复工具，支持恢复DD、E01、AFF镜像文件中NTFS系统的已删除文件，使用的SleuthKit套件的版本为4.12.1。

## 使用方式

安装python

```
https://www.python.org/downloads/
```

下载源码

```
git clone https://github.com/Forensax/ExportDeletedFiles.git
```

```
cd ExportDeletedFiles
```

运行main.py

```
python main.py
```

输入镜像位置

![image-20240305103818824](.\image\image-20240305103818824.png)

回车运行

![image-20240305104652302](.\image\image-20240305104652302.png)

运行完成后可以查看日志

![image-20240305104403910](.\image\image-20240305104403910.png)

导出的文件在export文件夹中，以NTFS分区的偏移地址作为文件夹名称，里面是这个分区导出的被删除文件

![image-20240305104556070](.\image\image-20240305104556070.png)

![image-20240305104609252](.\image\image-20240305104609252.png)

微信公众号：取证大喇叭Forensax

![image-20240305111715959](.\image\image-20240305111715959.png)

