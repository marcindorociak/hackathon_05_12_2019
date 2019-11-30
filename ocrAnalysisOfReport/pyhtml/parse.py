from html.parser import HTMLParser
from . import html
from . import css

class Parser(HTMLParser):
	def __init__(self):
		self.syntax = html.Document()
		self.stack = [self.syntax]
		HTMLParser.__init__(self)

	def handle_starttag(self, tag, attrs):
		dattrs = dict(attrs)
		if tag in ["area", "base", "br", "col", 
				   "command", "embed", "hr", "img", 
				   "input", "keygen", "link", "meta", 
				   "param", "source", "track", "wbr"]:
			if self.stack:
				self.stack[-1] << html.STag(tag, dattrs)
		else:
			insert = html.Tag(tag, list(), dattrs)
			if self.stack:
				self.stack[-1] << insert
			self.stack.append(insert)

	def handle_endtag(self, tag):
		if tag == self.stack[-1].name:
			self.stack.pop()

	def handle_data(self, data):
		if self.stack and data.strip():
			self.stack[-1] << data.strip()

def walk(syntax, func, parent=None, left=None):
	if isinstance(syntax, html.Tag):
		for i,elem in enumerate(syntax.content):
			syntax.content[i] = walk(elem, func, syntax, syntax.content[i-1] if i > 0 else None)
		return func(syntax, parent, left)
	else:
		return syntax

