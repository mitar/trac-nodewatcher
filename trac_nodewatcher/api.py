import re

from trac.core import *
from trac.wiki import IWikiSyntaxProvider
from trac.web import ITemplateStreamFilter

from genshi.builder import tag

class Nodewatcher(Component):
    """
    This component provides nodewatcher integration with Trac.
    """

    # TODO: Make a configuration option
    nodewatcher_base = 'https://nodes.wlan-si.net'

    implements(IWikiSyntaxProvider, ITemplateStreamFilter)

    # IWikiSyntaxProvider methods

    def _format_link(self, formatter, ns, target, label, fullmatch=None):
        return tag.a(label, href="%s/%s" % (self.nodewatcher_base, target))

    def get_wiki_syntax(self):
        """Return an iterable that provides additional wiki syntax."""

        return []

    def get_link_resolvers(self):
        """Return an iterable over (namespace, formatter) tuples."""

        yield ('nodes', self._format_link)
    
    # ITemplateStreamFilter methods

    def filter_stream(self, req, method, filename, stream, data):
        """Return a filtered Genshi event stream, or the original unfiltered
        stream if no match."""

        if not data:
            return stream

        # We try all at the same time to maybe catch also changed or processed templates
        if filename in ["report_view.html", "query_results.html", "ticket.html", "query.html"]:
            # For ticket.html
            if 'fields' in data and isinstance(data['fields'], list):
                for field in data['fields']:
                    if field['name'] == 'nodes' and data['ticket']['nodes']:
                        field['rendered'] = self._link_nodes(data['ticket']['nodes'])
            # For query_results.html and query.html
            if 'groups' in data and isinstance(data['groups'], list):
                for group, tickets in data['groups']:
                    for ticket in tickets:
                        if 'nodes' in ticket:
                            ticket['nodes'] = self._link_nodes(ticket['nodes'])
            # For report_view.html
            if 'row_groups' in data and isinstance(data['row_groups'], list):
                for group, rows in data['row_groups']:
                    for row in rows:
                        if 'cell_groups' in row and isinstance(row['cell_groups'], list):
                            for cells in row['cell_groups']:
                                for cell in cells:
                                    if cell.get('header', {}).get('col') in ['related nodes', 'nodes']:
                                        cell['value'] = self._link_nodes(cell['value'])

        return stream

    def _link_nodes(self, nodes):
        items = []

        for i, word in enumerate(re.split(r'([;,\s]+)', nodes)):
            if i % 2:
                items.append(word)
            elif word:
                items.append(tag.a(word, href="%s/node/%s" % (self.nodewatcher_base, word)))

        if nodes:
            return tag(items)
        else:
            return None
