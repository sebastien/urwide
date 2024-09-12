from urwide import ui

app = ui(
    """\
Hdr URWIDE - Git Commit $COMMIT

Box
  Edt Name          [$USERNAME]               #edit_user
  Edt Tags          [Update]                  #edit_tags    ?TAGS    &key=tag
  Edt Scope         [‥]                       #edit_scope   ?SCOPE   &key=scope
  Edt Summary       [‥]                       #edit_summary ?SUMMARY &key=sumUp
End
Dvd ┄┄┄

Box
  Edt [‥]                                   #edit_desc    ?DESC &key=describe multiline=True
End

Dvd ―――

Ple                                         #changes
End
Dvd ―――

GFl
	Btn [Cancel]                            #btn_cancel  &press=cancel
	Btn [Commit]                            #btn_commit  &press=commit
End
""",
    """
header : BL, WH, SO 
Edit   : Dg, _, BO
Edit*  : WH, DB, BO
""",
    USERNAME="Joe",
    COMMIT="asdsadasdasass",
)
app.run()
