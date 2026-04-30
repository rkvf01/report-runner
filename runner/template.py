from jinja2 import Template , StrictUndefined

def render_template(template_text: str, context: dict) -> str:
    template = Template(template_text, undefined=StrictUndefined)
    return template.render(**context)