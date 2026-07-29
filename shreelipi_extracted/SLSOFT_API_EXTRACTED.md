---
title: Shree-Lipi Soft API Reference (Extracted from SHREELIPI_SOFT_API.pdf)
source: /tmp/SL74DVD/PDF_FIies/SHREELIPI_SOFT_API.pdf
pages: 131
extracted: 2026-07-04
notes: >
  This is the "Shree-Samhita Reference Manual" by Modular InfoTech Pvt Ltd, Pune.
  Covers the Shree-Lipi Soft SDK API for integrating multilingual Indian language
  support into Windows applications. Key areas: script management, font layout system,
  format conversion (SL/Suchika/ISCII/Unicode/UTF-8), transliteration with dictionary
  support, dot matrix printing, and ISCII printer support.
---

# Shree-Samhita / Shree-Lipi Soft API Reference Manual

A
contact us at

Modular InfoTech Pvt Ltd,
26, Electronic Co-operative Estate,
Pune-Satara Road,
Pune-411009,
Maharashtra.
Phone : (020) 24223510, (020) 24227994
Fax : (020) 24225896
E-mail : modular@giaspn01.vsnl.net.in
Web-Site : http:// www.modular-infotech.com


## Chapter 1: Introduction
Rapid advancement in the field of Computer technology,
continuous fall in the price of hardware and ever increasing
public awareness of computer based systems has made
computers a common thing of the society. Gone are the days
when only a few selected companies and business houses used
to boast of computerized systems. Computers have spread into
all the sections of society including small offices, municipal
corporations, banking sectors and co-operative organizations.
There is an increasing need for software packages that can be
operated in multiple languages including English, as a layman
can understand only the local language. As a result, software
developers are faced with the tough task of developing
packages that support multiple languages.

What is Shree-Lipi Soft?
Modular Infotech Pvt Ltd is a renowned name in the field of
software solutions with multilingual support. Shree-Lipi
Soft is Modular Infotech Pvt Ltd's answer to the current
needs of the software developer. Using Shree-Lipi Soft, the
developer/programmer can incorporate multilingual facility
in his package with very little effort. As a matter of fact, the
developer need not change his development platform.
Shree-Lipi Soft provides full support for all window-based
platforms including Visual Basic, PowerBuilder, Delphi,
Visual C++, Oracle-Developer 2000 and so on. The
developer can get a bang start by using modules (platform
specific) provided along with Shree-Lipi Soft in his project.
In fact using Shree-Lipi Soft is as simple as using external


functions as it comprises of a set of Dynamic Link
Libraries(DLLs) and support files.
In addition to the API for the developers, Shreee-Lipi Soft
packs all the features of Shree-Lipi, Modular's most
popular multilingual package. This enables the users of the
applications to use Indian languages in other Windows
applications like MS Office, PageMaker, Corel Draw etc.
This manual covers the API supported by Shree-Lipi Soft. The
other features of Shree-Lipi are covered in the other product
manual.


## Chapter 2: Shree-Lipi Soft Installation
Install Shree-Lipi Soft from the CD 1. This CD has Autorun
facility, and after inserting the CD, you will be prompted through
the installation. Follow the installation procedures from the
Shree-Lipi product manual.
After installation, all the DLLs required for program development
are copied into the Shree-Lipi directory, say Shree60. The
following DLLs are required for the application development
using Shree-Lipi Soft:
SLSDLL.DLL : The interface DLL.
SHREE.DLL : DLL supporting Indian language composing
CONV32.DLL : DLL supporting conversions
CNVAPI32.DLL : DLL supporting conversions
TRANS32.DLL : DLL supporting transliteration
DMP.DLL : DLL supporting fast dot matrix printing calls.
There are a number of other DLLs and dependency files that
get installed in the Shree-Lipi directory.


System Requirements
Shree-Lipi Soft is a full-fledged 32-bit application and requires
Windows95 / 98 / NT (version 3.5 or above) / 2000 / XP as the
operating system. Shree-Lipi Soft API comprises of a set of
DLLs and support files. It is recommended that the end user
should have an Pentium processor with 32 MB RAM at the
minimum. In addition to the disk space occupied by the
developer's project files, Shree-Lipi Soft takes 20MB(approx.) of
hard
disk
space.


## Chapter 3: Shree-Lipi Soft API Overview
Shree-Lipi Soft API is supported by DLLs with exportable
functions that can be called from a project for getting the
desired multilingual features. The following are the points to
remember while working with Shree-Lipi Soft API.
1. Shree-Lipi Soft API supports all Indian language scripts
except Urdu. The current script is represented by a code. For
example if the typing mode is English then the script code is 0
and if typing in Indian languages is enabled then it is as below.
In some functions and procedures it is necessary to pass the
script code as a parameter. The following are the script codes
used throughout Shree-Lipi Soft API.
Code

Script

0

English


Devnagari (Hindi / Marathi)


Gujarati


Punjabi (Gurumukhi)


Bengali & Assamese


Oriya


Tamil


Kannada


Telugu


Malayalam


Sanskrit


Assamese

2. Shree-Lipi Soft provides calls for converting numbers to
Indian language strings. This requires one additional parameter,
which is the Script Language. A Script may support multiple
languages for e.g. Devnagari supports Hindi as well as Marathi
language. The following are the Script language codes used in
Shree-Lipi Soft API.
Script

Language

Code

Devnagari
Marathi
0
Devnagari
Hindi
The other scripts support only one language and hence the
value is 0 for all other languages.

Font Layout
Shree-Lipi Soft supports a number of font layouts for all the
scripts. They are as follows
Layouts supported for all scripts :
Layout
Constant

Description
0Shree-Lipi 2,3
Suchika for Shree-Lipi 2,3 (except for Bengali,
1Assamese, Oriya)
15 Shree-Lipi 4,5,6


Layout
Constant

Description
18 Suchika for Shree-Lipi 4,5,6

Layouts supported for Devnagari
Layout
Constant

Description
4Isfoc
8Indica (Chanakya)
9Akruti
30APS
29Isfoc bilingual fonts
2Swadesh 2.0
62Bharati

Layouts supported for Gujarati
Layout
Constant

Description
10Akruti
5IIsmguj

Layouts supported for Bengali
Layout
Constant

Description
21Bangla Academy font for Bengali special package
86Bengali Transparent Font


Layout
Constant

Description
75Bengali Summit
7Monotype Bengali
20Bengali Prakashak

Layouts supported for Assamese
Layout
Constant

Description
21Bangla Academy font for Bengali special package
86Bengali Transparent Font
75Bengali Summit
7Monotype Bengali
20Bengali Prakashak

Layouts supported for Oriya
Layout
Constant

Description
57Akruti95
58Akruti98
59Akruti99

Layouts supported for Tamil
Layout
Constant

Description
12Tamil 99 Monolingual


Layout
Constant

Description
13Tamil 99 Bilingual
70ANU
77IDS
52LASTECH (Indoword)
32Isfoc
68Monotype

Layouts supported for Kannada
Layout
Constant

Description
47Kannada Ganak Parishad standard layout / Nudi
33 Isfoc
36 Prakashak

Layouts supported for Telugu
Layout
Constant

Description
11 Anugraphic 1.0
14 Anugraphic 4.0
34 Isfoc

Layouts supported for Malayalam
Layout
Constant

Description


Layout
Constant

Description
6 Isfoc
29Isfoc bilingual fonts
17 Panchari font
37 Malayalam Thoolika

Layouts supported for all scripts for conversion only
Layout
Constant

Description
22 ISCII
23 PCISCII
24EAISCII (7 bit)
25 Sort32
26Modular editor
76UTF8
45 Unicode

In the above mentioned layouts (except the layouts supported
for conversion only), the user can type in the Indian languages
as supported by the package by activating the SCROLL-LOCK
key in the keyboard and selecting the proper script. As an
example, suppose the font for an Edit Control has been set as
SHREE-DEV-0708 (Modular Devnagari monolingual font of
Shree Layout) of Point size 14. If SCROLL-LOCK is the current
script activation key and it is active, then the user can type in
Devnagari script. If SCROLL-LOCK key is turned off, the user
can type in English but since the font has been set as SHREEDEV-0708, any text typed in that Edit Box will be meaningless.


Suchika fonts are bilingual fonts. i.e. these fonts contain
characters for English and one Indian language. In this layout
the user can type in any of the Indian languages supported by
the package as well as in English. When the SCROLL-LOCK
key is active, the user can type in Indian Language and with the
SCROLL-LOCK key inactive, the user can type in English. As
an example suppose the font for an Edit Control has been set
as SUCHI-DEV-0708 (Modular Devnagari Bilingual font) of
Point size 14. If SCROLL-LOCK is the current script activation
key and it is active, then the user can type in Devnagari script. If
SCROLL-LOCK key is turned off, the user can type in English.
Since the font this time is of Suchika layout, text typed in the
Edit control will be in meaningful English as is desired. Hence
Suchika Layout supports bilingual fonts (English and Indian
both). Also since English alphabet is to be incorporated in the
character set, all language characters may not be supported in
this layout.
Keyboard Layout
Since a typical keyboard consists of English characters only, for
typing in Indian Languages it is necessary to select a keyboard
layout. Keyboard layout refers to how the keys of Keyboard are
mapped to the Character set of Indian languages. This varies
with script. As an illustration when we are typing in English for
typing 'A' we type Shift + 'a'. In the same way for typing
ma(Devnagari) in MODULAR Keyboard layout we type 'a'. It is a
must that Shree-Lipi Soft be activated before this. In this way
various characters in a script are mapped to the keys of the
Keyboard. A set of mappings forms a Keyboard layout that is
stored in the form a file. For example MODULAR.DEV contains
the layout information of MODULAR Keyboard layout for
Devnagari script.


Application Types
Shree-Lipi Soft supports calls for identifying the type of the
application. This is required because different applications
behave differently when typing is done in Indian script. i.e. in
Indian languages. This is particularly significant of RichEdit
Controls. Application type basically describes the type of the
application whether it is a RichEdit Control or not.


Shree-Lipi Soft Data Exchange Structure
Shree-Lipi Soft uses a general data exchange structure for
communicating with the application. The application can use
this record structure for retrieving information back from ShreeLipi Soft for taking desired actions. The format of the data
exchange structure is as follows.
Variable Name
SHREE_ERROR

SHREE_ACTIVE

CUR_SCR

FONT_NAME

FONT_SIZE

FONT_ATTR

Data Types Description
Character/ Error code returned by
Byte
Shree-Lipi Soft to indicate
any error in the call
Character/ Non-zero value indicates
Byte
that Shree-Lipi Soft is active
and vice versa
Character/ This indicates the current
Byte
active script. The values are
to be interpreted as provided
in the Overview section.
[Array
ofName of the default font
Byte/Char] orassociated with the current
string of sizescript
32.
Double
Point size of the default font
Word/Long associated with the current
Integer
script
Character/ The attributes of the default
Byte
font associated with the
current script Values are 0
for Normal, 1 for Bold, 2 for
Italic, 3 for Bold Italic


FONT_LAYOUT

Character/
Byte
ACTIVATION_KEY Character/
Byte

Font layout of the current
script.
The Activation key for
switching to Indian script.
The values are
145 : SCROLL LOCK
20 : CAPSLOCK

144 : NUMLOCK
HYPHENATION_ON Character/Byt Currently this facility is not
e
supported.
KEYBOARDNAME [Array
ofFilename of the current
Byte/Char] orkeyboard layout for the
String of sizecurrent script.
12.


Facilities provided in Shree-Lipi Soft
Indian language scripting
For providing Indian language support, one of the most
essential features desired is Indian language scripting. i.e One
should be able to type in any of the regional languages. Until
and unless you have data or information in Indian Language
you will not be able to use the other facilities of Shree-Lipi Soft.
Shree-Lipi Soft provides Indian language scripting facility
directly once you have initialised Shree-Lipi Soft. After
initialising Shree-Lipi Soft, you only need to apply the font to any
editable control and you will be able to type in Indian language.
Additionally you may need to put on the activation key for
Shree-Lipi Soft.
Note: This scripting facility will be available only for those
scripts that you have purchased / installed.

Conversion from native layout to standard code
Shree-Lipi Soft has its native Font codes viz. Shree and
Suchika. Since the font codes are native, they do not support
lexicographical sorting in their native format. Sorting of data is
another key feature for applications with Indian language
support. For this Shree-Lipi Soft provides function calls using
which you can convert the data in font codes to standard
formats such as ISCII, EAISCII, PC-ISCII. All these formats
follow the lexicographical order of the specific language. These
conversion calls are available for all the ten scripts supported by
Shree-Lipi Soft. You can use these calls to obtain data in sorted
order.


Transliteration facility
This is another key feature desired in Indian language
applications. In many data processing applications, the names
are typed either in English or in Indian language. It would be
helpful if the data keyed in one language can be transliterated to
the other language especially from English to Indian language.
Shree-Lipi Soft provides this facility of transliterating from
English to Indian language and vice versa. The transliteration
technique used is dictionary-based transliteration. For each
script supported by Shree-Lipi Soft, you will find a main
dictionary in the Shree-Lipi directory. Additionally for some
scripts, you get an official language dictionary also. If the word
is found in the available dictionaries then you will get exact
transliteration, else Shree-Lipi Soft resorts to phonetic
transliteration. In the latter case the transliteration may not be
fully correct but it still aids the user, as he/she has only to make
the necessary corrections. Shree-Lipi Soft also provides the
facility of creating your own dictionary.

Fast Printing using Dot matrix printing
Printing of reports is the final goal of any application. Although
the data can be maintained in a computer, it is always desirable
to have a hardcopy of the entered information. If the application
is data intensive then the amount of resource consumed in
printing may be considerably high. Moreover the speed of the
printing will also be a major factor of consideration. Indian
language fonts are in graphical mode and hence the speed of
draft printing using Dot Matrix Printers cannot be achieved
directly. Shree-Lipi Soft again provides solution to this
discrepancy by providing fast printing calls. You can use this
calls to print to a Dot Matrix Printer attached to the printer port
of your machine. Though the speed of printing is not as high as
draft mode printing of English data, it is certainly higher than the
windows
graphics
printing.


## Chapter 4: General Shree-Lipi Soft Calls
In this chapter we will explore the general facilities provided by
Shree-Lipi Soft in the form of exported calls. Detailed
explanation of certain terms has been given wherever
necessary. The format of the calls used for explanation is a
general format and is not specific for any application. All these
calls are implemented in the "SLSDLL.DLL"
Application
specific calls are provided in the later chapters.
The most significant call is the call to the function
SLS_START2 Until and unless this call is made Shree-Lipi Soft
will not be enabled and the user may not be able to type in
Indian language. The format of the call is as follows
SLS_START2 (No parameters)
This function has a return value. The return value can be
Zero: Shree-Lipi Soft activated successfully.
Non-Zero: Unable to activate Shree-Lipi Soft. In this case the
error code is returned. The application developer can take
proper action according to the return value.
SLS_CLOSE (No parameters)


