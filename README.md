<!--
 * @Author: SunHebin dwlyshb@163.com
 * @Date: 2025-04-27 09:08:36
 * @LastEditors: SunHebin dwlyshb@163.com
 * @LastEditTime: 2025-04-27 09:40:51
 * @FilePath: \MGAME\README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# 文字选择养成游戏

这是一个基于Python和Pygame的文字选择养成类游戏框架。玩家可以通过不同的选择来培养角色，影响角色的属性和故事发展。

## 环境设置

### Windows系统

1. 创建虚拟环境：
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\activate
```

### Linux/Mac系统

1. 创建虚拟环境：
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 功能特点

- 角色属性系统（力量、智力、魅力、健康、金钱）
- 事件选择系统
- 物品系统
- 关系系统
- 存档系统
- 基于天数的游戏进程

## 运行游戏

```bash
python main.py
```

## 游戏说明

1. 开始新游戏时，需要输入角色名称
2. 每天都会遇到不同的事件，需要做出选择
3. 选择会影响角色的属性和后续事件
4. 游戏持续30天
5. 可以随时保存游戏进度

## 项目结构

- `main.py`: 游戏主程序
- `character.py`: 角色类
- `event.py`: 事件系统
- `game_manager.py`: 游戏管理器
- `events.json`: 事件数据
- `requirements.txt`: 项目依赖

## 扩展建议

1. 添加更多的事件和选择分支
2. 增加更多的角色属性
3. 添加成就系统
4. 增加更多的游戏结局
5. 添加音效和背景音乐
6. 优化UI界面

## 注意事项

1. 确保在虚拟环境中运行游戏
2. 如果遇到依赖问题，可以尝试重新安装：
```bash
pip install --upgrade -r requirements.txt
```
3. 退出虚拟环境：
```bash
deactivate
``` 