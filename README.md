# What is this?
This is a simple Machine learning app detects the tone used by the user of 
the application on typed text using ibm api for AI and ML.
 This App also include a Tkinter GUI.
 ## Application capabilites
 * identifying the tone from the text
 * notifying the user with the tone detected from the text
  ## packages used
 * ``ibm-watson`` - ML pre-trainned models
 * ``tkinter`` - User Interface
 * ``pillow`` -images on the UI
 * ``json`` - formarting text on deburging
 * ``win10toast`` - for windows notification
 
## Installation of packages
### ``ibm-watson``
This package allows us to interact with ibm api to perform some `Matchine Learning Stuff` The installation is as
 follows:
 
``
$  pip install --upgrade "ibm-watson>=4.0.1"
``
### ``pillow``
This package allows us to use images in our tkinter app
``
$  python -m pip install pillow
``

## ``win10toast``
This package allows us to make notifications on windows 10 Computers.
``
$  python -m pip install win10toast
``
## Documentation Reference
For the reference of the docummentation of ibm visit [this link](https://cloud.ibm.com/apidocs/tone-analyzer?code=python)
## Why this simple App?
This application was just build for practising purposes.


