== URWIDE
-- Making URWIDE even easier
-- Author: Sébastien Pierre <sebastien@xprima.com>
-- Date: 14-Jul-2005

Introduction
============

UI syntax
=========

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
Code || Value         || Foreground || Background || Font
--------------------------------------------------------------------------------
WH   || white         || yes        || no         || -
--------------------------------------------------------------------------------
BL   || black         || no         || yes        || -
--------------------------------------------------------------------------------
YL   || yellow        || yes        || no         || -
--------------------------------------------------------------------------------
BR   || brown         || yes        || no         || -
--------------------------------------------------------------------------------
DG   || dark red      || no         || yes        || -
--------------------------------------------------------------------------------
DB   || dark blue     || yes        || yes        || -
--------------------------------------------------------------------------------
DG   || dark green    || yes        || yes        || -
--------------------------------------------------------------------------------
DM   || dark magenta  || yes        || yes        || -
--------------------------------------------------------------------------------
DC   || dark cyan     || yes        || yes        || -
--------------------------------------------------------------------------------
Dg   || dark gray     || yes        || no         || -
--------------------------------------------------------------------------------
LR   || light red     || yes        || no         || -
--------------------------------------------------------------------------------
LG   || light green   || yes        || no         || -
--------------------------------------------------------------------------------
LB   || light blue    || yes        || no         || -
--------------------------------------------------------------------------------
LM   || light magenta || yes        || no         || -
--------------------------------------------------------------------------------
LC   || light cyan    || yes        || no         || -
--------------------------------------------------------------------------------
Lg   || light gray    || yes        || yes        || -
--------------------------------------------------------------------------------
BO   || bold          || -          || -          || yes
--------------------------------------------------------------------------------
UL   || underline     || -          || -          || yes
--------------------------------------------------------------------------------
SO   || standout      || -          || -          || yes
--------------------------------------------------------------------------------
_    || default       || yes        || yes        || yes
================================================================================

# vim: ts=4 sw=4 et fenc=latin-1 syn=kiwi
