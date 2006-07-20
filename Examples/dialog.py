import urwide, os

# Defines the style and user interface
STYLE = """
Frame         : Dg,  _, SO
header        : WH, DC, BO
shade         : DC, Lg, BO

label         : Lg,  _, SO
dialog        : BL, Lg, SO
shadow        : WH, BL, SO
shadow.border : BL,  _, SO

Edit          : BL,  _, BO
Edit*         : DM, Lg, BO
Button        : WH, DC, BO
Button*       : WH, DM, BO
Divider       : Lg,  _, SO

#subject      : DM,  _, SO
"""

UI = """\
Hdr URWIDE Dialog example
::: @shade

Txt Please select any of these buttons to pop-up a dialog !
GFl
Btn [Alert]                         #btn_alert  &press=alert
Btn [Ask]                           #btn_ask    &press=ask
Btn [Choose]                        #btn_choose &press=choose
End

Ftr Press any button to pop up a dialog
"""

ALERT = """\
Hdr ALERT dialog

___

Txt This is an alert box, display the message you want here

GFl
# And do not forget to provide a buttong with an exit handler
Btn [OK]                                        &press=end
End
"""


# Defines strings referenced in the UI
ui                 = urwide.UI()
ui.parse(STYLE, UI)

# Event handler
class Handler(urwide.Handler):

	def onAlert( self, button ):
		self.ui.dialog(urwide.Dialog(ui=ALERT))

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
