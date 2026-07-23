# TODO 管理中心

跨工作区任务管理平台，自动生成静态 HTML 看板。

## 🚀 快速开始

### 本地测试

```bash
# 构建看板
python build.py

# 打开生成的看板
# Windows:
start dist\index.html
# Mac/Linux:
open dist/index.html  # Mac
xdg-open dist/index.html  # Linux
```

### 在线部署

#### 1. 创建 GitHub 仓库

```bash
# 在 GitHub 上创建新仓库（例如：todo-dashboard）
# 不要初始化 README、.gitignore 或 license
```

#### 2. 推送代码到 GitHub

```bash
# 初始化 git（如果还没有）
git init
git add .
git commit -m "Initial commit: TODO dashboard system"

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/todo-dashboard.git
git branch -M main
git push -u origin main
```

#### 3. 启用 GitHub Pages

1. 进入仓库的 **Settings** → **Pages**
2. **Source** 选择 **GitHub Actions**
3. 保存后，每次 push 都会自动部署

#### 4. 访问在线看板

```
https://YOUR_USERNAME.github.io/todo-dashboard/
```

## 📁 项目结构

```
E:\TODO\
├── TODO.md              # 中心工作区待办
├── WORKSPACES.md        # 工作区索引
├── TODO_SPEC.md         # TODO 管理规范
├── AGENTS.md            # Agent 指令
├── dashboard.html       # HTML 模板
├── build.py             # 构建脚本
├── dist/                # 生成的静态文件（自动生成）
│   └── index.html
└── .github/
    └── workflows/
        └── deploy.yml   # GitHub Actions 配置
```

## 🔄 工作流程

```
编辑 TODO.md
    ↓
git add & commit
    ↓
git push
    ↓
GitHub Actions 自动触发
    ↓
运行 build.py 生成 HTML
    ↓
部署到 GitHub Pages
    ↓
浏览器访问在线看板
```

## 🛠️ 技术栈

- **数据存储**: Markdown 文件
- **构建工具**: Python 3.11+
- **托管平台**: GitHub Pages
- **自动化**: GitHub Actions
- **前端**: 纯 HTML/CSS/JavaScript（无框架依赖）

## 📝 功能特性

- ✅ 多工作区聚合展示
- ✅ 按优先级筛选（P0/P1/P2/P3）
- ✅ 实时统计（总数/进行中/待办/已完成）
- ✅ 响应式设计（支持移动端）
- ✅ 逾期任务高亮
- ✅ 标签系统
- ✅ 自动部署

## 🎨 自定义

### 修改样式

编辑 `dashboard.html` 中的 CSS 部分。

### 修改构建逻辑

编辑 `build.py` 脚本。

### 修改工作流

编辑 `.github/workflows/deploy.yml`。

## 📊 工作区管理

### 添加新工作区

1. 在 `WORKSPACES.md` 中添加工作区信息
2. 确保工作区有 `TODO.md` 文件
3. 提交并推送

### 移除工作区

从 `WORKSPACES.md` 中删除对应行即可。

## 🔧 故障排查

### 构建失败

```bash
# 本地测试构建
python build.py

# 查看 GitHub Actions 日志
# 进入仓库的 Actions 页面
```

### 页面未更新

```bash
# 强制清除缓存
# Windows: Ctrl + F5
# Mac: Cmd + Shift + R
```

### 404 错误

- 确认 GitHub Pages 已启用
- 确认部署完成（查看 Actions 日志）
- 等待 1-2 分钟（CDN 缓存）

## 📄 License

MIT

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
