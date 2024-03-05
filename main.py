import os
import subprocess
from datetime import datetime

def main():
    # 获取镜像文件地址
    image_path = input("请输入镜像文件地址：")

    # 检查.mmls.exe是否存在
    mmls_path = os.path.join(os.path.dirname(__file__), "bin", "mmls.exe")
    if not os.path.exists(mmls_path):
        print("错误：mmls.exe 文件不存在")
        return

    # 构建命令
    mmls_command = [mmls_path, "-B", image_path]

    # 执行mmls命令
    try:
        mmls_result = subprocess.run(mmls_command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("mmls命令执行失败：", e)
        return

    # 解析mmls命令输出结果
    lines = mmls_result.stdout.split('\n')
    basic_partitions_starts = []  # 存储Basic data partition的Start列内容

    for line in lines:
        if "Basic data partition" in line:
            parts = line.split(None, 4)
            start = parts[2]
            basic_partitions_starts.append(start)

    # 生成日志文件名
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_folder = os.path.join(os.path.dirname(__file__), "log")
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    log_file = os.path.join(log_folder, f"file_{current_time}.log")

    # 创建export文件夹
    export_folder = os.path.join(os.path.dirname(__file__), "export")
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    # 写入结果到日志文件
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("MMLS输出日志：\n")  # 添加日志开头
        f.write(mmls_result.stdout)
        f.write("\n\nBasic data partition的Start列内容：\n")
        for start in basic_partitions_starts:
            f.write(start + "\n")

        f.write("\n\nFLS输出日志：\n")  # 添加FLS日志开头

        # 调用fls命令
        fls_path = os.path.join(os.path.dirname(__file__), "bin", "fls.exe")
        for start in basic_partitions_starts:
            fls_command = [fls_path, "-prd", "-f", "ntfs", "-o", start, image_path]
            try:
                fls_result = subprocess.run(fls_command, capture_output=True, text=True, check=True)
                f.write(f"\n\nStart地址: {start}\n")
                f.write(fls_result.stdout)

                # 调用icat命令
                icat_path = os.path.join(os.path.dirname(__file__), "bin", "icat.exe")
                for line in fls_result.stdout.split('\n'):
                    parts = line.split()
                    if len(parts) >= 4:
                        inode = parts[2]
                        filename_full = ' '.join(parts[3:])
                        # 去掉最后的冒号
                        inode = inode[:-1] if inode.endswith(":") else inode
                        # 解析文件名
                        filename = os.path.basename(filename_full)
                        icat_command = [icat_path, "-o", start, image_path, inode]
                        try:
                            icat_result = subprocess.run(icat_command, capture_output=True)
                            export_file_path = os.path.join(export_folder, filename)
                            with open(export_file_path, "wb") as icat_file:
                                icat_file.write(icat_result.stdout)
                        except subprocess.CalledProcessError as e:
                            print(f"icat命令执行失败：{e}")

            except subprocess.CalledProcessError as e:
                print(f"fls命令执行失败：{e}")

    print(f"结果已保存到 {log_file}")

if __name__ == "__main__":
    main()
