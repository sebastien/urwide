import urwide, os, sys

# Defines the style and user interface
CONSOLE_STYLE = """
Frame         : Dg, DB, SO
header        : WH, DC, BO
shade         : DC, DB, BO

label         : Lg, DB, SO

Edit          : WH, DB, BO
Edit*         : DM, Lg, BO
Button        : WH, DC, BO
Button*       : WH, DM, BO
Divider       : Lg, DB, SO

#subject      : DM, DB, SO
"""

CONSOLE_UI = """\
Hdr URWIDE Mail Editor
::: @shade

Edt   From          [%s]          #from         ?FROM
Edt   To            [List of recipients]    #to           ?TO
---
Edt   Subject       [Subject]               #subject      ?SUBJECT
---

Box  border=1
Edt  [Content]     #content &edit=changeContent multiline=True
End

===
GFl
Btn [Cancel]                        #btn_cancel &press=cancel
Btn [Save]                          #btn_save   &press=save
Btn [Send]                          #btn_commit &press=send
End
""" % ("me")


# Event handler
class Handler(urwide.Handler):

	def onSave( self, button ):
		self.ui.info("Saving")

	def onCancel( self, button ):
		self.ui.info("Cancel")
		self.exit()

	def onSend( self, button ):
		self.ui.info("Send")

	def onChangeContent( self, widget, oldtext, newtext ):
		if oldtext != newtext:
			self.ui.info("Email content changed !")

	def exit( self ):
		sys.exit()

# Defines strings referenced in the UI
ui                 = urwide.Console()
ui.strings.FROM    = "Your email address"
ui.strings.TO      = "Comma separated list of recipient adresses"
ui.strings.SUBJECT = "The subject for your email"
ui.create(CONSOLE_STYLE, CONSOLE_UI, Handler())

# Main
if __name__ == "__main__":
	ui.main()

# EOF
