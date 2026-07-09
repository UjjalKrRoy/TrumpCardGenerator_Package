Files to update:
1. config.json - default styles only.
2. src/config.py - your current version is fine.
3. src/renderer.py - your current version is fine.
4. src/text_engine.py - your current version is fine.
5. src/gui.py - replace with the version previously shared or extend it.
6. run.py - launcher.

Recommended new modules:
- src/settings.py
- src/preview.py
- src/widgets.py
- src/generator.py

#python -m PyInstaller run.py --onefile --windowed --icon icon.ico --name TrumpCardGenerator --add-data "config.json;." --add-data "icon.ico;." --add-data "dist\Updater.exe;." --hidden-import=requests --hidden-import=src.version --hidden-import=src.updater --hidden-import=src.gui --hidden-import=src.renderer --hidden-import=src.config --collect-all matplotlib --clean
#python -m PyInstaller updater_main.py --onefile --windowed --icon icon.ico --name Updater --clean