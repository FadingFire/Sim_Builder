pip install virtualenv
virtualenv .venv
python3.11 -m venv .venv
# In cmd.exe
venv\Scripts\activate.bat
# In PowerShell
venv\Scripts\Activate.ps1
# In Mac/Linux
source .venv/bin/activate
pip install --upgrade pip
pip install Flask
pip install numpy
pip install bluesky-simulator[full]