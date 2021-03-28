from jinja2 import Environment, FileSystemLoader

jinja_env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
)
