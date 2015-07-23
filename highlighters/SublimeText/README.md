WDL Syntax Highlighter for SublimeText and TextMate
===================================================

Building .tmLanguage file
-------------------------
This set of instructions assumes SublimeText running on a Mac

* Install SublimeText 2 or 3 (see http://www.sublimetext.com)
* Install Package Control (see https://packagecontrol.io/installation)
* Use Package Control to install `AAAPackageDev` (CMD+SHIFT+P | Package Control : Install Package)
* Open the `WDL.YAML-tmLanguage` file (File | Open...)
* Open the Command Palette (CMD+SHIFT+P)
* Select the "AAAPackageDev: Convert (YAML,JSON, Plist) to..." option
* This should write the `WDL.tmLanguage` file to the same directory as `WDL.YAML-tmLanguage`

Installation (SublimeText)
--------------------------
This set of instructions assumes SublimeText running on a Mac

* Create a directory `~/Library/Application Support/Sublime Text 3/Packages/WDL Syntax Highlighting`
  * For version 2, replace *Sublime Text 3* with *Sublime Text 2*
* Copy the `WDL.tmLanguage` file to this new directory
* Restart SublimeText, open a WDL file, enjoy!

Installation (TextMate)
--------------------------
* Drag the WDL.tmLanguage generated above onto the TextMate application.  
* This will convert it and leave you in the BundleEditor window, close the window.
* Open a WDL file, enjoy!
