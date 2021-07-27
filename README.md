# Solar System Voyager (SSVG)

SSVG is simulation software that allows us to fly our own spacecrafts in the solar system.  Each spacecraft has three propulsion systems: a chemical propulsion engine, an electric propulsion engine, and a solar sail.  

Fly your own spacecrafts in the precisely simulated solar system.

Read more on the home page. <[http://whsk.sakura.ne.jp/ssvg/index-en.html](http://whsk.sakura.ne.jp/ssvg/index-en.html)>

### Required environment
* Python 3.8

### Packages and Modules
* Numpy v1.20.1
* Scipy v1.6.2
* matplotlib v3.2.2
* PyQt5 (QT_VERSION_STR=5.9.6, PYQT_VERSION_STR=5.9.2, SIP_VERSION_STR=4.19.8)
* jplephem v2.16
* julian v0.14
* pytwobodyorbit v1.0.0
* spktype01 v1.0.0
* spktype21 v0.1.0

### Modification Log
#### v1.5.0 July 27, 2021
* The development environment became to Anaconda3-2021.06
* To use the latest planetary ephemeris of NASA/JPL
* To use parallel projection to draw figures on the 3D Orbit window

#### v1.4.1 September 30, 2019
* The development environment was renewed to Anaconda3-2019.07
* The font settings of GUI was improved
* A statement to use "Qt5Agg" backend for Matplotlib was added

#### v1.4.0 July 5, 2019
* Maneuver Description was implemented
* Import/export functions were implemented
* Edit Target command was improved
* The user interface was improved
* Errors in words were corrected
* Problems in file access in Windows environments were fixed

#### v1.3.1 March 10, 2019
* A defect that terminates SSVG accidentally was fixed
* Menu items to open the SSVG User's Guide and the home page of SSVG were added

#### v1.3.0 February 21, 2019
* SSVG was internationalized (we added user interface in Japanese with an extensible manner)
* The user interface was improved

#### v1.2.1 January 1, 2019
* SSVG corresponded to pytwobodyorbit v1.0.0

#### v1.2.0 December 4, 2018
* SSVG became to support Type 21 SPK file
* The user interface was improved

#### v1.1.0 August 18, 2018
* The user interface was improved
* The B-plane coordinates was introduced

#### v1.0.0 April 2, 2018
* The first release
