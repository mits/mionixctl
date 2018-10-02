mionixctl
--

**mionixctl** is an unofficial configuration tool for the Mionix Avior 7000 Mouse under linux.
It is based on [**RivalCTL**](https://github.com/nixi-awoo/rivalctl) and [**SenseiCTL**](https://github.com/dneto/senseictl).
As the projects it's based on, the configuration protocol had to be reverse-engineered
from packets captured from use of the official Windows configuration utility.
It is therefore incomplete, and might contain errors which might misconfigure your mouse, cause it to explode,
wipe your hard driver and set your pc on fire. Use at your own risk.
Currently, only the Avior 7000 mouse is supported but hopefully support for additional models 
The functions supported are profile upload to mouse, and activation of a specific profile.
The profile features currently supported are
 - polling rate
 - button function
 - led (scrollwheel / logo) color and effect



Installation
--

Requirements:

    Required:
    pyudev>=0.16
    ioctl-opt>=1.2
    PyYAML==3.11

    Write permission to the device is required as well

Manual Installation:

    git clone https://github.com/dneto/senseictl.git
    sudo python setup.py install

 
Usage
--

    usage: mionixctl [-h] {upload,create_default,activate,find_device} ...
    
    Mionix Avior 7000 configuration utility
    
    positional arguments:
      {upload,create_default,activate,find_device}
                            commands
        upload              upload a profile to the mouse
        create_default      Create a default profile and write it to a file
        activate            activate a profile
        find_device         find and print the hidraw device
    
Profiles
--

As far as I've seen, 