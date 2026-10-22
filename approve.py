"""Sign a device decision from a labelled issue (run by .github/workflows/approve.yml). Created by Rahees.

The approvals key (the secret RVM_APPROVALS_KEY) may only approve / stop / revoke PCs - it cannot sign a release.
"""
import base64, json, os, re, time, datetime, pathlib
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

label = os.environ["LABEL"].strip()
text = (os.environ.get("TITLE", "") + "\n" + os.environ.get("BODY", "")).upper()
match = re.search(r"\b([A-Z2-7]{4}-[A-Z2-7]{4}-[A-Z2-7]{4}-[A-Z2-7]{4})\b", text)
if not match:
    raise SystemExit("no device code in the issue")
code = match.group(1)
state = {"approve": "approved", "stop": "stopped", "revoke": "revoked"}[label]

key = Ed25519PrivateKey.from_private_bytes(base64.b64decode(os.environ["RVM_APPROVALS_KEY"]))
path = pathlib.Path("devices.json")
devices = json.loads(path.read_text()).get("signed", {}) if path.exists() else {}
devices.setdefault("product", "RVM")
devices.setdefault("devices", {})
entry = devices["devices"].get(code, {})
entry["s"] = state
entry["t"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
devices["devices"][code] = entry
devices["serial"] = int(time.time())
devices["updated"] = entry["t"]

canon = json.dumps(devices, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
signature = base64.b64encode(key.sign(canon)).decode()
path.write_text(json.dumps({"signed": devices, "signature": signature}, indent=2, sort_keys=True) + "\n")

with open(os.environ["GITHUB_ENV"], "a") as env:
    env.write(f"DEVICE={code}\n")
print(f"{label} {code}")
