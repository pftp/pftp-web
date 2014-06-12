The main site for the Programming: Feel the Power DeCal.

## Setup
You will need
 * Python 2.7
 * setuptools
 * Pip
 * Node.js

Install Python dependencies with
```bash
pip install -r requirements.txt
```
and Node.js dependencies
```bash
npm install reflect
npm install ast-traverse
```

## Building
```bash
fab build
```

## Running
```bash
fab
```
git submodule init
git submodule update


To Deploy to Website:
cd pftp; fab build; cd ..; chown -R www-data:www-data pftp
