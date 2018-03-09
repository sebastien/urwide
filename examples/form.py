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
Hdr Form

{0}

GFl
Btn [Cancel]                        #btn_cancel &press=cancel
Btn [Save]                          #btn_save   &press=save
End
"""

# This is a dynamic list of fields
FIELDS = [
	{"id": "project", "label" :"Project name"},
	{"id": "client",  "client":"Client  name"},
	{"type":"separator"},
	{"id": "description",  "client":"Client  name", "multiline":True},
]

def create_fields(fields=FIELDS):
	res = []
	labels_len = max(len(_.get("label", _.get("id", ""))) for _ in fields)
	for f in fields:
		if f.get("type") == "separator":
			res.append("---")
		else:
			id          = f.get("id")
			ID          = id.upper()
			label       = f.get("label", id).capitalize()
			label       = label + " " * (labels_len - len(label))
			placeholder = f.get("placeholder", "")
			attributes  = []
			if f.get("multiline"):
				res.append("Txt {label}".format(label=label))
				field = "Edt [{placeholder}] #{id} ?{ID} {attributes}".format(
					id=id,
					ID=ID,
					label=label,
					placeholder=placeholder,
					attributes=" ".join(attributes)
				)
			else:
				field = "Edt {label} [{placeholder}] #{id} ?{ID} {attributes}".format(
					id=id,
					ID=ID,
					label=label,
					placeholder=placeholder,
					attributes=" ".join(attributes)
				)
			res.append(field)
	return "\n".join(res)


# Event handler
class Handler(urwide.Handler):

	def onSave( self, button ):
		self.ui.info("Saving")
		res = {}
		for field in FIELDS:
			fid = field.get("id")
			if not fid: continue
			res[fid] = getattr(self.ui.widgets, fid).get_edit_text()
		# NOTE: We write the files to `form.json`
		with open("form.json","w") as f:
			json.dump(res, f)
		self.exit()

	def onCancel( self, button ):
		self.ui.info("Cancel")
		self.exit()

	def exit( self ):
		sys.exit()

# Defines strings referenced in the UI
ui                 = urwide.Console()
ui.create(CONSOLE_STYLE, CONSOLE_UI.format(create_fields()), Handler())

# Main
if __name__ == "__main__":
	ui.main()

# EOF
