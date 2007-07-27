== URWIDE
== An easy to use extension to URWID
-- Author: Sébastien Pierre <sebastien@type-z.org>
-- Date: 30-Mar-2007

Introduction
============

    [URWID][1] is a  powerful library that allows to write command-line
    interfaces in the [Python][2] language. While URWID is very powerful, it is
    quite low-level compared to existing UI toolkits, which can make development
    of more advanced user interface a bit difficult.

    The main idea behing URWIDE is to extend URWID with a set of functions that
    allow to *write an URWID application with less code*, and that helps you in
    common tasks involved in writing a UI.

    Currently, URWIDE offers you the following features:

    - Natural text-based description of your UI
    - Event support (key, focus, press, edit)
    - Collections of strings (for i18n)
    - Dialog support

    To give you an idea of what URWIDE can provide, here is a very simple
    `helloworld.py` example:

    >   import urwide
    >   CONSOLE_STYLE = """
    >   Frame         : Dg,  _, SO
    >   header        : WH, DC, BO
    >   """
    >   CONSOLE_UI = """\
    >   Hdr URWIDE Hello world
    >   ___
    >   
    >   Txt Hello World !                     args:#txt_hello
    >   GFl
    >   Btn [Hello !]                         &press=hello
    >   Btn [Bye   !]                         &press=bye
    >   End
    >   """
    >   class Handler(urwide.Handler):
    >       def onHello( self, button ):
    >           self.ui.widgets.txt_hello.set_text("You said hello !")
    >       def onBye( self, button ):
    >           self.ui.end("bye !")
    >   urwide.Console().create(CONSOLE_STYLE, CONSOLE_UI, Handler()).main()

UI Description Language
=======================

    URWIDE allows to describe a user interface using a very simple line-oriented
    language. You can define a complete UI in just a few lines. This description
    allows you to:

        - Identify your widgets with a unique name
        - Associate detailed information and tooltip
        - Bind style information to your widgets
        - Bind event handlers

    The description syntax is very simple, and simply consists of a set of lines of
    the following form:

    >   CLS DATA? [ID|STYLE|INFO|EVENT]* [ARGUMENTS]

    as an example, here is the definition of a button with `Click me!` as label,
    which will be available as `btn_click`, displayed using the `clickButton`
    style, displaying the `CLICK` tooltip when focused, and calling the
    `clicked` callback when pressed :

    >   Btn [Click me!] #btn_click @clickButton !CLICK &press=clicked

    To sum up the available attributes:

        - _CLS_ is a three letter code that corresponds to the widget code
        - _DATA_ is a widget-specific text content
        - _ID_ sets the identifier of the widget
        - _STYLE_ sets the style class of the widget
        - _EVENT_ defines an event handler attached to the widget
        - _INFO_ defines the widget tooltip and detailed information 
        - _ARGUMENTS_ defines additional widget attributes 

    Widget identifier::

        >    #id

    Widget style class::

        >    @style

    Widget tooltip::

        >    !TEXT

    Widget info::

        >    ?TEXT

    Event handling::

        >    &event=method

    Supported events::

        - _focus_ 
        - _edit_
        - _key_

    Python arguments::

        >    name=value, name=value, name=value

    Comments::

        >    # This is a comment

    Comments are useful to annotate your URWIDE source code, or to enable/disable
    parts of it. Comments are simply lines starting with the `#` character.

    Blocks
    ------

    >   Ple
    >   Txt I am within the above pile
    >   End

    or

    >   GFl
    >   Txt Here are buttons
    >   Btn [previous]
    >   Btn [next]
    >   End

    == Syntax summary
    ==========================================================================
    *SYNTAX*          || *DESCRIPTION*
    ==========================================================================
    `#name`           || Widget name, makes it accessible as `ui.widgets.name`
    --------------------------------------------------------------------------
    `@class`          || Style class associated with the widget.
    --------------------------------------------------------------------------
    `&event=callback` || Makes the `onCallback` method of the `ui.handler()`
                      || react to the  `event` (press, key, edit, focus) when
                      || it occurs on the widget.
    --------------------------------------------------------------------------
    `!TOOLTIP`        || `ui.strings.TOOLTIP` or `"TOOLTIP"` is used as a
                      || tooltip for the widget (when it is focused)
    --------------------------------------------------------------------------
    `?INFO`           || `ui.strings.INFO` or `"INFO"` is used as
                      || information for the widget (when it is focused)
    --------------------------------------------------------------------------
    `arg=value, ...`  || Additional Python arguments that will be passed to
                      || the widget constructor (eg. `multiline=true` for Edit)
    --------------------------------------------------------------------------
    `# comment`       || a comment line that will be ignored when parsing
    ==========================================================================