Use this function to terminate Shree-Lipi Soft API gracefully.
When this function is called, all necessary cleanup tasks are
automatically handled by Shree-Lipi Soft such as the freeing of
the Libraries and support modules. Once this function is called,
the user will no longer be able to use any of the multilingual
facilities including Conversion and Transliteration. For doing so
SLS_START2 has to be called again.
This function has been implemented as a subroutine and does
not have a return value.
Note: It is recommended that SLS_START2 be called during the
start of the application and SLS_CLOSE be called during the
termination of the application.
SLS_SETUP (No parameters)
Use this call to invoke a form that enables the user to change
the settings as well as specify the default settings, which will be
used throughout the application. Default settings are required
for all the Indian scripts. As an example suppose Shree-Lipi Soft
supports two scripts English and Devnagari. A default font is
required to be specified for both the scripts. Suppose for English
the default font is set as Arial normal with 10 points size and for
Devnagari it is SHREE_DEV_0708 (Modular Shree font) of size
14. Then whenever we change the script by activating or
deactivating the SCROLL-LOCK, the font would be changed
accordingly. This default font is used throughout the application
until the user explicitly changes it.
Note: This call is required only when the user is to be given
control of the settings. All settings of Shree-Lipi Soft can be


controlled programmatically using proper function calls if it is not
necessary to extend control to the end user.
A detailed description of all the features is as follows.
As is visible in the form, the user interface consists of a tabbed
page sheet.

Page-1
The General page is for specifying the general settings. This
comprises of setting the activation key. As mentioned earlier,
activation key refers to the key on the keyboard that will enable


typing in Indian Languages. Users can choose from one of the
available three options. They are as follows.
Scroll-Lock: Sets Scroll-lock key as the activation key.
Caps-Lock: Sets the Caps-Lock key as the activation key
Num-Lock: Sets the Num-lock key as the activation key.
Note: It is not possible to select more than one key as the
activation key. Selecting one key automatically disables the
previous activation key.


Page-2
Current Script
The script page consists of settings related to the scripts that
are installed as part of Shree-Lipi Soft. A drop down combo box
at the top left corner lists all the available scripts. To have a
view of all the installed scripts simply click the arrow at the end
of the box. To specify the settings for a script select the script in
the combo box.
Default Font


If fonts are installed for the selected script then the font name
control will list all the installed fonts. If no fonts are installed then
a warning would appear on the screen and the Sample Box
would show meaningless characters. To set a font as the
default font for this script, simply click on the font name in the
font list box. If the name of the font is not visible then use the
scroll bar at the right to scroll to the desired name. Additionally
the user can specify size and Style for the selected font. As the
various changes are made the Sample box shows the sample
output of the selected combination.
Keyboard Layout
At the top right corner, below script name list is the Keyboard
Layout Selection box. User can set the desired keyboard layout
by selecting it from the list of available layouts. To view the list
of available keyboard layouts available for the selected script,
simply click the drop down arrow of the Combo box. User can
change the layout to any desired layout. The keys in the
keyboard would be mapped according to the selected layout.
Font Layout
At the bottom right corner is the Font layout selection Combo
box. As mentioned earlier, a number of font layouts are
supported for all Indian scripts. If the font layout is that for a
non-Modular font, it is necessary that the user has the font for
that layout is installed on the user's machine. Modular does not
supply fonts of other font vendors' font layouts. It is necessary
to set the default font any of the font layouts, if they are
available and you want to use it. To preserve the settings made
for a font layout simply click the Apply button. Select the other
layout available and do as above for specifying the default font.


Page-3
The Keyboard tutor page consists for settings for Keyboard
tutor. If the "Show Key contents on tool tip" option is selected,
then enlarged view of the various typing combinations will be
visible in the form of Tool tips when the mouse is moved over
the keys. This option is selected by default.
Position on Screen
Using this option the user can set the position for the keyboard
tutor on the screen. Selecting the top-left option (the default
option) makes the tutor appear at the top-left corner of the


screen, whenever the tutor is activated. Other options apply in
the same way.
After all the settings have been made the user can click the OK
button to save all the changes made to the Shree-Lipi Soft
settings. Alternatively the user can keep the previous settings
by clicking the Cancel Button. Clicking the OK or the Cancel
button closes the dialog.
Help
The user can obtain online help on Shree-Lipi Soft setup by
clicking the Help button.
This function returns an integer value. The Result is 0 if user
pressed cancel button on the setup form, and 1 if user presses
OK button.
SLS_KBD_SETUP (No parameters)
Use this call to invoke a concise Shree-Lipi Soft setup dialog
box. This dialog box consists of information relating to Keyboard
setup only. The developer should use this call in the project, if
the facility of setting the keyboard is to be extended to the user.
This function has been implemented as a subroutine and need
never be called if all the settings are hard coded in the
application itself and the user has no control to change the
settings.


The dialog has been implemented as a page control as
explained below.

Page-1
The first page is the General Page. This page shows a radio
group using which the user can set the Activation key. The
options available are Scroll-Lock, Caps-Lock and Num-Lock.
The default is Scroll-Lock. Users can at a time have only one
key as the activation key. Selecting a different option disables
the previous activation key. For a detailed description about
activation key, see the SLS_SETUP function.


Page - 2
The Script Page consists of the keyboard settings related to the
script. The current script can be selected from a list of available
scripts from the drop down combo box. Only the set of installed
scripts will be visible in the list. After selecting a script the user
can select a keyboard layout from the second dropdown combo
box. The default value is set to MODULAR. After selecting a
script and a keyboard layout, the user can make the changes
permanent by pressing the Apply button. Please note that,
selecting the script from the combo box, does not change the
default script. The control is given only to select the script for
specifying the keyboard layout.


Page - 3
The keyboard tutor page is the same as in the Shree-Lipi Soft
general setup. Selecting the "Show Key contents on tool tip"
shows the various key combinations in the form of tool tip when
the mouse is moved over the tutor. The position of the
Keyboard tutor can be set using the Position on Screen options.
For a detailed description of Keyboard Tutor setup, refer to the
SLS_SETUP function.
Save/Cancel the settings: The user can save all the changes
by pressing the OK button. Alternatively the user can choose
the Cancel button to cancel any changes made to the previous
settings.
Help: Online help for Shree-Lipi Soft keyboard tutor can be
obtained by pressing the Help button.


SLS_SET_SCRIPT (Script Code)
Use this function to change the script programmatically. This
function takes one parameter. The parameter is the Script
Code. This parameter is of type LongInt / DWORD. The values
for Script code are as mentioned in the overview section. When
the function is executed the current script changes automatically
to the value as specified in the Script code. Also the previous
value of the script is disabled. As an example suppose that
Shree-Lipi Soft supports two scripts English and Devnagari.
Suppose the current script is English. On calling this function as
below
SLS_SET_SCRIPT(1)
will lead to the following changes.
1. Typing in Devnagari will be enabled automatically and the
user can no longer type in English.
2. The Activation key will turn on automatically. The default font
for the script will be used for typing if no font specific font is set.
3. The fields of Shree-Lipi Soft data exchange structure will
change to reflect the change in script.
Use: For example suppose a form consists of two Edit controls
for which two different fonts have been assigned. The first Edit
control is assigned an English font say 'Arial' and the second


Edit control has been assigned Devnagari font 'SHREE-DEV0708'. Assume that Shree-Lipi Soft has been made active by a
previous call to SLS_START2. When the first Edit control gets
focus this function can be called to set the current script to
English whence the user can type in English. When the second
Edit control receives focus the function can again be called to
set the active script to Devnagari. The user will not have to
change the script explicitly. This will increase the speed of the
Data Entry.
This function has a return value. If the function has been
executed successfully, then the return value is Zero. If an error
occurs then the error code is returned. For a detailed list of error
codes see the section Shree-Lipi Soft error codes
SLS_SET_FONTTYPE (Script Code, Font layout code)
Use this call to change the Font Layout for a script. As has been
mentioned earlier, Shree-Lipi Soft supports a number of font
layouts. The current font layout for a script can be changed
using the above call.
The first parameter is the script code for which the font layout is
to be changed. For a list of possible values for this parameter
see the overview section. The second parameter is the Font
Layout Type code. For the possible values, see the overview
section.
This call is valid only for scripts that have been installed along
with Shree-Lipi Soft. If a script has not been installed then on
calling this function error will be indicated in the form of Error
Code. The function returns zero if successful.


SLS_GET_FONTTYPE (Script Code)
Use this call to find the Font Layout for a script. As has been
mentioned earlier, Shree-Lipi Soft supports a number of font
layouts. The current font layout for a script can be obtained by
using the above call.
The parameter is the script code for which the font layout is to
be obtained. For a list of possible values for this parameter see
the overview section. The return value specifies the font layout
for the script passed in the form of Script Code. For the possible
values. see the overview section.
This call is valid only for scripts that have been installed along
with Shree-Lipi Soft. If a script has not been installed then on
calling this function, a value of -1 will be returned.
SLS_SET_KEYBOARD (Script code, Name of the file
associated with the desired Keyboard Layout)
Use this function for changing the keyboard layout of an
installed script. If the function is executed successfully the
keyboard layout is changed to the value passed as the second
parameter.
The first parameter is the Script code. For a list of possible
values see the overview section. The second parameter is a
pointer to a string that holds the value of the file name for the
desired keyboard layout. As an illustration the following call sets
the keyboard for Devnagari script to 'ENG'.


SLS_SET_KEYBOARD (1, 'ENG.DEV').
All the files associated with the various keyboard layouts for a
script are present in the directory in which Shree-Lipi Soft has
been installed.
This function is to be called only for scripts installed along with
Shree-Lipi Soft. Otherwise the function fails and an error code is
returned.
The possible return values for this function is:
Zero: The function has been executed successfully and the
keyboard layout for the specified script has been changed.
Non-zero: The function has failed. The return value is equal to
the error code.
SLS_GET_KEYBOARD_NAME (Script code, Pointer to a
string to hold the name of the file associated with the
current Keyboard Layout)
Use this function for knowing the current keyboard layout of an
installed script.
The first parameter is the Script code. For a list of possible
values see the overview section. The second parameter is a
pointer to a string. On return, this will hold the value of the file
name for the current keyboard layout. The caller must allocate
enough memory to this pointer before calling this function.


This function is to be called only for scripts installed along with
Shree-Lipi Soft. Otherwise the function fails.
SLS_GET_KEYBOARDS_LIST (Script Code, Pointer to a
string or Buffer, Size of the Buffer or string)
Use this function for finding out the list of keyboard layouts
available for a specified script.
The first parameter is the script code for which the list of
Keyboard layouts is to be retrieved. For a list of possible values
for the Script code see the overview section. The second
parameter is a pointer to the string or buffer in which the names
of keyboards will be retrieved. The names of the keyboards are
separated by comma. The third parameter, which is to be
passed by reference, indicates the size of the buffer or the
string.
If the function is called with the second parameter set to Null,
the size of the string is returned in the third parameter. The user
can then allocate memory of this size to the buffer and then call
the function again to retrieve the list of Keyboard names
available.
The caller must pass the size of buffer or string in the third
parameter. If the size of the string/buffer is less than the
required size, the string will be truncated and on return the third
parameter will hold the size of the truncated string.
Note: If the development platform does not support Pointers,
then the second and the third parameters can be passed as
reference parameters. The List will consist of the keyboard


names separated by comma. It is up to the developer to parse
the string.
This function has a return value. If the function is executed
successfully then the return code is Zero. If an error occurs in
executing the function then appropriate error code is returned.

SLS_SET_APPLICATION_TYPE ( Application Type)
Use this function call to set the application type. As has been
mentioned earlier this call is required because different
applications behave differently while typing in Indian languages.
The parameter indicates the application type. The permissible
values are 0 and 1. The default setting is 0 because this applies
to most of the edit controls. If Rich Edit control is being used in
the application for that control, the application type has to be set
to 1.
To check which application type is applicable to your
application, activate Shree-Lipi Soft and try to type conjuncts or
characters with Matra Modifiers in Indian language. If the edit
control shows excess characters, try with the other application
type.
Consider the following Demo Application. The keyboard layout
has been set to 'ENG' and the current Indian script is
Devnagari. The current application type is set to 0. We presume
that we want to type 'Aa' in Devnagari. This can be done by


pressing the 'a' key in the keyboard twice. The results of doing
so for a Simple Edit and Rich Edit are as shown in the screen.
In the simple Edit the character appears properly whereas in the
Rich Edit control two characters are getting typed.

Now let us set the Application Type to 1 and try the same
operation. The result is as shown below.

This time the output is opposite of the earlier one. The Simple
Edit now contains two characters, whereas the Rich Edit Control
contains a single 'Aa' character. For proper working, the
Application types for the two controls should be set separately.


Note: In the above Application type 1 corresponds to setting
Application type value to 0 and Application type 2 corresponds
to setting Application type value to 1.
Return value: The function returns 0 if the function has been
executed properly whence the application type is identified
properly. If an error occurs then the function fails and the
appropriate error code is returned.
SLS_GET_STATUS (Pointer
Exchange structure)

to

Shree-Lipi

Soft

Data

Use this function to retrieve the current value of the various
fields of the Shree-Lipi Soft Data Exchange structure.
The parameter is a pointer or reference to the Data Exchange
structure. For a detailed format of the Data Exchange Structure
see the section Shree-Lipi Soft Data Exchange Structure.
Sufficient memory must be allocated to this parameter before
the call is made. On return the record structure contains the
values of the current settings of Shree-Lipi Soft.
Return value: If the function succeeds then the return value is
Zero. If an error occurs, then appropriate error is returned in the
form of Error code. For a list of error codes see the section
Shree-Lipi Soft Error codes.
SLS_GET_INSTALLED_SCRIPTS (Script List, Script List
size)


Use this function to retrieve the list of installed scripts in the
computer. It is not necessary that all the scripts be installed in
the computer. The list of available scripts is returned in the
Script list parameter. The individual script codes are separated
by comma. It is up to the user to parse the script list for
separating individual scripts.
The first parameter is a pointer or reference to the string/buffer.
On return this parameter will hold the list of all installed scripts.
Sufficient memory must be allocated to the Script list parameter
before a call to this function is made. The second parameter
must specify the size of the memory allocated to the Script list
parameter.
If the function is called with the Script list set to null then the
required size for the string/buffer is returned in the Script list
size. The user can allocate this much memory to the script list
parameter and call the function again to retrieve the list of
scripts installed.
If sufficient memory is not allocated for the script list then the list
is truncated.
Return value: If the function succeeds then the return value is
zero. If an error occurs then the appropriate error code is
returned. For a list of error codes see the section Shree-Lipi
Soft Error codes.
SLS_GET_DEFAULTFONT_FOR_SCRIPT (Script code, Font
Layout Code, Default Font name)


