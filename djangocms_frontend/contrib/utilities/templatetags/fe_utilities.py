from django import template

from djangocms_frontend import settings

from ..cms_plugins import create_tree

register = template.Library()


@register.inclusion_tag(f"djangocms_frontend/{settings.framework}/toc.html", takes_context=True)
def table_of_contents(context):
    return dict(TOC=create_tree(context.get("request", [])))  # Empty TOC if no request object available
