import os

from logger_setup import setup_logger

logger=setup_logger(__name__)
def get_script_absolute_path(file_path,relative_path):
    """
    将相对路径转换为基于当前脚本所在目录的绝对路径。


    """
    # 获取当前脚本所在的目录
    script_dir = os.path.dirname(os.path.abspath(file_path))
    logger.info(f"script_dir:{script_dir}")
    # 返回绝对路径
    return os.path.abspath(os.path.join(script_dir, relative_path)).replace('\\', '/')


# 示例使用
