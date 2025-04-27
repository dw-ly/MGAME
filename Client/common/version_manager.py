import json
import os
from datetime import datetime
from typing import Tuple, Dict, Any
from .config_loader import ConfigLoader
from .logger import info, error

class Version:
    def __init__(self, major: int, minor: int, patch: int, build: str = None):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.build = build or datetime.now().strftime("%Y%m%d")
        
    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}-{self.build}"
        
    def __eq__(self, other: 'Version') -> bool:
        return (self.major == other.major and 
                self.minor == other.minor and 
                self.patch == other.patch)
                
    def __lt__(self, other: 'Version') -> bool:
        return (self.major < other.major or 
                (self.major == other.major and self.minor < other.minor) or
                (self.major == other.major and self.minor == other.minor and self.patch < other.patch))

class VersionManager:
    def __init__(self):
        self.config_loader = ConfigLoader('version', {
            "version": {
                "major": 1,
                "minor": 0,
                "patch": 0,
                "build": datetime.now().strftime("%Y%m%d"),
                "description": "初始版本"
            },
            "compatibility": {
                "min_version": "1.0.0",
                "max_version": "1.9.9"
            },
            "update": {
                "check_url": "",
                "auto_check": True,
                "check_interval": 86400
            }
        })
        self.load_version()
        
    def load_version(self) -> None:
        """加载版本信息"""
        try:
            config = self.config_loader.load()
            version_info = config["version"]
            self.current_version = Version(
                major=version_info["major"],
                minor=version_info["minor"],
                patch=version_info["patch"],
                build=version_info.get("build")
            )
            self.description = version_info.get("description", "")
            
            compat = config["compatibility"]
            self.min_version = self._parse_version_string(compat["min_version"])
            self.max_version = self._parse_version_string(compat["max_version"])
            
            self.update_config = config["update"]
            info(f"当前版本: {self.current_version}, 描述: {self.description}")
            
        except Exception as e:
            error(f"加载版本信息失败: {e}")
            # 使用默认版本
            self.current_version = Version(1, 0, 0)
            self.description = "初始版本"
            self.min_version = Version(1, 0, 0)
            self.max_version = Version(1, 9, 9)
            self.update_config = {"check_url": "", "auto_check": True, "check_interval": 86400}
            
    def _parse_version_string(self, version_str: str) -> Version:
        """解析版本字符串，如 "1.0.0" """
        try:
            major, minor, patch = map(int, version_str.split('.'))
            return Version(major, minor, patch)
        except Exception as e:
            error(f"解析版本字符串失败 {version_str}: {e}")
            return Version(1, 0, 0)
            
    def check_compatibility(self, other_version: Version) -> Tuple[bool, str]:
        """检查版本兼容性"""
        if other_version < self.min_version:
            return False, f"版本过低，最低要求 {self.min_version}"
        if other_version > self.max_version:
            return False, f"版本过高，最高支持 {self.max_version}"
        return True, "版本兼容"
        
    def check_update(self) -> Tuple[bool, str]:
        """检查更新"""
        if not self.update_config["check_url"]:
            return False, "未配置更新检查地址"
            
        try:
            # TODO: 实现实际的更新检查逻辑
            return False, "当前已是最新版本"
        except Exception as e:
            error(f"检查更新失败: {e}")
            return False, f"检查更新失败: {e}"
            
    def save_version(self) -> bool:
        """保存版本信息"""
        config = {
            "version": {
                "major": self.current_version.major,
                "minor": self.current_version.minor,
                "patch": self.current_version.patch,
                "build": self.current_version.build,
                "description": self.description
            },
            "compatibility": {
                "min_version": f"{self.min_version.major}.{self.min_version.minor}.{self.min_version.patch}",
                "max_version": f"{self.max_version.major}.{self.max_version.minor}.{self.max_version.patch}"
            },
            "update": self.update_config
        }
        return self.config_loader.save(config)

# 全局版本管理器实例
version_manager = VersionManager() 