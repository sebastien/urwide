import urwide, os

# Defines the style and user interface
CONSOLE_STYLE = """
Frame         : Dg,  _, SO
header        : WH, DC, BO
"""

CONSOLE_UI = """\
Hdr URWIDE Hello world
___

Txt Hello World !                     args:#txt_hello
GFl
Btn [Hello !]                         &press=hello
Btn [Bye   !]                         &press=bye
End
"""

# Event handler
class Handler(urwide.Handler):
	def onHello( self, button ):
		self.ui.widgets.txt_hello.set_text("You said hello !")
	def onBye( self, button ):
		self.ui.end("bye !")

urwide.Console().create(CONSOLE_STYLE, CONSOLE_UI, Handler()).main()


# EOF
