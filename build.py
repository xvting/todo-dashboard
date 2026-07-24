#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TODO Dashboard Builder
读取所有工作区的 TODO.md 文件，生成静态 HTML 看板
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

# 使用相对路径，支持任何平台
CENTRAL_WORKSPACE = Path(__file__).parent
WORKSPACES_FILE = CENTRAL_WORKSPACE / "WORKSPACES.md"


def parse_workspaces_index():
    """解析 WORKSPACES.md 获取所有工作区列表"""
    workspaces = []
    
    if not WORKSPACES_FILE.exists():
        print(f"警告: {WORKSPACES_FILE} 不存在")
        return workspaces
    
    with open(WORKSPACES_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配表格行：| 工作区名 | 路径 | 说明 | 状态 |
    pattern = r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'
    
    for match in re.finditer(pattern, content):
        name = match.group(1).strip()
        path = match.group(2).strip()
        description = match.group(3).strip()
        status = match.group(4).strip()
        
        # 跳过表头
        if name == '工作区' or '---' in name:
            continue
        
        # 提取路径（去除反引号）
        path = path.replace('`', '').strip()
        
        workspaces.append({
            'name': name,
            'path': path,
            'description': description,
            'status': status
        })
    
    return workspaces


def parse_todo_file(todo_path):
    """解析单个 TODO.md 文件"""
    if not os.path.exists(todo_path):
        print(f"警告: {todo_path} 不存在")
        return None
    
    with open(todo_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取项目名称
    title_match = re.search(r'^#\s+TODO\s*-\s*(.+)$', content, re.MULTILINE)
    project_name = title_match.group(1).strip() if title_match else '未命名项目'
    
    # 提取最后更新时间
    update_match = re.search(r'>\s*最后更新:\s*(.+)$', content, re.MULTILINE)
    last_update = update_match.group(1).strip() if update_match else '未知'
    
    sections = []
    
    # 解析三个状态区
    status_sections = [
        ('进行中', r'##\s+🔴\s+进行中(.*?)(?=##\s+🟡|$)', '进行中'),
        ('待办', r'##\s+🟡\s+待办(.*?)(?=##\s+🟢|$)', '待办'),
        ('已完成', r'##\s+🟢\s+已完成(.*?)$', '已完成')
    ]
    
    for status_name, pattern, status_key in status_sections:
        section_match = re.search(pattern, content, re.DOTALL)
        if not section_match:
            continue
        
        section_content = section_match.group(1)
        tasks = parse_tasks(section_content)
        
        if tasks:
            sections.append({
                'status': status_key,
                'title': '',  # 可以在这里添加子标题
                'tasks': tasks
            })
    
    return {
        'name': project_name,
        'last_update': last_update,
        'sections': sections
    }


def parse_tasks(section_content):
    """解析任务列表"""
    tasks = []
    
    # 匹配任务行：- [ ] 或 - [x]
    task_pattern = r'^-\s+\[([ x])\]\s+(.+)$'
    
    for line in section_content.split('\n'):
        line = line.strip()
        match = re.match(task_pattern, line)
        if not match:
            continue
        
        is_completed = match.group(1) == 'x'
        task_text = match.group(2).strip()
        
        # 解析任务内容
        task = parse_task_content(task_text, is_completed)
        tasks.append(task)
    
    return tasks


def parse_task_content(task_text, is_completed):
    """解析任务文本，提取描述、优先级、日期、标签"""
    
    # 已完成的任务可能有删除线
    strikethrough_match = re.search(r'~~(.+?)~~', task_text)
    if strikethrough_match:
        description = strikethrough_match.group(1).strip()
    else:
        description = task_text
    
    # 提取所有日期
    dates = re.findall(r'`(\d{4}-\d{2}-\d{2})`', task_text)
    
    # 根据任务状态解析日期
    created_date = None
    due_date = None
    completed_date = None
    
    if is_completed:
        # 已完成任务：第一个日期是创建日期，第二个是完成日期
        if len(dates) >= 1:
            created_date = dates[0]
        if len(dates) >= 2:
            completed_date = dates[1]
    else:
        # 未完成任务：第一个日期是创建日期，第二个是截止日期
        if len(dates) >= 1:
            created_date = dates[0]
        if len(dates) >= 2:
            due_date = dates[1]
    
    # 提取优先级
    priority_match = re.search(r'`(P[0-3])`', task_text)
    priority = priority_match.group(1) if priority_match else None
    
    # 提取标签
    tags = re.findall(r'`#(\w+)`', task_text)
    
    # 清理描述（移除优先级、日期、标签）
    description = re.sub(r'`P[0-3]`', '', description)
    description = re.sub(r'`\d{4}-\d{2}-\d{2}`', '', description)
    description = re.sub(r'`#\w+`', '', description)
    description = re.sub(r'~~|~~', '', description)
    description = description.strip()
    
    return {
        'text': description,
        'priority': priority,
        'createdDate': created_date,
        'dueDate': due_date,
        'completedDate': completed_date,
        'tags': tags,
        'completed': is_completed
    }


def build_dashboard():
    """构建看板"""
    print("🔍 扫描工作区...")
    workspaces_info = parse_workspaces_index()
    
    print(f"✅ 发现 {len(workspaces_info)} 个工作区")
    
    dashboard_data = {
        'workspaces': [],
        'generated_at': datetime.now().isoformat()
    }
    
    for ws_info in workspaces_info:
        print(f"📖 读取: {ws_info['name']}")
        todo_data = parse_todo_file(ws_info['path'])
        
        if todo_data:
            dashboard_data['workspaces'].append(todo_data)
        else:
            print(f"⚠️  跳过: {ws_info['name']} (无法解析)")
    
    # 读取 HTML 模板
    template_path = CENTRAL_WORKSPACE / "dashboard.html"
    with open(template_path, 'r', encoding='utf-8') as f:
        html_template = f.read()
    
    # 注入数据
    json_data = json.dumps(dashboard_data, ensure_ascii=False, indent=2)
    html_output = html_template.replace('__TODO_DATA_PLACEHOLDER__', json_data)
    
    # 输出到 dist 目录
    dist_dir = CENTRAL_WORKSPACE / "dist"
    dist_dir.mkdir(exist_ok=True)
    
    output_path = dist_dir / "index.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print(f"\n✅ 看板已生成: {output_path}")
    print(f"📊 总计: {len(dashboard_data['workspaces'])} 个工作区")
    
    # 统计任务数
    total_tasks = sum(
        sum(len(section['tasks']) for section in ws['sections'])
        for ws in dashboard_data['workspaces']
    )
    print(f"📝 总计: {total_tasks} 个任务")


if __name__ == '__main__':
    build_dashboard()
