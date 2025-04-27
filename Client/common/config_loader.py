import json
import os
import sys
from typing import Any, Dict, Optional

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
        
        # 1. 当前工作目录下的config文件夹
        paths.append(os.path.join(os.getcwd(), 'config', f'{self.config_name}.json'))
        
        # 2. 脚本所在目录下的config文件夹
        if getattr(sys, 'frozen', False):
            # 如果是打包后的可执行文件
            base_path = os.path.dirname(sys.executable)
        else:
            # 如果是开发环境
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        paths.append(os.path.join(base_path, 'config', f'{self.config_name}.json'))
        
        # 3. 用户数据目录下的config文件夹
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
            
        return paths

    def load(self) -> Dict[str, Any]:
        """
        加载配置文件
        按优先级尝试从不同位置加载
        :return: 配置数据
        """
        for path in self.config_paths:
            try:
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        self.config = json.load(f)
                        return self.config
            except Exception as e:
                print(f"加载配置文件 {path} 失败: {e}")
                continue
                
        # 如果所有路径都加载失败，使用默认配置
        print(f"警告: 未能加载配置文件 {self.config_name}.json，使用默认配置")
        self.config = self.default_config.copy()
        return self.config

    def save(self, config: Dict[str, Any] = None, path: Optional[str] = None) -> bool:
        """
        保存配置到文件
        :param config: 要保存的配置数据，如果为None则保存当前配置
        :param path: 保存路径，如果为None则使用第一个可用路径
        :return: 是否保存成功
        """
        if config is not None:
            self.config = config
            
        if self.config is None:
            print("错误: 没有可保存的配置数据")
            return False
            
        save_path = path
        if save_path is None:
            # 使用第一个可写的路径
            for p in self.config_paths:
                try:
                    os.makedirs(os.path.dirname(p), exist_ok=True)
                    save_path = p
                    break
                except Exception:
                    continue
                    
        if save_path is None:
            print("错误: 没有可用的保存路径")
            return False
            
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
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