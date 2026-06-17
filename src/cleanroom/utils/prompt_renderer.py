from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

_PROMPTS_ROOT = Path(__file__).parent.parent / "agents"


class PromptRenderer:
    def __init__(self) -> None:
        self.env = Environment(
            loader=FileSystemLoader(str(_PROMPTS_ROOT)),
            undefined=StrictUndefined,
            autoescape=False,
        )

    def render(self, template_name: str, context: dict) -> str:
        # searches recursively under agents/ for the template filename
        matches = list(_PROMPTS_ROOT.rglob(template_name))
        if not matches:
            raise FileNotFoundError(f"Prompt template '{template_name}' not found under {_PROMPTS_ROOT}")
        relative = matches[0].relative_to(_PROMPTS_ROOT)
        template = self.env.get_template(str(relative))
        return template.render(**context)
