# graph_girth

This project uses
https://graph-tool.skewed.de/

find install instructions here:
https://git.skewed.de/count0/graph-tool/wikis/installation-instructions#debian-ubuntu


# Windows 
If you are on windows you need:
 * ubuntu linux subsystem. 
 * X windows subsystem.

## ubuntu linux subsystem 
Simply open the Microsoft Store and search for Ubuntu, after install launch to setup. Now follow ubuntu instructions. (Use xenial for distribution)

## X
Install https://sourceforge.net/projects/vcxsrv/
Open VcXsrv

in bash enter the following commands:
```bash
echo "export DISPLAY=localhost:0.0" >> ~/.bashrc
. ~/.bashrc
```

Test with
```bash
sudo apt-get install x11-apps
xeyes

#For some reason you have to run these commands before graph-tools will work
export NO_AT_BRIDGE=1
sudo service dbus start
#found from here https://github.com/Microsoft/WSL/issues/2016 because I got this error
```

# Testing
```bash
git clone https://github.com/SeanMeyer/graph-theory-thickness/
bash #If you are in windows only, to get to the windows linux subsystem
python3 graph-theory-thickness
```