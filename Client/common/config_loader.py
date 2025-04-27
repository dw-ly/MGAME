import json
import os
import sys
from typing import Any, Dict, Optional
from .logger import info

class ConfigLoader:
    """通用配置文件加载器"""
    
    def __init__(self, config_name: str, default_config: Dict[str, Any] = None):
        """
        初始化配置加载器
        :param config_name: 配置文件名（不含扩展名）
        :param default_config: 默认配置，当配置文件不存在或加载失败时使用
        """
        self.config_name = config_name
        self.default_config = default_config or {}
        self.config = None
        self.config_paths = self._get_config_paths()
        
    def _get_config_paths(self) -> list:
        """
        获取可能的配置文件路径列表
        按优先级从高到低排序
        """
        paths = []
        
        # 1. 如果是打包后的可执行文件，从资源目录加载
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
            paths.append(os.path.join(base_path, 'config', f'{self.config_name}.json'))
        
        # 2. 当前工作目录下的config文件夹
        paths.append(os.path.join(os.getcwd(), 'config', f'{self.config_name}.json'))
        
        # 3. 脚本所在目录下的config文件夹
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        paths.append(os.path.join(base_path, 'config', f'{self.config_name}.json'))
        
        # 4. 用户数据目录下的config文件夹
        if sys.platform == 'win32':
            appdata = os.getenv('APPDATA')
            if appdata:
                paths.append(os.path.join(appdata, 'MGAME', 'config', f'{self.config_name}.json'))
        elif sys.platform == 'darwin':
            home = os.path.expanduser('~')
            paths.append(os.path.join(home, 'Library', 'Application Support', 'MGAME', 'config', f'{self.config_name}.json'))
        else:  # linux
            home = os.path.expanduser('~')
            paths.append(os.path.join(home, '.config', 'MGAME', f'{self.config_name}.json'))
            
        info(f"配置文件搜索路径: {paths}")
        return paths
        
    def load(self) -> Dict[str, Any]:
        """
        加载配置文件
        如果所有路径都找不到配置文件，则返回默认配置
        """
        if self.config is not None:
            return self.config
            
        for path in self.config_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        self.config = json.load(f)
                    info(f"成功加载配置文件: {path}")
                    return self.config
                except Exception as e:
                    info(f"加载配置文件失败 {path}: {e}")
                    continue
                    
        info(f"未找到配置文件，使用默认配置")
        self.config = self.default_config.copy()
        return self.config
        
    def save(self, config: Dict[str, Any]) -> bool:
        """
        保存配置到文件
        优先保存到用户数据目录，如果失败则尝试保存到当前目录
        """
        self.config = config
        
        # 优先尝试保存到用户数据目录
        save_paths = []
        if sys.platform == 'win32':
            appdata = os.getenv('APPDATA')
            if appdata:
                save_path = os.path.join(appdata, 'MGAME', 'config')
                save_paths.append(save_path)
                
        # 如果不是打包环境，也可以保存到当前目录
        if not getattr(sys, 'frozen', False):
            save_paths.append(os.path.join(os.getcwd(), 'config'))
            
        for save_path in save_paths:
            try:
                os.makedirs(save_path, exist_ok=True)
                file_path = os.path.join(save_path, f'{self.config_name}.json')
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, ensure_ascii=False, indent=4)
                info(f"成功保存配置文件: {file_path}")
                return True
            except Exception as e:
                info(f"保存配置文件失败 {save_path}: {e}")
                continue
                
        info("保存配置文件失败：所有路径都无法写入")
        return False

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项
        :param key: 配置键名
        :param default: 默认值
        :return: 配置值
        """
        if self.config is None:
            self.load()
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        设置配置项
        :param key: 配置键名
        :param value: 配置值
        """
        if self.config is None:
            self.load()
        self.config[key] = value 