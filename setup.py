from cx_Freeze import setup, Executable, sys
includefiles=['ico.ico']
excludes=[]
packages=[]
base=None
if sys.platform=="win32":
    base="Win32GUI"

shortcut_table=[
    ("DesktopShortcut",
     "DesktopFolder",
     "Vessels Management System",
     "TARGETDIR",
     "[TARGETDIR]\system.exe",
     None,
     None,
     None,
     None,
     None,
     None,
     "TARGETDIR",
     )
]
msi_data={"Shortcut":shortcut_table}

bdist_msi_options={'data':msi_data}
setup(
    version="0.1",
    description="Vessels Management System",
    author="Hicham Garoum",
    name="Operations Management System",
    options={'build_exe':{'include_files':includefiles},'bdist_msi':bdist_msi_options,},
    executables=[
        Executable(
            script="system.py",
            base=base,
            icon='ico2.ico',
        )
    ]
)