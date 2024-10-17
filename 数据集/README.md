# 操作步骤

### 1.下载压缩包

打开*download_links.py*选择要下载的部分，复制对应一条语句到终端。

### 2.修改输出文件夹位置

    python download_tool_mvhuman.py --data_name MVHumanNet_Part_01 --url https://cuhko365.sharepoint.com/:f:/s/SSE_GAP-Lab/EsVY9MmilqBAtvM5vvsrFPkBgqUWRMQOn3H3OV3GgnwaFg?e=zSgxQI --download_folder ./zipData

执行代码。

### 3.暂停下载

如果让代码下载完的话会造成数据量过大，硬盘直接下满，来不及清理。平均一个压缩文件1.5G，解压缩后约2.6G。

当下载到100个的时候会结束下载，输入ctrl+c也能提前结束下载，保证有足够的硬盘空间。

**非正常终止**  的时候一般最后一个文件没有下载完全，所以我们这里可以选择删除最后下载的这个文件保证我们内容完整，同时我们还需要将./zipData/.hash/zipData中对应的最后一个文件删除，因为下次下载会更具这个里面的文件来判断是否已经下载过了。

### 4.解压

执行unZip.py文件对./zipData内的压缩文件解压。

    python unZip.py --input_dir ./zipData --output_dir ./raw_imgs

### 5.处理图像

将我们待处理的人像图和对应的掩码图结合去除图片的环境因素。

    python ImageProcessing.py --input_dir ./raw_imgs --output_dir ./new_imgs
# MVHumanNet_download_and_processing