Supported Widgets
=================

    URWIDE tries to support most used URWID widgets, and also introduces _pseudo
    widgets_ that facilitate the specification of your application layout.

    Blank
    -----

    >    EOL

    A blank widget is simply an _empty line_ within the UI description.

    Divider
    -------

    >   ---
    >   ===
    >   :::

    These three forms create dividers composed of respectively `-`, `=` and `:`
    characters. In case you will want a particular pattern in your divider, you
    can user the following form:

    >   Dvd ~-~-

    Which will make you a divider composed of `~-~-`.


    Text
    ----

    >   Txt TEXT
    >   Txt TEXT args:ARGUMENTS
    
    Examples

    >   Txt Hello, I'm a text 
    >   Txt Hello, I'm a text args:align='left'

        Note _________________________________________________________________
        Be sure to use the `args:` prefix to give arguments to the text, because
        otherwise your arguments will be interpreted as being part of the
        displayed text.

    Button
    ------

    >   Btn [LABEL]

    Choice
    ------

    >   Chc [ :group] I am an unselected option
    >   Chc [X:group] I am a selected option
    >   Chc [X:other] I am a selected option from the 'other' group
    >   Chc [ :group] I am an unselected option args:#my_choice

    A choice is composed of:

    - Its _state_ and _group_ represented by the leading '[S:GROUP]', where 'S'
      is either ' ' or 'X' and 'GROUP' is any string. Groups are availabled in
      as 'ui.groups.GROUP' ('ui.groups' is a 'UI.Collection' instance)

    - Its _label_, following the state and group definition. It can be free-form
      text.

    - The _ui arguments_, optionally following the label, but prefixed by
      'args:'

    Pile
    ----

    >   Ple
    >   ...
    >   End

    Gridflow
    --------

    >   Gfl 
    >   ...
    >   End

    Box
    ---

    >   Box border=1
    >   ...
    >   End

    Boxes allow to draw a border around a widget. You can simply indicate the
    size of the border using the `border` attribute.

    Columns
    -------

    >   Col
    >       ***
    >   End

    Summary
    -------
  
    == Supported Widgets
    ==========================================================================
    *CODE* || *WIDGET*           ||*TYPE*
    ==========================================================================
    `Txt`  || Text               || widget
    --------------------------------------------------------------------------
    `Edt`  || Edit               || widget
    --------------------------------------------------------------------------
    `Btn`  || Button             || widget
    --------------------------------------------------------------------------
    `Chc`  || RadioButton        || widget
    --------------------------------------------------------------------------
    `Dvd`  || Divider            || widget
    --------------------------------------------------------------------------
    `Ple`  || Pile               || container
    --------------------------------------------------------------------------
    `GFl`  || GridFlow           || container
    --------------------------------------------------------------------------
    `Box`  || Box (not in URWID) || container
    ==========================================================================


Event handling
==============

    URWIDE provides support for handling events and binding event handlers to each
    individual widget. The events currently supported are:

     - `focus` (any), which is triggered when the widget received focus
     - `key` (any), which is triggered when a key is pressed on a widget
     - `edit` (Edit), which is triggered after an Edit was edited
     - `press` (Buttons, CheckBox), which is triggered when a button is pressed

    Events are handled by _handlers_, which are objects that define methods that
    implement a particular reaction. For instance, if you have an event named
    `showHelp`, you handler class will be like that:

    >   class MyHandler(urwide.Handler):
    >   
    >       def onShowHelp( self, widget ):
    >           # Do something here

    And then, if you want to trigger the "`showHelp`" event when a button is
    pressed:

    >   Btn [Show help] &press=showHelp

    This will automatically make the binding between the ui and the handler,
    provided that you register your handler into the ui:

    >   ui.handler(MyHandler())

