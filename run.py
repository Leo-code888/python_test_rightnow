""""""
"""
项目入口，主程序
收集用例，运行用例，生成报告
"""
import os
import pytest
from config import path
from datetime import datetime

# pytest 收集用例
# 如何放到 reports 路径中
# TODO:报告+时间戳：避免报告重名被覆盖

# 获取现在的时间戳
ts = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
# print(ts)
report_file_name = "report" + ts + ".html"

# 获取测试报告存储目录
report_dir = path.reports_path
# 拼接文件
report_file = os.path.join(report_dir, report_file_name)

pytest.main(["--html={}".format(report_file)])

# 尽量不要右击运行，要用命令行运行,因为后面基本不用pycharm运行，会用jenkins
# TODO: python run.py
