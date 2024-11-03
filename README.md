# FileSync
Sync files between folders
To create an executable app from your FileSync.py script, you can use a tool like PyInstaller. Here are the steps:
1. Install PyInstaller: Open your terminal and run:
  pip install pyinstaller
2. Create the Executable: Navigate to the directory containing your FileSync.py file and run:
   pyinstaller --onefile FileSync.py
   This command will generate a single executable file. The --onefile option ensures that all dependencies are bundled into one executable.
3. Locate the Executable: After the process completes, you will find the executable in the dist directory inside your project folder.
4. Run the Executable: You can now distribute the executable file found in the dist directory. Users can run it without needing to install Python or any dependencies.
