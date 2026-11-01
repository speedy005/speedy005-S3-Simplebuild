#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import sys
import shutil
import re
import html

EXPECTED_URL = "https://github.com/speedy005/oscam-git"

if len(sys.argv) < 3:
    sys.exit("Aufruf: script REPO_PFAD REPOSITORY_URL [set CAMNAME C_BUILD HTML_BUILD]")

repo = Path(sys.argv[1]).resolve()
url = sys.argv[2]

if url != EXPECTED_URL or repo.name != "oscam-git":
    sys.exit("Abbruch: Repository ist nicht das Speedy005-Repository.")

cfile = repo / "oscam.c"
htmlfile = repo / "webif/status/status.html"

if not cfile.is_file() or not htmlfile.is_file():
    sys.exit("Abbruch: OSCam-Dateien nicht vollständig gefunden.")

config_dir = Path(__file__).resolve().parent / "configs"
config_file = config_dir / "speedy005_branding.conf"

defaults = {
    "camname": "OSCam-Icam",
    "c_build": "by speedy005",
    "html_build": "- by speedy005",
}

def load_settings():
    settings = defaults.copy()
    if config_file.is_file():
        for line in config_file.read_text(encoding="utf-8").splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                if key in settings:
                    settings[key] = value
    return settings

def save_settings(settings):
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file.write_text(
        "".join(f"{key}={settings[key]}\n" for key in defaults),
        encoding="utf-8"
    )

settings = load_settings()

if len(sys.argv) > 3:
    if len(sys.argv) != 7 or sys.argv[3] != "set":
        sys.exit("Aufruf: script REPO URL set CAMNAME C_BUILD HTML_BUILD")

    settings = {
        "camname": sys.argv[4],
        "c_build": sys.argv[5],
        "html_build": sys.argv[6],
    }

    if any("\n" in value or "\r" in value for value in settings.values()):
        sys.exit("Abbruch: Zeilenumbrüche sind nicht erlaubt.")

    if any(ch in settings["camname"] + settings["c_build"] for ch in ('"', "\\")):
        sys.exit("Abbruch: Camname und C-Build dürfen keine Anführungszeichen oder Backslashes enthalten.")

c = cfile.read_text(encoding="utf-8")
h = htmlfile.read_text(encoding="utf-8")

new_c = c
new_h = h

# Gesamten OSCam-Info-Block erkennen und ersetzen.
info_pattern = re.compile(
    r'(?ms)^(?P<indent>[ \t]*)fprintf\(fp,\s*"Unix Starttime:.*?'
    r'^\s*if\s*\(osi\.system_ca_file\).*?^\s*#endif[ \t]*(?:\r?\n)?'
)

