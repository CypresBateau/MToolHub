"""
注册表管理模块

负责加载和管理三类资源的注册表
"""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from app.models.registry import (
    ToolMetadata,
    ModelMetadata,
    SkillMetadata,
    ToolsRegistry,
    ModelsRegistry,
    SkillsRegistry,
)
from app.config import settings


class RegistryManager:
    """注册表管理器"""

    def __init__(self):
        self.tools: List[ToolMetadata] = []
        self.models: List[ModelMetadata] = []
        self.skills: List[SkillMetadata] = []
        self._load_all()

    def _load_all(self):
        """加载所有注册表"""
        self._load_tools()
        self._load_models()
        self._load_skills()

    def _load_tools(self):
        """加载工具注册表"""
        tools_path = Path(settings.tools_registry_path)
        if not tools_path.exists():
            print(f"警告：工具注册表不存在：{tools_path}")
            return

        with open(tools_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 兼容两种格式：JSON 数组 或 {"tools": [...]}
        if isinstance(data, list):
            items = data
        else:
            items = data.get("tools", [])

        loaded = []
        for item in items:
            try:
                tool = ToolMetadata(**item)
                if tool.enabled:
                    loaded.append(tool)
            except Exception as e:
                print(f"  跳过工具（字段不匹配）：{item.get('id', item.get('resource_id', '?'))} — {e}")
        self.tools = loaded
        print(f"已加载 {len(self.tools)} 个工具")

    def _load_models(self):
        """加载模型注册表"""
        models_path = Path(settings.models_registry_path)
        if not models_path.exists():
            print(f"警告：模型注册表不存在：{models_path}")
            return

        with open(models_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            registry = ModelsRegistry(**data)
            self.models = [model for model in registry.models if model.enabled]

        print(f"已加载 {len(self.models)} 个模型")

    def _load_skills(self):
        """加载技能注册表"""
        skills_path = Path(settings.skills_registry_path)
        if not skills_path.exists():
            print(f"警告：技能注册表不存在：{skills_path}")
            return

        with open(skills_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            registry = SkillsRegistry(**data)
            self.skills = [skill for skill in registry.skills if skill.enabled]

        print(f"已加载 {len(self.skills)} 个技能")

    def get_tool_by_id(self, tool_id: str) -> Optional[ToolMetadata]:
        """根据 ID 获取工具"""
        for tool in self.tools:
            if tool.id == tool_id:
                return tool
        return None

    def get_model_by_id(self, model_id: str) -> Optional[ModelMetadata]:
        """根据 ID 获取模型"""
        for model in self.models:
            if model.id == model_id:
                return model
        return None

    def get_skill_by_id(self, skill_id: str) -> Optional[SkillMetadata]:
        """根据 ID 获取技能"""
        for skill in self.skills:
            if skill.id == skill_id:
                return skill
        return None

    def get_resource_by_id(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """根据 ID 获取任意资源"""
        tool = self.get_tool_by_id(resource_id)
        if tool:
            return {"category": "tool", "item": tool}

        model = self.get_model_by_id(resource_id)
        if model:
            return {"category": "model", "item": model}

        skill = self.get_skill_by_id(resource_id)
        if skill:
            return {"category": "skill", "item": skill}

        return None

    def get_all_resources(self) -> List[Dict[str, Any]]:
        """获取所有资源"""
        resources = []
        for tool in self.tools:
            resources.append({"category": "tool", "item": tool.model_dump()})
        for model in self.models:
            resources.append({"category": "model", "item": model.model_dump()})
        for skill in self.skills:
            resources.append({"category": "skill", "item": skill.model_dump()})
        return resources

    def reload(self):
        """重新加载所有注册表"""
        self.tools = []
        self.models = []
        self.skills = []
        self._load_all()


# 全局注册表管理器实例
registry_manager = RegistryManager()
