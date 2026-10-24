"""Add profile links, then rebuild the deploy zip from outputs/_site. Usage: python3 tools/build_zip.py"""
import os, subprocess, sys, zipfile
subprocess.run([sys.executable, "tools/add_profiles.py"], check=True)
subprocess.run([sys.executable, "tools/ai_prompt_blocks.py"], check=True)
subprocess.run([sys.executable, "tools/add_call_bar.py"], check=True)
subprocess.run([sys.executable, "tools/add_offer_box.py"], check=True)
z = "outputs/_deploy/contentfellow-site-2026-10-16.zip"
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as f:
    for r, _, fs in os.walk("outputs/_site"):
        for n in fs:
            p = os.path.join(r, n); f.write(p, os.path.relpath(p, "outputs/_site"))
print("zip:", len(zipfile.ZipFile(z).namelist()), "files")
