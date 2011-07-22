import re

from trac.core import *
from trac.wiki import IWikiSyntaxProvider
from trac.web import IRequestFilter

from genshi.builder import tag

class Nodewatcher(Component):
    """
    This component provides nodewatcher integration with Trac.
    """

    nodewatcher_base = 'https://nodes.wlan-si.net'

    implements(IWikiSyntaxProvider, IRequestFilter)

    # IWikiSyntaxProvider methods

    def _format_link(self, formatter, ns, target, label, fullmatch=None):
        return tag.a(label, href="%s/%s" % (self.nodewatcher_base, target))

    def get_wiki_syntax(self):
        """Return an iterable that provides additional wiki syntax."""

        return []

    def get_link_resolvers(self):
        """Return an iterable over (namespace, formatter) tuples."""

        yield ('nodes', self._format_link)
    
    # IRequestFilter methods

    def pre_process_request(self, req, handler):
        """Called after initial handler selection, and can be used to change
        the selected handler or redirect request."""

        return handler

    def post_process_request(self, req, template, data, content_type):
        """Do any post-processing the request might need; typically adding
        values to the template `data` dictionary, or changing template or
        mime type."""

        if req.path_info.startswith('/ticket/'):
            if not data:
                return (template, data, content_type)

            for field in data.get('fields', []):
                if field['name'] == 'nodes' and data['ticket']['nodes']:
                    items = []
                    for i, word in enumerate(re.split(r'([;,\s]+)', data['ticket']['nodes'])):
                        if i % 2:
                            items.append(word)
                        elif word:
                            items.append(tag.a(word, href="%s/nodes/%s" % (self.nodewatcher_base, word)))
                    field['rendered'] = tag(items)

        return (template, data, content_type)
