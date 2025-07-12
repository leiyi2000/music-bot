# 音乐机器人 (Music Bot)

一个基于FastAPI和NapCat的QQ音乐点歌机器人，支持网易云音乐平台的音乐搜索和分享。

## 功能特点

- 支持QQ群和私聊的音乐点歌功能
- 使用「点歌」命令搜索并分享网易云音乐
- 基于FastAPI构建的高性能异步API服务
- 支持Docker容器化部署
- 简单易用的插件系统，便于扩展新功能

## 技术栈

- Python 3.13+
- FastAPI - Web框架
- Granian - ASGI服务器
- Pydantic - 数据验证
- HTTPX - 异步HTTP客户端
- Docker - 容器化部署

## 安装与运行

### 环境要求

- Python 3.13 或更高版本
- Docker 和 Docker Compose (可选，用于容器化部署)

### 本地开发

1. 克隆仓库

```bash
git clone https://github.com/yourusername/music-bot.git
cd music-bot
```

2. 创建并配置环境变量

```bash
cp env.example .env
```

编辑 `.env` 文件，设置以下参数：

```
PORT=8000                      # API服务端口
NAPCAT_API=http://ip:3000      # NapCat API地址
LOG_LEVEL=INFO                 # 日志级别（可选）
```

3. 安装依赖

```bash
pip install uv
uv sync
```

4. 运行服务

```bash
uv run granian --access-log --host 0.0.0.0 --interface asgi bot.main:app
```

### Docker部署

1. 配置环境变量

```bash
cp env.example .env
```

编辑 `.env` 文件，设置必要的环境变量。

2. 构建并启动容器

```bash
docker-compose up -d
```

## 使用方法

### 点歌功能

在QQ群或私聊中发送以下命令：

```
点歌 歌曲名称
```

例如：

```
点歌 海阔天空
```

机器人将搜索网易云音乐并分享找到的第一首匹配歌曲。

## 插件开发

本项目采用简单的插件系统，可以轻松扩展新功能。

1. 在 `bot/plugins/` 目录下创建新的插件文件
2. 使用 `Command` 装饰器定义新命令
3. 在 `bot/plugins/__init__.py` 中注册新插件

示例插件：

```python
from bot.command import Command
from bot.napcat import NapCatClient
from bot.types import ReceiveMessage, SendMessage, TextMessage

command = Command()

@command("你好")
async def hello(napcat: NapCatClient, receive: ReceiveMessage):
    await napcat.send(
        SendMessage(
            user_id=receive.user_id,
            group_id=receive.group_id,
            message_type=receive.message_type,
            message=TextMessage.from_text("你好！我是音乐机器人"),
        )
    )
```

## 许可证

[MIT License](LICENSE)

## 贡献

欢迎提交问题和拉取请求！




