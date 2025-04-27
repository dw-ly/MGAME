import os
import sys
from typing import Optional
from .logger import info

class ResourceLoader:
    @staticmethod
    def get_resource_path(relative_path: str) -> str:
        """获取资源文件的绝对路径，支持开发环境和打包环境
        
        Args:
            relative_path: 相对于资源目录的路径
            
        Returns:
            str: 资源文件的绝对路径
        """
        if getattr(sys, 'frozen', False):
            # 如果是打包后的可执行文件，从临时目录加载
            base_path = sys._MEIPASS
        else:
            # 开发环境下，使用当前目录
            base_path = os.getcwd()
        
        return os.path.join(base_path, relative_path)
    
    @staticmethod
    def load_font(font_name: str = "SIMHEI.TTF", font_size: int = 24) -> Optional[str]:
        """加载字体文件
        
        Args:
            font_name: 字体文件名
            font_size: 字体大小
            
        Returns:
            str: 字体文件路径，如果找不到则返回None
        """
        # 首先尝试从打包资源目录加载
        font_path = ResourceLoader.get_resource_path(font_name)
        if os.path.exists(font_path):
            info(f"从资源目录加载字体: {font_path}")
            return font_path
            
        # 开发环境下，尝试从多个位置加载
        candidates = [
            font_name,
            os.path.join("Tools", "Package", "language", font_name),
            font_name.lower(),
            "msyh.ttc",
            "msyh.ttf"
        ]
        
        for candidate in candidates:
            if os.path.exists(candidate):
                info(f"从开发环境加载字体: {candidate}")
                return candidate
                
        info("未找到字体文件")
        return None 