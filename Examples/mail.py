import urwide, os

# Defines the style and user interface
STYLE = """
Frame         : Dg,  _, SO
header        : WH, DC, BO
shade         : DC, Lg, BO

label         : Lg,  _, SO

Edit          : BL,  _, BO
Edit*         : DM, Lg, BO
Button        : WH, DC, BO
Button*       : WH, DM, BO
Divider       : Lg,  _, SO

#subject      : DM,  _, SO
"""

UI = """\
Hdr URWIDE Mail Editor
::: @shade

Edt  From          [%s]          #from         ?FROM
Edt  To            [List of recipients]    #to           ?TO
---
Edt  Subject       [Subject]               #subject      ?SUBJECT
---
Edt  [Content]     #content &edit=changeContent multiline=True
===
GFl
Btn [Cancel]                        #btn_cancel &press=cancel
Btn [Save]                          #btn_save   &press=save
Btn [Send]                          #btn_commit &press=send
End
""" % ("me")

# Defines strings referenced in the UI
ui                 = urwide.Console()
ui.strings.FROM    = "Your email address"
ui.strings.TO      = "Comma separated list of recipient adresses"
ui.strings.SUBJECT = "The subject for your email"
ui.parse(STYLE, UI)

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

ui.handler(Handler())

# Main
if __name__ == "__main__":
	ui.main()

# EOF