def replace_info_block(match):
    start_indent = match.group("indent")
    outer_match = re.search(
        r'(?m)^(?P<outer>[ \t]*)\}[ \t]*$',
        match.group(0)
    )
    if outer_match is None:
        raise ValueError("Äußere Block-Klammer nicht gefunden.")

    indent = start_indent[:-1]
    time_inner = start_indent + "\t"
    inner = indent + "\t"
    camname = settings["camname"].replace("%", "%%")
    c_build = settings["c_build"].replace("%", "%%")

    lines = [
        f'{start_indent}fprintf(fp, "Unix Starttime:       %ld\\n", walltime);',
        f'{start_indent}fprintf(fp, "Starttime:            %02d.%02d.%04d %02d:%02d:%02d\\n",',
        f'{time_inner}st.tm_mday, st.tm_mon + 1, st.tm_year + 1900,',
        f'{time_inner}st.tm_hour, st.tm_min, st.tm_sec);',
        f'{indent}}}',
        '',
        f'{indent}fprintf(fp, "Build Date:           am%s\\n", CS_BUILD_DATE);',
        f'{indent}fprintf(fp, "Version:              {camname} %s\\n",',
        f'{inner}CS_VERSION);',
        f'{indent}fprintf(fp, "S3 mit                -ggdb -pipe -ffunction-sections -fdata-sections -fomit-frame-pointer -fno-schedule-insns\\n");',
        f'{indent}fprintf(fp, "compiler_option       -O2   \\n");',
        f'{indent}fprintf(fp, "compress              nein   \\n");',
        f'{indent}fprintf(fp, "Toolchain             arm_7a  standart aus S3 \\n");',
        f'{indent}fprintf(fp, "Bibliothek            SSL_3.5.0\\n");',
        f'{indent}fprintf(fp, "Bibliothek            LIB_USBB_1.0.29\\n");',
        f'{indent}fprintf(fp, "Bibliothek            LIB_PCSC_2.3.3\\n");',
        f'{indent}fprintf(fp, "Bibliothek            LIB_Curl_8.14.1\\n");',
        f'{indent}fprintf(fp, "Bibliothek            CCID_1.6.2\\n");',
        f'{indent}fprintf(fp, "Bibliothek            LIB_ZLIB_1.3.1\\n");',
        f'{indent}fprintf(fp, "Bibliothek            libdvbcsa_1.1.0\\n");',
        f'{indent}fprintf(fp, "Patch                 \\n");',
        f'{indent}fprintf(fp, "Patch                \\n");',
        f'{indent}fprintf(fp, "Patch                \\n");',
        f'{indent}fprintf(fp, "Neon                    ja / 128 \\n");',
        f'{indent}fprintf(fp, "Compiler:                %s\\n", CS_TARGET);',
        f'{indent}fprintf(fp, "Box type:                %s (%s)\\n", boxtype_get(), boxname_get());',
        f'{indent}fprintf(fp, "PID:                     %d\\n", getppid());',
        '#ifdef USE_COMPRESS',
        f'{inner}fprintf(fp, "Compression:             %s, level %s\\n", COMP_VERSION, COMP_LEVEL);',
        '#endif',
        f'{indent}fprintf(fp, "TempDir:                           %s\\n", cs_tmpdir);',
        '#ifdef MODULE_GBOX',
        f'{indent}if(cfg.gbox_tmp_dir == NULL)',
        f'{indent}{{',
        f'{inner}fprintf(fp, "GBox tmp_dir:   not defined using: %s\\n", cs_tmpdir);',
        f'{indent}}}',
        f'{indent}else',
        f'{indent}{{',
        f'{inner}fprintf(fp, "GBox tmp_dir:        %s\\n", cfg.gbox_tmp_dir);',
        f'{indent}}}',
        '#endif',
        '',
        f'{indent}fprintf(fp, "ConfigDir:               %s\\n", cs_confdir);',
        '',
        '#ifdef WEBIF',
        f'{inner}fprintf(fp, "WebifPort:               %d\\n", cfg.http_port);',
        '#endif',
        '',
        '#ifdef WITH_SIGNING',
        f'{inner}fprintf(fp, "\\n");',
        f'{inner}fprintf(fp, "Signature:               %s\\n", (osi.is_verified ? "Valid - successfully verified using built-in Public Key" : "Invalid - wrong signature or internal error occured!"));',
        f'{inner}fprintf(fp, "  Signer:                %s\\n", config_ssl);',
        f'{inner}fprintf(fp, "  SHA256:                %s\\n", osi.hash_sha256 ? osi.hash_sha256 : "n/a");',
        f'{inner}fprintf(fp, "Certificate:             %s %s Certificate\\n", ((osi.cert_is_valid_self || osi.cert_is_valid_system) ? "Trusted" : "Untrusted"), (osi.cert_is_cacert ? "CA" : "self signed"));',
        f'{inner}fprintf(fp, "  Subject:               %s\\n", osi.cert_subject);',
        f'{inner}fprintf(fp, "  Issuer:                %s\\n", osi.cert_issuer);',
        f'{inner}fprintf(fp, "  Version:               %d\\n", osi.cert_version);',
        f'{inner}fprintf(fp, "  Serial:                %s\\n", osi.cert_serial);',
        f'{inner}fprintf(fp, "  Fingerprint:           %s\\n", osi.cert_fingerprint);',
        f'{inner}fprintf(fp, "  Valid from:            %s\\n", osi.cert_valid_from);',
        f'{inner}fprintf(fp, "  Valid to:              %s\\n", osi.cert_valid_to);',
        f'{inner}fprintf(fp, "  Status:                %s\\n", (osi.cert_is_expired ? "Expired" : "Valid"));',
        f'{inner}fprintf(fp, "  Type:                  %s\\n", osi.pkey_type);',
        f'{inner}if (osi.system_ca_file) fprintf(fp, "System CA:      %s\\n", osi.system_ca_file);',
        '#endif',
    ]
    return "\n".join(lines) + "\n"

