
# http://stackoverflow.com/a/34120478
def bsplit(s, d):
	if not s:
		return ['']

	p = chr(ord(max(s))+1)
	if isinstance(d, (list, tuple)):
		for di in d:
			s = s.replace(di, p+di)
	else:
		s = s.replace(d, p+d)

	return s.split(p)

class STag:
	def __init__(self,
							 name,
							 attrs,
							 usr = None):
		self.name = name
		self.attrs = dict((str(k).lower(), v) for k,v in attrs.items())
		self.usr = usr if usr else {}

	def __str__(self):
		return "\n".join(self.emit())

	def __lshift__(self, other):
		if isinstance(other, dict):
			self.attrs.update((str(k).lower(), v) for k,v in other.items())
		return other

	def get(self, Type=None, Class=None, Id=None):
		return []

	def __getitem__(self, Str):
		return []
	
	def emit(self, tab = ""):
		attrs = []
		for k,v in self.attrs.items():
			if isinstance(v, bool) and v:
				attrs.append(k)
			else:
				attrs.append(k + "=\"" + str(v) + "\"")
		
		if attrs:
			return [tab + "<" + self.name + " " + " ".join(attrs) + ">"]
		else:
			return [tab + "<" + self.name + ">"]

class Tag:
	def __init__(self,
							 name,
							 content,
							 attrs,
							 usr = None):
		self.name = name
		self.content = list(content)
		self.attrs = dict((str(k).lower(), v) for k,v in attrs.items())
		self.usr = usr if usr else {}

	def __str__(self):
		return "\n".join(self.emit())

	def __lshift__(self, other):
		if isinstance(other, dict):
			self.attrs.update((str(k).lower(), v) for k,v in other.items())
		elif isinstance(other, (list, tuple)):
			self.content += other
		else:
			self.content.append(other)
		return other

	def get(self, Type=None, Class=None, Id=None):
		result = []
		for item in self.content:
			if isinstance(item, (Tag, STag)):
				if ((not Type or item.name == Type) and
					 (not Class or "class" in item.attrs and item.attrs["class"] == Class) and
					 (not Id or "id" in item.attrs and item.attrs["id"] == Id)):
					result.append(item)

			if isinstance(item, Tag):
				result += item.get(Type=Type, Class=Class, Id=Id)

		return result

	def __getitem__(self, Str):
		Type = None
		Class = None
		Id = None

		s = bsplit(Str, [".", "#"])

		for i in s:
			if len(i) > 0:
				if i[0] == ".":
					Class = i[1:]
				elif i[0] == "#":
					Id = i[1:]
				else:
					Type = i

		return self.get(Type=Type, Class=Class, Id=Id)
	
	def emit(self, tab = ""):
		result = []
		attrs = []
		for k,v in self.attrs.items():
			if isinstance(v, bool) and v:
				attrs.append(k)
			else:
				attrs.append(k + "=\"" + str(v) + "\"")
		
		if attrs:
			start_line = "<" + self.name + " " + " ".join(attrs) + ">"
		else:
			start_line = "<" + self.name + ">"
		end_line = "</" + self.name + ">"

		content_lines = []
		for c in self.content:
			if isinstance(c, Tag):
				content_lines += c.emit(tab + "\t")
			elif isinstance(c, STag):
				content_lines += c.emit(tab + "\t")
			elif content_lines:
				content_lines[-1] += " " + c
			else:
				content_lines.append(tab + "\t" + str(c))

		if content_lines:
			result.append(tab + start_line)
			result += content_lines
			result.append(tab + end_line)
		else:
			result.append(tab + start_line + end_line)
		
		return result

class Document(Tag):
	def __init__(self, *args):
		Tag.__init__(self, "document", args, dict())

	def emit(self, tab=""):
		content_lines = ["Content-type: text/html\r\n\r\n"]
		for c in self.content:
			if isinstance(c, Tag):
				content_lines += c.emit(tab)
			elif isinstance(c, STag):
				content_lines += c.emit(tab)
			elif content_lines:
				content_lines[-1] += " " + c
			else:
				content_lines.append(tab + str(c))
		return content_lines

class Html(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "html", args, kwargs)
		for k,v in kwargs:
			if k not in ["manifest", "xmins"]:
				print("error: unrecognized attribute '" + k +
							"' for tag '" + self.name + "'")

class Head(Tag):
	def __init__(self, *args):
		Tag.__init__(self, "head", args, dict())

class Body(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "body", args, kwargs)

# Header Tags

class Title(Tag):
	def __init__(self, title, **kwargs):
		Tag.__init__(self, "title", [str(title)], kwargs)

class Link(STag):
	def __init__(self, **kwargs):
		STag.__init__(self, "link", kwargs)

class Script(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "script", args, kwargs)

# Layout Tags

class A(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "a", args, kwargs)

class Abbr(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "abbr", args, kwargs)

class Address(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "address", args, kwargs)

class Area(STag):
	def __init__(self, **kwargs):
		STag.__init__(self, "area", kwargs)

class Article(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "article", args, kwargs)

class Aside(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "aside", args, kwargs)

class Audio(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "audio", args, kwargs)

