"""
Varnaakshara Auto-Updater
Checks GitHub releases for newer versions, downloads installer, runs it.
"""

import os
import sys
import json
import tempfile
import threading
import urllib.request
import urllib.error
import ssl

# Current version — MUST match the version in varnaakshara_ime.py
CURRENT_VERSION = "1.3.0"

# GitHub release API
GITHUB_REPO = "Exaggarate/Varnaakshara"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
USER_AGENT = f"Varnaakshara/{CURRENT_VERSION}"

# Installer filename pattern
INSTALLER_PREFIX = "Varnaakshara_Setup_v"


def _parse_version(v):
    """Parse version string like '1.0.0' into tuple (1, 0, 0)."""
    v = v.strip().lstrip('v')
    parts = []
    for p in v.split('.'):
        try:
            parts.append(int(p))
        except ValueError:
            parts.append(0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])


# Path for post-update marker file
UPDATE_MARKER = os.path.join(tempfile.gettempdir(), 'varnaakshara_updated.txt')


def check_post_update():
    """Check if app was just updated. Returns (version, notes) or (None, None)."""
    try:
        if os.path.isfile(UPDATE_MARKER):
            with open(UPDATE_MARKER, 'r', encoding='utf-8') as f:
                lines = f.read().strip().split('\n', 1)
            os.remove(UPDATE_MARKER)
            version = lines[0].strip() if lines else None
            notes = lines[1].strip() if len(lines) > 1 else None
            return version, notes
    except Exception:
        pass
    return None, None


def check_for_update(callback=None):
    """Check GitHub for a newer release. Runs in background thread.
    
    callback(has_update, version, download_url, release_notes, error) is called on completion.
    - has_update: True if newer version available
    - version: remote version string (e.g. '1.1.0')
    - download_url: direct download URL for the installer
    - release_notes: short summary from release body (first 200 chars)
    - error: error string if check failed, None otherwise
    """
    def _check():
        try:
            ctx = ssl.create_default_context()
            req = urllib.request.Request(GITHUB_API, headers={
                'User-Agent': USER_AGENT,
                'Accept': 'application/vnd.github.v3+json',
            })
            resp = urllib.request.urlopen(req, timeout=15, context=ctx)
            data = json.loads(resp.read().decode('utf-8'))
            
            remote_tag = data.get('tag_name', '')
            remote_ver = _parse_version(remote_tag)
            current_ver = _parse_version(CURRENT_VERSION)
            
            if remote_ver <= current_ver:
                if callback:
                    callback(False, remote_tag, None, None, None)
                return
            
            # Find installer asset
            download_url = None
            for asset in data.get('assets', []):
                name = asset.get('name', '')
                if name.startswith(INSTALLER_PREFIX) and name.endswith('.exe'):
                    download_url = asset.get('browser_download_url')
                    break
            
            if not download_url:
                if callback:
                    callback(False, remote_tag, None, None, "No installer found in release")
                return
            
            # Extract short release notes from body
            body = data.get('body', '') or ''
            # Strip markdown headers and clean up
            notes_lines = []
            for line in body.split('\n'):
                line = line.strip()
                if line.startswith('#'):
                    continue  # skip headers
                if line.startswith('- '):
                    # Strip bold markdown
                    clean = line[2:].replace('**', '')
                    notes_lines.append(clean)
            release_notes = '\n'.join(notes_lines[:5])  # max 5 bullet points
            if not release_notes:
                release_notes = data.get('name', f'v{remote_tag}')
            
            if callback:
                callback(True, remote_tag.lstrip('v'), download_url, release_notes, None)
                
        except Exception as e:
            if callback:
                callback(False, None, None, None, str(e))
    
    t = threading.Thread(target=_check, daemon=True)
    t.start()
    return t


