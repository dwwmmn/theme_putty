# theme_putty

Short script to set a theme for PuTTY profiles. I do this pretty often, either
just for aesthetic reasons (I want it to match my editor) or for practical
reasons (it's an easy way to tell the difference between two servers). 

PuTTY settings are all stored in the registry, so PuTTY themes are just `.reg`
files. However the `.reg`file must know where to put these colors, so the only
option is if you want to switch themes is editing the file for every session you
want to apply the theme to, or storing (number of themes x number of sessions)
registry files, neither of which is a great option. IMHO this is something
that's ridiculously hard to do and should be easier and anyone who uses PuTTY
should be able to appreciate this script.

Usage:

```
PS C:\> python .\theme_putty.py -h
usage: theme_putty.py [-h] [-b] theme [profiles [profiles ...]]

positional arguments:
  theme            File to read colors from OR session to read from.
  profiles         Profiles to change; by default an empty list means 'all
                   profiles'.

optional arguments:
  -h, --help       show this help message and exit
  -b, --blacklist  Make the passed list of profiles a blacklist.
```
