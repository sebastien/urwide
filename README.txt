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

>    #id

Widget style class

>    @style

Widget tooltip

>    !TEXT

Widget info

>    ?TEXT

Event handling

>    >event=method

Supported events:

    - _focus_ 
    - _edit_
    - _key_

Python arguments

>    name=value, name=value, name=value

Container widgets

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

# vim: ts=4 sw=4 et fenc=latin-1 syn=kiwi
