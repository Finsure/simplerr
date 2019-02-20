from jinja2 import Environment, FileSystemLoader

class Template(object):
    # TODO: This should be attached at the wsgi app level
    # TODO: Updates this to add filters, eg filters['escapejs'] = json.dumps
    filters = {}

    def __init__(self, cwd):
        self.cwd = cwd
        self.env = Environment(
            loader=FileSystemLoader(cwd), autoescape=True
        )

        filters = self.env.filters

    def render(self, template, data={}):
       return self.env.get_template(template).render(**data)

# TODO: Remove when rest is updated
T=Template
