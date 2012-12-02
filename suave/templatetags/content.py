from django import template

register = template.Library()

from suave.models import ContentBlock


class ContentNode(template.Node):
    def __init__(self, nodelist, parser, token):
        bits = token.split_contents()
        if len(bits) != 4 or bits[-2] != 'as':
            raise template.TemplateSyntaxError(self.error_msg)
        self.identifier = parser.compile_filter(bits[1])
        self.as_var = bits[-1]
        self.nodelist = nodelist

    def render(self, context):
        identifier = self.identifier.resolve(context)
        try:
            kwargs = {}
            if hasattr(context, 'active'):
                kwargs['active'] = context['active']

            content = ContentBlock.objects.get(identifier=identifier,
                **kwargs)
            context.push()
            context[self.as_var] = content
            output = self.nodelist.render(context)
            context.pop()
            return output
        except ContentBlock.DoesNotExist:
            return ''

@register.tag
def content(parser, token):
    nodelist = parser.parse(('endcontent',))
    parser.delete_first_token()

    return ContentNode(nodelist, parser, token)
