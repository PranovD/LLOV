# LLOV

Check Python3 installation
    
    python -v

Check pip3 installation
    
    pip -V

Create virtual env
    
    python3 -m venv venv
    source venv/bin/activate

Install package dependencies
    
    pip install --upgrade pip
    pip install -r requirements.txt

export flask app var in root directory of project
    
    export FLASK_APP=run.py

run application
    
    python run.py


Common Plaid Errors

    NameError: name 'plaid' is not defined
    AttributeError: module 'plaid' has no attribute 'Client'

Possible solutions
    
    Download the newest keys.py from Google Drive
    There are two packages that python gets confused with each other: plaid & plaid-python
        We want plaid-python. So make sure you don't have plaid (pip show plaid), but if
        you do have it make sure to uninstall it (pip uninstall plaid) and then rerun
        pip install plaid-python

