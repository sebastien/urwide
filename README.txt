== URWIDE
-- An easy to use extension to URWID
-- Author: Sébastien Pierre <sebastien@xprima.com>
-- Date: 17-Jul-2005

Introduction
============

[URWID] is a very powerful library that allows to write command-line interfaces
in the [Python] language.

While URWID is very powerful, it is quite low-level compared to existing UI
toolkits, which can make development of more advanced user interface difficult.
The main idea behing URWIDE is to extend URWID with a set of functions that
allow to write an URWID application with less code, and that helps you in
common tasks involved in writing a UI.

UI generation
=============

URWIDE allows to describe a user interface using a very simple line-oriented
language. You can define a complete UI in just a few lines. This description
allows you to:

    - Identify your widgets with a unique name
    - Associate detailed information and tooltip
    - Bind style information to your widgets
    - Bind event handlers

The description syntax is very simple, and simply consists of a set of lines of
the following form:

>    CLS DATA? [ID|STYLE|INFO|EVENT]* [ARGUMENTS]

    - _CLS_ is a three letter code that corresponds to the widget code
    - _DATA_ is a widget-specific text content
    - _ID_ sets the identifier of the widget
    - _STYLE_ sets the style class of the widget
    - _EVENT_ defines an event handler attached to the widget
    - _INFO_ defines the widget tooltip and detailed information 
    - _ARGUMENTS defines additional widget attributes 

Widget identifier
-----------------

>    #id

Widget style class
------------------

>    @style

Widget tooltip
--------------

>    !TEXT

Widget info
-----------

>    ?TEXT

Event handling
----------------

>    &event=method

Supported events:

    - _focus_ 
    - _edit_
    - _key_

Python arguments
----------------

>    name=value, name=value, name=value

Comments
--------

>   # This is a comment

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

Supported Widgets
=================

Blank
-----

>   

Divider
-------

>   ---
>   ===
>   :::


Text
----

>   Txt TEXT
>   Txt TEXT args:ARGUMENTS

Button
------

>   Btn [LABEL]


Pile
----

Gridflow
--------

>   Gfl 

Events
======

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
the styles. These values are described in the URWID reference for the [Screen](
http://excess.org/urwid/reference.html#Screen-register_palette_entry)class.

== Style values
================================================================================
*CODE* || *VALUE*       ||*FOREGROUND*||*BACKGROUND*|| *FONT*
================================================================================
WH     || white         || yes        || no         || -
--------------------------------------------------------------------------------
BL     || black         || no         || yes        || -
--------------------------------------------------------------------------------
YL     || yellow        || yes        || no         || -
--------------------------------------------------------------------------------
BR     || brown         || yes        || no         || -
--------------------------------------------------------------------------------
DG     || dark red      || no         || yes        || -
--------------------------------------------------------------------------------
DB     || dark blue     || yes        || yes        || -
--------------------------------------------------------------------------------
DG     || dark green    || yes        || yes        || -
--------------------------------------------------------------------------------
DM     || dark magenta  || yes        || yes        || -
--------------------------------------------------------------------------------
DC     || dark cyan     || yes        || yes        || -
--------------------------------------------------------------------------------
Dg     || dark gray     || yes        || no         || -
--------------------------------------------------------------------------------
LR     || light red     || yes        || no         || -
--------------------------------------------------------------------------------
LG     || light green   || yes        || no         || -
--------------------------------------------------------------------------------
LB     || light blue    || yes        || no         || -
--------------------------------------------------------------------------------
LM     || light magenta || yes        || no         || -
--------------------------------------------------------------------------------
LC     || light cyan    || yes        || no         || -
--------------------------------------------------------------------------------
Lg     || light gray    || yes        || yes        || -
--------------------------------------------------------------------------------
BO     || bold          || -          || -          || yes
--------------------------------------------------------------------------------
UL     || underline     || -          || -          || yes
--------------------------------------------------------------------------------
SO     || standout      || -          || -          || yes
--------------------------------------------------------------------------------
_      || default       || yes        || yes        || yes
================================================================================


# vim: ts=4 sw=4 et fenc=latin-1 syn=kiwi
