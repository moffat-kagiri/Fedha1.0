[app]

# Application details
title = Fedha
package.name = fedha
package.domain = org.test
source.dir = .

# Supported file extensions
source.include_exts = py,png,jpg,kv,atlas

# Application version
version = 0.1

# Application requirements
requirements = python3,kivy,kivy-garden,pillow,android

# Screen orientation
orientation = portrait

# Fullscreen mode
fullscreen = 1

# Application icon (uncomment if available)
#icon.filename = %(source.dir)s/assets/images/icon.svg
icon.adaptive_foreground.filename = %(source.dir)s/assets/images/icon.svg
icon.adaptive_background.filename = %(source.dir)s/assets/images/icon.svg


# Android presplash screen (uncomment if available)
#android.presplash_color = #FFFFFF
#presplash.filename = %(source.dir)s/data/presplash.png

# Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Target Android API (latest stable recommended)
android.api = 33
android.minapi = 21
android.ndk_api = 21

# Enable AndroidX support (important for compatibility)
android.enable_androidx = True

# Storage option (default is private, False means external storage)
android.private_storage = True

# Whitelisted patterns (uncomment if needed)
# android.whitelist_src =

# Gradle dependencies (add any external libraries here)
# android.gradle_dependencies =

# Compile options (for compatibility with Java 8+ features)
android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# Packaging options (helps avoid common conflicts)
android.add_packaging_options = "exclude 'META-INF/common.kotlin_module'", "exclude 'META-INF/*.kotlin_module'"
