# DouYin Spark Flow

![cover](docs/images/cover.png)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Playwright](https://img.shields.io/badge/Playwright-%E2%9C%94-green?logo=playwright)
![chrome-headless-shell](https://img.shields.io/badge/chrome--headless--shell-%E2%9C%94-brightgreen?logo=googlechrome)

由项目[DouYinSparkFlow](https://github.com/2061360308/DouYinSparkFlow)修改而来

**抖音火花自动续火脚本** —— 自动给你的抖音好友和群聊发送消息，保持火花不断。

## 特性

- [x] 私信续火花（支持昵称/抖音号匹配）
- [x] 群聊续火花（支持群名称匹配）
- [x] 在线可视化配置器
- [x] 多账号、多目标批量支持
- [x] 一言 API 丰富消息内容
- [x] GitHub Actions 定时自动运行
- [x] 源码部署（本地/服务器/青龙面板）

基于 Playwright + Chrome 自动化操作[抖音创作者中心](https://creator.douyin.com/)。

## 快速开始

### 1. 获取配置

打开 [配置生成器](https://bthawake.github.io/DouYinSpark-ALL/) 或本地打开 `docs/index.html`，填写：

- 消息模板、一言类型等基础设置
- 账号 cookies（需手动从浏览器导出，[教程](docs/配置生成器使用.md)）
- 目标好友（私信对象）
- 目标群聊（群聊对象）

点击 **一键复制 CONFIG**，得到 JSON 配置。

### 2. 部署

**GitHub Actions（推荐）：**

Fork 仓库 → Settings → Secrets and Variables → Actions → 新建 Secret，名称为 `CONFIG`，粘贴 JSON → 手动触发一次 workflow ,每天早上5点和下午2点自动运行，高峰期间可能会有延迟。

**本地运行：**

```bash
pip install -r requirements.txt
playwright install chromium
```

在项目目录创建 `config.json`，粘贴 CONFIG 内容，然后：

```bash
python main.py
```

## 配置结构

```json
{
  "messageTemplate": "[API]",
  "matchMode": "short_id",
  "groupMatchMode": "name",
  "accounts": [{
    "username": "我的账号",
    "unique_id": "1234567890",
    "cookies": ["..."],
    "targets": ["12345678901"],
    "groups": ["群名称"]
  }]
}
```

- `matchMode`: `nickname`（昵称）或 `short_id`（抖音号）
- `groupMatchMode`: `name`（群名称）或 `id`（群ID）
- `targets`: 好友列表，匹配模式决定填什么
- `groups`: 群聊列表，匹配模式决定填什么

## 本地修改说明（2026-10）

以下改动均在 `core/tasks.py`，用于解决"好友较多时只能发送最近会话中的部分目标"的问题：

1. **虚拟列表滚动修复**：好友列表是 ReactVirtualized 虚拟滚动列表（实测 552 个好友，列表总高约 4~6 万像素）。原实现的滚动容器选择器（`[class*="semi-list"]`）指向的元素并不可滚动，导致列表实际从未滚动过，脚本只能看到按最近会话排序的前十几个目标，深处目标全部报"未找到可见的"。现改为定位包含会话条目（`[class*="item-header-name-"]`）的最大 `ReactVirtualized__Grid` 容器进行滚动（`_SCROLL_CONTAINER_JS` / `_GRID_TOP_JS`）。

2. **点击时序竞态修复**：原实现要求目标元素"视觉上完全可见"（矩形完全落在窗口内）才允许点击，而虚拟列表滚动后的重新渲染存在延迟，导致部分目标即使已渲染进 DOM 也会被漏掉。现改为：目标昵称一旦渲染进 DOM 即就近点击（`element.click()` 不要求视觉可见），点击后以"聊天输入框出现"（`_CHAT_OPENED_JS`）确认会话成功打开；若未打开则视为未命中，继续滚动重试（`_FIND_AND_CLICK_JS`）。

修复后经 552 好友列表、19 个目标 + 1 个群聊全量实测，连续两轮 100% 发送成功，单轮约 3 分钟。

## 免责声明

1. 本项目为开源学习用途，仅用于技术研究和个人自用，严禁商业用途。
2. 使用本脚本产生的一切风险（包括账号限流、封禁等）由使用者自行承担。
3. 请合理控制运行频率，避免给抖音服务器造成压力。

## 开源协议

MIT License，详见 [LICENSE](LICENSE)。
