# 🚀 s3_releases

**Simple S3 Build System · Native Builds · Cross-Compilation**

Ein schlankes Build-System für die **Simple Console Cam**, inklusive Toolchain-Verwaltung, Updates, Patches und Cross-Compilation zusätzlicher Software.

A lightweight build system for the **Simple Console Cam**, including toolchain management, updates, patches, and cross-compilation of additional software.

---

## 🌍 Languages / Sprachen

- 🇩🇪 [Deutsch](#-deutsch)
- 🇬🇧 [English](#-english)

---

# 🇩🇪 Deutsch

## 📖 Über das Projekt

`s3_releases` stellt die Werkzeuge und Skripte bereit, um die Entwicklungsumgebung für die Simple Console Cam einzurichten, zu aktualisieren und zu verwalten.

Neben dem nativen Build unterstützt das Projekt die Cross-Compilation weiterer Software. Unter `support/software` findest du Beispiele und Dokumentation, die zeigen, wie zusätzliche Programme in das Build-System integriert werden können.

### ✨ Features

- 🛠️ Einrichtung und Verwaltung der Build-Umgebung
- 🔄 Automatische Updates der Build-Skripte
- 📦 Verwaltung und Aktualisierung von Toolchains
- 🩹 Einbindung zusätzlicher Patches
- ⚙️ Native Builds
- 🔧 Cross-Compilation eigener Software
- 📚 Dokumentierte Beispiele für die Integration weiterer Programme

## 🚀 Installation & Setup

### 1. Repository klonen

```bash
git clone https://github.com/speedy005/speedy005-S3-Simplebuild
cd speedy005-S3-Simplebuild
```

### 2. Build-Umgebung vorbereiten

Führe die folgenden Befehle der Reihe nach aus:

```bash
./s3 checkout
./s3 native
./s3 update_me
./s3 repopatch
./s3 tcupdate --reset
./s3 menu
```

**Was machen die Befehle?**

| Befehl | Beschreibung |
|---|---|
| `./s3 checkout` | Repository bzw. benötigte Komponenten vorbereiten |
| `./s3 native` | Native Build-Umgebung einrichten |
| `./s3 update_me` | Build-System aktualisieren |
| `./s3 repopatch` | Patches aus dem Repository einbinden |
| `./s3 tcupdate --reset` | Toolchain aktualisieren bzw. zurücksetzen |
| `./s3 menu` | Konfigurationsmenü öffnen |

### 3. Patches hinzufügen

Zusätzliche Patches, beispielsweise der **OSCam-EMU-Patch**, können im Verzeichnis `support/patches` abgelegt werden.

Anschließend die Patch-Verarbeitung starten:

```bash
./s3 repopatch
```

### 4. Toolchain prüfen und aktualisieren

Ersetze `your_toolchainname` durch den Namen deiner gewünschten Toolchain.

Toolchain überprüfen:

```bash
./s3 tccheck your_toolchainname
```

Toolchain aktualisieren:

```bash
./s3 tcupdate your_toolchainname
```

> 💡 **Tipp:** Führe die Befehle in der angegebenen Reihenfolge aus und prüfe bei Problemen die verfügbaren Optionen des jeweiligen Skripts.

## 🔧 Eigene Software cross-kompilieren

Das Verzeichnis `support/software` ist der Einstiegspunkt, um weitere Software in das Build-System zu integrieren und für das gewünschte Zielsystem zu cross-kompilieren.

```text
support/
└── software/
    └── _vlmscd/
```

Das Beispiel **`_vlmscd`** dokumentiert, wie eine Software in das Build-System integriert und kompiliert werden kann.

Nutze dieses Beispiel als Vorlage für eigene Projekte und passe die Build-Konfiguration an die Anforderungen der jeweiligen Software an.

---

# 🇬🇧 English

## 📖 About the Project

`s3_releases` provides the tools and scripts needed to set up, update, and manage the development environment for the Simple Console Cam.

In addition to native builds, the project supports cross-compiling additional software. The `support/software` directory contains examples and documentation explaining how to integrate new programs into the build system.

### ✨ Features

- 🛠️ Build environment setup and management
- 🔄 Build script updates
- 📦 Toolchain management and updates
- 🩹 Integration of additional patches
- ⚙️ Native builds
- 🔧 Cross-compilation of custom software
- 📚 Documented examples for integrating additional programs

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/speedy005/speedy005-S3-Simplebuild
cd speedy005-S3-Simplebuild
```

### 2. Prepare the build environment

Run the following commands in order:

```bash
./s3 checkout
./s3 native
./s3 update_me
./s3 repopatch
./s3 tcupdate --reset
./s3 menu
```

**Command overview**

| Command | Description |
|---|---|
| `./s3 checkout` | Prepare the repository and required components |
| `./s3 native` | Set up the native build environment |
| `./s3 update_me` | Update the build system |
| `./s3 repopatch` | Apply or process repository patches |
| `./s3 tcupdate --reset` | Update or reset the toolchain |
| `./s3 menu` | Open the configuration menu |

### 3. Add patches

Additional patches, such as the **OSCam-EMU patch**, can be placed in `support/patches`.

Then run the patch processing command:

```bash
./s3 repopatch
```

### 4. Check and update the toolchain

Replace `your_toolchainname` with the name of your desired toolchain.

Check the toolchain:

```bash
./s3 tccheck your_toolchainname
```

Update the toolchain:

```bash
./s3 tcupdate your_toolchainname
```

> 💡 **Tip:** Execute the commands in the specified order and check each script's available options if you encounter any issues.

## 🔧 Cross-compile your own software

The `support/software` directory is the starting point for integrating additional software and cross-compiling it for the target system.

```text
support/
└── software/
    └── _vlmscd/
```

The **`_vlmscd`** example documents the required steps and build configuration for compiling software within this build system.

Use it as a template for your own projects and adapt the build configuration to the requirements of the software you want to compile.

---

## 📂 Project Structure

```text
s3_releases/
├── s3
└── support/
    ├── patches/       # Additional patches
    └── software/      # Software for cross-compilation
        └── _vlmscd/   # Example integration
```

*The structure above is a simplified overview; the actual repository layout may differ.*

## 🤝 Contributing

Suggestions, improvements, bug reports, and additional software integrations are welcome.

Feel free to open an issue or submit a pull request.

## 📜 License

Please refer to the repository for license information.

---

**Happy Building!** 🚀

*Build smart. Compile fast. Keep it simple.*
