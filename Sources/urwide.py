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
# Last mod  : 15-Jul-2006
# -----------------------------------------------------------------------------

import string, re
import urwid, urwid.curses_display

__version__ = "0.0.2"
__doc__ = """\
URWIDE provides a nice wrapper around the awesome urwid Python library. It
enables the creation of complexe console user-interfaces, using a simple syntax. 

URWIDE provides extensions to support events, tooltips, dialogs as well as other
goodies.

URWID can be downloaded at <http://www.excess.org/urwid>.
"""

COLORS =  {
	# Colors
	"WH": "white",
	"BL": "black",
	"YL": "yellow",
	"BR": "brown",
	"LR": "light red",
	"LG": "light green",
	"LB": "light blue",
	"LC": "light cyan",
	"LM": "light magenta",
	"Lg": "light gray",
	"DR": "dark red",
	"DG": "dark green",
	"DB": "dark blue",
	"DC": "dark cyan",
	"DM": "dark magenta",
	"Dg": "dark gray",
	# Font attributes
	"BO": "bold",
	"SO": "standout",
	"UL": "underline",
	"_" : "default"
}
RIGHT  = "right"
LEFT   = "left"
CENTER = "center"

CLASSES = {
	"Edt": urwid.Edit,
	"Ple": urwid.Pile,
	"GFl": urwid.GridFlow,
}

# ------------------------------------------------------------------------------
#
# UI CLASS
#
# ------------------------------------------------------------------------------

