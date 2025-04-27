# MGAME

## 目录结构说明

- `UI/` 目录下存放所有UI组件（如InputBox、Button、Popup等），引用方式：
  - `from UI.input_box import InputBox`
  - `from UI.button import StartButton`
  - `from UI.popup import DialogPopup, BannerPopup`
- 其他核心逻辑、管理器、配置等仍在原有目录

## 主要依赖
- pygame >= 2.0
- Python 3.7+

## 运行方式
```bash
python main.py
```

## 说明
- 支持中文输入、弹窗系统模块化、UI组件高度解耦，便于维护和扩展。 