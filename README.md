# autoslide-Aboda7m
A small script to automate Bodyslide mesh conversions from old Skyrim UNP to new BHUNP format.


# BodySlide Automation Script

This Python script automates the process of using BodySlide to convert NIF files from UNP to BHUNP format. It is designed to streamline the conversion process for multiple NIF files within a specified mesh directory.

## Prerequisites

- Python 3.x
- [pywinauto](https://pywinauto.readthedocs.io/en/latest/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

## Usage

Run `autoslide - Aboda7m.exe`. The tool will automatically search for all `.nif` meshes inside the `Data` folder and convert them. **Be cautious and ensure that only the meshes you want to convert are present.**
it will load a refernce unp to bhunp body and convert your meshes 

## Installation Steps

1. Extract the contents of the packaged app to an empty folder outside Skyrim. **It is crucial to avoid conflicts with your Skyrim installation.**

    Example structure:
    ```
    F:\Dev\ready to package apps\autoslide - Aboda7m\
    ├── Data
    │   ├── CalienteTools
    │   │   └── BodySlide
    │   └── meshes
    ├── Textures
    │   └── actors
    ├── _internal
    │   ├── Pythonwin
    │   ├── pywin32_system32
    │   └── win32
    ├── autoslide - Aboda7m.exe
    └── ...
    ```

2. Navigate to the `Data` folder inside the app and run BodySlide once to set up folder paths. Ensure that the paths are configured to the `Data` folder.

3. Install the mod you want to convert inside the `Data` folder. Unpack the mod contents, especially meshes, inside the `Data/meshes` directory.

4. Run `autoslide - Aboda7m.exe`. The tool will automatically search for all `.nif` meshes inside the `Data` folder and convert them. **Be cautious and ensure that only the meshes you want to convert are present.**

## Important Note

Always perform the conversion in a separate directory to prevent conflicts with your Skyrim installation.

**Happy modding!**