Collections
===========

    URWIDE will create an instance of the `urwide.UI` class when given a style (will
    be presented later) and a UI description. This instance will take care of
    everything for you, from events to widgets. You will generally only want to
    access or modify the `widgets` and `strings` collections.

    Both collections can be edited by accessing values as attribute. Setting an
    attribute will add a key within the collection, accessing it will return the
    bound value, or raise an exception if the value was not found.

    >   ui.strings.SOME_TEXT = "This text can be used as a value in a widget"

    >   ui.widgets


API
===

    1. The 'Console' class
    ----------------------


Style syntax
============

    >   [STYLE] : FG, BG, FN

        - _STYLE_ is the name of the style
        - _FG_ is the foreground color
        - _BG_ is the backgrond color
        - _FN_ is the font style

    A style name can be:

        - _URWID widget name_ (`Edit`, `Text`, etc)
        - _style name_ (defined by `@style` in the widgets list)
        - _widget id_, as defined by the `#id` of the UI

    Focus styles can be specified by appending `*` to each style name:

    >   Edit        : BL, _, SO
    >   Edit*       : DM, Lg, SO

    means that all `Edit` widgets will have black as color when unfocused, and dark
    magenta when focused.


    Here is a table that sums up the possible values that can be used to describe
    the styles. These values are described in the URWID reference for the
    [Screen](http://excess.org/urwid/reference.html#Screen-register_palette_entry)
    class.

    == Style values
    ==========================================================================
    *CODE* || *VALUE*       ||*FOREGROUND*||*BACKGROUND*|| *FONT*
    ==========================================================================
    WH     || white         || yes        || no         || -
    --------------------------------------------------------------------------
    BL     || black         || no         || yes        || -
    --------------------------------------------------------------------------
    YL     || yellow        || yes        || no         || -
    --------------------------------------------------------------------------
    BR     || brown         || yes        || no         || -
    --------------------------------------------------------------------------
    DG     || dark red      || no         || yes        || -
    --------------------------------------------------------------------------
    DB     || dark blue     || yes        || yes        || -
    --------------------------------------------------------------------------
    DG     || dark green    || yes        || yes        || -
    --------------------------------------------------------------------------
    DM     || dark magenta  || yes        || yes        || -
    --------------------------------------------------------------------------
    DC     || dark cyan     || yes        || yes        || -
    --------------------------------------------------------------------------
    Dg     || dark gray     || yes        || no         || -
    --------------------------------------------------------------------------
    LR     || light red     || yes        || no         || -
    --------------------------------------------------------------------------
    LG     || light green   || yes        || no         || -
    --------------------------------------------------------------------------
    LB     || light blue    || yes        || no         || -
    --------------------------------------------------------------------------
    LM     || light magenta || yes        || no         || -
    --------------------------------------------------------------------------
    LC     || light cyan    || yes        || no         || -
    --------------------------------------------------------------------------
    Lg     || light gray    || yes        || yes        || -
    --------------------------------------------------------------------------
    BO     || bold          || -          || -          || yes
    --------------------------------------------------------------------------
    UL     || underline     || -          || -          || yes
    --------------------------------------------------------------------------
    SO     || standout      || -          || -          || yes
    --------------------------------------------------------------------------
    _      || default       || yes        || yes        || yes
    ==========================================================================

Using dialogs:

    dialog = Dialog()
    # Don't know why this is necessary, but it doesn't work if it's not there
    sialog.handler(dialog_handler)
    self.pushHandler(dialog_handler)

    def dialog_end():
        self.popHandler()

 [1]: URWID by Ian Ward, <http://www.excess.org/urwid>
 [2]: Python Language (2.4), <http://www.python.org>

# vim: ts=4 sw=4 et fenc=latin-1 syn=kiwi
