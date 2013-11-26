# Welcome

safep is a console program that allows to manage passwords via CLI.

Crypto-part: *AES, Blowfish*


# Use-case

Before using you may create an sh script to run safep.py.

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
* **rm** - delete item. 
* **ed** - edit item. 
* **chpass** - change password for db. 
* **pg** - generate random sequence
* **use** - change file password db
* **backup** - create backup of current db
* **backups** - display list of backups
* **restore** - restore default db from backup


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/miphreal/safep/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

