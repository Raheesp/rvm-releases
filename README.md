# RVM releases - signed by the owner

This public folder is what every installed **RVM** checks. It is produced by `scripts/guard_sign.py` and is signed
with the owner's key; the private key never leaves the owner's PC, so nothing here can be forged. Created by Rahees.

- **control.json** - which versions are revoked, the oldest allowed, the newest release (PCs update themselves to it),
  how long a PC may stay offline, whether new PCs need approval, and an emergency "stop every PC".
- **devices.json** - the PCs the owner approved / stopped / revoked, by *device code* (a one-way hash of the PC - it
  cannot be turned back into the PC).
- **releases/<version>.json** - the SHA-256 fingerprints of that release's `RVM.exe`, `RVM-Agent.exe` and installer.

## Approve a new PC from GitHub

A new PC shows its **device code** and opens an issue here. To approve it, add the **`approve`** label to the issue
(or `stop` / `revoke`). A GitHub Action signs the change with a limited key and pushes it; that PC picks it up within
half an hour. The approvals key can only approve or stop PCs - it can never mark a release official.
