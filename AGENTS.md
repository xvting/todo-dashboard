# 中心工作区 Agent 指令

## 工作区职责

这是一个 **TODO 管理中心**，负责：
- 管理临时任务（`TODO.md`）
- 维护工作区索引（`WORKSPACES.md`）
- 定义 TODO 管理规范（`TODO_SPEC.md`）
- 初始化新工作区并纳入管理体系

## 核心文件

| 文件 | 用途 |
|---|---|
| `TODO.md` | 中心工作区的临时任务清单 |
| `WORKSPACES.md` | 所有工作区的索引（路径 + 规范对齐状态） |
| `TODO_SPEC.md` | TODO 管理规范（各工作区遵循的标准） |

## 任务生命周期

```
临时任务 (本工作区 TODO.md)
    ↓ 升级为项目
独立工作区 (各工作区自己的 TODO.md)
    ↓ 注册到索引
中心可见 (WORKSPACES.md)
```

## 工作区局部 Skill

| Skill | 位置 | 职责 |
|---|---|---|
| `workspace-init` | `.agents/skills/workspace-init/` | 初始化新工作区（仅本工作区可见） |

**全局 Skill**（所有工作区自动生效）：
- `todo-manager`：位于 `C:\Users\xvtin\.agents\skills\todo-manager\`，指导各工作区 Agent 如何管理 TODO

## 初始化新工作区流程

当用户要求初始化新工作区时，按以下步骤执行：

1. **创建 `TODO.md`**：按 `TODO_SPEC.md` 规范创建标准待办文件
2. **创建 `AGENTS.md`**：包含 TODO 管理规范引用和职责要求
3. **分析项目**（如果有内容）：识别技术栈、发现问题、生成初始任务
4. **注册索引**：更新 `WORKSPACES.md`，添加新工作区路径和描述

## 当前已注册工作区

| 工作区 | 路径 | 状态 |
|---|---|---|
| AIStore ASR (海康) | `E:\siyun\haikang_asr\todo.md` | ✅ 已对齐 |

查看完整列表请读取 `WORKSPACES.md`。

## 关键原则

- **临时任务在这里管理**，项目升级后移到独立工作区
- **规范统一**：所有工作区遵循 `TODO_SPEC.md`
- **即时更新**：任务状态变更后立即更新 TODO 文件
- **保持索引同步**：新工作区必须注册到 `WORKSPACES.md`