Use this function to find out the default font associated with a
particular script and font layout. For every script and font layout,
one font is set as the default font which is not necessarily the
first font for the script and layout.
The first parameter is the code of the script for which default
font is to be retrieved. For a list of script codes see the overview
section. The second parameter is the font layout code for which
the default font has to be retrieved. For possible values of the
font layout code, see the overview section. The third parameter
is a pointer or reference to the default font name string.
Sufficient memory must be allocated to the string before a call is
made.
Return value: If the function succeeds, the return value is zero.
If an error occurs then the appropriate error code is returned.
For a list of error codes see the section Shree-Lipi Soft Error
codes.
SLS_SET_DEFAULTFONT (Script code, Font Layout Code,
Default Font name, Font Size, Font Style)
Use this function to set the default font associated with a
particular script and font layout. For every script and font layout,
one font is set as the default font which is not necessarily the
first font for the script and layout.
The first parameter is the code of the script for which default
font is to be set. For a list of script codes see the overview
section. The second parameter is the font layout code for which
the default font has to be set. For possible values of the font
layout code, see the overview section. The third parameter is


name of the default font. The third parameter is the point size of
the default font, and the fourth parameter indicates the style of
the font. The possible values are as follows:
0: Normal
1: Bold
2: Italic
3: Bold Italic
Return value: If the function succeeds, the return value is zero.
If an error occurs then the appropriate error code is returned.
For a list of error codes see the section Shree-Lipi Soft Error
codes.

SLS_GET_CURRENTSCRIPT(no parameters)
Use this function to obtain the current Active script for ShreeLipi Soft. This function is particularly useful if you want to have
multiple languages enabled in your application, for Example an
Editor. If the user toggles the Activation key then, Shree-Lipi
Soft toggles between English and this script.
Return Value : The return value is the current script. For
possible values, see the overview section.


SLS_SET_ESCAPEMENT (CONTROL KEY, SHIFT KEY,
KEYCODE )
The characters in English script can be typed by using the
keyboard in normal and shift mode. However, while typing
Indian languages, it is not possible to accommodate all the keys
in these two modes. To extend the keyboard to a third layer, an
escapement key is used. The user has to press the escapement
key and then another key to get the desired key typed. The
default escapement key in Shree-Lipi Soft is Ctrl+Space.
This function sets the escapement key parameters. 1st
parameter specifies whether control key forms the escapement
combination. Possible values are
0 : no
1 : yes
2nd parameter specifies whether shift key forms the
escapement combination. Possible values are
0 : yes
1 : no
3rd parameter specifies the virtual key code of the key. This
cannot be 0.
e.g.
1. if you want to set escapement key as ctrl + shift + 1
then the function should be called in following way
SLS_SET_ESCAPEMENT(1,1,49);
2. if you want to set escapement key as ctrl + 1
then the function should be called in following way
SLS_SET_ESCAPEMENT (1,0,49);
3. if you want to set escapement key as F1
then the function should be called in following way
SLS_SET_ESCAPEMENT (0,0,VK_F1);
This function returns zero on success, and on failure, a negative
value which signifies that an improper key combination has
been given.
SLS_SET_ACTIVATION_KEY (Activation Key value)


Use this function to set the activation key. Once set, the user
can switch from English language to Indian language by turning
on the activation key.
The parameter is the Windows virtual key code for the activation
key. They can be one of the following
VK_Scroll :

scroll lock key :


VK_Num

:

num lock key

:


VK_Capital:

caps lock key

:


This function has been implemented as a subroutine and does
not have a return value.
SLS_GET_ACTIVATION_KEY (no parameters)
Use this function to obtain the current value of the activation
key.
Returns the windows standard virtual key code for the
activation keys. The activation key
can be one of the following
VK_Scroll : the scroll lock key
VK_Num : the num lock key


VK_Capital : the caps lock key

SLS_ENABLE_IN_DIALOGS (boolean value specifying
whether to Enable or not )
When running applications, we use some controls like file
specification dialogs to specify the file names. These file names
have to be given in English, and user does not want to enable
Indian language typing in these controls. That is why, Shree-Lipi
Soft normally disables Indian language typing in certain type of
controls. However, if your application uses these components
and you require Indian language typing in these, you can use
this function.
The parameter is a boolean value, which is interpreted as
shown below
0 : not allow typing in certain Edit controls
1 : allow typing in those Edit controls
The function returns zero on success and -1 on failure.
Tutor Related Calls:
Shree-Lipi Soft comes along with a utility for typing in Indian
Languages using the keyboard. While working in any
application, the tutor can be activated to find out how the
various keys in the Keyboard have been mapped to the
characters of the language. For a detailed description of the
Keyboard tutor see the section Keyboard Tutor.
The keyboard tutor can be activated using one of the following
two calls.


SLS_TUTOR_ON (Handle of the active window of the
application)
The parameter is the window handle of the active window of the
project. All window-based applications have a unique window
handle associated with them. When this function is called a
Keyboard tutor dialog appears on the screen at the position set
in the Shree-Lipi Soft Keyboard Setup or Shree-Lipi Soft
General Setup. If any of the keys in the tutor window is pressed
using a mouse the character automatically gets typed on the
active window's active Edit control. The parameter is used by
the function for pasting the selected character in the active Edit
control.
SLS_TUTOR_ON1 (Window Title of the active window of the
application)
The parameter in this call is the Title of the active window of the
application. This is an alternative function for invoking the
Shree-Lipi Soft Keyboard tutor on the screen. The format of the
Keyboard Tutor is as shown below.

Shree-Lipi Soft Keyboard Tutor


This call can be used if the Window handle cannot be found
from the application. As above when any of the keys in the tutor
window is pressed using mouse the character automatically
gets typed on the active window's active Edit control. The
parameter is used for identifying the active window.
Note: Two different calls for activating Tutor have been
provided. In some platforms, it is not possible to specify the
handle of the Active Form/window. In such cases
SLS_TUTOR_ON1 can be used passing the TITLE of the
Window/Form as parameter.
SLS_TUTOR_OFF (No Parameters)
This call is to be used if the Keyboard tutor is to be closed.
Calling this function closes the Tutor window and it will be no
longer visible on the screen.
All the above tutor related calls have been implemented as
Subroutines and do not have any return value.
SLS_SET_TUTOR_POSITION (Tutor position)
The position of the keyboard tutor can be changed by dragging
with mouse. However, you may like to control the position
through your program. This function allows you to set the
position of keyboard tutor on the Screen. The parameter
specifies the tutor position. The Tutor position values are
interpreted as shown below
0:
Top Left
1:
Top Right
2:
Bottom Left
3:
Bottom Right


4:

Screen Center

The function returns zero on success, and -1 on failure.

SLS_ENABLE_TUTOR_TOOLTIP (boolean value specifying
whether to show the tooltips or not )
When the user takes the mouse cursor on any of the tutor
buttons, Shree-Lipi Soft shows a little bigger window there
showing the enlarged view of the characters that can be typed
using that key. This call can be used to enable / disable this tool
tip window. The parameter is interpreted as below:
0 : tool tip not to be shown

1: Tool tip to be shown.

The function returns zero if successful, and a negative value if
not successful.

General Utility Calls:

SLS_FONTNAME_TO_SCRIPT_TYPE (Font name, Script
code, Font Layout Code)
Use this function to find out the script associated with the font. It
is customary to use series of fonts for a specified language. For
example if the font name is ("Shree708"/”Shree-Dev-0708”)
then it depicts Shree Font. Also since it is in the range 700 to


750 it is a Devnagari font. Similarly there are different series for
other languages.
The first parameter to be passed to this function is the name of
the font. It can be passed as a pointer or as a reference string.
This function returns the script code for the script and the font
layout type code for the font layout associated with the font. The
various script codes and font layout codes are given in the
overview section. The caller has to pass these two parameters
by reference, and Shree-Lipi Soft will return the proper values.
SLS_FIRSTFONT_FOR_SCRIPT_TYPE (Script Code, Font
Layout Code, First Font)
Use this function to find out the first installed font for a given
script and for a given font layout. This may be necessary
because not all the fonts may be installed on the system for a
particular script.
Use: The font name can be used to assign default font to the
components for a given script at run time.
This function takes three parameters. The first parameter is the
code for the script for which the First Font is to be found. For a
list of available scripts and their codes see the overview section.
The second parameter is the font layout type for which the first
font needs to be found. See the overview section for the
possible values. The third parameter is a pointer to the name of
the font or a reference to the name of the font. The caller must
allocate sufficient memory for this parameter before calling the
function.


This function has been implemented as a subroutine and does
not have a return value.
SLS_SCRIPT_TO_STR (Script Code, Script String)
Use this function to get the full name of the script in the form of
a string. This function is useful if the current script is to be
displayed in any of the user interface. For example, the full
name for script value of 1 is "Devnagari"
This function takes two parameters. The first parameter is the
code of the script for which full name is to be found. For a list of
available scripts and their codes see the overview section. The
second parameter is the pointer or reference to the name of the
script. Sufficient memory must be allocated to this string before
this call is made.
This function has been implemented as a subroutine and does
not have a return value.
SLS_STR_TO_SCRIPT (Script Name)
Use this function to find out the code for the full script name
passed as the parameter.
This function takes only one parameter, which is the name of
the script for which code is to be found. This is to be passed in
the form a pointer or a reference string.
Example: SLS_STR_TO_SCRIPT ("Devnagari")


Return value: The return value is the code for the script name.
For a list of available scripts and their codes see the overview
section.
SLS_SCRIPT_TO_SHORTSTR (Script Code, Script String)
Use this function to get the short name of a given script. Short
names for scripts have been provided as an alternative to the
full names. For example the short name for "Devnagari", whose
script code is 1, is "DEV"
This function takes two parameters. The first parameter is the
code of script for which short name is to be found. For a list of
permissible values for script code see the overview section. The
second parameter is a pointer to a string or a reference string.
On return this string will hold the short name for the script.
Sufficient memory must be allocated to this string parameter
before a call is made. The size of the string on return will
necessarily be 3.
This function has been implemented as a subroutine and does
not have a return value.
SLS_SHORTSTR_TO_SCRIPT (Short name for script)
Use this function to get the code associated with the script
passed as a short name.
This function takes only one parameter, which is the short name
for the script whose code is to be found. For example the


following call retrieves the script code for "Devnagari" script.
The size of the input string should be 3.
SLS_SHORTSTR_TO_SCRIPT ("DEV");
Return value: The return value is the code for the script name
passed as parameter. For a list of values see the overview
section.
SLS_GET_FONTNAMES_FOR_LAYOUT (Script code, Font
Layout Code, Font list, Size of Font list)
Use this function to retrieve the list of available fonts for a
specified script and font layout. It is not necessary that all fonts
for a script are active as they can be controlled using the Fonts
option in the control panel. On return the Font list parameter
holds the list of all available fonts for the script and font layout
whose codes are passed as parameters. For a list of Script and
layout codes see the overview section. The individual font
names are separated by comma. It is up to the user to parse the
string and obtain individual font names.
The first parameter is the code of Script for which the list of
available fonts is to be retrieved. The second parameter is the
code of the font layout for which the list of the fonts is to be
retrieved. The third parameter is a pointer or reference to a
string / buffer. The fourth parameter must specify the size of the
string / buffer.
If the function is called with a null value for the third parameter
(Font list), then the required size of the string is returned in the
fourth parameter. The user can then allocate sufficient memory


to the font list parameter and call the function again to retrieve
the list of available fonts.
If sufficient memory is not allocated then the font list is
truncated.
Return value: If the function executes successfully, then the
return value is Zero. If an error occurs, the appropriate error
code is returned. For a
list of error codes see the Shree-Lipi Soft Error Codes section.
SLS_FONTLAYOUT_TO_STR (Font Layout Code, Font
Layout String)
Use this function to get the full name of the Font Layout in the
form of a string. This function is useful if the current font layout
is to be displayed in any of the user interface. For example, the
full name for font layout value of 15 is "Shree-Lipi 4.0/5.0"
This function takes two parameters. The first parameter is the
code of the font layout for which full name is to be found. For a
list of available font layouts and their codes see the overview
section. The second parameter is the pointer or reference to the
name of the font layout. Sufficient memory must be allocated to
this string before this call is made.
This function has been implemented as a subroutine and does
not have a return value.


SLS_FONT_LAYOUTSTR_TO_LAYOUT (Font Layout Name,
Script code)
Use this function to find out the code for the full font layout
name passed as the parameter.
This function takes two parameters, first is the name of the font
layout for which code is to be found. This is to be passed in the
form a pointer or a reference string. The second parameter is
the script code to which the font layout belongs. For a list of
possible scripts and their codes, see the overview section.
Example: SLS_FONT_LAYOUTSTR_TO_LAYOUT ("ShreeLipi 4.0/5.0" , 1)
Return value: The return value is the code for the font layout
name. For a list of available layouts and their codes see the
overview section.
SLS_GET_FONTLAYOUTS_LIST (Script code, Size of Font
Layout list, Font Layout list)
Use this function to retrieve the list of available font layouts for a
specified script. On return the Font list parameter holds the list
of all available font layouts for the script whose code is passed
as parameter. For a list of Script codes see the overview
section. The individual font layout names are separated by
comma. It is up to the user to parse the string and obtain
individual font layout names.


The first parameter is the code of Script for which the list of
available font layouts is to be retrieved. The second parameter
must specify the size of the buffer. The third parameter is a
pointer or reference to a string / buffer.
If the function is called with a null value for the third parameter
(Font layout list), then the required size of the string is returned
in the second parameter. The user can then allocate sufficient
memory to the font layout list parameter and call the function
again to retrieve the list of available fonts layouts.
If sufficient memory is not allocated then the font layout list is
truncated.
Return value: If the function executes successfully, then the
return value is Zero. If an error occurs, the appropriate error
code is returned. For a list of error codes see the Shree-Lipi
Soft Error Codes section.

Registry Setting Calls:
SLS_SET_REGISTRY_ROOT_KEY (const PCREG, const
HROOT)
Routine to set the name of the registry key under which
application specific settings will be stored.
If a single machine contains multiple applications using the
Shree-Lipi Soft API, then it is possible to retain the Shree-Lipi


Soft settings for each of the applications. Each application must
call this function to specify the location for the registry key. All
the Shree-Lipi Soft API related settings information will be
stored under that particular registry key.
In this way you can retain the settings for that application.
Parameters
PCREG : Pointer to the name of the registry key
HROOT : Predefined reserved values which can be one of the
following :
Type of HROOT

Hex Values

HKEY_CLASSES_ROOT

(( HKEY ) 0x80000000 )

HKEY_CURRENT_USER

(( HKEY ) 0x80000001 )

HKEY_LOCAL_MACHINE

(( HKEY ) 0x80000002 )

HKEY_USERS

(( HKEY ) 0x80000003 )

The user can either specify the Type of HROOT or he can use
its
corresponding
hex
values.
i.e.
either
use
HEY_LOCAL_MACHINE or use 0x80000002.


