from collections import OrderedDict

class Rgb:
	def __init__(self, r = 0.0, g = 0.0, b = 0.0):
		self.r = r
		self.g = g
		self.b = b

	def rgba(self):
		return "rgb({},{},{})".format(
			max(0.0, min(1.0, self.r)),
			max(0.0, min(1.0, self.g)),
			max(0.0, min(1.0, self.b)))

	def hex(self):
		return "#{:02x}{:02x}{:02x}".format(
			max(0, min(255, int(255.0*self.r))), 
			max(0, min(255, int(255.0*self.g))), 
			max(0, min(255, int(255.0*self.b))))

	def __str__(self):
		return self.hex()

class Rgba:
	def __init__(self, r = 0.0, g = 0.0, b = 0.0, a = 1.0):
		self.r = r
		self.g = g
		self.b = b
		self.a = a

	def rgba(self):
		return "rgba({},{},{},{})".format(
			max(0.0, min(1.0, self.r)),
			max(0.0, min(1.0, self.g)),
			max(0.0, min(1.0, self.b)),
			max(0.0, min(1.0, self.a)))

	def __str__(self):
		return self.rgba()

class Style:
	def __init__(self, prop = OrderedDict()):
		self.prop = OrderedDict()
		for key,value in prop.items():
			self.set(key, value)

	def __str__(self):
		return " ".join(self.emit())

	def emit(self):
		result = []
		for key,value in self.prop.items():
			result.append(str(key) + ": " + str(value) + ";")
		return result

	def get(self, key):
		return self.prop[key]

	def set(self, key, value):
		#if key == "background":
		#elif key == "border":
		#elif key == "border-bottom":
		#elif key == "border-image":
		#elif key == "border-left":
		#elif key == "border-radius":
		#elif key == "border-right":
		#elif key == "border-top":
		#elif key == "margin":
		#elif key == "padding":
		#elif key == "font":
		#elif key == "list-style":
		#elif key == "animation":
		#elif key == "outline":
		#elif key == "column-rule":
		#else:
		self.prop[key] = value

	def __getitem__(self, key):
		return self.get(key)

	def __setitem__(self, key, value):
		self.set(key, value)

class Css:
	def __init__(self, elems = OrderedDict()):
		self.elems = elems

	def __str__(self):
		return "\n".join(self.emit())

	def emit(self):
		result = []
		for selector,style in self.elems.items():
			result.append(selector + " {")
			lines = style.emit()
			for line in lines:
				result.append("\t" + line)
			result.append("}")
			result.append("")
		return result

	
