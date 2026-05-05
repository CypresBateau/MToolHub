"""
从 skills/ 目录导入技能到注册表

运行方式：
    python scripts/import_skills.py

功能：
    1. 扫描 skills/ 目录下的所有子目录
    2. 读取每个技能的 SKILL.md 文件
    3. 检测技能类型（document_only / tool_reference / executable / complex_workflow）
    4. 提取名称、描述、关键词等元数据
    5. 生成 skills.json 注册表文件
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional


def detect_skill_type(skill_dir: Path) -> str:
    """
    检测技能类型

    规则：
    - 仅 SKILL.md → document_only
    - SKILL.md + references/ → tool_reference
    - SKILL.md + coworker.py（导出 TOOLS）→ executable
    - SKILL.md + 大型数据/repo → complex_workflow
    """
    has_skill_md = (skill_dir / "SKILL.md").exists()
    has_references = (skill_dir / "references").exists() and (skill_dir / "references").is_dir()
    has_coworker = (skill_dir / "coworker.py").exists()

    if not has_skill_md:
        return "unknown"

    # 检查 coworker.py 是否导出 TOOLS
    if has_coworker:
        try:
            coworker_content = (skill_dir / "coworker.py").read_text(encoding="utf-8")
            if "TOOLS" in coworker_content or "def " in coworker_content:
                return "executable"
        except:
            pass

    # 检查是否有大型数据或复杂结构
    subdirs = [d for d in skill_dir.iterdir() if d.is_dir() and d.name not in ["references", "__pycache__"]]
    if len(subdirs) > 0 or len(list(skill_dir.glob("*.json"))) > 5:
        return "complex_workflow"

    if has_references:
        return "tool_reference"

    return "document_only"


def parse_skill_md(skill_md_path: Path) -> Dict[str, Optional[str]]:
    """
    解析 SKILL.md 提取元数据

    返回：
        {
            "name": str,
            "name_zh": str,
            "description": str,
            "description_zh": str,
            "keywords": List[str]
        }
    """
    try:
        content = skill_md_path.read_text(encoding="utf-8")
    except:
        return {}

    # 提取标题（第一个 # 标题）
    name_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else skill_md_path.parent.name

    # 提取描述（第一段文本）
    lines = content.split('\n')
    description = ""
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('```'):
            description = line
            break

    # 提取关键词（如果有 Keywords: 或 关键词: 行）
    keywords = []
    keywords_match = re.search(r'(?:Keywords?|关键词)[：:]\s*(.+)', content, re.IGNORECASE)
    if keywords_match:
        keywords_text = keywords_match.group(1)
        keywords = [k.strip() for k in re.split(r'[,，、]', keywords_text) if k.strip()]

    # 简单的中英文检测
    name_zh = name if any('\u4e00' <= c <= '\u9fff' for c in name) else None
    description_zh = description if any('\u4e00' <= c <= '\u9fff' for c in description) else None

    return {
        "name": name,
        "name_zh": name_zh,
        "description": description,
        "description_zh": description_zh,
        "keywords": keywords
    }


def import_skills(skills_dir: str, output_dir: str):
    """主导入流程"""
    skills_path = Path(skills_dir)
    if not skills_path.exists():
        print(f"❌ Skills 目录不存在: {skills_dir}")
        return

    print(f"🔍 正在扫描 Skills 目录: {skills_dir}")

    all_skills = []
    skill_dirs = [d for d in skills_path.iterdir() if d.is_dir() and not d.name.startswith('.')]

    print(f"✅ 发现 {len(skill_dirs)} 个技能目录")

    for skill_dir in sorted(skill_dirs):
        skill_md_path = skill_dir / "SKILL.md"
        if not skill_md_path.exists():
            print(f"⚠️  跳过 {skill_dir.name}（无 SKILL.md）")
            continue

        print(f"\n📦 处理: {skill_dir.name}")

        # 检测类型
        skill_type = detect_skill_type(skill_dir)
        print(f"   类型: {skill_type}")

        # 解析元数据
        metadata = parse_skill_md(skill_md_path)

        # 构建注册表条目
        skill = {
            "resource_id": f"skill:{skill_dir.name}",
            "resource_type": "skill",
            "name": metadata.get("name", skill_dir.name),
            "name_zh": metadata.get("name_zh"),
            "description": metadata.get("description", ""),
            "description_zh": metadata.get("description_zh"),
            "keywords": metadata.get("keywords", []),
            "skill_type": skill_type,
            "skill_md_path": str(skill_md_path.relative_to(Path.cwd())),
            "coworker_path": str((skill_dir / "coworker.py").relative_to(Path.cwd())) if (skill_dir / "coworker.py").exists() else None,
            "references_dir": str((skill_dir / "references").relative_to(Path.cwd())) if (skill_dir / "references").exists() else None
        }

        all_skills.append(skill)
        print(f"   ✅ 导入成功")

    # 保存到 JSON
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    skills_file = output_path / "skills.json"
    with open(skills_file, "w", encoding="utf-8") as f:
        json.dump(all_skills, f, ensure_ascii=False, indent=2)

    print(f"\n💾 已保存 {len(all_skills)} 个技能到: {skills_file}")

    # 统计各类型数量
    type_counts = {}
    for skill in all_skills:
        skill_type = skill["skill_type"]
        type_counts[skill_type] = type_counts.get(skill_type, 0) + 1

    print("\n📊 技能类型统计:")
    for skill_type, count in sorted(type_counts.items()):
        print(f"   {skill_type}: {count}")

    print("\n✨ 导入完成！")


if __name__ == "__main__":
    import sys

    # 默认配置
    SKILLS_DIR = "../skills"
    OUTPUT_DIR = "data/registry"

    # 支持命令行参数
    if len(sys.argv) > 1:
        SKILLS_DIR = sys.argv[1]
    if len(sys.argv) > 2:
        OUTPUT_DIR = sys.argv[2]

    import_skills(SKILLS_DIR, OUTPUT_DIR)
