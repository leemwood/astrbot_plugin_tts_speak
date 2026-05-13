# astrbot_plugin_tts_speak

一个让 LLM 能够自主调用 TTS 合成语音并发送语音消息的 AstrBot 插件。

## 功能介绍

本插件注册了一个名为 `tts_speak` 的工具函数，让 LLM 可以主动调用 TTS 功能，将文字转换为语音并发送给用户。

## 安装方法

1. 将本插件文件夹复制到 AstrBot 的 `plugins` 目录下
2. 重启 AstrBot

## 使用方法

安装并配置好 TTS 提供商后，LLM 会自动识别何时需要使用语音回复用户，并调用 `tts_speak` 工具合成语音。

### 前提条件

需要在 AstrBot 控制面板中配置 TTS 提供商（如百炼平台 TTS）。

## 配置说明

本插件无需额外配置，依赖 AstrBot 的 TTS 配置。

## 作者

- 小炎 & 柠枺

## 版本

v1.0.0
