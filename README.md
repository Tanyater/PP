# PP
# System requirements

According to my variant the project uses
- Python 3.8.0
- venv as a virtual environment manager + re

# Project setup

1. Install python 3.8.0 
1.1 On Windows...
 ```
   pyenv install -l
 ```
    pyenv install 3.8.0
   
2. Create virtual environment 
    ```
   python -m venv venv
   ```
3. Then activate it
   ```
   venv\Scripts\activate.ps1
   ```
   In order to check which pythin version you are using 
   ```
   python --version
   ```
4. Install necessary modules by running 
   ```
   pip install -r requirements.txt
   ```
    pip freeze > requirement.txt