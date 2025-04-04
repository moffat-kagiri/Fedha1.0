from kivy.logger import Logger
import os
import csv
from datetime import datetime
from threading import Thread

# Kivy imports
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen

# KivyMD imports
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

# App imports
from ui.screens import HomeScreen, LoansScreen, InputScreen, SummariesScreen
from ui.screens.budget import BudgetScreen
from android.permissions import AndroidPermissions, request_android_permissions, check_android_permission
from android.storage import get_app_path
from core.storage import DataManager, CSVManager, get_storage_path
from core.services.gdrive_service import GoogleDriveService
from core.errors import StorageError
from core.finance import LoanCalculator, FinanceError, CalculationError, ValidationError

class TrackerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = DataManager(get_storage_path=get_app_path)
        self.permissions = AndroidPermissions()
        self.gdrive_service = None  # Initialize Google Drive service
        self.screen_manager = ScreenManager()  # Initialize screen manager

    def build(self):
        Logger.info("App: Building the application")
        Builder.load_file("ui/widgets/cards.kv")
        Builder.load_file("ui/widgets/inputs.kv")
        
        # Set theme properties first
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Green"
        self.theme_cls.theme_style = "Dark"

        # Create a BoxLayout as root
        root = BoxLayout(orientation='vertical')
        
        # Create and add Toolbar if needed
        # self.toolbar = MDToolbar(...)
        # root.add_widget(self.toolbar)
        
        # Create the screen manager
        self.screen_manager = ScreenManager()
        
        # Create screens
        screens = {
            'home': HomeScreen,
            'loans': LoansScreen,
            'input': InputScreen,
            'summaries': SummariesScreen
        }
        
        for name, screen_class in screens.items():
            screen = screen_class(name=name)
            self.screen_manager.add_widget(screen)
        
        # Add screen manager to root
        root.add_widget(self.screen_manager)
        
        # Create navigation bar using MDBoxLayout instead of BoxLayout
        self.nav_bar = MDBoxLayout(
            size_hint_y=None,
            height=dp(56),
            spacing=dp(10),
            padding=dp(10),
            md_bg_color=[0.204, 0.373, 0.384, 1]  # #345f62
        )
        
        # Create navigation buttons with consistent styling
        nav_items = [
            {'icon': 'home', 'text': 'Home', 'screen': 'home'},
            {'icon': 'cash', 'text': 'Loans', 'screen': 'loans'},
            {'icon': 'plus', 'text': 'Input', 'screen': 'input'},
            {'icon': 'chart-bar', 'text': 'Summary', 'screen': 'summaries'}
        ]
        
        for item in nav_items:
            btn = MDRaisedButton(
                text=item['text'],
                icon=item['icon'],
                md_bg_color=[0.153, 0.278, 0.288, 1],  # Slightly darker than nav bar
                on_release=lambda x, s=item['screen']: self.switch_screen(s)
            )
            self.nav_bar.add_widget(btn)
        
        # Add navigation bar to root
        root.add_widget(self.nav_bar)
        
        # Set initial screen
        self.screen_manager.current = 'home'
        
        # Ensure permissions before initializing the app
        self.permissions.ensure_permissions(self.initialize_app)
        
        return root

    def initialize_app(self):
        """Called after permissions are granted"""
        Logger.info("App: Initializing after permissions granted")
        Logger.info("App: Initializing Google Drive service")
        # Initialize Google Drive service
        self.gdrive_service = GoogleDriveService(
            credentials_path=get_app_path("gdrive_creds.json"),
            get_storage_path=get_storage_path
        )
        # Initialize your app components here

    def register_screens(self):
        Logger.info("App: Registering screens")
        self.screen_manager.add_widget(HomeScreen(name='home'))
        self.screen_manager.add_widget(LoansScreen(name='loans'))
        self.screen_manager.add_widget(SummariesScreen(name='summaries'))
        self.screen_manager.add_widget(InputScreen(name='input'))

    def save_data(self, data):
        if not check_android_permission('android.permission.WRITE_EXTERNAL_STORAGE'):
            self.show_warning_dialog(
                title="Permissions Required",
                message="Storage access is required to save data."
            )
            return False
        
        # Save data to storage
        Logger.info("App: Saving data to storage")
        return True

    def sync_with_drive(self):
        if not check_android_permission('android.permission.INTERNET'):
            self.show_warning_dialog(
                title="Permissions Required",
                message="Internet access is required for Google Drive sync."
            )
            return False
        
        # Perform Google Drive sync
        Logger.info("App: Syncing with Google Drive")
        
        def _sync():
            try:
                if not self.gdrive_service:
                    raise Exception("Google Drive service is not initialized")
                
                files = {
                    "expenses.csv": "DRIVE_FOLDER_ID_1",
                    "loans.csv": "DRIVE_FOLDER_ID_2"
                }
                
                for fname, folder_id in files.items():
                    self.gdrive_service.sync_to_drive(fname, folder_id)
                    
                self.show_toast("Sync completed successfully")
            except Exception as e:
                self.show_error(f"Sync failed: {str(e)}")
        
        Thread(target=_sync).start()
        return True

    def show_warning_dialog(self, title, message):
        """Show a warning dialog to the user"""
        dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def show_toast(self, message):
        self.root.current_screen.ids.snackbar.show(message)

    def show_error(self, message):
        MDDialog(
            title="Error",
            text=message,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.dismiss())]
        ).open()

    def validate_monetary_input(self, value):
        try:
            # Convert the input to a float
            value = float(value)
            # Round to 2 decimal places
            value = round(value, 2)
            return value
        except ValueError:
            # Handle the case where the input is not a valid number
            return None

    def switch_screen(self, screen_name):
        """Switch to the specified screen"""
        self.screen_manager.current = screen_name

if __name__ == '__main__':
    TrackerApp().run()