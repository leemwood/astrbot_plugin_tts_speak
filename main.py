"""
astrbot_plugin_tts_speak

一个让LLM能够自主调用TTS合成语音并发送语音消息的插件。
注册了名为 tts_speak 的工具函数，让LLM可以主动调用TTS说话。
"""

from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.message_components import Record
from astrbot.api.star import Context, Star
from astrbot.core.message.message_event_result import MessageChain
from astrbot.api import logger


class TtsSpeakPlugin(Star):
    def __init__(self, context: Context, config: dict = None) -> None:
        super().__init__(context)
        self.config = config or {}
        logger.info("astrbot_plugin_tts_speak 插件已加载")

    @filter.llm_tool(name="tts_speak")
    async def tts_speak(
        self, event: AstrMessageEvent, text: str
    ) -> MessageEventResult:
        """调用TTS语音合成并发送语音消息给当前用户。

        当你想用语音（而不是文字）说出某句话时使用此工具。
        合成后的语音会直接发送给用户。

        Args:
            text(string): 要合成语音的文本内容，支持的 Speech Synthesis Markup Language (SSML) 由所使用的 TTS 提供商决定。
        """
        try:
            tts_provider = self.context.get_using_tts_provider(
                umo=event.unified_msg_origin
            )
            if not tts_provider:
                yield event.plain_result(
                    "TTS服务不可用，请先在AstrBot控制面板中配置TTS提供商（如百炼平台TTS）。"
                )
                return

            logger.info(f"TTS Speak: 正在合成语音 → {text[:60]}...")
            audio_path = await tts_provider.get_audio(text)

            if audio_path:
                record = Record(file=audio_path)
                await event.send(MessageChain([record]))
                logger.info(f"TTS Speak: 语音已发送，音频文件: {audio_path}")
                yield event.plain_result("TTS语音已发送！")
            else:
                yield event.plain_result("TTS语音合成失败，未能生成音频文件。")

        except Exception as e:
            logger.error(f"TTS Speak 调用异常: {e}")
            yield event.plain_result(f"TTS调用出错: {str(e)}")

    async def terminate(self) -> None:
        """插件卸载时清理资源"""
        logger.info("astrbot_plugin_tts_speak 插件已卸载")
