# Troubleshooting / Risoluzione problemi

[English](../README.md) · [Italiano](../README.it.md) · [Rollback](rollback.md)

## Start here

| Symptom | Check | Caution |
| --- | --- | --- |
| NVIDIA reports **EDID (File)** but Settings still scrolls incorrectly | Identify the NVIDIA monitor in **Settings → System → Display**; check **primary**, scale, resolution and multi-monitor layout | An EDID source of File does **not** prove a good desktop layout |
| Start menu/apps look too small or offset | Verify 100% scale on the NVIDIA monitor as a baseline; close/reopen affected apps | A new Windows logon may be necessary for some DPI-aware applications; keep fallback access |
| Server Manager/Supremo windows look blank | Test whether a known-working virtual display temporarily restores composition, then review NVIDIA primary display | Do not assume an application-specific fault |
| AnyDesk says **Waiting for image** | Confirm an active display is attached to the *console* and that remote image capture works | An RDP-only virtual adapter may exist for a disconnected session |
| Display device says **Unknown** | Check whether it is a stale/disconnected **Microsoft Remote Display Adapter** | Unknown alone is not proof of a broken NVIDIA GPU |
| NVIDIA **Disp.A Off** | Compare with physical cable state and forced EDID topology | Display status depends on GPU/driver and connection |
| EDID loads but monitor isn't usable | Confirm connector and digital signal type, EDID monitor mode, Windows arrangement | Do not blindly load a different EDID on every connector |
| Physical monitor changes the arrangement | A forced EDID on a dedicated port may ignore hot-plug | Prefer a separate physical connector; test before assuming seamless switching |

## Diagnosis order (non-destructive)

1. Check GPU/driver status with **nvidia-smi** and **Win32_VideoController**.
2. Inspect NVIDIA **View System Topology**: distinguish **EDID (Monitor)** from **EDID (File)**.
3. Inspect **Settings → Display**, not just **Advanced display**.
4. Map the NVIDIA screen using **Identify**; then check whether it is the **primary** display, the current resolution and scaling.
5. Compare behavior with the temporary working virtual display **present** and later **removed**, with fallback access.
6. If symptoms remain, investigate compositor/driver, monitor EDID validity and remote capture as **separate hypotheses**.

## Read-only PowerShell

~~~powershell
Get-CimInstance Win32_VideoController |
  Select-Object Name,DriverVersion,DriverDate,Status

Get-PnpDevice -Class Display,Monitor |
  Format-Table Class,Status,FriendlyName,InstanceId -AutoSize

Get-CimInstance Win32_Service |
  Where-Object { $_.Name -match 'rustdesk|anydesk|supremo' } |
  Select-Object Name,State,StartMode

Get-WinEvent -FilterHashtable @{
  LogName = 'System'
  StartTime = (Get-Date).AddDays(-5)
} -ErrorAction SilentlyContinue |
  Where-Object {
    $_.ProviderName -match 'nvlddmkm|Display' -or $_.Id -eq 4101
  } |
  Select-Object -First 20 TimeCreated,Id,ProviderName,Message
~~~

**Warnings:** Event ID 1 from nView with **NVAPI_ERROR**, or a .NET crash in rundll32, can be relevant to diagnosis but does not establish the root cause on its own. Do not treat reinstalling a GPU driver as the first step when the same driver works after correcting the display configuration.

## Monitor names and privacy

Windows screen numbers (e.g. **1**, **2**) and Win32 API devices (e.g. **DISPLAY1**, **DISPLAY5**) are not guaranteed to match. Verify the GPU association and primary display before editing.

Before sharing logs or topology screenshots, redact hostnames, serials, usernames, EDID-derived serials, IPs and remote-support IDs.

## When it is NOT solved

If the UI still fails after primary-display and scaling changes, document exactly which screen is primary and whether each screen is physically connected, EDID-forced or an IDD display. Create an issue with the [bug report template](../.github/ISSUE_TEMPLATE/bug_report.yml). Do not label the setup as fixed until the same apps work **without** the temporary virtual display.