Returns Values : Returns 0 if successful, non zero if any error
occurred

For e.g. if you want to store settings under the key
'HKEY_LOCAL_MACHINE\SOFTWARE\XYZ\ABC' then
call SET_REGISTRY_ROOT_KEY(, 'SOFTWARE\XYZ\ABC', ,
HKEY_LOCAL_MACHINE);

SLS_RESTORE_REGISTRY
Routine to RESTORE the default application specific registry
settings.
Suppose you have made changes in the registry settings and
you want to revert back to Modular default Modular’s registry
settings then use this function.
Returns 0 if successful, non zero if any error occurred.


## Chapter 5: Conversion Calls
Conversion: In the world of multilingual software, It is very
essential to convert data in one format to another format. Hence
in this context Conversion primarily refers to the conversion of
format of text in one language to another format for the same
language. Before we peep into the Conversion calls let us have
a brief idea about the various standard formats and its
terminology.
SL-Format: SL-Format or Shree format, a characteristic format
of Modular Infotech, refers to the format in which the keys in the
keyboard are mapped to characters in the background. This
format was available along with earlier Shree-Lipi / ShreeSamhita versions and is no longer available. For Example in
ASCII, the 'A' key of the keyboard is mapped to the ASCII 'A', a
character from the English alphabet. The character stored
internally is 'A'. In the case of Indian languages, this does not
apply. The key 'A' in keyboard may be mapped to some specific
character of the Indian Language. Also the character will be
different from the ASCII 'A'. Thus SL-Format refers to this
mapping of the keys. SL-Format applies only to text typed using
Shree Fonts. In this format all the keys are mapped to Indian
language characters and none else. The format for the Font
Names as visible in Fonts folder of Control Panel is
SHREEXXX.
SL2000-Format: SL2000-Format or Shree2000 format, is the
improved version of SL-Format and is fully compatible with
Windows2000. The format for the font names as visible in Fonts
folder of the control panel is Shree-Dev-XXXX. If you are an old


Samhita user and if you want your application to be compatible
with Windows2000 then you must upgrade your existing data in
SL-Format to SL-2000 format. This you can do by using the
newer calls provided along with Shree-Lipi Soft.
Suchika - Format: Suchika Format is again provided by
Modular Infotech. This again refers to a format in which the keys
in the Keyboard are mapped to specific Indian language
character depending upon the script. The added specialty of this
format is that by deactivating Shree-Lipi (toggle off the ShreeLipi Activation Key), the user can type in English. When the
Activation key is off the mapping followed is default. Thus 'A' in
the keyboard will be interpreted internally as ASCII 'A'. If the
activation key is ON then the mapping is according to the
Suchika Format for the language. Thus Suchika format provides
bilingual support. Suchika format applies to text typed using
Suchika Fonts provided by Modular Infotech.
ISCII - Format: ISCII is an acronym and stands for Indian
Standard Code for Information Interchange. This is the standard
format for all Indian languages supported by DOE (Department
of Electronics). ISCII Code is compatible to the ISO 8-bit code.
The characteristic feature of this format is that the letters are in
the lexicographical order of the Indian language. For example
ASCII follows the English alphabet sequence. In the same way,
ISCII standard has been provided for every Indian language.
Since ISCII follows the lexicographical format, it can be used for
Sorting of Strings.
PC-ISCII Format: PC-ISCII is the version of ISCII code defined
for compatibility with IBM-PC. IBM-PC doesn't follow the ISO 8
bit code recommendation. It uses a line drawing character
located between hex B0 and hex DF. Since these line drawing


characters have to co-exist along with ASCII and Indian scripts,
the PC-ISCII code has been split into two half-character sets. In
functionality PC-ISCII gives identical result to ISCII code.
EA-ISCII Format: EA-ISCII or Extended ISCII is meant for
those computers or packages that do not allow use of 8-bit
code. Hence the Indian language characters have to be
mapped to the ASCII 7 bit. This means mapping of all Indian
language characters in the span of 52 characters occupied by
the upper and lower case characters of English alphabet. A
small 'x' character is used in the beginning of a word to mark it
as an Indian Script word. In functionality, EA-ISCII gives the
same result as ISCII code.
Sort32 Format: Sorting of strings is one of the main
requirements for database applications. Analysis has shown
that the ISCII ordering for sorting in Indian languages gets
distorted for some 32-bit development platforms such as
PowerBuilder 5.0. To cope with this problem Shree-Lipi Soft
supports a format for converting the string in font Format to a
suitable format so that the strings are in the dictionary order for
that language. This format is called SORT32.
Conversion Calls:
In this chapter we will explore the conversion facilities provided
by Shree-Lipi Soft in the form of exported calls. Detailed
explanation of certain terms has been given wherever
necessary. The format of the calls used for explanation is a
general format and is not specific for any application. All these
calls are implemented in the "SLSDLL.DLL" DLL. Application
specific calls are provided in the later chapters.


The most significant call for enabling conversion is the call to
function SLS_INIT_CONVERT. Unless this function is called no
conversion call should be used. This conversion call initializes
the environment necessary for the conversion calls. The format
of the call is as follows
SLS_INIT_CONVERT
This function does not take any parameter.
Return value: If the conversion has been initialized successfully
then the function returns zero. If there was an error during the
execution of the call, the function returns a Shree-Lipi Soft error
code appropriate to the error. For a detailed list of errors see the
section 'Shree-Lipi Soft Error Codes'
SLS_CONVERTDATA (Input string, Output String, Output
string size, Script Code, Input string font layout, Output
string font layout)
This is one generalized function provided to support all types of
conversions. Use this function to convert text in any supported
Format to any other supported format of the same script. This
function takes six parameters.
The first parameter is the pointer to the input string.
Alternatively this can be a string variable passed by reference.
On return the second parameter will be the corresponding
destination layout string for the input string. This parameter is a
pointer to a string or Buffer. The caller function must allocate
sufficient memory for the string / buffer. If pointers are not
supported, then a reference to a string can also be passed. If


the ISCII string does not fit in the space allocated for the output
string then the string is truncated. If this parameter is nul, then
the required size for the string is returned in the third parameter.
The caller then must allocate sufficient memory and call this
function again. The size allocated to the string must be passed
in the third parameter. The fourth parameter, Script Code is the
code for the script of the input string such as (1 for Devnagari).
For a detailed list of the various supported scripts and their
script codes see the 'Overview' section. The fifth parameter
specifies the font layout code of the Input String, and the sixth
parameter specifies the font layout code of the Output String.
The supported font layouts and their code values are explained
in the Overview section.
Return value: On return the function returns the pointer to the
output string.
Note: Usually ISCII-format takes more space than the SLFormat. Hence it is recommended to allocate more memory
than the size of the input string. To be on the safer side, it is
better to allocate 2-3 times the memory for the output string
though it is not mandatory.
Number to words conversion call
SLS_NUM_TO_WORDS (Number to be converted, Output
string, Size of Output String, Script Code, Font Layout
Code, Script Language, Splitting position)
Use this function to convert a number to string in Indian
language script in any of the supported font formats.


This function takes seven parameters.
The first parameter is the number that is to be converted. This
parameter is to be passed as a double type for enabling
conversion of huge numbers exceeding the range of Long
Integers. The second parameter is the pointer to the string /
buffer in which the converted string will be retrieved. If pointers
are not supported by the development platform, then a
reference to a string can be passed.
The caller function must allocate sufficient memory to this
parameter before calling the function.
The third parameter is the size of the output string. This
parameter should also be passed as reference (pointer to the
variable holding the size must be passed). If you call this
function with Nil as second parameter, the required size of the
output string is returned in this parameter. If sufficient memory
is not allocated, i.e. the value of this parameter is less than the
required size, the output string will be truncated.
The fourth parameter is the code for the script in which the
output string will be retrieved. For a list of permissible values
see the 'Overview' section. The fifth parameter is the font layout
code in which the string has to be retrieved. For a list of
permissible values see the 'Overview' section.
A script may support multiple languages. For example the script
'Devnagari' supports Hindi as well as Marathi. In such cases, it
is necessary to specify the language because the terminology of
thousands, lakhs etc. may vary from one language to another,
though the script is same. This occurs only for Devnagari Script.


The sixth parameter denotes the script language for Devnagari
the values are 0 for Marathi and 1 for Hindi. If multiple
languages are not supported for the script then this parameter
must be set to zero.
The seventh parameter denotes the splitting position for very
huge numbers. The permissible values are as follows.
0: This applies to numbers only within the range of 0 to
99,99,99,999. If the number exceeds this range and the Splitting
position is set to 0 then the output string does not retrieve the
converted value and returns Nil (NULL).
1: If the number is exceedingly large, then setting the Splitting
position to 1 makes the return string to be in Thousands.
2: If the number is exceedingly large, then setting the Splitting
position to 2 makes the return string to be in Lakhs.
3: If the number is exceedingly large, then setting the Splitting
position to 3 makes the return string to be in Crores.
Return value: If the function executes successfully, then the
function returns Zero. If an error occurs during the execution of
the function, then an appropriate error code is returned. For a
detailed list of Errors Codes and their description see the
section 'Shree-Samhita Error Codes'

Date-Time Call


In most of the applications, there is a need for maintaining dates
and time in various formats. Shree-Lipi Soft supports call for
converting Date and Time values to various formats in Indian
languages. The codes for the formats that have been supported
are as follows
Format
Number
00

Format

Example

dd/mm/yyyy
dd/mm/yyyy
hh:mm:ss a.m.

02/02/1998
02/02/1999 15:4:30 P.M.

hh:mm:ss a.m.
dd, Month, yyyy
Month dd, yyyy
dd-Mon-yy
Month, yy
Mon-yy
dd/mm/yy hh:mm
hh:mi
hh:mi:se
hh:mi a.m.
Day, Mon dd, yyyy

15:4:30 P.M.
2, February, 1999
February 2, 1999
2-Feb-99
February, 99
Feb-99
2/2/99 15:4
15:4
15:4:30
3:4 P.M.
Tuesday, Feb 2, 1999

SLS_DATETIME_TO_STR (Input Date-Time string, Output
String, Size of output string, Format number, Script Code,
Font Layout Code, Script language)
Use this function to convert a date-time string to a desired
format string in Indian language script and selected font format.
The function takes 7 Parameters in all.


The first parameter is a pointer to the Date-Time argument in
the form of string. The user must use platform specific function
to convert the Date-Time variable to a string and then pass this
string as argument to the function. This parameter is a pointer to
the Date-Time string. If pointers are not supported by a
platform, then reference to a string can also be passed.
On return, the second parameter contains the resultant string in
the desired format. This parameter is a pointer to a string /
buffer. Sufficient memory must be allocated by the caller
function before the function is called. A reference to a string can
be passed, if pointers are not supported.
If the function is called with this parameter set to NULL value
then the fourth parameter retrieves the Size of output string.
The user can then allocate the required memory space and call
the function again to retrieve the formatted string. This
parameter has to be passed by reference (pointer to the
variable holding the size must be passed). This parameter
indicates the size of the Output string / buffer. If the space
allocated is not sufficient for holding the output formatted string,
the output string is truncated.
The fifth parameter indicates the number for the format in which
the output will be retrieved. For a list of permissible values, refer
to the above table.
The sixth parameter refers to the code for the script in which the
output-formatted date-time will be retrieved (for example 1 for
Devnagari). For a list of permissible values see the 'Overview'
section. The seventh parameter indicates the font layout code in
which the output string needs to be retrieved. The last
parameter indicates the script language in which the string will


be retrieved. A script may support multiple languages. For
example the Devnagari script supports Marathi and Hindi
Languages. All other scripts support only one language and
hence the value of this parameter must be set to 0 for these
languages.
Return Value: This function has been implemented as a
subroutine and does not have a return value.

Custom Sort Calls
Sorting in Indian languages can be done using ISCII
conversion. However, ISCII sorting may not be acceptable to
some of the customers. One of the reasons can be given as an
example for Devnagari. In Devnagari, consonant "ksha" is
treated as a conjunct character of "ka" and " sha" in ISCII and
hence falls under "ka" while sorting. Whereas, many people like
to treat it as a separate consonant and want to have it towards
end in sorting. Same is the case with "dnya". Custom sorting
can be used to solve these problems. A custom sort order can
be specified for doing Indian language sorting.
SLS_INIT_CUSTSORT (Script Language)
Use this function to Initiate Custom Sorting.
This function takes 1 parameter.
The parameter is the Code of the Script.


Return value: If the function executes successfully, then the
function returns Zero. If an error occurs during the execution of
the function, then an appropriate error code is returned.
Detailed list of Errors Codes is as below
151 : if the script value in not between 1 to 9,18
152 : if the custom sorting entries cannot be written in registry
153 : if the custom sorting file does not exists
154 : if the custom sorting file cannot be opened.
SLS_SET_CUSTFILE (CUSTFileName)
Use this function to initialize the Custom Sort file. You need to
call this function before calling SLS_INIT_CUSTSORT Function.
This function takes 1 parameter.
The parameter is the Name 0f the Cust File.
Return value: If the function executes successfully, then the
function returns Zero. If an error occurs during the execution of
the function, then an appropriate error code is returned.
Detailed list of Error Codes is as below


155 : if the custom sorting entries cannot be written in registry or
if the custom sorting file does not exists
156 : if the script set before is not in range 1 to 9, 18
157 : if the name of the file cannot be written in the registry
SLS_SELECT_CUSTFILE (ScriptCode, CUSTFileName)
Use this function to initialize the Custom Sort file. This function
Pops up Dialog Box for User to select the Custfile. You need to
call this function before calling INIT_CUSTSORT Function.
This function takes 2 parameters.
The parameters are :
ScriptCode : ScriptCode of the Language.
CUSTFileName : Name 0f the Cust File.
Return value: If the function executes successfully, then the
function returns Zero. If an error occurs during the execution of
the function, then an appropriate error code is returned.
Detailed list of Errors Codes is as below
158 : if the script set before is not in range 1 to 9, 18


159 : if the custom sorting entries cannot be written in registry
160 : if the name of the selected file cannot be written in the
registry
SLS_CONVERT_TO_CUST (Input String, Output String,
Output string Size, Script code, Font Type code)
This is a function to convert string to custom format from a
string in any of the supported font layout codes.
The function takes 5 Parameters in all.
The first parameter is a pointer to the input string to be
converted. This parameter is a pointer to the string. If pointers
are not supported by a platform, then reference to a string can
also be passed.
On return, the second parameter contains the resultant string in
the custom sort format. This parameter is a pointer to a string /
buffer. Sufficient memory must be allocated by the caller
function before the function is called. A reference to a string can
be passed, if pointers are not supported.
If the function is called with this parameter set to NULL value
then the third parameter retrieves the Size of output string. The
user can then allocate the required memory space and call the
function again to retrieve the converted string. This parameter
has to be passed by reference (pointer to the variable holding
the size must be passed). This parameter indicates the size of