matches = list(info_pattern.finditer(c))

if len(matches) != 1:
    sys.exit(
        f"Abbruch: OSCam-Info-Block nicht eindeutig gefunden "
        f"(Treffer: {len(matches)}). Keine Dateien geändert."
    )

new_c = info_pattern.sub(replace_info_block, c, count=1)
# Speedy005-Build-Anzeige direkt vor Commit einfügen oder aktualisieren.
marker_start = "<!-- SPEEDY005_BUILD_START -->"
marker_end = "<!-- SPEEDY005_BUILD_END -->"

escaped_html_build = html.escape(settings["html_build"], quote=False)

branding_block = (
    marker_start
    + "\n<LI CLASS=\"configmenu\"><B>- "
    + '<font style="color:#0048ff;">build</font> '
    + '<font style="color:#0048ff;">'
    + escaped_html_build
    + "</font></B></LI>\n"
    + marker_end
)

if marker_start in h or marker_end in h:
    if marker_start not in h or marker_end not in h:
        sys.exit("Abbruch: Speedy005-HTML-Marker unvollständig. Keine Dateien geändert.")

    marker_pattern = re.compile(
        re.escape(marker_start) + r".*?" + re.escape(marker_end),
        re.DOTALL
    )
    new_h, count_h = marker_pattern.subn(
        lambda m: branding_block,
        h,
        count=1
    )
else:
    commit_line = (
        '<LI CLASS="configmenu"><A HREF="##SCM_URL##/commit/##CS_GIT_COMMIT##" '
        'TARGET="_blank">Commit</A></LI>'
    )

    if h.count(commit_line) != 1:
        sys.exit("Abbruch: Commit-Eintrag in status.html nicht eindeutig gefunden. Keine Dateien geändert.")

    new_h = h.replace(
        commit_line,
        branding_block + "\n" + commit_line,
        1
    )
    count_h = 1

if count_h != 1:
    sys.exit("Abbruch: Speedy005-Build-Anzeige konnte nicht eindeutig aktualisiert werden.")

# Vorhandenen Build-Block unabhängig von seiner bisherigen Position vor Commit verschieben.
marker_pattern = re.compile(
    re.escape(marker_start) + r".*?" + re.escape(marker_end),
    re.DOTALL
)
new_h = marker_pattern.sub("", new_h, count=1)

commit_line = (
    '<LI CLASS="configmenu"><A HREF="##SCM_URL##/commit/##CS_GIT_COMMIT##" '
    'TARGET="_blank">Commit</A></LI>'
)

if new_h.count(commit_line) != 1:
    sys.exit("Abbruch: Commit-Eintrag in status.html nicht eindeutig gefunden. Keine Dateien geändert.")

new_h = new_h.replace(
    commit_line,
    branding_block + "\n" + commit_line,
    1
)

changed = []
if new_c != c:
    changed.append((cfile, new_c))
if new_h != h:
    changed.append((htmlfile, new_h))

if not changed:
    save_settings(settings)
    print("Metadaten entsprechen bereits den gespeicherten Einstellungen.")
    sys.exit(0)

backup_dir = Path(__file__).resolve().parent / "patch_backups"
backup_dir.mkdir(exist_ok=True)
stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

for file, content in changed:
    shutil.copy2(file, backup_dir / f"{file.name}.backup_{stamp}")
    file.write_text(content, encoding="utf-8")

save_settings(settings)

print("Speedy005-Metadaten erfolgreich übernommen.")
print(f"Camname: {settings['camname']}")
print(f"Build in oscam.c: {settings['c_build']}")
print(f"Build in status.html: {settings['html_build']}")
print(f"Sicherungen: {backup_dir}")
