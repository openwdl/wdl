WDL Syntax Highlighter for [SublimeText][1] and TextMate
===================================================

Installation ([SublimeText][1])
--------------------------
This set of instructions assumes [SublimeText][1] running on a Mac

* Create a directory `~/Library/Application Support/Sublime Text 3/Packages/WDL Syntax Highlighting`
  * For version 2, replace *Sublime Text 3* with *Sublime Text 2*
* Copy the `WDL.tmLanguage` file to this new directory
* Restart [SublimeText][1], open a WDL file, enjoy!

Installation ([TextMate][2])
--------------------------
* Drag the `WDL.tmLanguage` generated above onto the [TextMate][2] application.
* This will convert it and leave you in the BundleEditor window, close the window.
* Open a WDL file, enjoy!

Building .tmLanguage file
-------------------------
This repository has the `WDL.tmLanguage` file that you can use in the installation section to start using the syntax highlighter immediately.  However, if you care to make changes to the current tmLanguage file, you will need to edit `WDL.YAML-tmLanguage` and then use [SublimeText][1] to recompile the `WDL.tmLanguage` file.  To do this, you can use the following set of instructions (assumes [SublimeText][1] running on a Mac):

* Install [SublimeText][1] 2 or 3
* Install the [Package Control][3] package
* Use [Package Control][3] to install `PackageDev` (CMD+SHIFT+P | Package Control : Install Package)
* Open the `WDL.YAML-tmLanguage` file (File | Open...)
* Open the Command Palette (CMD+SHIFT+P)
* Select the "PackageDev: Convert (YAML,JSON, Plist) to..." option
* This should write the `WDL.tmLanguage` file to the same directory as `WDL.YAML-tmLanguage`

[1]: http://www.sublimetext.com/ "SublimeText"
[2]: https://macromates.com/ "TextMate"
[3]: https://packagecontrol.io/ "Package Control"
