import string, re
import urwid

COLORS =  {
	# Colors
	"DC": "dark cyan",
	"LC": "light cyan",
	"DG": "dark gray",
	"LG": "light gray",
	"WH": "white",
	# Font attributes
	"BL": "bold",
	"SO": "standout",
	"_" : "default"
}

def palette( data ):
	res = []
	for line in data.split("\n"):
		if not line.strip(): continue
		line = line.replace("\t", " ").replace("  ", " ")
		name, attributes = map(string.strip, line.split(":"))
		res_line = [name]
		for attribute in attributes.split(","):
			attribute = attribute.strip().upper()
			color     = COLORS.get(attribute)
			if not color: raise Exception("Unsupported color: " + attribute)
			res_line.append(color)
		if not len(res_line) == 4:
			raise Exception("Expected NAME: FOREGROUND BACKGROUND FONT")
		res.append(tuple(res_line))
	return res


palette("""
	background    : DG,  _, SO
	header        : WH, DG, BL
	footer        : LG,  _, SO
	info          : WH, LG, BL
	shade         : DC, LG, BL
""")


CLASSES = {
	"Edt": urwid.Edit,
	"Ple": urwid.Pile,
	"GFl": urwid.GridFlow,
}


class UISyntaxError(Exception): pass
class UI:
	"""The UI class allows to build an URWID user-interface from a simple set of
	string definitions.

	Instanciation of this class, may raise syntax error if the given text data
	is not formatted as expected, but you can easily get detailed information on
	what the problem was."""

	BLANK = urwid.Text("")
	EMPTY = urwid.Text("")
	NOP   = lambda x:x

	def __init__( self, text ):
		"""Creates a new user interface object from the given text
		description."""
		self.parse(text)
		self.content = None
		self.stack = None
		self.currentLine = None

	def parse( self, text ):
		"""Parses the given text and initializes this user interface object."""
		self.content = []
		self.stack   = []
		self.currentLine = 0
		for line in text.split("\n"):
			line = line.strip()
			try:
				self._parseLine(line)
			except SyntaxError, e:
				print "ERROR:", e
				print "at line %d: %s" % (self.currentLine, repr(line))
				print e
				print
			self.currentLine += 1

	# EVENT HANDLERS
	# -------------------------------------------------------------------------

	def _onPress( self, button ):
		pass

	# PARSING WIDGETS STACK MANAGEMENT
	# -------------------------------------------------------------------------

	def _add( self, widget ):
		# Piles cannot be created with [] as content, so we fill them with the
		# EMPTY widget, which is replaced whenever we add something
		if self.content == [self.EMPTY]: self.content[0] == widget
		self.content.append(widget)

	def _push( self, endCallback, ui=None, args=(), kwargs={} ):
		self.stack.append((self.content, endCallback, ui, args, kwargs))
		self.content = []
		return self.content

	def _pop( self ):
		previous_content = self.content
		self.content, end_callback, end_ui, end_args, end_kwargs = self.stack.pop()
		return previous_content, end_callback, end_ui, end_args, end_kwargs

	# GENERIC PARSING METHODS
	# -------------------------------------------------------------------------

	RE_LINE = re.compile("^\s*(...)\s*")
	def _parseLine( self, line ):
		"""Parses a line of the UI definition file. This automatically invokes
		the specialized parsers."""
		if not line:
			self._add( self.BLANK )
			return
		match = self.RE_LINE.match(line)
		if not match: raise UISyntaxError("Unrecognized line: " + line)
		name  = match.group(1)
		data  = line[match.end():]
		if hasattr(self, "_parse" + name ):
			getattr(self, "_parse" + name)(data)
		elif name[0] == name[1] == name[2]:
			self._parseDvd(name)
		else:
			raise UISyntaxError("Unrecognized widget: " + name)

	def _parseAttributes( self, data ):
		assert type(data) in (str, unicode)
		ui_attrs, data = self._parseUIAttributes(data)
		args, kwargs   = self._parseArguments(data)
		return ui_attrs, args, kwargs

	RE_UI_ATTRIBUTE = re.compile("\s*([#@\?\>\:])([\w\d_\-]+)\s*")
	def _parseUIAttributes( self, data ):
		"""Parses the given UI attributes from the data and returns the rest of
		the data (which corresponds to something else thatn the UI
		attributes."""
		assert type(data) in (str, unicode)
		while True:
			match = self.RE_UI_ATTRIBUTE.match(data)
			if not match: break
			data = data[match.end():]
		return None, data

	def _parseArguments( self, data ):
		"""Parses the given text data which should be a list of attributes. This
		returns a dict with the attributes."""
		assert type(data) in (str, unicode)
		def as_dict(*args, **kwargs): return args, kwargs
		res = eval("as_dict(%s)" % (data))
		try:
			res = eval("as_dict(%s)" % (data))
		except:
			raise SyntaxError("Malformed arguments: " + repr(data))
		return res

	def _createWidget( self, widgetClass, *addargs, **kwargs ):
		if kwargs.get("data"):
			ui, args, kwargs = self._parseAttributes(kwargs.get("data"))
		else:
			ui     = kwargs.get("ui")
			args   = kwargs.get("args") or ()
			kwargs = kwargs.get("args") or {}
		addargs = list(addargs)
		if args: addargs.extend(args)
		if not kwargs: kwargs == {}
		res = widgetClass(*addargs, **kwargs)
		return res

	# WIDGET-SPECIFIC METHODS
	# -------------------------------------------------------------------------

	def _parseTxt( self, data ):
		args = data.find("args:")
		if args == -1:
			attr = ""
		else:
			attr = data[args+5:]
			data = data[:args]
		ui, args, kwargs = self._parseAttributes(attr)
		self._add(self._createWidget(urwid.Text,data, ui=ui, args=args, kwargs=kwargs))

	RE_BTN = re.compile("\s*\[([^\]]+)\]")
	def _parseBtn( self, data ):
		match = self.RE_BTN.match(data)
		data  = data[match.end():]
		if not match: raise SyntaxError("Malformed button: " + repr(data))
		self._add(self._createWidget(urwid.Button, match.group(1), self._onPress, data=data))

	def _parseDvd( self, data ):
		self._add(urwid.Divider(data))

	RE_EDT = re.compile("([^\[]*)\[([^\]]+)\]")
	def _parseEdt( self, data ):
		match = self.RE_EDT.match(data)

	def _parsePle( self, data ):
		def end( content, ui=None, **kwargs ):
			if not content: content = [self.EMPTY]
			self._add(urwid.Pile(content, **kwargs))
		ui, args, kwargs = self._parseAttributes(data)
		self._push(end, ui=ui, args=args, kwargs=kwargs)

	def _parseGFl( self, data ):
		def end( content, ui=None, **kwargs ):
			max_width = 0
			for widget in self.content:
				if hasattr(widget, "get_text"):
					max_width = max(len(widget.get_text()), max_width)
				if hasattr(widget, "get_label"):
					max_width = max(len(widget.get_label()), max_width)
		ui, args, kwargs = self._parseAttributes(data)
		self._push(end, ui=ui, args=args, kwargs=kwargs)

	def _parseEnd( self, data ):
		if data.strip(): raise UISyntaxError("End takes no argument: " + repr(data))
		# We get the end callback that will instanciate the widget and add it to
		# the content.
		if not self.stack: raise SyntaxError("End called without container widget")
		end_content, end_callback, end_ui, end_args, end_kwargs = self._pop()
		end_callback(end_content, end_ui, *end_args, **end_kwargs)

ui = UI("""
::: @shade

Edt  State         [Project state]  #edit_state
Edt  Commit Type   [Project state]  #edit_type
Edt  Summary       [Summary]        #edit_summary
---
Edt  [Description] multiline=True   #edit_desc
===
Txt  Changes to commit  
---
Ple                                 #pile_commit
End
GFl 
Btn [Cancel]                         #btn_cancel
Btn [Save]                           #btn_save
Btn [Commit]                         #btn_commit
End
""")