class B(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "b", args, kwargs)

class Base(STag):
	def __init__(self, **kwargs):
		STag.__init__(self, "base", kwargs)

class Bdi(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "bdi", args, kwargs)

class Bdo(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "bdo", args, kwargs)

class Blockquote(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "blockquote", args, kwargs)

class Br(STag):
	def __init__(self, **kwargs):
		STag.__init__(self, "br", kwargs)

class Button(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "button", args, kwargs)

class Canvas(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "canvas", args, kwargs)

class Caption(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "caption", args, kwargs)

class Cite(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "cite", args, kwargs)

class Code(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "code", args, kwargs)

class Col(STag):
	def __init__(self, **kwargs):
		STag.__init__(self, "col", kwargs)

class Colgroup(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "colgroup", args, kwargs)

class Datalist(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "datalist", args, kwargs)

class Dd(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "dd", args, kwargs)

class Del(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "del", args, kwargs)

class Details(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "details", args, kwargs)

class Dfn(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "dfn", args, kwargs)

class Dialog(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "dialog", args, kwargs)

class Div(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "div", args, kwargs)

class Dl(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "dl", args, kwargs)

class Dt(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "dt", args, kwargs)

class Em(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "em", args, kwargs)

class Embed(STag):
	def __init__(self, **kwargs):
		STag.__init__(self, "embed", kwargs)

class Fieldset(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "fieldset", args, kwargs)

class Figcaption(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "figcaption", args, kwargs)

class Figure(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "figure", args, kwargs)

class Footer(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "footer", args, kwargs)

class Form(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "form", args, kwargs)

class H1(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "h1", args, kwargs)

class H2(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "h2", args, kwargs)

class H3(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "h3", args, kwargs)

class H4(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "h4", args, kwargs)

class H5(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "h5", args, kwargs)

class H6(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "h6", args, kwargs)

class Header(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "header", args, kwargs)

class Hr(STag):
	def __init__(self, **kwargs):
		STag.__init__(self, "hr", kwargs)

class I(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "i", args, kwargs)

class Iframe(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "iframe", args, kwargs)

class Img(STag):
	def __init__(self, **kwargs):
		STag.__init__(self, "img", kwargs)

class Input(STag):
	def __init__(self, **kwargs):
		STag.__init__(self, "input", kwargs)

class Ins(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "ins", args, kwargs)

class Kbd(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "kbd", args, kwargs)

class Keygen(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "keygen", args, kwargs)

class Label(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "label", args, kwargs)

class Legend(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "legend", args, kwargs)

class Li(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "li", args, kwargs)

class Main(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "main", args, kwargs)

class Map(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "map", args, kwargs)

class Mark(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "mark", args, kwargs)

class Menu(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "menu", args, kwargs)

class Menuitem(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "menuitem", args, kwargs)

class Meta(STag):
	def __init__(self, **kwargs):
		STag.__init__(self, "meta", kwargs)

class Meter(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "meter", args, kwargs)

class Nav(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "nav", args, kwargs)

class Noscript(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "noscript", args, kwargs)

class Object(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "object", args, kwargs)

class Ol(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "ol", args, kwargs)

class Optgroup(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "optgroup", args, kwargs)

class Option(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "option", args, kwargs)

class Output(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "output", args, kwargs)

class P(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "p", args, kwargs)

class Param(STag):
	def __init__(self, **kwargs):
		STag.__init__(self, "param", kwargs)

class Picture(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "picture", args, kwargs)

class Pre(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "pre", args, kwargs)

class Progress(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "progress", args, kwargs)

class Q(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "q", args, kwargs)

class Rp(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "rp", args, kwargs)

class Rt(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "rt", args, kwargs)

class Ruby(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "ruby", args, kwargs)

class S(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "s", args, kwargs)

class Samp(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "samp", args, kwargs)

class Section(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "section", args, kwargs)

class Select(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "select", args, kwargs)

class Small(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "small", args, kwargs)

class Source(STag):
	def __init__(self, **kwargs):
		STag.__init__(self, "source", kwargs)

class Span(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "span", args, kwargs)

class Strong(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "strong", args, kwargs)

class Style(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "style", args, kwargs)

class Sub(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "sub", args, kwargs)

class Summary(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "summary", args, kwargs)

class Sup(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "sup", args, kwargs)

class Table(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "table", args, kwargs)

class Tbody(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "tbody", args, kwargs)

class Td(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "td", args, kwargs)

class Textarea(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "textarea", args, kwargs)

class Tfoot(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "tfoot", args, kwargs)

class Th(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "th", args, kwargs)

class Thead(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "thead", args, kwargs)

class Time(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "time", args, kwargs)

class Tr(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "tr", args, kwargs)

class Track(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "track", args, kwargs)

class U(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "u", args, kwargs)

class Ul(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "ul", args, kwargs)

class Var(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "var", args, kwargs)

class Video(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "video", args, kwargs)

class Wbr(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "wbr", args, kwargs)

class Doctype(Tag):
	def __init__(self, *args, **kwargs):
		Tag.__init__(self, "!DOCTYPE", args, kwargs)

