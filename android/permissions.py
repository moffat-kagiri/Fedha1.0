from kivy.logger import Logger
from jnius import autoclass, cast
from jnius import JavaException

class AndroidPermissions:
    """Handles Android runtime permissions"""
    
    REQUIRED_PERMISSIONS = [
        'android.permission.READ_EXTERNAL_STORAGE',
        'android.permission.WRITE_EXTERNAL_STORAGE',
        'android.permission.INTERNET',
        'android.permission.ACCESS_NETWORK_STATE'
    ]
    
    def __init__(self):
        self.permissions_granted = False
    
    def check_permissions(self):
        """Check if all required permissions are granted"""
        try:
            Permission = autoclass('android.Manifest$permission')
            PackageManager = autoclass('android.content.pm.PackageManager')
            Context = autoclass('android.content.Context')
            activity = autoclass('org.kivy.android.PythonActivity').mActivity
            self.permissions_granted = all(
                activity.checkSelfPermission(perm) == PackageManager.PERMISSION_GRANTED
                for perm in self.REQUIRED_PERMISSIONS
            )
            return self.permissions_granted
        except JavaException as e:
            Logger.error(f"JavaException: {e}")
            return False
        except Exception as e:
            Logger.error(f"Exception: {e}")
            return False
    
    def request_permissions(self, callback=None):
        """
        Request required permissions
        Args:
            callback (callable): Function to call after permissions are granted
        """
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            ActivityCompat = autoclass('androidx.core.app.ActivityCompat')

            def on_permissions_result(request_code, permissions, grant_results):
                if all(grant_results):
                    Logger.info("Permissions: All permissions granted")
                    self.permissions_granted = True
                    if callback:
                        callback()
                else:
                    Logger.error("Permissions: Some permissions were denied")
                    self.permissions_granted = False
            
            ActivityCompat.requestPermissions(
                PythonActivity.mActivity,
                self.REQUIRED_PERMISSIONS,
                0
            )
        except JavaException as e:
            Logger.error(f"JavaException: {e}")
        except Exception as e:
            Logger.error(f"Exception: {e}")
    
    def ensure_permissions(self, callback=None):
        """
        Ensure all permissions are granted
        Args:
            callback (callable): Function to call after permissions are granted
        """
        if not self.check_permissions():
            Logger.info("Permissions: Requesting missing permissions")
            self.request_permissions(callback)
        elif callback:
            callback()

def request_android_permissions():
    try:
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        ActivityCompat = autoclass('androidx.core.app.ActivityCompat')
        permissions = [
            'android.permission.READ_EXTERNAL_STORAGE',
            'android.permission.WRITE_EXTERNAL_STORAGE',
            'android.permission.INTERNET'
        ]
        ActivityCompat.requestPermissions(
            PythonActivity.mActivity,
            permissions,
            0
        )
    except JavaException as e:
        Logger.error(f"JavaException: {e}")
    except Exception as e:
        Logger.error(f"Exception: {e}")

def check_android_permission(permission):
    try:
        PackageManager = autoclass('android.content.pm.PackageManager')
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        return activity.checkSelfPermission(permission) == PackageManager.PERMISSION_GRANTED
    except JavaException as e:
        Logger.error(f"JavaException: {e}")
        return False
    except Exception as e:
        Logger.error(f"Exception: {e}")
        return False