from django import template
from django.conf import settings

from sass_processor.templatetags.sass_tags import SassSrcNode

register = template.Library()


class CustomSassSrcNode(SassSrcNode):
    def render(self, context):
        result = super().render(context) + '?version=1.0.0'
        return result


@register.tag(name='static')
def render_sass_src(parser, token):
    return CustomSassSrcNode.handle_token(parser, token)
