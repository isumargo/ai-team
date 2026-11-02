#!/usr/bin/env python3
"""
Set Syncthing GUI auth (user+password) and verify folder + device ID.

CARA PAKAI:
  python3 guardian/syncthing_auth.py            # dry-run: hanya cek & laporan
  python3 guardian/syncthing_auth.py --apply    # ubah config + restart Syncthing

PERINGATAN:
  Mode --apply melakukan PATCH config GUI dan me-RESTART Syncthing. Restart
  memutus session sync selama beberapa detik. Selalu cek dulu output dry-run
  dan pastikan Syncthing sedang idle (tidak sedang sync file besar).

  Jalankan dari mesin VPS. Kredensial dibaca dari file LUAR repo
  (/root/.config/syncthing/), tidak pernah ditulis ke dalam repo.
"""
import json, urllib.request, urllib.error, base64, time, re, sys

CFG = "/root/.config/syncthing/config.xml"
CRED = "/root/.config/syncthing/gui-credentials.txt"
BASE = "http://127.0.0.1:8384"
APPLY = "--apply" in sys.argv

KEY = re.search(r"<apikey>([^<]+)</apikey>", open(CFG).read()).group(1)
PW = open(CRED).read().strip()


def api(method, path, body=None, basic=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method)
    req.add_header("X-API-Key", KEY)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    if basic:
        req.add_header("Authorization", "Basic " + base64.b64encode(
            f"{basic[0]}:{basic[1]}".encode()).decode())
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")


def plain_code():
    try:
        with urllib.request.urlopen(BASE + "/", timeout=6) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return f"ERR {e}"


st, txt = api("GET", "/rest/config/gui")
gui = json.loads(txt)
print("mode    :", "APPLY (akan ubah config + restart)" if APPLY else "DRY-RUN (tidak ada yang diubah)")
print("sebelum :", {"user": gui.get("user"), "authMode": gui.get("authMode"),
                     "address": gui.get("address"), "pw_set": bool(gui.get("password"))})

if not APPLY:
    print()
    print("Dry-run berhenti di sini. Tidak ada config yang diubah, Syncthing tidak direstart.")
    print("Untuk menerapkan: python3 guardian/syncthing_auth.py --apply")
    print()
    st, txt = api("GET", "/rest/config/folders")
    folders = json.loads(txt)
    print("folders :", [(f["id"], f["path"], f["type"]) for f in folders])
    st, txt = api("GET", "/rest/system/status")
    s = json.loads(txt)
    print("myID    :", s.get("myID"))
    print("uptime  :", s.get("uptime"), "| errors:", s.get("errors"))
    print("panel tanpa auth saat ini:", plain_code(), "(200 = panel TERBUKA tanpa password)")
    sys.exit(0)

gui["user"] = "ical"
gui["password"] = PW
st, out = api("PATCH", "/rest/config/gui", gui)
print("PATCH   :", st, out[:120].replace("\n", " "))
time.sleep(2)

print("tanpa auth:", plain_code(), "(401 = panel terkunci)")
print("dengan auth:", api("GET", "/", basic=("ical", PW))[0])

api("POST", "/rest/system/restart")
time.sleep(7)

st, txt = api("GET", "/rest/config/folders")
folders = json.loads(txt)
print("folders :", [(f["id"], f["path"], f["type"]) for f in folders])

st, txt = api("GET", "/rest/system/status")
s = json.loads(txt)
print("myID    :", s.get("myID"))
print("uptime  :", s.get("uptime"), "| errors:", s.get("errors"))

st, txt = api("GET", "/rest/config/gui")
g2 = json.loads(txt)
print("sesudah :", {"user": g2.get("user"), "pw_set": bool(g2.get("password")),
                     "authMode": g2.get("authMode")})
print("VERDICT :", "OK" if (g2.get("user") == "ical" and g2.get("password")) else "GAGAL")
