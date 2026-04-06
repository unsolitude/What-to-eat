#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
今天吃什么 - 随机点餐小程序
使用 tkinter 开发的轻量级桌面工具
支持加权随机抽取和数据持久化
支持早餐、午餐、晚餐分类管理
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os


class FoodRandomApp:
    """随机点餐应用主类"""
    
    # 餐类配置
    MEAL_TYPES = {
        'breakfast': {'name': '🌅 早餐', 'label': '早餐'},
        'lunch': {'name': '☀️ 午餐', 'label': '午餐'},
        'dinner': {'name': '🌙 晚餐', 'label': '晚餐'}
    }
    
    def __init__(self, root):
        """
        初始化应用
        
        Args:
            root: tkinter 主窗口对象
        """
        self.root = root
        self.root.title("今天吃什么")
        self.root.geometry("500x750")
        self.root.resizable(True, True)
        
        # 设置最小窗口大小
        self.root.minsize(400, 650)
        
        # 餐品数据，按餐类分组存储
        # 格式: {'breakfast': [...], 'lunch': [...], 'dinner': [...]}
        self.all_meals = {
            'breakfast': [],
            'lunch': [],
            'dinner': []
        }
        
        # 当前选中的餐类
        self.current_meal_type = tk.StringVar(value='lunch')
        
        # 数据文件路径（与程序同目录）
        self.data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meals_data.json')
        
        # 加载已保存的数据
        self.load_data()
        
        # 创建界面
        self.setup_ui()
        
        # 刷新列表显示
        self.refresh_list()
    
    def setup_ui(self):
        """创建用户界面"""
        # ========== 餐类选择区域 ==========
        meal_type_frame = ttk.LabelFrame(self.root, text="选择餐类", padding=10)
        meal_type_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 单选按钮容器
        radio_frame = ttk.Frame(meal_type_frame)
        radio_frame.pack()
        
        # 创建三个单选按钮
        for meal_type, config in self.MEAL_TYPES.items():
            rb = ttk.Radiobutton(
                radio_frame, 
                text=config['name'], 
                value=meal_type,
                variable=self.current_meal_type, 
                command=self.on_meal_type_change
            )
            rb.pack(side=tk.LEFT, padx=20)
        
        # ========== 输入区域 ==========
        input_frame = ttk.LabelFrame(self.root, text="添加餐品", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 餐品名称输入
        name_frame = ttk.Frame(input_frame)
        name_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(name_frame, text="餐品名称:").pack(side=tk.LEFT)
        self.name_entry = ttk.Entry(name_frame, width=30)
        self.name_entry.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        
        # 权重输入
        weight_frame = ttk.Frame(input_frame)
        weight_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(weight_frame, text="权重(概率):").pack(side=tk.LEFT)
        self.weight_entry = ttk.Entry(weight_frame, width=10)
        self.weight_entry.pack(side=tk.LEFT, padx=10)
        self.weight_entry.insert(0, "1")  # 默认权重为1
        
        ttk.Label(weight_frame, text="(数字越大，被选中概率越高)", foreground="gray").pack(side=tk.LEFT)
        
        # 添加按钮
        add_btn = ttk.Button(input_frame, text="添加餐品", command=self.add_meal)
        add_btn.pack(pady=10)
        
        # 绑定回车键添加餐品
        self.name_entry.bind('<Return>', lambda e: self.add_meal())
        self.weight_entry.bind('<Return>', lambda e: self.add_meal())
        
        # ========== 列表展示区域 ==========
        list_frame = ttk.LabelFrame(self.root, text="餐品列表", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 创建 Treeview 和滚动条
        tree_scroll = ttk.Scrollbar(list_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 定义列
        columns = ('name', 'weight', 'probability')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', 
                                  yscrollcommand=tree_scroll.set)
        
        # 设置列标题和宽度
        self.tree.heading('name', text='餐品名称')
        self.tree.heading('weight', text='权重')
        self.tree.heading('probability', text='概率')
        
        self.tree.column('name', width=200, anchor=tk.CENTER)
        self.tree.column('weight', width=80, anchor=tk.CENTER)
        self.tree.column('probability', width=100, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        tree_scroll.config(command=self.tree.yview)
        
        # ========== 操作按钮区域 ==========
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 删除选中按钮
        delete_btn = ttk.Button(btn_frame, text="删除选中", command=self.delete_selected)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # 清空列表按钮
        clear_btn = ttk.Button(btn_frame, text="清空列表", command=self.clear_all)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # ========== 抽取区域 ==========
        pick_frame = ttk.LabelFrame(self.root, text="随机抽取", padding=10)
        pick_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 结果显示标签
        self.result_label = ttk.Label(pick_frame, text="点击下方按钮开始抽取", 
                                       font=('微软雅黑', 16), foreground='gray')
        self.result_label.pack(pady=10)
        
        # 开始抽取按钮（使用醒目样式）
        style = ttk.Style()
        style.configure('Pick.TButton', font=('微软雅黑', 14, 'bold'))
        
        pick_btn = ttk.Button(pick_frame, text="🎲 开始抽取", 
                              command=self.random_pick, style='Pick.TButton')
        pick_btn.pack(pady=10, ipadx=20, ipady=10)
    
    def get_current_meals(self):
        """获取当前餐类的餐品列表"""
        return self.all_meals.get(self.current_meal_type.get(), [])
    
    def set_current_meals(self, meals):
        """设置当前餐类的餐品列表"""
        self.all_meals[self.current_meal_type.get()] = meals
    
    def get_current_meal_label(self):
        """获取当前餐类的中文名称"""
        meal_type = self.current_meal_type.get()
        return self.MEAL_TYPES.get(meal_type, {}).get('label', '餐品')
    
    def on_meal_type_change(self):
        """餐类切换时的回调函数"""
        # 刷新列表显示
        self.refresh_list()
        # 重置结果显示
        self.result_label.config(text="点击下方按钮开始抽取", foreground='gray',
                                  font=('微软雅黑', 16))
    
    def add_meal(self):
        """添加餐品到列表"""
        name = self.name_entry.get().strip()
        weight_str = self.weight_entry.get().strip()
        meal_label = self.get_current_meal_label()
        
        # 验证餐品名称
        if not name:
            messagebox.showwarning("输入错误", "请输入餐品名称！")
            self.name_entry.focus()
            return
        
        # 验证权重
        try:
            weight = float(weight_str)
            if weight <= 0:
                messagebox.showwarning("输入错误", "权重必须为正数！")
                self.weight_entry.focus()
                return
        except ValueError:
            messagebox.showwarning("输入错误", "请输入有效的数字权重！")
            self.weight_entry.focus()
            return
        
        # 检查是否已存在同名餐品
        current_meals = self.get_current_meals()
        for meal in current_meals:
            if meal['name'] == name:
                messagebox.showwarning("重复添加", f"{meal_label}中已存在 '{name}'！")
                return
        
        # 添加到列表
        current_meals.append({'name': name, 'weight': weight})
        self.set_current_meals(current_meals)
        
        # 刷新显示
        self.refresh_list()
        
        # 保存数据
        self.save_data()
        
        # 清空输入框，准备下次输入
        self.name_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.weight_entry.insert(0, "1")
        self.name_entry.focus()
    
    def delete_selected(self):
        """删除选中的餐品"""
        selected = self.tree.selection()
        meal_label = self.get_current_meal_label()
        
        if not selected:
            messagebox.showinfo("提示", "请先选择要删除的餐品！")
            return
        
        # 确认删除
        if len(selected) == 1:
            item = self.tree.item(selected[0])
            name = item['values'][0]
            confirm = messagebox.askyesno("确认删除", f"确定要从{meal_label}中删除 '{name}' 吗？")
        else:
            confirm = messagebox.askyesno("确认删除", f"确定要从{meal_label}中删除选中的 {len(selected)} 个餐品吗？")
        
        if not confirm:
            return
        
        # 获取要删除的餐品名称
        names_to_delete = []
        for item_id in selected:
            item = self.tree.item(item_id)
            names_to_delete.append(item['values'][0])
        
        # 从数据列表中删除
        current_meals = self.get_current_meals()
        current_meals = [meal for meal in current_meals if meal['name'] not in names_to_delete]
        self.set_current_meals(current_meals)
        
        # 刷新显示
        self.refresh_list()
        
        # 保存数据
        self.save_data()
    
    def clear_all(self):
        """清空当前餐类的所有餐品"""
        current_meals = self.get_current_meals()
        meal_label = self.get_current_meal_label()
        
        if not current_meals:
            messagebox.showinfo("提示", f"{meal_label}列表已经是空的了！")
            return
        
        # 确认清空
        confirm = messagebox.askyesno("确认清空", f"确定要清空{meal_label}的所有餐品吗？此操作不可恢复！")
        
        if not confirm:
            return
        
        # 清空数据
        self.set_current_meals([])
        
        # 刷新显示
        self.refresh_list()
        
        # 保存数据
        self.save_data()
        
        # 重置结果显示
        self.result_label.config(text="点击下方按钮开始抽取", foreground='gray',
                                  font=('微软雅黑', 16))
    
    def random_pick(self):
        """随机抽取一个餐品"""
        current_meals = self.get_current_meals()
        meal_label = self.get_current_meal_label()
        
        if not current_meals:
            messagebox.showwarning("无法抽取", f"请先在{meal_label}中添加一些餐品！")
            return
        
        # 提取名称和权重列表
        names = [meal['name'] for meal in current_meals]
        weights = [meal['weight'] for meal in current_meals]
        
        # 使用加权随机抽取
        result = random.choices(names, weights=weights, k=1)[0]
        
        # 更新界面显示
        self.result_label.config(text=f"🍽️ {result}", foreground='#e74c3c', 
                                  font=('微软雅黑', 24, 'bold'))
        
        # 弹窗显示结果
        messagebox.showinfo("抽取结果", f"今天{meal_label}吃：\n\n🍽️ {result} 🍽️")
    
    def refresh_list(self):
        """刷新列表显示"""
        # 清空现有显示
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        current_meals = self.get_current_meals()
        
        # 计算总权重
        total_weight = sum(meal['weight'] for meal in current_meals)
        
        # 添加所有餐品
        for meal in current_meals:
            # 计算概率百分比
            if total_weight > 0:
                probability = (meal['weight'] / total_weight) * 100
                prob_str = f"{probability:.1f}%"
            else:
                prob_str = "0%"
            
            self.tree.insert('', tk.END, values=(meal['name'], meal['weight'], prob_str))
    
    def migrate_old_data(self, data):
        """
        迁移旧版数据格式
        
        旧格式: {'meals': [...]}
        新格式: {'breakfast': [...], 'lunch': [...], 'dinner': [...]}
        """
        if 'meals' in data:
            # 旧格式，将数据迁移到午餐
            return {
                'breakfast': [],
                'lunch': data['meals'],
                'dinner': []
            }
        return data
    
    def save_data(self):
        """保存数据到 JSON 文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.all_meals, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("保存失败", f"无法保存数据：{str(e)}")
    
    def load_data(self):
        """从 JSON 文件加载数据"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 检查并迁移旧格式数据
                    data = self.migrate_old_data(data)
                    # 确保所有餐类都存在
                    for meal_type in self.MEAL_TYPES.keys():
                        if meal_type not in data:
                            data[meal_type] = []
                    self.all_meals = data
                    # 如果进行了数据迁移，保存新格式
                    self.save_data()
        except json.JSONDecodeError:
            messagebox.showwarning("数据加载", "数据文件格式错误，将使用空列表。")
            self.all_meals = {'breakfast': [], 'lunch': [], 'dinner': []}
        except Exception as e:
            messagebox.showwarning("数据加载", f"无法加载数据：{str(e)}\n将使用空列表。")
            self.all_meals = {'breakfast': [], 'lunch': [], 'dinner': []}


def main():
    """程序入口"""
    root = tk.Tk()
    app = FoodRandomApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
