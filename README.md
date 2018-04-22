Description
============

Teardrop is a memory dwelling webchat running over Tor.
The server creates a temporary URL which can be accessed through Tor browser.
No information is stored on disk.

- Runs on Tor network.
- No JS, can be used with NoScript
- Nothing touches storage, everything happens in memory
- No configuration
- No need for a client
- Chats are deleted every 3 minutes
- Randomized usernames - decreasing chance of username reuse
- New service URL upon each server restart

Requirements
=======

flask, stem

Install
=======

Install Tor

Activate some virtual environment and install:

`apt-get install python-virtualenv`

`virtualenv sandboxme`

`source sandboxme/bin/activate`

`pip install git+https://github.com/etherwvlf/teardrop.git`


Usage
=====

Start Tor or Tor Browser, make Control Port open and listening on its default port.

`teardrop`

Share the service URL with clients to open in Tor Browser.

Bundle
=====

Create Windows bundle:

`pyinstaller -F --icon=raindrop.ico --upx-dir=../upx394w teardrop.py`

Create Linux bundle:

`pyinstaller -F --upx-dir=/upx394w teardrop.py`
