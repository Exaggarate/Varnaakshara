"""
Varnaakshara Font Installer
----------------------------
Installs bundled fonts to the user's Windows Fonts directory on first run.
Works silently — no admin required (installs per-user on Windows 10+).

Usage:
    from font_installer import install_fonts
    installed = install_fonts()  # Returns list of newly installed font names
"""

import os
import sys
import shutil
import ctypes
import platform
import logging

logger = logging.getLogger("varnaakshara.fonts")

# Windows API constants
WM_FONTCHANGE = 0x001D
HWND_BROADCAST = 0xFFFF

def get_bundled_fonts_dir():
    """Find the fonts directory bundled with the app."""
    # When running from PyInstaller bundle
    if getattr(sys, '_MEIPASS', None):
        fonts_dir = os.path.join(sys._MEIPASS, 'fonts')
        if os.path.isdir(fonts_dir):
            return fonts_dir
    
    # When running from source
    source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
    if os.path.isdir(source_dir):
        return source_dir
    
    return None


def get_user_fonts_dir():
    """Get the per-user fonts directory (no admin needed)."""
    if platform.system() == 'Windows':
        local_app = os.environ.get('LOCALAPPDATA', '')
        if local_app:
            return os.path.join(local_app, 'Microsoft', 'Windows', 'Fonts')
    elif platform.system() == 'Darwin':
        return os.path.expanduser('~/Library/Fonts')
    else:
        return os.path.expanduser('~/.local/share/fonts')
    return None


def get_installed_fonts_windows():
    """Get set of already-installed font filenames on Windows."""
    installed = set()
    
    # Check system fonts
    sys_fonts = os.path.join(os.environ.get('WINDIR', r'C:\Windows'), 'Fonts')
    if os.path.isdir(sys_fonts):
        installed.update(f.lower() for f in os.listdir(sys_fonts) if f.lower().endswith(('.ttf', '.otf')))
    
    # Check user fonts
    user_fonts = get_user_fonts_dir()
    if user_fonts and os.path.isdir(user_fonts):
        installed.update(f.lower() for f in os.listdir(user_fonts) if f.lower().endswith(('.ttf', '.otf')))
    
    return installed


def register_font_windows(font_path):
    """Register a font with Windows using AddFontResourceEx (per-session)."""
    try:
        gdi32 = ctypes.windll.gdi32
        # FR_PRIVATE = 0x10 (font visible only to this process)
        # Use 0 to make it visible to all processes
        result = gdi32.AddFontResourceExW(font_path, 0, 0)
        return result > 0
    except Exception as e:
        logger.debug(f"AddFontResourceEx failed for {font_path}: {e}")
        return False


def register_font_registry(font_name, font_filename):
    """Add font to Windows registry for persistence across reboots (per-user)."""
    try:
        import winreg
        reg_path = r"Software\Microsoft\Windows NT\CurrentVersion\Fonts"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
        user_fonts = get_user_fonts_dir()
        font_path = os.path.join(user_fonts, font_filename)
        winreg.SetValueEx(key, font_name + " (TrueType)", 0, winreg.REG_SZ, font_path)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        logger.debug(f"Registry write failed for {font_name}: {e}")
        return False


def get_font_name(font_path):
    """Extract the font's internal name from the TTF file."""
    try:
        # Try fonttools if available
        from fontTools.ttLib import TTFont
        font = TTFont(font_path)
        name_table = font['name']
        # Get font family name (nameID 1) or full name (nameID 4)
        for record in name_table.names:
            if record.nameID == 4 and record.platformID == 3:  # Windows full name
                return record.toUnicode()
        for record in name_table.names:
            if record.nameID == 1 and record.platformID == 3:  # Windows family name
                return record.toUnicode()
        font.close()
    except ImportError:
        pass
    except Exception as e:
        logger.debug(f"fonttools failed for {font_path}: {e}")
    
    # Fallback: use filename without extension
    return os.path.splitext(os.path.basename(font_path))[0]