the Output string / buffer. If the space allocated is not sufficient
for holding the output string, the output string is truncated.
The fourth parameter refers to the code for the script in which
the output will be retrieved (for example 1 for Devnagari). For a
list of permissible values see the 'Overview' section. The fifth
parameter indicates the font layout code in which the input
string is specified.
Return Value: This function has been implemented as a
subroutine and does not have a return value.
SLS_CONVERT_FROM_CUST (Input String, Output String,
Output string Size, Script code, Font Type code)
This is a function to convert string in custom format to a
string in any of the supported font layout codes.
The function takes 5 Parameters in all.
The first parameter is a pointer to the input string to be
converted. This parameter is a pointer to the string. If pointers
are not supported by a platform, then reference to a string can
also be passed.
On return, the second parameter contains the resultant string in
the desired font format. This parameter is a pointer to a string /
buffer. Sufficient memory must be allocated by the caller
function before the function is called. A reference to a string can
be passed, if pointers are not supported.


If the function is called with this parameter set to NULL value
then the third parameter retrieves the Size of output string. The
user can then allocate the required memory space and call the
function again to retrieve the converted string. This parameter
has to be passed by reference (pointer to the variable holding
the size must be passed). This parameter indicates the size of
the Output string / buffer. If the space allocated is not sufficient
for holding the output string, the output string is truncated.
The fourth parameter refers to the code for the script in which
the output will be retrieved (for example 1 for Devnagari). For a
list of permissible values see the 'Overview' section. The fifth
parameter indicates the font layout code in which the output
string needs to be retrieved.
Return Value: This function has been implemented as a
subroutine and does not have a return value.

## Chapter 6: Transliteration Calls
Transliteration: 'Transliteration' refers to the conversion of text
in one language to text in another language. Transliteration is
different from translation. Translation means converting the text
from one language to another without affecting the essence of


the statement. In transliteration, the words are converted
phonetically rather than on the base of the meaning. Hence the
pronunciation of words remains the same whereas the
characters change. This facility can be of utmost importance in
the case of Proper nouns such as Name and Address of
persons that occur as fields in most of the database
applications. Transliteration can aid in converting these fields in
one language to another. As has been mentioned earlier,
sorting on the basis of strings is another potential requirement
of database applications. By coupling transliteration with
conversion, one can achieve the desired results for multilingual
databases.
Currently transliteration is supported from English to any Indian
language and vice versa. Transliteration from one Indian
language to another is not possible. If required, the same can
be achieved by transliterating text in one Indian language to
English and then transliterating it to another language.
In this chapter, we will focus the calls pertaining to
Transliteration as provided by Shree-Lipi Soft. All these calls are
exportable calls defined in the DLL 'SLSDLL.DLL'
The most significant call for transliteration is the call to initialize
transliteration. The format for this call is as follows
SLS_LOADTRANSLITERATION (No Parameters)
This call initializes the environment for transliteration. No other
call related to transliteration should be made before a call to this
function is effected.


Return value: If the function is successful then the return value
is zero. If an error occurs during the execution of the function
then, the appropriate error code is returned. For a detailed list of
error codes, see the section 'Shree-Lipi Soft Error Codes'
Another significant call related to transliteration is the call that
resets the environment for transliteration. The format for this call
is as follows.
SLS_UNLOADTRANSLITERATION (No parametrs)
This function has been implemented as subroutine and does not
return a value. Once this function is called, No function for
transliteration should be called.
It is recommended that this call to be placed in the project at the
close of the application along with a call to SLS_CLOSE, the
call for closing Shree-Lipi Soft. However the call to
SLS_UNLOADTRANSLITERATION must precede the call to
SLS_CLOSE.
Transliteration Main Functions
SLS_CONVERTLANGTOENG (Input string, Output string,
Size of the Output string, Script code, Font layout code)
Use this function to convert a string in one language to English.
When a call to this function is made a dialog box may appear
depending upon the setting. The format of the dialog box is as
shown below.


The First Edit box shows the language string, which is to be
transliterated. The second edit box shows the corresponding
English word. If the string is a phrase, then the drop down box
beside the label master word can be used to see the individual
word. The user can change the transliterated word according to
his wish by simply editing the Change to Edit box. The
suggestions list box shows the list of suggestions available for
transliteration. This happens when the same word has multiple
transliterations in the dictionary. The user can select his desired
option.
User has the option of adding the transliterated word/phrase to
the user dictionary by selecting the appropriate option along
side. By Clicking the Add in user Dictionary button, the word /
phrase is added automatically to the user dictionary as set in
the Settings for transliteration. Alternatively the user can delete
the word from the user dictionary by selecting the delete option.


This works only if the word has been added earlier by the user
to his own dictionary. Otherwise no effect takes place.
Update: Click this button to update the word in the main
dictionary if the transliterated word has been updated in the
Change To Edit box. If the same word comes for transliteration
the next time, the modified transliterated word is shown instead
of the original word.
Clicking the Options button evokes the transliteration setup
dialog box. For details see the SLS_SET_TRANS_OPTIONS
function below.
Ok button: Clicking this button confirms the transliteration and
closes the dialog box.
Cancel button: Clicking this button discards the transliteration
and closes the dialog box.
Help: Clicking the help button evokes the online help.
When a call to SLS_CONVERTLANGTOENG is made, the
above dialog box appears only if the settings contain the
Confirm every transliterated word or the option Confirm new
transliterated word. Other wise the word is transliterated
directly. For details of the transliteration setup see the function
SLS_SET_TRANS_OPTIONS.
This function takes five parameters. The first parameter is a
pointer to the language string that is to be transliterated in
English. Alternatively this parameter can be a string passed by


reference if pointers are not supported. The second parameter
is a pointer to the string in which the output string will be
retrieved. Again a reference string can be passed if pointers are
not supported. The caller function must allocate sufficient
memory to the output string before calling this function. If
sufficient space is not allocated then the string is truncated. The
third parameter is the size of the output string. If the function is
called with second parameter as a Null pointer, the size
required for the output string is returned in this parameter. The
caller function can then allocate enough memory and call the
function again. The fourth parameter is the code for the script
for the input Indian language string. For a detailed list of various
scripts available and their corresponding codes see the
Overview section. The fifth parameter is the code for the font
layout for the input Indian language string. For a detailed list of
various font layouts supported and their corresponding codes
see the Overview section.
Return Value: If the function executes successfully, the return
value is zero. If there is an error executing the function, then an
appropriate error code is returned. For a detailed list of errors
see the section 'Shree-Lipi Soft Error Codes'
SLS_CONVERTLANGTOENGEX (Input string, Output string,
Suggestions string, Output string size, Suggestion string
size, Script code, Font layout code)
Use this function to convert a string in one language to English.
This function takes seven parameters. The first parameter is a
pointer to the language string that is to be transliterated in
English. Alternatively this parameter can be a string passed by
reference if pointers are not supported. The second parameter


is a pointer to the string in which the output string will be
retrieved. Again a reference string can be passed if pointers are
not supported. The caller function must allocate sufficient
memory to the output string before calling this function. If
sufficient space is not allocated then the string is truncated. The
third parameter is a string that contains suggestions for the
transliteration if any. The fourth parameter is the size of the
output string. If the function is called with second parameter as
a Null pointer, the size required for the output string is returned
in this parameter. The caller function can then allocate enough
memory and call the function again. The fifth parameter is the
size of the suggestions string. If the function is called with third
parameter as a Null pointer, the size required for the suggestion
string is returned in this parameter. The caller function can then
allocate enough memory and call the function again. The sixth
parameter is the code for the script for the input Indian language
string. For a detailed list of various scripts available and their
corresponding codes see the Overview section. The seventh
parameter is the code for the font layout for the input Indian
language string. For a detailed list of various font layouts
supported and their corresponding codes see the Overview
section.
Return Value: If the function executes successfully, the return
value is zero. If there is an error executing the function, then an
appropriate error code is returned. For a detailed list of errors
see the section 'Shree-Lipi Soft Error Codes'.
SLS_CONVERTENGTOLANG ( Input string, Output string,
Size of the Output string, Script code, Font layout code )


Use this function to convert a string in English to Indian
Language. When a call to this function is made a dialog box
may appear depending upon the setting. The format of the

dialog box is as shown below.

For more details on the Dialog box see the function
SLS_CONVERTLANGTOENG
When a call to SLS_CONVERTENGTOLANG is made, the
above dialog box appears only if the settings contains the
Confirm every transliterated word or the option Confirm new
transliterated word. Other wise the word is transliterated


directly. For details of the transliteration setup see the function
SLS_SET_TRANS_OPTIONS
This function takes five parameters. The first parameter is a
pointer to the English string that is to be transliterated to
language. Alternatively this parameter can be a string passed
by reference if pointers are not supported. The second
parameter is a pointer to the string in which the output string will
be retrieved. Again a reference string can be passed if pointers
are not supported. The caller function must allocate sufficient
memory to the output string before calling this function. If
sufficient space is not allocated then the string is truncated. The
third parameter is the size of the output string. If the function is
called with second parameter as a Null pointer, the size
required for the output string is returned in this parameter. The
caller function can then allocate enough memory and call the
function again. The fourth parameter is the code for the script
for the output Indian language string. For a detailed list of
various scripts available and their corresponding codes see the
Overview section. The fifth parameter is the code for the font
layout for the output Indian language string. For a detailed list of
various font layouts supported and their corresponding codes
see the Overview section.
Return Value: If the function executes successfully, the return
value is zero. If there is an error executing the function, then an
appropriate error code is returned. For a detailed list of errors
see the section 'Shree-Lipi Soft Error Codes'
SLS_CONVERTENGTOLANGEX (Input string, Output string,
Suggestions string, Output string size, Suggestion string
size, Script code, Font layout code)


Use this function to convert a string in English to Indian
language.
This function takes seven parameters. The first parameter is a
pointer to the English string that is to be transliterated to
language. Alternatively this parameter can be a string passed
by reference if pointers are not supported. The second
parameter is a pointer to the string in which the output string will
be retrieved. Again a reference string can be passed if pointers
are not supported. The caller function must allocate sufficient
memory to the output string before calling this function. If
sufficient space is not allocated then the string is truncated. The
third parameter is a string that contains suggestions for the
transliteration if any. The fourth parameter is the size of the
output string. If the function is called with second parameter as
a Null pointer, the size required for the output string is returned
in this parameter. The caller function can then allocate enough
memory and call the function again. The fifth parameter is the
size of the suggestions string. If the function is called with third
parameter as a Null pointer, the size required for the suggestion
string is returned in this parameter. The caller function can then
allocate enough memory and call the function again. The sixth
parameter is the code for the script for the output Indian
language string. For a detailed list of various scripts available
and their corresponding codes see the Overview section. The
seventh parameter is the code for the font layout for the output
Indian language string. For a detailed list of various font layouts
supported and their corresponding codes see the Overview
section.
Return Value: If the function executes successfully, the return
value is zero. If there is an error executing the function, then an
appropriate error code is returned. For a detailed list of errors
see the section 'Shree-Lipi Soft Error Codes'.


Transliteration Setup functions
All the effects of transliteration can be achieved in one of the
two ways. They are as follows
1. Extending full control to the end user for setting the options.
2. Setting the options programmatically. The user will not have
any control over the setup. This can be done by using the
following calls. For a detailed description of the various
transliteration
settings
see
the
function
SLS_SET_TRANS_OPTIONS.
SLS_REFRESH_TRANS_SETUP (No parameter)
Use this function to refresh the transliteration setup. As has
been mentioned earlier, in the call to SLS_LoadTransliteration
various environment variables are initialized. These variables
are affected by a change in the Shree-Lipi Soft general setup.
For example, a change in the Script or the font layout may effect
a change upon these variables. To modify the transliteration
setup accordingly, it is necessary to make a call to this function.
This function has been implemented as a subroutine and does
not return a value.
SLS_SET_TRANS_OPTIONS
Use this function to evoke a dialog box that contains the various
settings for transliteration. This function is required only if
control of settings for transliteration is to be extended to the


user. The format of the dialog box that appears on the screen is
as follows. This dialog box consists of a Page control having
two tab sheets.

Page-1
This page contains options for setting up the various
dictionaries.
Main dictionaries Available
Main dictionary refers to the dictionary that is explicitly provided
with Shree-Lipi Soft for each installed script. When the dialog


box appears, this dropdown box contains the name of the Main
dictionary along with full path depending upon the current script.
If the name is not visible in the dropdown window, then select
the dictionary by clicking the button to the right of the drop down
box. This opens a file selection dialog box. The main dictionary
is in the form of an encrypted .DBF file present in the Shree-Lipi
Soft directory. For example, for Devnagari script it is
DEVDICT.DBF.
Subject Dictionaries available
Subject dictionary refers to the dictionaries provided on the
basis of subjects. This dictionary contains words and phrases
used in the context of Government offices, Accounts offices and
so on. This dictionary is provided explicitly along with Shree-Lipi
Soft and is present in the Shree-Lipi Soft directory. The
dropdown window under the label Subject dictionaries available
shows the name of the available subject dictionary (. DBF file)
for the current script along with full path name. If the name is
not visible, the user can select it from the drop down list.
User Dictionaries
While transliterating a string from one language to another,
sometimes a word may not be present in the dictionary. In such
cases, a confirmation dialog appears prompting for
confirmation. Also the users can add the word to their own
dictionary. Prior to this, it is necessary to create the user
dictionary. The dropdown window under the label User
Dictionaries shows the list of user dictionaries along with the
path if any has been created already.


A user dictionary can be created by simply clicking the Create
button. On clicking this button the format of the dialog box
changes to as shown below

Enter the name of the dictionary along with the path in the Edit
box. Also it is necessary to specify a script for the dictionary.
The dropdown combo box shows the list of Scripts installed
along with Shree-Lipi Soft.


After entering the name, click the create button to confirm the
creation of user dictionary. Alternatively, the user can cancel the
creation of dictionary by clicking the cancel button.
Significance: Once a user dictionary is created, the process of
transliteration will take the following course. The word to be
transliterated will be searched in the user dictionary followed by
the main dictionary available.
The format of the Preferences page is as shown below

Page-2


As the name itself indicates, this page contains settings for
preferences for confirmation and transliteration.
Confirm every transliterated word: Selecting this option
evokes a confirmation dialog box for every transliterated word.
Users can then update the word or add it to the user dictionary.
For more details see the section below.
Confirm only new transliterated word: When this option is
selected, the confirmation dialog box would be evoked only for
words not present in any of the predefined user dictionaries or
main dictionaries.
No confirmation for transliterated word: Checking this
options does not evoke a confirmation dialog box even if the
word is not present in any of the available dictionaries. In such
cases the program resorts to phonetic transliteration. This
option is particularly useful for Offline transliteration, when the
whole text is to be transliterated in one pass.

