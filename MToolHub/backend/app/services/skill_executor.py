"""
技能执行器

负责执行医疗技能（Skills），将 SKILL.md 注入 Claude system prompt
"""

from pathlib import Path
from typing import Dict, Any, Optional
from app.services.executor import Executor
from app.core.claude_client import claude_client
from app.config import settings


class SkillExecutor(Executor):
    """技能执行器"""

    def __init__(self):
        self.skills_dir = Path(settings.skills_dir)

    async def execute(
        self,
        resource: Dict[str, Any],
        user_message: str,
        arguments: Optional[Dict[str, Any]] = None,
        file_bytes: Optional[bytes] = None,
        filename: Optional[str] = None,
        conversation_history: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        执行技能

        流程：
        1. 加载 SKILL.md
        2. 根据 skill_type 加载额外内容（references/handler）
        3. 调用 Claude API
        """
        trace = []
        skill_type = resource["skill_type"]

        # 步骤 1：加载 SKILL.md
        trace.append(f"正在加载技能：{resource['name']}")
        try:
            system_prompt = self._load_skill_md(resource["skill_md_path"])
            trace.append("SKILL.md 加载成功")
        except Exception as e:
            trace.append(f"SKILL.md 加载失败：{e}")
            return {
                "success": False,
                "response": f"技能加载失败：{e}",
                "result": None,
                "trace": "\n".join(trace),
            }

        # 步骤 2：根据类型加载额外内容
        tools = []

        if skill_type == "tool_reference":
            # 加载 references 目录
            if resource.get("references_path"):
                try:
                    refs = self._load_references(resource["references_path"])
                    system_prompt += f"\n\n## Reference Materials\n{refs}"
                    trace.append("参考资料加载成功")
                except Exception as e:
                    trace.append(f"参考资料加载失败：{e}")

        elif skill_type == "executable":
            # 加载 handler.py 中的工具
            if resource.get("handler_path"):
                try:
                    tools = self._load_handler_as_tools(resource["handler_path"])
                    trace.append(f"加载了 {len(tools)} 个工具")
                except Exception as e:
                    trace.append(f"工具加载失败：{e}")

        elif skill_type == "complex_workflow":
            # 加载大文件摘要
            if resource.get("references_path"):
                try:
                    refs = self._load_references(resource["references_path"], max_chars=4000)
                    system_prompt += f"\n\n## Reference Materials (truncated)\n{refs}"
                    trace.append("参考资料摘要加载成功")
                except Exception as e:
                    trace.append(f"参考资料加载失败：{e}")

        # 添加免责声明
        system_prompt += f"\n\n⚠️ {settings.medical_disclaimer}"

        # 步骤 3：调用 Claude
        trace.append("正在调用 Claude API...")
        try:
            messages = conversation_history or []
            messages.append({"role": "user", "content": user_message})

            response = await claude_client.chat(
                messages=messages,
                system=system_prompt,
                tools=tools if tools else None,
            )

            # 提取响应文本
            response_text = ""
            for block in response.content:
                if block.type == "text":
                    response_text += block.text

            trace.append("Claude API 调用成功")

            return {
                "success": True,
                "response": response_text,
                "result": {"skill_type": skill_type, "response": response_text},
                "trace": "\n".join(trace),
            }

        except Exception as e:
            trace.append(f"Claude API 调用失败：{e}")
            return {
                "success": False,
                "response": f"技能执行失败：{e}",
                "result": None,
                "trace": "\n".join(trace),
            }

    def _load_skill_md(self, path: str) -> str:
        """加载 SKILL.md 文件"""
        full_path = self.skills_dir / path
        if not full_path.exists():
            raise FileNotFoundError(f"SKILL.md 不存在：{full_path}")
        return full_path.read_text(encoding="utf-8")

    def _load_references(self, path: str, max_chars: int = 8000) -> str:
        """加载 references 目录中的文件"""
        ref_dir = self.skills_dir / path
        if not ref_dir.exists():
            return ""

        content = ""
        for f in sorted(ref_dir.iterdir()):
            if f.is_file() and f.suffix in [".md", ".txt", ".json"]:
                file_content = f.read_text(encoding="utf-8")
                content += f"\n### {f.name}\n{file_content[:max_chars]}\n"
                if len(content) > max_chars:
                    break

        return content[:max_chars]

    def _load_handler_as_tools(self, handler_path: str) -> list:
        """
        从 handler.py 中加载工具定义

        handler.py 应导出一个 TOOLS 列表，每个元素是 Claude tool_use 格式
        """
        import importlib.util

        full_path = self.skills_dir / handler_path
        if not full_path.exists():
            raise FileNotFoundError(f"handler.py 不存在：{full_path}")

        spec = importlib.util.spec_from_file_location("handler", full_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return getattr(module, "TOOLS", [])


# 全局技能执行器实例
skill_executor = SkillExecutor()
