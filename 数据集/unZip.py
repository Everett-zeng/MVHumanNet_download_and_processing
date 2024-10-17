# python unZip.py --input_dir test_mvhuman_data --output_dir extracted_data

import os
import tarfile
import argparse
import shutil

def unzip_data(directory, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历指定目录及其子目录下的所有文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件是否是 .tar.gz 格式
            if file.endswith('.tar.gz'):
                # 构建完整的文件路径
                file_path = os.path.join(root, file)
                print(f'Unzipping {file_path}...')
                # 使用 tarfile 模块解压文件
                with tarfile.open(file_path, "r:gz") as tar:
                    tar.extractall(path=output_dir)
                print(f'Finished unzipping {file_path}')

                # 删除原始压缩文件
                try:
                    os.remove(file_path)
                    print(f'Deleted original file: {file_path}')
                except OSError as e:
                    print(f"Error: {file_path} : {e.strerror}")

if __name__ == '__main__':
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='Unzip .tar.gz files in a directory and delete the originals')
    parser.add_argument('--input_dir', type=str, required=True, help='Directory containing .tar.gz files')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to extract files to')

    # 解析命令行参数
    args = parser.parse_args()

    # 调用函数执行解压
    unzip_data(args.input_dir, args.output_dir)
    print('All .tar.gz files have been unzipped and the originals deleted.')