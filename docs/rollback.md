# Safe rollback / Ripristino sicuro

**Purpose:** recover from an EDID or Windows display-layout change that breaks remote access.

## Preconditions / Prima di iniziare

- Maintain an alternative active remote route, local keyboard/monitor, or out-of-band console. Verify it actually works.
- Keep the temporary known-good virtual display available until the NVIDIA display has passed testing.
- Note the dedicated connector, prior monitor layout and EDID file path.
- **Do not** uninstall NVIDIA, disable GPU devices, remove the last visible monitor, restart remote services blindly, or rely on an untested unattended reboot.

## Undo the NVIDIA EDID / Rimuovere l'EDID forzato

1. In a working session, open **NVIDIA Control Panel → Workstation → View System Topology → EDID**.
2. Locate the **same connector** where **EDID source = File** was loaded.
3. Select **Unload EDID** for that connector and apply.
4. In **Windows Settings → System → Display**, restore the previous primary screen and display arrangement.
5. Test Windows Settings, Server Manager and remote capture **before** removing the recovery monitor.

NVIDIA documents **Unload EDID** as the supported inverse of **Load EDID**: [official instructions](https://nvidia.custhelp.com/app/answers/detail/a_id/3301).

## If image capture is lost / Se perdi le immagini

- Use the **pre-verified** fallback connection or console.
- Restore the temporary display and confirm Windows can show a usable desktop.
- Undo the forced EDID and/or layout **one change at a time**.
- Record the failed stage and driver/model before reattempting.

This repository does **not** provide an automatic rollback command because device IDs, connectors, EDID sources and recovery methods depend on the machine. Manual, observable recovery is safer than an untested script.