Options for Transliteration from Language to English
Auto Correct Mode: Checking this option enables the auto
correct mode for transliteration from Language to English
according to the settings made. Otherwise a confirmation dialog
box appears, prompting for confirmation.
All Uppercase: Checking this option converts all the characters
in the transliterated English word to UPPERCASE.


All Lowercase: Checking this option converts all the characters
in the transliterated English word to lowercase.
Uppercase first character of first word or phrase: Check this
option to leave the other characters unchanged except the first
character of first word or phrase which is converted to
UPPERCASE.
Uppercase first character of first word /All words in phrase:
This option is similar to the above one except that all first
characters in the words of a phrase are converted to
UPPERCASE.

SLS_SET_TRANS_CONFIRM_MODE (MODE)
Use this function to set the confirmation mode for transliteration.
This function takes a single parameter, which designates the
mode to be followed for transliteration. The permissible values
are as shown in the following table.
Mode
0

Description
Show Confirmation dialog for every transliterated
word
Show confirmation dialog only for newly transliterated
word
Do not show the confirmation dialog box
The function has been implemented as a subroutine and does
not return a value.


SLS_SET_TRANS_AUTOCORRECT_ON (Flag)
Use this function to set the auto correct mode status for
transliteration of words from Language to English. The auto
correct mode applies to certain specific transformations made to
the transliterated English word as explained in the
SLS_SET_TRANS_OPTIONS call. This function takes only one
parameter, which signifies the Status of the AutoCorrect Mode.
The permissible values are
Flag = 0 means set AutoCorrect mode OFF
Flag = 1 means set AutoCorrect mode ON
SLS_SET_TRANS_AUTOCORRECT_MODE (MODE)
Use this function to set the Auto correct mode itself. Auto
correct mode refers to certain specific transformations made to
the transliterated word when the transliteration is from Indian
language word to English. This function takes a single
parameter designating the Auto correct mode. The permissible
values are as listed below along with the corresponding
transformation
Mode
0

Description
All characters in UPPERCASE
All characters in lowercase
First character of word/(first word of phrase) in
UPPERCASE and the rest in lowercase


First character of word/(first character of every word
of phrase) in UPPERCASE and the rest in lowercase
This function has been implemented as a subroutine and does
not return a value.
SLS_TRANS_RESTOREDEFAULTS (No parameters)
This function is used to restore default settings in Transliteration
Options. The default values are :
No Main Dictionary is assigned.
No Subject Dictionary is assigned.
No User Dictionary is assigned.
It will Confirm for every word.
Transliteration Dictionary Functions
SLS_SET_TRANS_MAINDICT (Dictionary Name)
Use this function to set the main dictionary for transliteration
programmatically.
The single parameter to this function is the pointer to the name
of the dictionary along with its full path. As mentioned earlier,
this dictionary is in the form of an encrypted .DBF file in the
Shree-Lipi Soft directory. Alternatively the name can be passed
as a reference string.


This function has been implemented as a subroutine and does
not return a value.
SLS_SET_TRANS_SUBDICT (Dictionary Name)
Use this function to set the subject dictionary for transliteration
programmatically. This function should be called only if a
subject dictionary is available for the installed script.
The single parameter to this function is the pointer to the name
of the dictionary along with its full path. As mentioned earlier,
this dictionary is also in the form of an encrypted .DBF file in the
Shree-Lipi Soft directory. Alternatively the name can be passed
as a reference string.
This function has been implemented as a subroutine and does
not return a value.
SLS_SET_TRANS_USERDICT (Dictionary Name)
Use this function to set the user dictionary for transliteration
programmatically. This function should be called only if a user
dictionary has been created.
The single parameter to this function is the pointer to the name
of the dictionary along with its full path. Alternatively the name
of the user dictionary can be passed as a reference string.
This function has been implemented as a subroutine and does
not return a value.


SLS_DELETE_FROM_DICT (EngWord, LangWord, Script
code, Font layout code)
This function can be called to delete the existing Word / Phrase
Entry in User Dictionary. The function takes four parameters.
The first parameter is the English Word, whereas the second
parameter is the Language Word. The function deletes the entry
that matches with this pair of words. The third parameter is the
code for the script for the Indian language word. For a detailed
list of various scripts available and their corresponding codes
see the Overview section. The fourth parameter is the code for
the font layout for the Indian language word. For a detailed list
of various font layouts supported and their corresponding codes
see the Overview section.
Return Value: The function returns 0 if word is successfully
deleted from user dictionary. A nonzero value indicates the
following errors:
22 : User Dictionary Does not exists.
23 : There are no records to be deleted.

SLS_ADD_TO_DICT (EngWord, LangWord, Script code,
Font layout code)
This function can be called to add a Word / Phrase Entry in
User Dictionary. The function takes four parameters. The first
parameter is the English Word, whereas the second parameter


is the Language Word. The function adds the pair of words as
an entry. The third parameter is the code for the script for the
Indian language word. For a detailed list of various scripts
available and their corresponding codes see the Overview
section. The fourth parameter is the code for the font layout for
the Indian language word. For a detailed list of various font
layouts supported and their corresponding codes see the
Overview section.
Return Value: The function returns 0 if word is successfully
deleted from user dictionary. A nonzero value indicates the
following errors:
22 : User Dictionary Does not exists.
23 : Entry already exists.
SLS_CREATE_USER_DICT (Path, Filename, Script Code)
This function is called to create a user dictionary. It takes three
parameters. The first parameter is a pointer to the string
containing the path where the user dictionary has to be created.
If pointers are not supported in the development platform, the
string can be passed by reference. The second parameter is a
pointer to the string containing the file name of the user
dictionary. If pointers are not supported in the development
platform, the string can be passed by reference. The third
parameter is the code for the script for the user dictionary. For a
detailed list of various scripts available and their corresponding
codes see the Overview section.


Returns Value: The function returns 0 if successful, and a non
zero value if failure occurs.
How to use the function:
SLS_CREATE_USER_DICT('c:\shree60','samdev',1)
This will create a Devnagari user dictionary with name 'samdev'
in 'c:\shree60' directory.
This call will result in making four files viz UserDict.dbf,
UserDict.mdx, UserDict.dit, and UserDict.did in the target path.
SLS_TRANS_MERGE_DICT
Dictionary FileName2)

