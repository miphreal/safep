# Welcome

safep - it's console program to manage passwords. Program has command line interface (CLI).

*Using: AES, Blowfish*


# Use-case

Before using you may create some script for running safep.py.

File: **safep**:
```bash
#!bash

#!/bin/sh
python /code/safep/code/safep.py $@

```

![](http://dl.dropbox.com/u/17976346/imgs/in_work.png)

* **ls** - search and display items. 
* **lsp** - search and display items with passwords.
* **mk** - add item.
* **rm** - delete items. 
* **ed** - edit item(s). 
* **chpass** - change password for db. 
* **pg** - generate random sequence
* **use** - change file password db
* **backup** - create backup of current db
* **backups** - display list of backups
* **restore** - restore default db from backup
