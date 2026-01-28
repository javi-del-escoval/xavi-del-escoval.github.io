#define version "0.1.6"

[Setup]
AppName=Web Scraper {#version}
AppVersion={#version}
DefaultDirName={userdocs}\Web Scraper {#version}
DisableDirPage=no
Uninstallable=yes
OutputDir=web-scraper-ecit\Installers
OutputBaseFilename=WebScraper_{#version}_Installer
AppPublisher=Xavier Del Escoval
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Files]
Source: "dist\Web Scraper\*"; DestDir: "{app}\"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{userdesktop}\Web Scraper"; Filename: "{app}\Web Scraper.exe"
