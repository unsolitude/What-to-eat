# 今天吃什么 🍽️

[![Release](https://img.shields.io/github/v/release/YOUR_USERNAME/今天吃什么?style=flat-square)](https://github.com/YOUR_USERNAME/今天吃什么/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)

一个简单实用的随机点餐小程序，帮你解决"今天吃什么"的世纪难题！

## ✨ 功能特点

- **加权随机抽取** - 支持为每个餐品设置权重，权重越高被选中概率越大
- **三餐分类管理** - 早餐、午餐、晚餐独立管理，互不干扰
- **数据持久化** - 自动保存餐品数据，下次打开自动加载
- **简洁界面** - 基于 tkinter 开发，界面简洁易用

## 📥 下载安装

### 方式一：直接运行 exe（推荐）

1. 从 [Releases](./dist) 页面下载 `今天吃什么.exe`
2. 双击运行即可，无需安装 Python 环境

### 方式二：运行 Python 源码

1. 确保已安装 Python 3.6+
2. 下载源码
3. 运行 `python main.py`

## 📖 使用方法

### 1. 选择餐类

程序顶部有三个单选按钮：
- 🌅 早餐
- ☀️ 午餐
- 🌙 晚餐

点击切换不同的餐类，每个餐类的餐品数据独立存储。

### 2. 添加餐品

1. 在"餐品名称"输入框中输入餐品名称
2. 在"权重"输入框中设置权重（默认为1）
3. 点击"添加餐品"按钮或按回车键

**权重说明：**
- 权重越大，被随机选中的概率越高
- 例如：面条权重1，米饭权重3，则米饭被选中的概率是面条的3倍

### 3. 管理餐品

- **删除选中** - 选中列表中的餐品后点击删除
- **清空列表** - 清空当前餐类的所有餐品

### 4. 随机抽取

点击"🎲 开始抽取"按钮，程序会根据权重随机选择一个餐品。

## 💾 数据存储

餐品数据保存在程序同目录下的 `meals_data.json` 文件中。

数据格式示例：
```json
{
  "breakfast": [
    {"name": "包子", "weight": 1},
    {"name": "豆浆油条", "weight": 2}
  ],
  "lunch": [
    {"name": "面条", "weight": 1},
    {"name": "米饭", "weight": 3}
  ],
  "dinner": [
    {"name": "火锅", "weight": 2},
    {"name": "烧烤", "weight": 1}
  ]
}
```

## 🔧 自行打包

如需自行打包成 exe 文件：

1. 安装 PyInstaller：
   ```bash
   pip install pyinstaller
   ```

2. 运行打包命令：
   ```bash
   pyinstaller --onefile --windowed --name "今天吃什么" main.py
   ```

3. 打包完成后，exe 文件位于 `dist` 目录

或者直接运行 `build.bat` 脚本（Windows）。

## ❓ 常见问题

**Q: 程序打不开怎么办？**

A: 请确保系统已安装 Visual C++ Redistributable。如果仍有问题，尝试以管理员身份运行。

**Q: 数据丢失了怎么办？**

A: 检查程序目录下是否有 `meals_data.json` 文件。如果文件损坏，可以删除后重新添加餐品。

**Q: 如何备份数据？**

A: 复制 `meals_data.json` 文件即可备份所有餐品数据。

## 📝 更新日志

### v2.0.0
- 新增早餐、午餐、晚餐分类功能
- 三餐数据独立存储
- 自动迁移旧版数据

### v1.0.0
- 初始版本
- 支持加权随机抽取
- 支持数据持久化

## 📄 许可证

MIT License
