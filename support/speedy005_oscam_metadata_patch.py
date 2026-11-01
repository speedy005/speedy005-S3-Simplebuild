#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import sys
import shutil

EXPECTED_URL = "https://github.com/speedy005/oscam-git"

if len(sys.argv) != 3:
    sys.exit("Aufruf: script REPO_PFAD REPOSITORY_URL")

repo = Path(sys.argv[1]).resolve()
url = sys.argv[2]

if url != EXPECTED_URL or repo.name != "oscam-git":
    sys.exit("Abbruch: Repository ist nicht das Speedy005-Repository.")

cfile = repo / "oscam.c"
htmlfile = repo / "webif/status/status.html"

if not cfile.is_file() or not htmlfile.is_file():
    sys.exit("Abbruch: OSCam-Dateien nicht vollständig gefunden.")

c = cfile.read_text()
h = htmlfile.read_text()

new_c = r'''                fprintf(fp, "Unix Starttime:       %ld\n", walltime);
                fprintf(fp, "Starttime:            %02d.%02d.%04d %02d:%02d:%02d\n",
                                st.tm_mday, st.tm_mon + 1, st.tm_year + 1900,
                                st.tm_hour, st.tm_min, st.tm_sec);
        }

        fprintf(fp, "Build Date:           am%s\n", CS_BUILD_DATE);
        fprintf(fp, "Version:              Oscam-Icam-%s-build by speedy005\n",
                CS_VERSION);
        fprintf(fp, "S3 mit                -ggdb -pipe -ffunction-sections -fdata-sections -fomit-frame-pointer -fno-schedule-insns\n");
        fprintf(fp, "compiler_option       -O2   \n");
        fprintf(fp, "compress              nein   \n");
        fprintf(fp, "Toolchain             arm_7a  standart aus S3 \n");
        fprintf(fp, "Bibliothek            SSL_3.5.0\n");
        fprintf(fp, "Bibliothek            LIB_USBB_1.0.29\n");
        fprintf(fp, "Bibliothek            LIB_PCSC_2.3.3\n");
        fprintf(fp, "Bibliothek            LIB_Curl_8.14.1\n");
        fprintf(fp, "Bibliothek            CCID_1.6.2\n");
        fprintf(fp, "Bibliothek            LIB_ZLIB_1.3.1\n");
        fprintf(fp, "Bibliothek            libdvbcsa_1.1.0\n");
        fprintf(fp, "Patch                 \n");
        fprintf(fp, "Patch                \n");
        fprintf(fp, "Patch                \n");
        fprintf(fp, "Neon                    ja / 128 \n");
        fprintf(fp, "Compiler:                %s\n", CS_TARGET);
        fprintf(fp, "Box type:                %s (%s)\n", boxtype_get(), boxname_get());
        fprintf(fp, "PID:                     %d\n", getppid());
        fprintf(fp, "Compiler:                %s\n", CS_TARGET);
#ifdef USE_COMPRESS
        fprintf(fp, "Compression:             %s, level %s\n", COMP_VERSION, COMP_LEVEL);
#endif
        fprintf(fp, "Box Type:                %s (%s)\n", boxtype_get(), boxname_get());
        fprintf(fp, "PID:                     %d\n", getppid());
        fprintf(fp, "TempDir:                           %s\n", cs_tmpdir);
#ifdef MODULE_GBOX
        if(cfg.gbox_tmp_dir == NULL)
        {
                fprintf(fp, "GBox tmp_dir:   not defined using: %s\n", cs_tmpdir);
        }
        else
        {
                fprintf(fp, "GBox tmp_dir:        %s\n", cfg.gbox_tmp_dir);
        }
#endif

        fprintf(fp, "ConfigDir:               %s\n", cs_confdir);

#ifdef WEBIF
        fprintf(fp, "WebifPort:               %d\n", cfg.http_port);
#endif

'''

if 'Oscam-Icam-%s-build by speedy005' not in c:
    start = c.find('fprintf(fp, "Unix Starttime:')
    if start < 0:
        sys.exit("Abbruch: Unix-Starttime-Anker fehlt.")
    start = c.rfind('\n', 0, start) + 1
    end = c.find('#ifdef WITH_SIGNING', start)
    if end < 0:
        sys.exit("Abbruch: WITH_SIGNING-Anker fehlt.")
    c = c[:start] + new_c + c[end:]
    change_c = True
else:
    change_c = False

html_line = '             <LI><B>##HTTPOSCAMLABEL## ##CS_VERSION##</B></LI>'
html_add = '             <li><b>- <font style="color:#0048ff;">build</font> <font style="color:#0048ff;">- by speedy005</font></b></li>'

if html_add not in h:
    lines = h.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.strip() == html_line.strip():
            newline = "\r\n" if line.endswith("\r\n") else "\n"
            lines.insert(i + 1, html_add + newline)
            h = "".join(lines)
            break
    else:
        sys.exit("Abbruch: Statusseiten-Anker fehlt.")
    change_h = True
else:
    change_h = False

if not change_c and not change_h:
    print("Speedy005-Patch bereits vollständig vorhanden.")
    sys.exit(0)

backup_dir = Path(__file__).resolve().parent / "patch_backups"
backup_dir.mkdir(exist_ok=True)
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

for f in (cfile, htmlfile):
    shutil.copy2(f, backup_dir / f"{f.name}.backup_{stamp}")

if change_c:
    cfile.write_text(c)
if change_h:
    htmlfile.write_text(h)

print("Speedy005-Metadatenpatch erfolgreich angewendet.")
print(f"Sicherungen: {backup_dir}")