def notify_font_change():
    """Notify all applications that fonts have changed."""
    if platform.system() == 'Windows':
        try:
            ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_FONTCHANGE, 0, 0)
        except Exception:
            pass


def install_fonts(force=False):
    """
    Install bundled fonts to the user's font directory.
    
    Args:
        force: If True, reinstall even if fonts already exist
    
    Returns:
        List of newly installed font names
    """
    fonts_dir = get_bundled_fonts_dir()
    if not fonts_dir:
        logger.info("No bundled fonts directory found")
        return []
    
    user_fonts = get_user_fonts_dir()
    if not user_fonts:
        logger.warning("Could not determine user fonts directory")
        return []
    
    # Create user fonts dir if needed
    os.makedirs(user_fonts, exist_ok=True)
    
    # Get already installed fonts
    installed = get_installed_fonts_windows() if platform.system() == 'Windows' else set()
    
    newly_installed = []
    
    # Walk through bundled fonts (including subdirectories like unicode/ and ansi/)
    for root, dirs, files in os.walk(fonts_dir):
        for filename in files:
            if not filename.lower().endswith(('.ttf', '.otf')):
                continue
            
            # Skip if already installed (unless forcing)
            if not force and filename.lower() in installed:
                logger.debug(f"Already installed: {filename}")
                continue
            
            src = os.path.join(root, filename)
            dst = os.path.join(user_fonts, filename)
            
            try:
                # Copy font file
                if not os.path.exists(dst) or force:
                    shutil.copy2(src, dst)
                    logger.info(f"Copied: {filename}")
                
                if platform.system() == 'Windows':
                    # Register with GDI for immediate use
                    register_font_windows(dst)
                    
                    # Register in registry for persistence
                    font_name = get_font_name(src)
                    register_font_registry(font_name, filename)
                
                newly_installed.append(filename)
                
            except Exception as e:
                logger.warning(f"Failed to install {filename}: {e}")
    
    # Notify apps about new fonts
    if newly_installed:
        notify_font_change()
        logger.info(f"Installed {len(newly_installed)} fonts")
    
    return newly_installed


def uninstall_fonts():
    """Remove all Varnaakshara-installed fonts."""
    fonts_dir = get_bundled_fonts_dir()
    if not fonts_dir:
        return []
    
    user_fonts = get_user_fonts_dir()
    if not user_fonts:
        return []
    
    removed = []
    
    for root, dirs, files in os.walk(fonts_dir):
        for filename in files:
            if not filename.lower().endswith(('.ttf', '.otf')):
                continue
            
            dst = os.path.join(user_fonts, filename)
            if os.path.exists(dst):
                try:
                    if platform.system() == 'Windows':
                        # Unregister from GDI
                        try:
                            ctypes.windll.gdi32.RemoveFontResourceExW(dst, 0, 0)
                        except:
                            pass
                        
                        # Remove from registry
                        try:
                            import winreg
                            reg_path = r"Software\Microsoft\Windows NT\CurrentVersion\Fonts"
                            font_name = get_font_name(os.path.join(root, filename))
                            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
                            winreg.DeleteValue(key, font_name + " (TrueType)")
                            winreg.CloseKey(key)
                        except:
                            pass
                    
                    os.remove(dst)
                    removed.append(filename)
                except Exception as e:
                    logger.warning(f"Failed to remove {filename}: {e}")
    
    if removed:
        notify_font_change()
    
    return removed


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    if '--uninstall' in sys.argv:
        removed = uninstall_fonts()
        print(f"Removed {len(removed)} fonts")
    else:
        installed = install_fonts(force='--force' in sys.argv)
        if installed:
            print(f"Installed {len(installed)} fonts:")
            for f in installed:
                print(f"  ✓ {f}")
        else:
            print("All fonts already installed")
