from kivy import platform
from pathlib import Path

def get_app_path(filename):
    if platform == 'android':
        from android.storage import app_storage_path
        base = Path(app_storage_path())
    else:
        base = Path.cwd()
        
    return str(base / filename)