class UISyntaxError(Exception): pass
class UIRuntimeError(Exception): pass
class UI:
	"""The UI class allows to build an URWID user-interface from a simple set of
	string definitions.

	Instanciation of this class, may raise syntax error if the given text data
	is not formatted as expected, but you can easily get detailed information on
	what the problem was."""

	BLANK = urwid.Text("")
	EMPTY = urwid.Text("")
	NOP   = lambda self:self

	class Collection(object):
		"""Keys of the given collection are recognized as attributes."""

		def __init__( self, collection=None ):
			object.__init__(self)
			if collection == None: collection = {}
			self.w_w_content = collection

		def __getattr__( self, name ):
			if name.startswith("w_w_"):
				return super(UI.Collection, self).__getattribute__(name)
			else:
				w = self.w_w_content
				if not w.has_key(name): raise UIRuntimeError("No widget with name: " + name)
				return w[name]

		def __setattr__( self, name, value):
			if name.startswith("w_w_"):
				return super(UI.Collection, self).__setattr__(name, value)
			else:
				if self.w_w_content.has_key(name):
					raise SyntaxError("Item name already used: " + name)
				self.w_w_content[name] = value

	def __init__( self ):
		"""Creates a new user interface object from the given text
		description."""
		self._content     = None
		self._stack       = None
		self._currentLine = None
		self._ui          = None
		self._palette     = None
		self._frame       = None
		self._header      = None
		self._footer      = None
		self._listbox     = None
		self._frame       = None
		self._topwidget   = None
		self._widgets     = {}
		self._strings     = {}
		self._data        = {}
		self._handlers    = []
		self._tooltiptext = ""
		self._infotext    = ""
		self._footertext  = ""
		self.widgets      = UI.Collection(self._widgets)
		self.strings      = UI.Collection(self._strings)
		self.data         = UI.Collection(self._data)
		self.isRunning    = False
		self.endMessage   = ""

	# USER INTERACTION API
	# -------------------------------------------------------------------------

	def tooltip( self, text=-1 ):
		"""Sets/Gets the current tooltip text."""
		if text == -1:
			return self._tooltiptext
		else:
			self._tooltiptext = str(text)

	def info( self, text=-1 ):
		"""Sets/Gets the current info text."""
		if text == -1:
			return self._infotext
		else:
			self._infotext = str(text)

	def footer( self, text=-1 ):
		"""Sets/Gets the current footer text."""
		if text == -1:
			return self._footertext
		else:
			self._footertext = str(text)

	# WIDGET INFORMATION
	# -------------------------------------------------------------------------

	def getFocused( self ):
		"""Gets the focused widget"""
		focused     = self._listbox.get_focus()[0]
		old_focused = None
		while focused != old_focused:
			old_focused = focused
			if isinstance(focused, urwid.AttrWrap):
				focused = focused.w or focused
			if hasattr(focused, "get_focus"):
				focused = focused.get_focus() or focused
		return focused

	def id( self, widget ):
		"""Returns the id for the given widget."""
		if hasattr(widget, "_urwideId"):
			return getattr(widget, "_urwideId")
		else:
			return None

	def new( self, widgetClass, *args ):
		"""Creates a new widget of the given urwid class, and returns it..
		"""
		return self._createWidget( widgetClass, *args )

	def wrap( self, widget, properties ):
		"""Wraps the given in the given properties."""
		_ui, _, _ = self._parseAttributes(properties)
		return self._wrapWidget( widget, _ui )

	def unwrap( self, widget ):
		"""Unwraps the widget (see `new` method)."""
		if isinstance(widget, urwid.AttrWrap):
			widget = widget.w or widget
		return widget

	# EVENT HANDLERS
	# -------------------------------------------------------------------------

	def handler( self, handler = None ):
		"""Sets/Gets the current event handler"""
		if handler == None:
			if not  self._handlers: raise UIRuntimeError("No handler defined")
			return self._handlers[-1]
		else:
			handler.ui = self
			if not self._handlers:
				self._handlers.append(handler)
			else:
				self._handlers[-1] = handler

	def responder( self, event ):
		"""Returns the function that responds to the given event."""
		return self.handler().responder(event)

	def pushHandler( self, handler ):
		"""Push a new handler on the list of handlers. This handler will handle
		events until it is popped out or replaced."""
		self._handlers.append(handler)
	
	def popHandler( self ):
		"""Pops the current handler of the list of handlers. The handler will
		not handle events anymore, while the previous handler will start to
		handle events."""
		return self._handlers.pop()

	def _handle( self, event_name, *args, **kwargs ):
		"""Handle the given given event name."""
		handler = self.handler()
		return handler.respond(event_name, *args, **kwargs)

	def _onPress( self, button ):
		if hasattr(button, "_urwideOnPress"):
			event_name = getattr(button, "_urwideOnPress")
			self._handle(event_name, button)
		else:
			raise UIRuntimeError("Widget does not respond to press event: %s" % (button))

	def _onFocus( self, widget, ensure=True ):
		if hasattr(widget, "_urwideOnFocus"):
			event_name = getattr(widget, "_urwideOnFocus")
			self._handle(event_name, widget)
		elif ensure:
			raise UIRuntimeError("Widget does not respond to focus event: %s" % (widget))

	def _onEdit( self, widget, before, after, ensure=True ):
		if hasattr(widget, "_urwideOnEdit"):
			event_name = getattr(widget, "_urwideOnEdit")
			self._handle(event_name, widget, before, after)
		elif ensure:
			raise UIRuntimeError("Widget does not respond to focus edit: %s" % (widget))

	def _onKeyPress( self, widget, key ):
		if widget:
			if hasattr(widget, "_urwideOnKey"):
				event_name = getattr(widget,  "_urwideOnKey")
				res = self._handle(event_name, widget, key)
				if res == False:
					self._topwidget.keypress(self._currentSize, key)
			else:
				self._topwidget.keypress(self._currentSize, key)
		else:
			self._topwidget.keypress(self._currentSize, key)

	# URWID EVENT-LOOP
	# -------------------------------------------------------------------------

	def main( self ):
		self._ui = urwid.curses_display.Screen()
		if self._palette: self._ui.register_palette(self._palette)
		self._ui.run_wrapper( self.run )

	def run( self ):
		self._currentSize = self._ui.get_cols_rows()
		self.isRunning    = True
		while self.isRunning:
			self.loop()
		# TODO: This does not work
		if self.endMessage:
			print self.endMessage

	def end( self, msg=None ):
		self.isRunning = False
		self.endMessage = msg

	def loop( self ):
		"""This is the main URWID loop, where the event processing and
		dispatching is done."""
		# We get the focused element, and update the info and and tooltip
		focused = self.getFocused() or self._topwidget
		# We update the tooltip and info in the footer
		if hasattr(focused, "_urwideInfo"): self.info(getattr(self.strings, focused._urwideInfo))
		if hasattr(focused, "_urwideTooltip"): self.tooltip(getattr(self.strings, focused._urwideTooltip))
		# We trigger the on focus event
		self._onFocus(focused, ensure=False)
		# We draw the screen
		self._updateFooter()
		self.draw()
		self.tooltip("")
		self.info("")
		# And process keys
		if not self.isRunning: return
		keys    = self._ui.get_input()
		if isinstance(focused, urwid.Edit): old_text = focused.get_edit_text()
		# We handle keys
		for key in keys:
			if key == "window resize":
				self._currentSize = self._ui.get_cols_rows()
			else:
				self._onKeyPress(focused, key)
		# We check if there was a change in the edit, and we fire and event
		if isinstance(focused, urwid.Edit):
			self._onEdit( focused, old_text, focused.get_edit_text(), ensure=False)

	def draw( self ):
		canvas = self._topwidget.render( self._currentSize, focus=True )
		self._ui.draw_screen( self._currentSize, canvas )

	def _updateFooter(self):
		"""Updates the frame footer according to info and tooltip"""
		self._footer.remove_widgets()
		footer = []
		if self.tooltip():
			footer.append(self._styleWidget(urwid.Text(self.tooltip()), {'style':'tooltip'}))
		if self.info():
			footer.append(self._styleWidget(urwid.Text(self.info()), {'style':'info'}))
		if self.footer():
			footer.append(self._styleWidget(urwid.Text(self.footer()), {'style':'footer'}))
		if footer:
			map(self._footer.add_widget, footer)
			self._footer.set_focus(0)

	# PARSING WIDGETS STACK MANAGEMENT
	# -------------------------------------------------------------------------

	def _add( self, widget ):
		# Piles cannot be created with [] as content, so we fill them with the
		# EMPTY widget, which is replaced whenever we add something
		if self._content == [self.EMPTY]: self._content[0] = widget
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

	def parse( self, style, ui ):
		self.parseStyle(style)
		self.parseUI(ui)

	def parseUI( self, text ):
		"""Parses the given text and initializes this user interface object."""
		text = string.Template(text).substitute(self._strings)
		self._content = []
		self._stack   = []
		self._header  = None
		self._currentLine = 0
		for line in text.split("\n"):
			line = line.strip()
			if not line.startswith("#"): self._parseLine(line)
			self._currentLine += 1
		self._listbox     = self._createWidget(urwid.ListBox,self._content)
		self._footer      = urwid.Pile([self.EMPTY])
		self._frame       = self._createWidget(urwid.Frame,
			self._listbox,
			self._header,
			self._footer
		)
		self._topwidget   = self._frame
		return self._content

	def parseStyle( self, data ):
		"""Parses the given style."""
		res = []
		for line in data.split("\n"):
			if not line.strip(): continue
			line = line.replace("\t", " ").replace("  ", " ")
			name, attributes = map(string.strip, line.split(":"))
			res_line = [name]
			for attribute in attributes.split(","):
				attribute = attribute.strip()
				color     = COLORS.get(attribute)
				if not color: raise UISyntaxError("Unsupported color: " + attribute)
				res_line.append(color)
			if not len(res_line) == 4:
				raise UISyntaxError("Expected NAME: FOREGROUND BACKGROUND FONT")
			res.append(tuple(res_line))
		self._palette = res
		return res

	RE_LINE = re.compile("^\s*(...)\s?")
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
			self._parseDvd(name + data)
		else:
			raise UISyntaxError("Unrecognized widget: " + name)

	def _parseAttributes( self, data ):
		assert type(data) in (str, unicode)
		ui_attrs, data = self._parseUIAttributes(data)
		args, kwargs   = self._parseArguments(data)
		return ui_attrs, args, kwargs

	RE_UI_ATTRIBUTE = re.compile("\s*([#@\?\:]|\&[\w]+\=)([\w\d_\-]+)\s*")
	def _parseUIAttributes( self, data ):
		"""Parses the given UI attributes from the data and returns the rest of
		the data (which corresponds to something else thatn the UI
		attributes."""
		assert type(data) in (str, unicode)
		ui = {"events":{}}
		while True:
			match = self.RE_UI_ATTRIBUTE.match(data)
			if not match: break
			ui_type, ui_value = match.groups()
			assert type(ui_value) == str
			if   ui_type    == "#": ui["id"]      = ui_value
			elif ui_type    == "@": ui["style"]   = ui_value
			elif ui_type    == "?": ui["info"]    = ui_value
			elif ui_type    == "!": ui["tooltip"] = ui_value
			elif ui_type[0] == "&": ui["events"][ui_type[1:-1]]=ui_value
			data = data[match.end():]
		return ui, data

	def hasStyle( self, name ):
		for r in self._palette:
			if r[0] == name: return name
		return False
	
	def _styleWidget( self, widget, ui ):
		"""Wraps the given widget so that it belongs to the given style."""
		styles = []
		if ui.has_key("id"): styles.append("#" + ui["id"])
		if ui.has_key("style"): styles.append(ui["style"])
		styles.append( widget.__class__.__name__ )
		unf_styles = filter(lambda s:self.hasStyle(s), styles)
		foc_styles = filter(lambda s:self.hasStyle(s), map(lambda s:s+"*", styles))
		if unf_styles:
			if foc_styles:
				return urwid.AttrWrap(widget, unf_styles[0], foc_styles[0])
			else:
				return urwid.AttrWrap(widget, unf_styles[0])
		else:
			return widget

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
		widget = widgetClass(*args, **kwargs)
		return self._wrapWidget(widget, _ui)

	def _wrapWidget( self, widget, _ui ):
		"""Wraps the given widget into anotger widget, and applies the various
		properties listed in the _ui (internal structure)."""
		# And now we process the ui information
		if not _ui: _ui = {}
		if _ui.has_key("id"):
			setattr(self.widgets, _ui["id"], widget)
			setattr(widget, "_urwideId", _ui["id"])
		if _ui.get("events"):
			for event, handler in _ui["events"].items():
				if   event == "press":
					if not isinstance(widget, urwid.Button):
						raise UISyntaxError("Press event only applicable to Button: " + repr(widget))
					setattr(widget, "_urwideOnPress", handler)
				elif event == "edit":
					if not isinstance(widget, urwid.Edit):
						raise UISyntaxError("Edit event only applicable to Edit: " + repr(widget))
					setattr(widget, "_urwideOnEdit", handler)
				elif event == "focus":
					setattr(widget, "_urwideOnFocus", handler)
				elif event == "key":
					setattr(widget, "_urwideOnKey", handler)
				else:
					raise UISyntaxError("Unknown event type: " + event)
		if _ui.get("info"):
			setattr(widget, "_urwideInfo", _ui["info"])
		if _ui.get("tooltip"):
			setattr(widget, "_urwideTooltip", _ui["tooltip"])
		res = self._styleWidget( widget, _ui )
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
		ui.setdefault("style", "header")
		self._header = self._createWidget(urwid.Text, data, ui=ui, args=args, kwargs=kwargs)

	def _parseFtr( self, data ):
		self.footer(data)

	RE_BTN = re.compile("\s*\[([^\]]+)\]")
	def _parseBtn( self, data ):
		match = self.RE_BTN.match(data)
		data  = data[match.end():]
		if not match: raise SyntaxError("Malformed button: " + repr(data))
		self._add(self._createWidget(urwid.Button, match.group(1), self._onPress, data=data))

	def _parseDvd( self, data ):
		ui, args, kwargs = self._parseAttributes(data[3:])
		self._add(self._createWidget(urwid.Divider, data, ui=ui, args=args, kwargs=kwargs))

	RE_EDT = re.compile("([^\[]*)\[([^\]]+)\]")
	def _parseEdt( self, data ):
		match = self.RE_EDT.match(data)
		data  = data[match.end():]
		label, text = match.groups()
		ui, args, kwargs = self._parseAttributes(data)
		if label and self.hasStyle('label'): label = ('label', label)
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

	def _parseCol( self, data ):
		def end( content, ui=None, **kwargs ):
			if not content: content = [self.EMPTY]
			self._add(self._createWidget(urwid.Columns, content, ui=ui, kwargs=kwargs))
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

	def _parseLBx( self, data ):
		def end( content, ui=None, **kwargs ):
			self._add(self._createWidget(urwid.ListBox, content, ui=ui, kwargs=kwargs))
		ui, args, kwargs = self._parseAttributes(data)
		self._push(end, ui=ui, args=args, kwargs=kwargs)

	def _parseEnd( self, data ):
		if data.strip(): raise UISyntaxError("End takes no argument: " + repr(data))
		# We get the end callback that will instanciate the widget and add it to
		# the content.
		if not self._stack: raise SyntaxError("End called without container widget")
		end_content, end_callback, end_ui, end_args, end_kwargs = self._pop()
		end_callback(end_content, end_ui, *end_args, **end_kwargs)

# ------------------------------------------------------------------------------
#
# HANDLER CLASS
#
# ------------------------------------------------------------------------------

FORWARD = False
class Handler:
	"""A handler can be subclassed an can be plugged into a UI to react to a
	specific set of events. The interest of handlers is that they can be
	dynamically switched, then making "modal UI" implementation easier.

	For instance, you could have a handler for your UI in "normal mode", and
	have another handler when a dialog box is displayed."""

	def __init__( self ):
		self.ui = None

	def respond( self, event, *args, **kwargs ):
		"""Responds to the given event name. An exception must be raised if the
		event cannot be responded to. False is returned if the handler does not
		want to handle the event, True if the event was handled."""
		responder = self.responder(event)
		return responder(*args, **kwargs) != FORWARD

	def responder( self, event ):
		"""Returns the function that responds to the given event."""
		_event_name = "on" + event[0].upper() + event[1:]
		if hasattr(self, _event_name):
			res = getattr(self, _event_name)
			assert res
			return res
		else:
			raise UIRuntimeError("Event not implemented: " + event)

# EOF
