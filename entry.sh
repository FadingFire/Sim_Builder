# In cmd.exe
.venv/Scripts/activate.bat
# In PowerShell
.venv/Scripts/Activate.ps1
# In Mac/Linux
source .venv/Scripts/activate
export PYTHONDONTWRITEBYTECODE=1
flask --app src.main.flaskr.main run --debug