def download_and_install(download_url, progress_callback=None, version=None, notes=None):
    """Download installer and run it. Runs in background thread.
    
    progress_callback(percent, status) is called with progress updates.
    - percent: 0-100 (or -1 for indeterminate)
    - status: string describing current step
    """
    def _download():
        try:
            if progress_callback:
                progress_callback(0, "Downloading update...")
            
            ctx = ssl.create_default_context()
            req = urllib.request.Request(download_url, headers={
                'User-Agent': USER_AGENT,
            })
            resp = urllib.request.urlopen(req, timeout=120, context=ctx)
            
            total = int(resp.headers.get('Content-Length', 0))
            
            # Download to temp file
            tmp_dir = tempfile.gettempdir()
            # Extract filename from URL
            fname = download_url.split('/')[-1]
            tmp_path = os.path.join(tmp_dir, fname)
            
            downloaded = 0
            chunk_size = 65536  # 64KB chunks
            
            with open(tmp_path, 'wb') as f:
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total > 0 and progress_callback:
                        pct = int(downloaded * 100 / total)
                        progress_callback(pct, f"Downloading... {downloaded // 1048576}MB / {total // 1048576}MB")
            
            if progress_callback:
                progress_callback(100, "Download complete. Launching installer...")
            
            # Save update marker for post-update notification
            try:
                marker_content = str(version or '')
                if notes:
                    marker_content += '\n' + str(notes)
                with open(UPDATE_MARKER, 'w', encoding='utf-8') as mf:
                    mf.write(marker_content)
            except Exception:
                pass
            
            # Launch the installer silently
            # /VERYSILENT = no UI at all
            # /CLOSEAPPLICATIONS = close running Varnaakshara
            # /NORESTART = don't restart Windows
            import subprocess
            
            # Determine the install path for relaunch
            install_dir = os.path.dirname(os.path.abspath(sys.argv[0])) if getattr(sys, 'frozen', False) else None
            exe_name = 'Varnaakshara.exe'
            
            # Write a small restart batch script that:
            # 1. Waits for installer to finish
            # 2. Launches the updated app
            # 3. Deletes itself
            restart_bat = os.path.join(tmp_dir, 'varnaakshara_restart.bat')
            # Find the exe path — either from current running location or default
            if install_dir and os.path.isfile(os.path.join(install_dir, exe_name)):
                exe_path = os.path.join(install_dir, exe_name)
            else:
                # Default install path
                exe_path = os.path.join(
                    os.environ.get('LOCALAPPDATA', ''),
                    'Programs', 'Varnaakshara', exe_name
                )
            
            # Pass /DIR= so installer updates the CURRENT install location
            dir_flag = f' /DIR="{install_dir}"' if install_dir else ''
            bat_content = f'''@echo off
"{tmp_path}" /VERYSILENT /CLOSEAPPLICATIONS /NORESTART /SUPPRESSMSGBOXES{dir_flag}
timeout /t 2 /nobreak >nul
start "" "{exe_path}"
del "%~f0"
'''
            with open(restart_bat, 'w') as bf:
                bf.write(bat_content)
            
            if progress_callback:
                progress_callback(100, "Installing update...")
            
            # Launch the batch script hidden (no visible cmd window)
            subprocess.Popen(
                ['cmd', '/c', restart_bat],
                shell=False,
                creationflags=0x08000000,  # CREATE_NO_WINDOW
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            
            # Give batch a moment to start, then exit current app
            import time
            time.sleep(1)
            os._exit(0)
            
        except Exception as e:
            if progress_callback:
                progress_callback(-1, f"Update failed: {e}")
    
    t = threading.Thread(target=_download, daemon=True)
    t.start()
    return t


if __name__ == '__main__':
    # CLI test
    import time
    
    def on_check(has_update, version, url, error):
        if error:
            print(f"Error: {error}")
        elif has_update:
            print(f"Update available: v{version}")
            print(f"Download: {url}")
        else:
            print(f"Up to date (remote: {version})")
    
    print(f"Current version: {CURRENT_VERSION}")
    print("Checking for updates...")
    t = check_for_update(on_check)
    t.join(timeout=20)
