
studitemps_storage is a package with helper funtions for File IO. It only works
in a Django Context. By now it includes three modules:

- `path.py`: Contains Basic File IO Functions for general usage

- `storage`: Django File Storages that make use of functions in path.py

- `middleware`: Django Middlewares releated to the usage of the other packages

