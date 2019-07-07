# Solar System Voyager (SSVG)

SSVG is simulation software that allows us to fly our own spacecrafts in the solar system.  Each spacecraft has three propulsion systems: a chemical propulsion engine, an electric propulsion engine, and a solar sail.  

Fly your own spacecrafts in the precisely simulated solar system.

Read more on the home page. <[http://whsk.sakura.ne.jp/ssvg/index-en.html](http://whsk.sakura.ne.jp/ssvg/index-en.html)>

### Required environment
* Python 3.7

### Packages and Modules
* Numpy v1.15.1
* Scipy v1.1.0
* matplotlib v2.2.3
* pyqt v5.9.2
* jplephem v2.8
* julian v0.14
* pytwobodyorbit v1.0.0
* spktype01 v1.0.0
* spktype21 v0.1.0

### Modification Log
#### v1.4.0 July 5, 2019
* Maneuver Description was implemented
* Import/export functions were implemented
* Edit Target command was improved
* User interface was improved
* Errors in words were corrected
* Problems in file access in Windows environments were fixed

#### v1.3.1 March 10, 2019
* A defect that terminates SSVG accidentally was fixed
* Display information elements were changed a little
* Menu items to open the SSVG User's Guide and the home page of SSVG were added

#### v1.3.0 February 21, 2019
* Internationalized (added user interface in Japanese, and became extensible)
* Improved user interface

#### v1.2.1 January 1, 2019
* Corresponded to pytwobodyorbit v1.0.0

#### v1.2.0 December 4, 2018
* Supported Type 21 SPK file
* Improved user interface
* Renewal of development environment

#### v1.1.0 August 18, 2018
* Improved user interface
* FTA function allows users to specify targeting point by B-plane coordinates
* Includes English version of document (SSVG_UsersGuide-en.pdf)

#### v1.0.0 April 2, 2018
* The first release
