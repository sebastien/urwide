#!/usr/bin/env python
# Encoding: iso-8859-1
# vim: tw=80 ts=4 sw=4 noet fenc=latin-1
# -----------------------------------------------------------------------------
# Project   : URWIDE - Extended URWID
# -----------------------------------------------------------------------------
# Author    : Sébastien Pierre                           <sebastien@xprima.com>
# License   : Lesser GNU Public License  http://www.gnu.org/licenses/lgpl.html>
# -----------------------------------------------------------------------------
# Creation  : 14-Jul-2006
# Last mod  : 14-Jul-2006
# -----------------------------------------------------------------------------

import string, re
import urwid, urwid.curses_display

__version__ = "0.0.2"
__doc__ = """\
URWIDE provides a nice wrapper around the awesome urwid Python library. It
enables the creation of complexe console user-interfaces, using a simple syntax. 

URWIDE provides extensions to support events, tooltips, dialogs as well as other
goodies.
"""

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

	def __init__( self, palette, ui ):
		"""Creates a new user interface object from the given text
		description."""
		self._content     = None
		self._stack       = None
		self._currentLine = None
		self._ui          = None
		self._palette     = self.parsePalette(palette)
		self._frame       = None
		self._header      = None
		self.parse(ui)
		self._frame       = urwid.Frame(
			urwid.ListBox(self._content),
			self._header
		)
		self._topwidget   = self._frame


	# EVENT HANDLERS
	# -------------------------------------------------------------------------

	def _onPress( self, button ):
		pass

	def _onKeyPress( self, key ):
		focused_widget = self.getFocused()
		if focused_widget:
			pass
		else:
			self._topwidget.keypress(self._currentSize, key)

	# UI STATE MANAGEMENT
	# -------------------------------------------------------------------------

	def getFocused( self ):
		return None

	# URWID EVENT-LOOP
	# -------------------------------------------------------------------------

	def main( self ):
		self._ui = urwid.curses_display.Screen()
		if self._palette: self._ui.register_palette(self._palette)
		self._ui.run_wrapper( self.run )

	def run( self ):
		self._currentSize = self._ui.get_cols_rows()
		while True:
			self.loop()

	def loop( self ):
		self.draw()
		keys = self._ui.get_input()
		# We handle keys
		for key in keys:
			if key == "window resize":
				self._currentSize = self._ui.get_cols_rows()
			else:
				self._onKeyPress(key)
	
	def draw( self ):
		canvas = self._topwidget.render( self._currentSize, focus=True )
		self._ui.draw_screen( self._currentSize, canvas )

	# PARSING WIDGETS STACK MANAGEMENT
	# -------------------------------------------------------------------------

	def _add( self, widget ):
		# Piles cannot be created with [] as content, so we fill them with the
		# EMPTY widget, which is replaced whenever we add something
		if self._content == [self.EMPTY]: self._content[0] == widget
		self._content.append(widget)

	def _push( self, endCallback, ui=None, args=(), kwargs={} ):
		self._stack.append((self._content, endCallback, ui, args, kwargs))
		self._content = []
		return self._content

	def _pop( self ):
		previous_content = self._content
		self._content, end_callback, end_ui, end_args, end_kwargs = self._stack.pop()
		return previous_content, end_callback, end_ui, end_args, end_kwargs

	# GENERIC PARSING METHODS
	# -------------------------------------------------------------------------

	def parse( self, text ):
		"""Parses the given text and initializes this user interface object."""
		self._content = []
		self._stack   = []
		self._header  = None
		self._currentLine = 0
		for line in text.split("\n"):
			line = line.strip()
			if not line.startswith("#"): self._parseLine(line)
			self._currentLine += 1
		return self._content

	@staticmethod
	def parsePalette( data ):
		res = []
		for line in data.split("\n"):
			if not line.strip(): continue
			line = line.replace("\t", " ").replace("  ", " ")
			name, attributes = map(string.strip, line.split(":"))
			res_line = [name]
			for attribute in attributes.split(","):
				attribute = attribute.strip().upper()
				color     = COLORS.get(attribute)
				if not color: raise UISyntaxError("Unsupported color: " + attribute)
				res_line.append(color)
			if not len(res_line) == 4:
				raise UISyntaxError("Expected NAME: FOREGROUND BACKGROUND FONT")
			res.append(tuple(res_line))
		return res

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

	def _createWidget( self, widgetClass, *args, **kwargs ):
		_data = _ui = _args = _kwargs = None
		for arg, value in kwargs.items():
			if   arg == "data":   _data = value
			elif arg == "ui":     _ui = value
			elif arg == "args":   _args = value
			elif arg == "kwargs": _kwargs = value
			else: raise Exception("Unrecognized optional argument: " + arg)
		if _data: _ui, _args, _kwargs = self._parseAttributes(_data)
		args = list(args)
		if _args: args.extend(_args)
		kwargs = _kwargs or {}
		res = widgetClass(*args, **kwargs)
		return res

	# WIDGET-SPECIFIC METHODS
	# -------------------------------------------------------------------------

	def _argsFind( self, data ):
		args = data.find("args:")
		if args == -1:
			attr = ""
		else:
			attr = data[args+5:]
			data = data[:args]
		return attr, data

	def _parseTxt( self, data ):
		attr, data = self._argsFind(data)
		ui, args, kwargs = self._parseAttributes(attr)
		self._add(self._createWidget(urwid.Text,data, ui=ui, args=args, kwargs=kwargs))

	def _parseHdr( self, data ):
		if self._header != None:
			raise UISyntaxError("Header can occur only once")
		attr, data = self._argsFind(data)
		ui, args, kwargs = self._parseAttributes(attr)
		self._header = self._createWidget(urwid.Text, data, ui=ui, args=args, kwargs=kwargs)

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
		data  = data[match.end():]
		label, text = match.groups()
		ui, args, kwargs = self._parseAttributes(data)
		if label:
			self._add(self._createWidget(urwid.Edit, label, text,
			ui=ui, args=args, kwargs=kwargs))
		else:
			self._add(self._createWidget(urwid.Edit, label, text,
			ui=ui, args=args, kwargs=kwargs))

	def _parsePle( self, data ):
		def end( content, ui=None, **kwargs ):
			if not content: content = [self.EMPTY]
			self._add(self._createWidget(urwid.Pile, content, ui=ui, kwargs=kwargs))
		ui, args, kwargs = self._parseAttributes(data)
		self._push(end, ui=ui, args=args, kwargs=kwargs)

	def _parseGFl( self, data ):
		def end( content, ui=None, **kwargs ):
			max_width = 0
			# Gets the maximum width for the content
			for widget in content:
				if hasattr(widget, "get_text"):
					max_width = max(len(widget.get_text()), max_width)
				if hasattr(widget, "get_label"):
					max_width = max(len(widget.get_label()), max_width)
			kwargs.setdefault("cell_width", max_width + 4)
			kwargs.setdefault("h_sep", 1)
			kwargs.setdefault("v_sep", 1)
			kwargs.setdefault("align", "center")
			self._add(self._createWidget(urwid.GridFlow, content, ui=ui, kwargs=kwargs))
		ui, args, kwargs = self._parseAttributes(data)
		self._push(end, ui=ui, args=args, kwargs=kwargs)

	def _parseEnd( self, data ):
		if data.strip(): raise UISyntaxError("End takes no argument: " + repr(data))
		# We get the end callback that will instanciate the widget and add it to
		# the content.
		if not self._stack: raise SyntaxError("End called without container widget")
		end_content, end_callback, end_ui, end_args, end_kwargs = self._pop()
		end_callback(end_content, end_ui, *end_args, **end_kwargs)

ui = UI("""
background    : DG,  _, SO
header        : WH, LG, BL
footer        : LG,  _, SO
info          : WH, LG, BL
shade         : DC, LG, BL
""",
"""
Hdr URWIDE - Sample application
::: @shade

Edt  State         [Project state]  #edit_state
Edt  Commit Type   [Commit type]    #edit_type
Edt  Name          [User name]
Edt  Summary       [Summary]        #edit_summary
---
Edt  [Description]  #edit_desc multiline=True
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
"""
)

ui.main()