(Dictionary

FileName1,

Use this function to Merge two User Dictionaries. This function
takes two parameters. The parameters are the names of the
Dictionaries with full path. The names have to be passed as
pointers or by reference if pointers are not supported in the
development platform. The Function merges DictFileName2
Dictionary in DictFileName1.
SLS_TRANS_EDIT_DICT (DictFileName)
Use this function to Edit the User Dictionary. This function takes
only one parameter. The parameter is a pointer to the name of
the Dictionary File. If pointers are not supported on the


development platform, the name can be passed by reference.
This Function Displays the Dictionary Editing Dialog Box.
SLS_FIND_WORD_IN_USERDICT (Input word, Output word,
Language Flag, Output string Size, Script code, Font layout
code)
This function can be called to find the word in user dictionary.
The function takes six parameters. Input word is a pointer
to the input word. If the third parameter (Language Flag) is
0, then the first parameter has to be an English word for
which language words have to be found. If Language Flag
is 1 then it has to be language word for which English
words have to be found. The second parameter is a pointer
to the Output string. If the third parameter (Language Flag)
is 0, then the Output string is the language word/s for the
given English word. If Language Flag is 1 then the Output
string is the English word/s for the given language word. If
the dictionary contains multiple entries for a given input
word, all the words / phrases are returned in the output
string separated by comma. The third parameter is the
Language Flag, the functionality of which is already
explained.
The fourth parameter is the size of the output string. The
calling program is supposed to acquire enough memory to
hold the output string. However, if the function is called
with the second parameter as a null string, then this
function returns the required size of the output string. The
caller can then acquire enough memory and call the
function again. If enough memory is not assigned, the
output string is truncated.


The fifth parameter is the code for the script for the Indian
language word. For a detailed list of various scripts
available and their corresponding codes see the Overview
section. The sixth parameter is the code for the font layout
for the Indian language word. For a detailed list of various
font layouts supported and their corresponding codes see
the Overview section.
SLS_FIND_WORD_IN_SUBDICT (Input word, Output word,
Language Flag, Output string Size, Script code, Font layout
code)
This function can be called to find the word in the subject
dictionary.
The function takes six parameters. Input word is a pointer
to the input word. If the third parameter (Language Flag) is
0, then the first parameter has to be an English word for
which language words have to be found. If Language Flag
is 1 then it has to be language word for which English
words have to be found. The second parameter is a pointer
to the Output string. If the third parameter (Language Flag)
is '0, then the Output string is the language word/s for the
given English word. If Language Flag is 1 then the Output
string is the English word/s for the given language word. If
the dictionary contains multiple entries for a given input
word, all the words / phrases are returned in the output
string separated by comma. The third parameter is the
Language Flag, the functionality of which is already
explained.
The fourth parameter is the size of the output string. The
calling program is supposed to acquire enough memory to


hold the output string. However, if the function is called
with the second parameter as a null string, then this
function returns the required size of the output string. The
caller can then acquire enough memory and call the
function again. If enough memory is not assigned, the
output string is truncated.
The fifth parameter is the code for the script for the Indian
language word. For a detailed list of various scripts
available and their corresponding codes see the Overview
section. The sixth parameter is the code for the font layout
for the Indian language word. For a detailed list of various
font layouts supported and their corresponding codes see
the Overview section.
SLS_FIND_WORD_IN_MAINDICT (Input word, Output word,
Language Flag, Output string Size, Script code, Font layout
code)
This function can be called to find the word in the main
dictionary.
The function takes six parameters. Input word is a pointer
to the input word. If the third parameter (Language Flag) is
0, then the first parameter has to be an English word for
which language words have to be found. If Language Flag
is 1 then it has to be language word for which English
words have to be found. The second parameter is a pointer
to the Output string. If the third parameter (Language Flag)
is 0, then the Output string is the language word/s for the
given English word. If Language Flag is 1 then the Output
string is the English word/s for the given language word. If
the dictionary contains multiple entries for a given input


word, all the words / phrases are returned in the output
string separated by comma. The third parameter is the
Language Flag, the functionality of which is already
explained.
The fourth parameter is the size of the output string. The
calling program is supposed to acquire enough memory to
hold the output string. However, if the function is called
with the second parameter as a null string, then this
function returns the required size of the output string. The
caller can then acquire enough memory and call the
function again. If enough memory is not assigned, the
output string is truncated.
The fifth parameter is the code for the script for the Indian
language word. For a detailed list of various scripts
available and their corresponding codes see the Overview
section. The sixth parameter is the code for the font layout
for the Indian language word. For a detailed list of various
font layouts supported and their corresponding codes see
the Overview section.
SLS_FIND_WORD_IN_ALLDICT (Input word, Output word,
Language Flag, Output string Size, Script code, Font layout
code)
This function can be called to find the word in all the three
dictionaries - user dictionary, subject dictionary, and main
dictionary.
The function takes six parameters. Input word is a pointer
to the input word. If the third parameter (Language Flag) is


0, then the first parameter has to be an English word for
which language words have to be found. If Language Flag
is 1 then it has to be language word for which English
words have to be found. The second parameter is a pointer
to the Output string. If the third parameter (Language Flag)
is 0, then the Output string is the language word/s for the
given English word. If Language Flag is 1 then the Output
string is the English word/s for the given language word. If
the dictionary contains multiple entries for a given input
word, all the words / phrases are returned in the output
string separated by comma. The third parameter is the
Language Flag, the functionality of which is already
explained.
The fourth parameter is the size of the output string. The
calling program is supposed to acquire enough memory to
hold the output string. However, if the function is called
with the second parameter as a null string, then this
function returns the required size of the output string. The
caller can then acquire enough memory and call the
function again. If enough memory is not assigned, the
output string is truncated.
The fifth parameter is the code for the script for the Indian
language word. For a detailed list of various scripts
available and their corresponding codes see the Overview
section. The sixth parameter is the code for the font layout
for the Indian language word. For a detailed list of various
font layouts supported and their corresponding codes see
the Overview section.
Browsing the User Dictionary :


If you want to give your own user interface for providing
the user dictionary editing functions, the following
functions of Shree-Lipi Soft can be used.
SLS_USER_DICT_BOF
Call this Function to check whether the beginning of dictionary
has been reached while traversing the User Dictionary.
Retrun Value :
In case of successful execution : If the BOF of Dictionary is
reached then the function returns 1 or else the function returns
0.
In case of unsuccessful execution : the error code is either of
the following values :
117 : User Dictionary is not Assigned.
118 : User Dictionary is not in Active State.
SLS_USER_DICT_EOF
Call this Function to check whether the end of dictionary has
been reached while traversing the User Dictionary.
Retrun Value :


In case of successful execution : If the EOF of Dictionary is
reached then the function returns 1 or else the function returns
0.
In case of unsuccessful execution : the error code is either of
the following values :
115 : User Dictionary is not Assigned.
116 : User Dictionary is not in Active State.
SLS_USER_DICT_FIRST(LangWord, EngWord)
Call this Function to get the values in the first record in the
Assigned User Dictionary.
Retrun Value :
In case of successful execution : The values are returned in the
LangWord and EngWord parameters.
In case of unsuccessful execution : the error code is either of
the following values :
107 : User Dictionary is not Assigned.
108 : User Dictionary is not in Active State.
SLS_USER_DICT_LAST(LangWord, EngWord)


Call this Function to get the values in the last record in the
Assigned User Dictionary.
Retrun Value :
In case of successful execution : The values are returned in the
LangWord and EngWord parameters.
In case of unsuccessful execution : the error code is either of
the following values :
113 : User Dictionary is not Assigned.
114 : User Dictionary is not in Active State.

SLS_USER_DICT_NEXT(LangWord, EngWord)
Call this Function to get the values in the next record in the
Assigned User Dictionary.
Retrun Value :
In case of successful execution : The values are returned in the
LangWord and EngWord parameters.
In case of unsuccessful execution : the error code is either of
the following values :


111 : User Dictionary is not Assigned.
112 : User Dictionary is not in Active State.
SLS_USER_DICT_PRIOR(LangWord, EngWord)
Call this Function to get the values in the previous record in the
Assigned User Dictionary.
Retrun Value :
In case of successful execution : The values are returned in the
LangWord and EngWord parameters.
In case of unsuccessful execution : the error code is either of
the following values :
109 : User Dictionary is not Assigned.
110 : User Dictionary is not in Active State.


## Chapter 7: Dot Matrix Printing Calls
Printing of Indian language string is another major concern in
developing multilingual solutions. Since Indian language
characters are treated as Graphical objects rather than Plain
text, one has to resort to the windows canvas printing. This
makes the printing process considerably slow. It is not possible
to get the draft quality output for Indian languages, as it is
possible for English. The effect is more pronounced while
printing on a dot matrix printer. Even for a small document the
printing process may eat up a considerable amount of time
which is not desirable.
Shree-Lipi Soft provides solution to the above mentioned
problems in the form of exportable calls. If these calls are used
for printing to any Dot matrix Printer, the printing process
speeds up without much loss of quality and resolution. The
basic requirement of using these calls is to have an EPSON
COMPATIBLE Dot Matrix Printer attached to the printer port
of the computer.
In this chapter we explore the various printing calls supported
by Shree-Lipi Soft. All these calls are in the form of exportable
functions and are present in the DLL 'SLSDLL.DLL'.
The most significant of the printing calls is the call to the
initialization of the Dot Matrix Printing Calls.
To print the data , printer has to be initialized first by function
SLS_DMP_INIT.


After initializing the printer , printer mode is set which is done by
using function SLS_DMP_SET_MODE and pagesize is set by
using function SLS_DMP_SET_PAGESIZE. If page size is not
set by this function it is set to size 8 by 11 by default.
The page to be printed is prepared using calls such as
SLS_PRINT_STRING and the like.
After the whole page has been prepared, SLS_PRINT_PAGE
should be called to actually send the page to the printer.
All the DMP functions are explained below.
It is a must to call this function before any other printer-related
call is made.
The format of the call is as follows.
SLS_DMP_INIT (PrinterDevicename)
The parameter is a pointer to the name of the Printer.
Alternatively the name of the printer can be passed as a
reference string. For example the name of the printer may be
'Epson FX-100'
Return Value: If the function is successful then the return value
is zero. If an error occurs, the appropriate error code is
returned. For a list of possible errors see the section 'Shree-Lipi
Soft error codes'


SLS_PRINT_STRING (X-Position, Y-Position, String, Script
Code, Font layout code, Numeral code)
Use this call for printing a string in any supported font format.
This function takes 6 parameters in all.
The first parameter indicates the X-Position (Columnar position
or distance from the left of paper) where the string will be
printed. Similarly the second parameter signifies the Y-position
(Row position or distance from the top of paper) where the
string will be printed. Both the parameters are DOUBLE type
parameters and the default unit for both the parameters is
INCHES. You can set a different unit by the call
SLS_DMP_SET_PRINT_UNIT, which is described later.
The third parameter is a pointer to the String that is to be
printed. Alternatively it can be a string passed as reference. The
fourth parameter (Script code) indicates the code for the script
of the string to be printed. For a detailed list of the various
permissible script codes see the Overview Section. The fifth
parameter is the code of the font layout of the string. For a
detailed list of the various permissible script codes see the
Overview Section.
The sixth parameter indicates the numeral script. In Tamil,
Kannada, Telugu and Malayalam, English numerals are used by
default, hence this parameter is not of any consequence for
these scripts. However, for Devnagri, Gujarati, Punjabi, Bengali,
Assamese and Oriya, the language numerals are used by
default. If may still want to print the numerals in English script.
This parameter is provided for you to specify the numeral script.


A value of zero means English numerals, and a value of 1
means language numerals.
SLS_RJ_PRINT_STRING (X-Position, Y-Position, Print
String, Script Code, Font layout code, Numeral Code)
Use this function to print a string in any of the supported font
layouts, right justified to a specific position in paper along the Xaxis in the Dot Matrix Printer. This function takes 6 parameters
in all.
The first parameter signifies the X-Position (along the Column),
in Inches or the specified unit as a distance from the left of the
paper, to which the string will be right justified while printing.
The second parameter signifies the Y-Position for the string in
Inches or specified units. The value of Y-Position is with respect
to the Top of the Paper. The unit for distances is inch by default,
but can be changed by the call SLS_DMP_SET_PRINT_UNIT.
Print String is the string to be printed. Script Code refers to the
code for the script of the string. For a list of permissible script
codes see the Overview Section. Font Layout Code is the code
for the layout of the font in which the print string is specified.
For a list of permissible codes see the Overview Section.
The sixth parameter indicates the numeral script. In Tamil,
Kannada, Telugu and Malayalam, English numerals are used by
default, hence this parameter is not of any consequence for
these scripts. However, for Devnagri, Gujarati, Punjabi, Bengali,
Assamese and Oriya, the language numerals are used by
default. If may still want to print the numerals in English script.
This parameter is provided for you to specify the numeral script.
A value of zero means English numerals, and a value of 1
means language numerals.


This function can be used for printing numbers. The numbers
should be converted to string format by using platform specific
functions.
Return Value: This function has been implemented as a
subroutine and does not return a value.
SLS_PRINT_MEMO (Left Margin, Right Margin, Y-Position,
Print String, Script Code, Font layout code, Numeral Code)
Use this function to print a long string (Memo) in any of the
supported font codes between the margins specified as left
Margin and Right margin. This function takes 7 Parameters in
all.
Left Margin is the X-Position in Inches (or specified units) from
which printing will actually start from. Right Margin is the extent
to which the actual printing will take place. If the string exceeds
the width, then it will automatically be wrapped. Right margin is
the distance from the left of the paper in Inches (or specified
units). Y-Position refers to the distance in Inches (or specified
units) from Top where the actual printing will start. The unit for
distances is inch by default, but can be changed by the call
SLS_DMP_SET_PRINT_UNIT. Print String is the reference or
pointer to the actual text that is to be printed. Script code refers
to the code for the script of the string to be printed. For a
detailed list of various available scripts and their codes see the
"Overview Section". The Font Layout Code is the code of the
layout of the font in which the Print String has been specified.
For a detailed list of various available font layout codes see the
"Overview Section".


The seventh parameter indicates the numeral script. In Tamil,
Kannada, Telugu and Malayalam, English numerals are used by
default, hence this parameter is not of any consequence for
these scripts. However, for Devnagri, Gujarati, Punjabi, Bengali,
Assamese and Oriya, the language numerals are used by
default. If may still want to print the numerals in English script.
This parameter is provided for you to specify the numeral script.
A value of zero means English numerals, and a value of 1
means language numerals.
This function has been implemented as a subroutine and does
not return a value.
SLS_PRINT_PAGE (no parameters)
Use this function to actually send the page to the printer. The
page should be prepared by using calls such as
SLS_PRINT_STRING and the like. After the whole page has
been prepared, this procedure should be called.
Printing Formatted Strings
It is possible to print the strings with some formatting like bold,
italic, underline etc. The possible formatting attributes and their
values are as follows:
Value

Style Combination

============================

Bold Only


Italic Only


Bold Italic


Underline Only


Bold + Underline


Italic + Underline


Bold + Italic + Underline


Strike-Out


Bold + Strike-Out


Italic + Strike-Out


Bold + Italic + Strike-Out


Underline + Strike-Out


Bold + Underline + Strike-Out


Italic + Underline + Strike-Out


Bold + Italic + Underline + Strike-Out


It is also possible to specify the alignment for such strings. The
possible values are as under:
Alignment

value

======================
Left Aligned

0

Right Aligned


SLS_FORMATTED_PRINT_STRING (X-Position, Y-Position,
String, Script Code, Font layout code, Numeral code, Style
code, Align Mode)
Use this call for printing a formatted string in any supported font
format.
This function takes 8 parameters in all.
The first parameter indicates the X-Position (Columnar position
or distance from the left of paper) where the string will be
printed. Similarly the second parameter signifies the Y-position
(Row position or distance from the top of paper) where the
string will be printed. Both the parameters are DOUBLE type
parameters and the default unit for both the parameters is
INCHES. You can set a different unit by the call
SLS_DMP_SET_PRINT_UNIT, which is described later.


The third parameter is a pointer to the String that is to be
printed. Alternatively it can be a string passed as reference. The
fourth parameter (Script code) indicates the code for the script
of the string to be printed. For a detailed list of the various
permissible script codes see the Overview Section. The fifth
parameter is the code of the font layout of the string. For a
detailed list of the various permissible script codes see the
Overview Section.
The sixth parameter indicates the numeral script. In Tamil,
Kannada, Telugu and Malayalam, English numerals are used by
default, hence this parameter is not of any consequence for
these scripts. However, for Devnagri, Gujarati, Punjabi, Bengali,
Assamese and Oriya, the language numerals are used by
default. If may still want to print the numerals in English script.
This parameter is provided for you to specify the numeral script.
A value of zero means English numerals, and a value of 1
means language numerals.
The seventh parameter gives the print style in which the string
is to be printed. The possible values are given above. The
eighth parameter is for the alignment of the string. The possible
values are as given above.
Note: Currently right alignment is not supported.
Return Values: If the function is successful then it returns
ZERO. Otherwise it returns an error code. For a list of possible
errors see Shree-Lipi Soft Error Codes.
On return the function stores the value of the current X and Y
Position in the variables X-Position and Y-Position.


SLS_FORMATTED_PRINT_MEMO (Left Margin, Right
Margin, Y-Position, Print String, Script Code, Font layout
code, Numeral code, Style code, Align Mode)
Use this function to print a formatted long string (Memo) in any
of the supported font codes between the margins specified as
left Margin and Right margin. This function takes 9 Parameters
in all.
Left Margin is the X-Position in Inches (or specified units) from
which printing will actually start from. Right Margin is the extent
to which the actual printing will take place. If the string exceeds
the width, then it will automatically be wrapped. Right margin is
the distance from the left of the paper in Inches (or specified
units). Y-Position refers to the distance in Inches (or specified
units) from Top where the actual printing will start. The unit for
distances is inch by default, but can be changed by the call
SLS_DMP_SET_PRINT_UNIT. Print String is the reference or
pointer to the actual text that is to be printed. Script code refers
to the code for the script of the string to be printed. For a
detailed list of various available scripts and their codes see the
"Overview Section". The Font Layout Code is the code of the
layout of the font in which the Print String has been specified.
For a detailed list of various available font layout codes see the
"Overview Section"
The seventh parameter indicates the numeral script. In Tamil,
Kannada, Telugu and Malayalam, English numerals are used by
default, hence this parameter is not of any consequence for
these scripts. However, for Devnagri, Gujarati, Punjabi, Bengali,
Assamese and Oriya, the language numerals are used by
default. If may still want to print the numerals in English script.
This parameter is provided for you to specify the numeral script.


A value of zero means English numerals, and a value of 1
means language numerals.
The eighth parameter gives the print style in which the string is
to be printed. The possible values are given above. The ninth
parameter is for the alignment of the string. The possible values
are as given above.
Note: Currently right alignment is not supported.
Return Values: If the function is successful then it returns
ZERO. Otherwise it returns an error code. For a list of possible
errors see Shree-Lipi Soft Error Codes.
On return the function stores the value of the current Y Position
in the variable Y-Position.
SLS_DMP_SET_MODE (Print Mode)
Use this function to set the printing mode. The permissible
values for Print Mode are 1, 2, 3 and 10. Each value signifies a
point size for the character. The print mode 10 can be used on
24 pin printers only. The other 3 modes can be used on either of
the printers, but the printing is done for the resolution supported
by the 9 pin printers. The line spacing for modes 1 and 10 is
1/8th of an inch, whereas line spacing for modes 2 and 3 is
1/4th of an inch.
Return value: 0 if successful, non-zero if any error occurred.
The return value is the error code. For a detailed list of errors
that can occur see the section Shree-Lipi Soft Error Codes.


SLS_DMP_SET_PRINT_UNIT (UNIT)
This function can be called to change the Printer Units. By
Default the Unit is Inches. The values that UNIT can take are as
follows.
Units

Code

=========================
Inches

0

Centimeter


Millimeter


Pixels


Return Values: If the function is successful then it returns Zero
otherwise it returns a Non Zero Error Code.
SLS_DMP_SET_PRINTTOFILE ( PrnFlag, const PrnFile )
This function sets the PrintToFile Flag ON and also sets the
name of the .PRN File.
To Set the PrintToFile Option ON, Set PrnFlag to Any NONZERO VALUE.


To Set the PrintToFile Option OFF, Set PrnFlag to ZERO.
If PrnFlag is ZERO "PrnFIle" is ignored. If PrnFlag is Non-ZERO
then "PrnFile" must point to a Valid Path and FileName. The
FileName need not exist but the Path must exist.
Return Values : If the function is successful then the return
value is zero else the function returns a Error Code.
SLS_DMP_CLOSE_PRINTFILE ( No Parameters )
This function must be called when a previous call to
SLS_DMP_SET_PRINTTOFILE has been made. This function
writes the final mandatory commands to the .PRN File. The
.PRN File will contain the whole document including all the
pages. This call should be given after the SLS_PRINT_PAGE
command has been called for all the pages.
Return Values : If the function is successful then the Return
value is ZERO. If not then it returns a Error Code.

SLS_DMP_SET_PAGESIZE ( PageWidth, PageHeight)
Use this function to set the page dimensions. All X and Y
Positions passed as parameters to function Calls such as
SLS_PRINT_STRING and the like would be with respect to
these dimensions. The function takes 2 parameters.


PageWidth is the width of the page. PageHeight refers to the
height of the page. The unit for the parameters is inch by
default,
but
can
be
changed
by
the
call
SLS_DMP_SET_PRINT_UNIT.
Return Value: If the function executes successfully, then the
return value is 0. If an error occurs, the return value is an Error
Code. For a detailed list of possible errors and their codes see
the section Shree-Lipi Soft Error Codes

Printing on ISCII Printers
A number of printers are available in the market, which
support direct printing of ISCII strings. This printing is
much faster than the Windows graphics printing, or even
Shree-Lipi Soft DMP printing. Shree-Lipi Soft has provided
a few calls to facilitate printing on such ISCII printers.
SLS_INIT_ISCII_PRINTER ( Mode, PrnFile )
This function initialises the Printer for ISCII Mode printing. Mode
refers to the Quality of the Printing.
Values for Mode
================
Draft Quality : 0


Letter Quality : 1
The Parameter PrnFile indicates the name of the .PRN file with
full Path. If the file already exists then it is overwritten. The
caller must specify the full path, otherwise the file will be created
in the current directory. If you want to output directly to the
Printer, then set PrnFile to "Nil".
Note : This function applies only to the SPECIAL Printers from
TVSE and WIPRO which have an In-Built ISCII printing facility
If the Printer is not an ISCII Printer then the Printer will print
JUNK.
Return Values : If the function is successful then the return
value is ZERO Other wise the return value is -1 or Any of the
Error codes .
SLS_ISCII_PRINT_STRING (X-Position, Y-Position, String,
Script Code, Font layout code, Style code, Pitch code)
This function is a special call provided for printing ISCII-Strings
to the ISCII printer.
Note :This function works only with the ISCII Printers ( Printers
that have in built capability for printing Indian language ISCII
strings).
This function takes 7 parameters in all.
The first parameter indicates the X-Position (Columnar position
or distance from the left of paper) where the string will be


printed. Similarly the second parameter signifies the Y-position
(Row position or distance from the top of paper) where the
string will be printed. Both the parameters are DOUBLE type
parameters and the default unit for X-Position is INCHES. You
can
set
a
different
unit
by
the
call
SLS_DMP_SET_PRINT_UNIT. The Y-Position has to be given
as the line number from the top.
The third parameter is a pointer to the String that is to be
printed. Alternatively it can be a string passed as reference. The
fourth parameter (Script code) indicates the code for the script
of the string to be printed. For a detailed list of the various
permissible script codes see the Overview Section. The fifth
parameter is the code of the font layout of the string. For a
detailed list of the various permissible script codes see the
Overview Section.
The sixth parameter gives the print style in which the string is to
be printed. The possible values are given above the
SLS_FORMATTED_PRINT_STRING
call.
The
seventh
parameter is for the The Pitch used for printing this string. After
the string is printed, the pitch is reverted to the global value.
Return Values: If the function is successful then it returns
ZERO. Otherwise it returns an error code. For a list of possible
errors see Shree-Lipi Soft Error Codes.
SLS_ISCII_PRINT_PAGE (No Parameters)
This procedure is to be called to print the page actually. All the
print strings have to be sent to the SLSDLL.DLL by previous


calls
to
SLS_ISCII_PRINT_STRING
SLS_ISCII_PRINT_PAGE should be called.

and

then

Return Values: If the function is successful then the return
value is ZERO. Other wise the return value is -1 or Any of the
Error codes .
SLS_ISCII_CLOSE_PRINTFILE (No Parameters)
This is the finalisation call for ISCII Printing. Individual
commands given using SLS_ISCII_PRINT_STRING are
queued and they are actually printed only when
SLS_ISCII_CLOSE_PRINTFILE is called.
Return Values: If the function is successful then the return
value is ZERO. Other wise the return value is -1 or Any of the
Error codes .
SLS_DMP_SET_DPI ( XDPI, YDPI )
This is a function to set the DPI for ISCII Printing. This DPI
value will be interpreted as a global value, which will be
applicable for all the ISCII Printing being done. It is mandatory
to
call
SLS_DMP_SET_DPI
after
every
call
to
SLS_INIT_ISCII_PRINTER.

XDPI : Number of characters along X-axis per inch
YDPI : Number of characters along Y-axis per inch


Miscellaneous printing calls
SLS_GET_DMP_STRINGWIDTH (String, Script Code, Font
layout code)
Use this function to find the width of the string in Inches. This
may be necessary for formatting the report according to the
desired specifications.
String is the string for which length is to be found out. Script
code refers to the code for the script of the string, and Font
layout code is the code for the font layout of the string. For a list
of permissible values see the Overview Section.
This function is not available for ISCII printing calls.
Return Value: If the function is successful, it returns the size of
the string in Inches (as a double variable).
SLS_GET_DMP_STRINGHEIGHT (String, Script Code, Font
layout code)
This is a generalized call for obtaining the String height of any
string in any font layout.
String is the string for which length is to be found out. Script
code refers to the code for the script of the string, and Font


layout code is the code for the font layout of the string. For a list
of permissible values see the Overview Section.
This function is not available for ISCII printing calls.
Return Values : The return value is the Height of the input
string.
SLS_DRAW_HRULE (X1, X2, Y, THICKNESS)
Function to be called to draw a horizontal line of the required
thickness.
X1, X2 are the starting and ending positions of the Line. Y is the
Offset from the Top Margin where the line will be printed.
THICKNESS is the line thickness in pixels.
SLS_DRAW_VRULE (X, Y1, Y2, THICKNESS)
Function to be called to draw a vertical line of the required
thickness.
X is the Offset from the Left Margin where the line will be
printed. Y1, Y2 are the starting and ending positions of the Line.
THICKNESS is the line thickness in pixels.

SLS_SET_DMP_REVERSEFEED ( Feed )
A Function call for moving the head of printer in reverse
direction (in Upward Direction).


Feed is the Amount of Reverse Feed in Inches.
This function should be called before any print function.
Return Values: Zero in case of Successful Operation.

Spooling the Print Jobs

If you use SLS_PRINT_PAGE for a number of pages, different
jobs are created for different pages for the same document.
Shree-Lipi Soft supports a few functions so that you can send
the print jobs through a single queue. This guarantees the
sequence of pages printed, and makes cancellation of the job
easy.

SLS_SPOOL_PRINT_PAGE
Use this procedure to send all the print page jobs through a
single queue. The job name can be assigned by a previous call
to the function SLS_DMP_SET_PRINTJOBNAME.
SLS_DMP_RESET_SPOOLFLAGS
This function resets the flags used for spooling.
Call this function after the call to the function
SLS_SPOOL_PRINT_PAGE.


SLS_DMP_SET_PRINTJOBNAME ( Print Job Name )
This procedure is to be called for setting the User specified
name to the document for printing. This name is assigned to the
spooled jobs.
The function takes only one parameter, that is the Print Job
Name, which is a pointer to the string containing name to be
given for the Job for Printing. If pointers are not supported in
your development platform, pass the parameter by reference.


## Chapter 8: Shree-Lipi Soft Error Codes
The following are the list of Error codes returned by Shree-Lipi
Soft along with the detailed explanation.
Error Code


Description
0No Error, Function executed successfully
Error in loading the Script composing DLL. I.e.
the DLLs ???DL32.DLL or SU_???32.DLL
are not found. Confirm that these DLLs are
present in the Shree-Lipi Soft path and that the
path is accessible. Alternatively the DLL may
be unreadable by Shree-Lipi Soft. The third
reason may be that the script code used in
Shree-Lipi Soft functions is illegitimate. I.e.
Shree-Lipi Soft does not support that particular
script.
Incorrect Passwords have been specified in
the function calls.
Shree-Lipi Soft is not active. I.e. SLS_START2
has not been called.
Error in reading the specified Keyboard layout
File
The pathname specified for Shree-Lipi Soft is
too long ( > 127 characters)
Application
type
not
supported.
Call
SLS_SET_APPLICATION_TYPE.
Incorrect value of Message No. for Shree-Lipi
Soft activation function SLS_START1. The
message number must be between 0 and
0x7FFF-WM_USER = 0x7BFF


Shree-Lipi Soft is already active for this
application.
The specified script was not purchased by the
user
The transliteration was successful in mode
"Confirmation for all the
words" but the
user clicked on the Cancel button to revert the
Transliteration.
Transliteration Initialization has not been done.
Use LOAD_TRANSLITERATION prior to using
any transliteration call.
Incorrect
Print
Mode
value
in
DMP_SET_MODE The permissible values are
between 1 to 3 for 9 Pin DMP and 10(only) for
24 Pin DMP
The value specified for PageWidth exceeds
the maximum value for the physical page.
The value specified for PageHeight exceeds
the maximum value for the physical page.
Invalid value for Unit.
Invalid
PathName
in
DMP_SET_PRINTTOFILE command.
DMP_CLOSE_PRINTFILE has been called
without DMP_SET_PRINTTOFILE.
String passed is Empty.
Invalid value for Alignment in call to
DMP_PRINT_STRING.


## Chapter 9: Shree-Lipi Soft Utilities
Keyboard Tutor
Keyboard Tutor Program for Indian Languages is a special
utility of Shree-Lipi Soft. For novices it will guide how to type
phonetic key sequences to get different conjuncts. For experts
sometimes it will guide on how to form a particular conjunct for a
particular layout with a particular script. It also provides a facility
of printing the current keyboard. It replaces Key-Tops with
sticker as per current Keyboard and script.

With this simulated keyboard available on desktop, user can
either click or press the keys as per the layout. In the simulated
mode i.e. clicking the key-tops on desktop, it simulates the
pressing of a key from the keyboard.
How to use the tutor
The Keyboard Tutor works in conjunction with Shree-Lipi Soft.


Through Shree-Lipi Soft and its Data exchange structure the
Tutor receives all the information like current active Script,
current Key-Layout and similar information required to display
the Key-Tops. To display Key-Tops as per current layout,
Shree-Lipi Soft must be active while using the tutor. As
mentioned in the Shree-Lipi Soft general calls, the Tutor can be
evoked
by
using
the
call
SLS_TUTOR_ON
or
SLS_TUTOR_ON1. The Tutor will display Key Tops in English,
if activation key is off. Now toggle the activation key. The normal
(i.e. unshifted) layout will appear. If you click on Shift button,
SHIFT layout will appear. By clicking CTRL+SP button the third
additional layer will appear. One can click a keycap with the left
mouse button. In this case the key described on top of the key
as per the current layer will appear in your application window.
One can also switch between scripts. As you move the mouse
cursor over various keys, the characters present on the normal,
Shift and alter layers of the key where the mouse cursor is
currently positioned are displayed in enlarged view.
By clicking on the 'Print' button you can print the currently
selected keyboard. If you enable the 'Always on Top' option
from the System menu of the Keyboard tutor, the tutor will
appear in front of all other open windows and dialog boxes.


## Appendix A: Shree-Lipi Soft Data Exchange Structure
Shree-Lipi Soft uses a general data exchange structure for
communicating with the application. The application can use
this record structure for retrieving information back from ShreeLipi Soft for taking desired actions. The format of the data
exchange structure is as follows.
Variable Name
SHREE_ERROR

SHREE_ACTIVE

CUR_SCR

FONT_NAME

FONT_SIZE

FONT_ATTR

Data Types Description
Character/ Error code returned by
Byte
Shree-Lipi Soft to indicate
any error in the call
Character/ Non-zero value indicates
Byte
that Shree-Lipi Soft is
active and vice versa
Character/ This indicates the current
Byte
active script. The values
are to be interpreted as
provided in the Overview
section.
[Array
ofName of the default font
Byte/Char] orassociated with the current
string of sizescript
32.
Double
Point size of the default
Word/Long font associated with the
Integer
current script
Character/ The attributes of the
Byte
default font associated
with the current script
Values are 0 for Normal, 1
for Bold, 2 for Italic, 3 for
Bold Italic


FONT_LAYOUT
ACTIVATION_KEY

Character/
Byte
Character/
Byte

Font layout of the current
script.
The Activation key for
switching to Indian script.
The values are
145 : SCROLL LOCK
20 : CAPSLOCK

144 : NUMLOCK
HYPHENATION_ON Character/Byt Currently this facility is not
e
supported.
KEYBOARDNAME
[Array
ofFilename of the current
Byte/Char] orkeyboard layout for the
String of sizecurrent script.
12.


## Appendix B: Shree-Lipi Soft Network Trouble
Shooter
If you face any problem in using Shree-Lipi Soft over a network
then read the following carefully and follow the steps mentioned
in it. In the following documentation the word "Server" refers to
the computer where the Network Lock has been attached. It can
be a
genuine WinNT server or
a Node in a WinNT based LAN or
a Node in Peer-Peer Network or
Novell Netware Server.

What problems you can face using Shree-Lipi Soft on a
network?
The problems can be one of the following.
1.Shree-Lipi Soft is not getting activated at all in any of the
machines
2.Shree-Lipi Soft is getting activated at the server but not in any
of the nodes.
3.The Nethasp License manager is not getting evoked properly
4.Shree-Lipi Soft was working fine until another software was
installed, which also uses the Nethasp license manager.
5.Shree-Lipi Soft is accessible in only one DOMAIN and not in
another DOMAIN present in the same server.

The Solutions to the above problems are being listed one by
one.
Problem No 1:
This problem can occur because of any of the following.


1.You have not attached the lock to any of the machine that is
present in the Network.
2.The parallel port of the machine where you have attached the
lock is not functioning properly.
3.You have not installed the HASP driver in the machine where
you have fixed the lock. This is essential when you are
using network version of Shree-Lipi Soft. Until and unless
the HASP driver is installed Shree-Lipi Soft will not be
invoked even in the computer where the Lock has been
attached.
As a measure of Solution follow the Check-List given in the end
of the trouble shooter.
Problem No 2:
This problem occurs because of one of the following reasons.
1.You have installed the Nethasp license manager but you have
not invoked the actual license manager. If your Server is a
WinNT server then it is recommended that you install the
driver in the form of Service if possible. In any case it is
recommended to put the Shortcut to Nethasp license
Manager in the Startup of the Machine. In the case of
Novell Netware Server, it is recommended that you add the
Load haspServ statement in the Autoexec.ncf file
2.If you have run the Nethasp license manager and are still
unable to access Shree-Lipi Soft from the node, then check
the list of protocols that have been activated. If none of the
NetBEUI or TCP-IP or IPX protocol is loaded, you will not
be able to access Shree-Lipi Soft. A possible case is when
you have fixed the lock to a WinNT node in which no
supportive protocol has been configured. For configuring
any of the three protocols contact your network
administrator. It is recommended that for WinNT machine
you configure the TCP-IP and for Novell Netware you
configure the IPX/SPX protocol.


Problem No 3:
The only reason for this that you have two versions of the
Nethasp license manager installed on your machine. I.e the
Nethasp license manager is not compatible with the HASP
driver present in your machine. As an illustration, suppose you
installed Shree-Lipi Soft along with the HASP driver and the
Nethasp license manager. Later you installed another software
which is using the same Nethasp license manager. During the
later installation the older HASP driver is overwritten and hence
the license manager being invoked by Shree-Lipi Soft is not
compatible with the overwritten driver. Hence the Nethasp
license manager is not getting invoked.
Another reason may be incompatibility with the System DLLs of
the Windows operating system. This is possible if you upgrade
Windows OS.
In both the cases the solution is to reinstall the latest Nethasp
driver. For this run the program lmSetup.exe from the ShreeLipi Soft CD's HASP\INSTALL directory.
Problem No 4:
This problem is similar to the above problem. For this remove
the existing version of HASP driver and the Nethasp License
Manager and reinstall them again. Also while fixing the locks,
you must cascade them to the same Server. I.e Fix both the
locks one behind the another. While doing so remember to
attach the Shree-Lipi Soft lock to the Parallel port directly and fix
the other application's lock to the back of the Shree-Lipi Soft
lock.

Problem No 5:


The only reason for this is that computers present in one
DOMAIN are unable to access Computers in another DOMAIN.
To solve this problem ask your Network Administrator to make
the DOMAINS accessible.

Check List before running Shree-Lipi Soft on a
network
1.Make sure that the Parallel Port where the lock is attached is
functioning properly.
2.Make sure that the Lock is attached to the Parallel Port and
not to any other port.
3.Check whether any of the three protocols TCP-IP / IPX /
NetBEUI are supported. This you can view from the
Network Neighbourhood properties in a WinNT network and
in the network configuration in the Novell Netware server.
4.If you have multiple applications using the HASP protection
lock, make sure that all of them are connected to the Same
Server. Also Make sure that Shree-Lipi Soft lock is directly
attached to the Parallel port and the other locks are
connected to the back of the Shree-Lipi Soft lock
5.Check whether you have installed HASP driver and the
Nethasp License Manager on ONE and ONLY ONE
machine. This is essential. If you have installed them on
multiple machines then remove them and reinstall them on
only ONE Server.
If you are sure of the above points then Shree-Lipi Soft will work
properly on the Network and you will not face any problem.


