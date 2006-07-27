import urwide, os

# Defines the style and user interface
CONSOLE_STYLE = """
Frame         : Lg, DB, SO
header        : WH, DC, BO
shade         : DC, DB, BO

label         : WH, DB, SO
dialog        : BL, Lg, SO
shadow        : WH, BL, SO
shadow.border : BL,  _, SO

Edit          : BL, DB, BO
Edit*         : DM, Lg, BO
Button        : WH, DC, BO
Button*       : WH, DM, BO
Divider       : Lg, DB, SO
"""

DIALOG_STYLE = """
header        : BL, Lg, BO
"""

CONSOLE_UI = """\
Hdr URWIDE Dialog example
___

Txt Please select any of these buttons to pop-up a dialog !
GFl
Btn [Alert]                         #btn_alert  &press=alert
Btn [Ask]                           #btn_ask    &press=ask
Btn [Choose]                        #btn_choose &press=choose
End

Ftr Press any button to pop up a dialog
"""

ALERT_UI = """\
Hdr Alert dialog

Txt This is an alert box, display the message you want here

GFl
# And do not forget to provide a buttong with an exit handler
Btn [OK]                              #btn_end
End
"""

ASK_UI = """\
Hdr Ask dialog

Txt Please respond to this question
Edt [your answer]

GFl
# And do not forget to provide a buttong with an exit handler
Btn [OK]                              #btn_end
Btn [Cancel]                          #btn_cancel
End
"""

# Event handler
class Handler(urwide.Handler):

	def onAlert( self, button ):
		dialog = urwide.Dialog(self.ui, ui=ALERT_UI,palette=DIALOG_STYLE, height=10)
		dialog.onPress(dialog.widgets.btn_end, lambda b:dialog.end())
		self.ui.dialog(dialog)

	def onCancel( self, button ):
		self.ui.info("Cancel")
		self.exit()

	def onAsk( self, button ):
		dialog = urwide.Dialog(self.ui, ui=ASK_UI,palette=DIALOG_STYLE, height=10)
		dialog.onPress(dialog.widgets.btn_end, lambda b:dialog.end())
		self.ui.dialog(dialog)

# Defines strings referenced in the UI
ui = urwide.Console().create(CONSOLE_STYLE, CONSOLE_UI, Handler())

# Main
if __name__ == "__main__":
	ui.main()

# EOF
