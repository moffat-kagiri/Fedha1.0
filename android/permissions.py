# android/permissions.py
from android.permissions import Permission, request_permissions, check_permission
from kivy.logger import Logger

class AndroidPermissions:
    """Handles Android runtime permissions"""
    
    REQUIRED_PERMISSIONS = [
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.INTERNET,
        Permission.ACCESS_NETWORK_STATE
    ]
    
    def __init__(self):
        self.permissions_granted = False
    
    def check_permissions(self):
        """Check if all required permissions are granted"""
        self.permissions_granted = all(
            check_permission(perm) for perm in self.REQUIRED_PERMISSIONS
        )
        return self.permissions_granted
    
    def request_permissions(self, callback=None):
        """
        Request required permissions
        Args:
            callback (callable): Function to call after permissions are granted
        """
        def on_permissions_result(permissions, grant_results):
            if all(grant_results):
                Logger.info("Permissions: All permissions granted")
                self.permissions_granted = True
                if callback:
                    callback()
            else:
                Logger.error("Permissions: Some permissions were denied")
                self.permissions_granted = False
        
        request_permissions(self.REQUIRED_PERMISSIONS, on_permissions_result)
    
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