# NVIDIA Headless EDID Fix for Windows Server

**Make Windows Server desktop applications and remote-access tools usable without a physical monitor using NVIDIA's built-in EDID emulation.**

[Italiano / Guida in italiano](README.it.md) · [Troubleshooting](docs/troubleshooting.md) · [Safe rollback](docs/rollback.md) · [Validation matrix](docs/validation-matrix.md)

> **Case study, not a universal driver fix.** Reproduced on Windows Server 2022 with an NVIDIA Quadro P620. The final working configuration used NVIDIA forced EDID **and** correct Windows primary-display/layout settings. An EDID being accepted by NVIDIA alone was **not enough** to fix the UI. Unattended reboot persistence, hot-plug behavior, and other GPUs remain unverified.

## Symptoms

On a **headless** Windows Server, with no monitor connected, we observed:

- Windows Settings scrolling, dropdowns and mouse-hit areas behaving incorrectly;
- Server Manager and remote application windows appearing white or not fully rendered;
- Start menu and application elements looking incorrectly scaled or occupying only part of the desktop;
- AnyDesk displaying **Waiting for image**, while Supremo and RustDesk had inconsistent window rendering;
- the NVIDIA GPU appearing healthy despite no active physical display.

A temporary indirect/virtual display made all these symptoms disappear, suggesting a display-enumeration/desktop-layout issue rather than a need to reinstall Windows.

## Environment observed

| Component | Observed value |
| --- | --- |
| OS | Windows Server 2022 Datacenter |
| GPU | NVIDIA Quadro P620 |
| NVIDIA display driver | 582.99 (32.0.15.8299) |
| NVIDIA RTX Desktop Manager | 205.40 |
| Display cable / physical monitor | None |
| Reserved GPU output | DisplayPort 4 (Mini DisplayPort connector) |
| Forced EDID source | **File**, as shown in NVIDIA System Topology |
| Emulated monitor mode | 1920 × 1080, 60 Hz, RGB 8-bit, SDR |
| Remote access observed | RustDesk, AnyDesk, Supremo |
| Test date | 26 November 2026 |

The labels and screenshots from the source machine are intentionally anonymized here. The EDID monitor name is arbitrary; the example below uses **HEADLESS-1080**.

## Safety first

**A display-mode change can cut off your only remote session.** Before starting:

1. Ensure a fallback remote connection or out-of-band/local recovery path.
2. Keep any **working temporary virtual display** active until the NVIDIA display has been tested.
3. Record the previous Windows display layout and selected NVIDIA port.
4. Do **not** disable GPU adapters, kill Desktop Window Manager, remove RDS drivers or uninstall remote-access services as part of this guide.

This procedure does not require a permanent RustDesk display driver, a GPU driver downgrade or a hardware dummy plug *in the tested setup*. It does **not** imply that those alternatives are never useful.

## Step-by-step solution

### 1. Establish a working temporary display

If the desktop is blank or interactive only by blind clicks, use a known-working temporary display path (for example, a remote-support tool's virtual monitor) so that Windows Settings and NVIDIA Control Panel can be operated. **This is a temporary safety measure**; the documented end state uses NVIDIA's forced EDID.

### 2. Prepare a suitable EDID

In **NVIDIA Control Panel → Workstation → View System Topology → EDID**, export the EDID of a suitable compatible monitor, or obtain a known-good EDID using a trusted process. NVIDIA stores the export as a text file on Windows.

The successful case used a locally prepared 1080p60 EDID accepted by NVIDIA, but **this repository deliberately does not distribute a generic, unverified EDID blob**. Validate the display mode, EDID integrity and licensing/provenance of any file you choose.

### 3. Force EDID on an unused NVIDIA connector

Navigate to **NVIDIA Control Panel → Workstation → View System Topology → EDID → Load**:

1. Choose the EDID file.
2. Select **one unused output** on your professional NVIDIA GPU.
3. For the case-study P620 on **DisplayPort 4**, choose **DisplayPort (digital)** as the signal type.
4. Confirm the warning and select **Load EDID**.
5. Return to **View System Topology**. Confirm that the chosen output is listed as connected, and **EDID source = File**.
6. Confirm the NVIDIA display's advanced properties show the expected **1920 × 1080 at 60 Hz** (or your validated mode).

**Do not stop here.** In the original case, the EDID showed **File** and the GPU monitor appeared connected, yet scrolling and sizing defects still occurred until Windows desktop configuration was corrected.

### 4. Make the NVIDIA emulated display the Windows primary display

With the temporary virtual display **still active**:

1. Open **Settings → System → Display** (not only *Advanced display*).
2. Use **Identify** and select the NVIDIA EDID-backed monitor (for example, **HEADLESS-1080**). The numbers in Windows UI do not necessarily match API names such as DISPLAY1/DISPLAY5.
3. Set the NVIDIA display to the EDID's supported resolution and refresh rate; in the case study: **1920 × 1080, 60 Hz**.
4. Set scaling to **100%** as the initial troubleshooting baseline. Apply the same baseline to the temporary display if necessary.
5. While both monitors are active, select **Extend these displays**; do not rely on mirroring or automatic layout detection.
6. For the NVIDIA monitor, enable **Make this my main display** if not already selected.
7. Apply changes and reopen **Windows Settings, Server Manager, Start, Supremo and AnyDesk** to check scrolling, hit testing, scaling, and image capture.

The final user-reported resolution occurred after correcting the primary-display / Windows display configuration. This sequence is a practical diagnostic guide, not proof that every sub-setting is independently required.

### 5. Remove the temporary display only after verification

Once the NVIDIA EDID-backed screen is functional, deactivate the temporary third-party display **only with fallback access available**, and repeat the UI and remote-capture checks. The machine owner reported that the desktop and remote tools then behaved normally.

**Not yet verified in this case:** persistence across unattended reboot, behavior before login, and automatically switching back after plugging/unplugging a physical monitor. See [validation matrix](docs/validation-matrix.md).

## Read-only diagnostics

Run from an elevated PowerShell where necessary. These commands **do not change** display configuration.

~~~powershell
Get-CimInstance Win32_VideoController |
  Select-Object Name, DriverVersion, Status, CurrentHorizontalResolution, CurrentVerticalResolution

Get-PnpDevice -Class Display,Monitor |
  Format-Table Class, Status, FriendlyName, InstanceId -AutoSize

Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.Screen]::AllScreens |
  Select-Object DeviceName, Primary,
    @{Name='Resolution';Expression={"$($_.Bounds.Width)x$($_.Bounds.Height)"}} |
  Format-Table -AutoSize

nvidia-smi
~~~

**Interpretation:** NVIDIA reporting **Disp.A Off** before emulation or a stale Microsoft Remote Display Adapter entry does not alone prove a GPU failure. A healthy driver and an EDID with **File** also do not prove that Windows UI composition and capture are correct.

## Connecting a physical monitor later

NVIDIA's forced EDID may ignore hot-plug events **on the chosen output**. Reserve the emulated connector for headless use and connect a real monitor to another available output; Windows may treat that monitor as a second screen rather than automatically clone the headless desktop. Do not promise seamless switching without testing your hardware.

## Recovery and troubleshooting

- [Troubleshooting — white windows, bad scroll, mixed DPI and remote capture](docs/troubleshooting.md)
- [Rollback — safely unload the forced EDID](docs/rollback.md)
- [Validation matrix — what actually passed and what remains untested](docs/validation-matrix.md)
- [How to contribute verified configurations](CONTRIBUTING.md)

## Official references

- [NVIDIA: How to Manage Display EDIDs on Quadro and NVS Boards](https://nvidia.custhelp.com/app/answers/detail/a_id/3301)
- [NVIDIA: Managing a Display EDID on Windows](https://nvidia.custhelp.com/app/answers/detail/a_id/3569)
- [Microsoft: Enumeration and Display Control](https://learn.microsoft.com/en-us/windows/win32/gdi/enumeration-and-display-control)
- [Microsoft: EnumDisplayDevicesW](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdisplaydevicesw)

**Disclaimer:** Community documentation by CodeCorn Technology. Not endorsed by NVIDIA, Microsoft or any remote-support vendor. Preserve recoverable access before changing headless display settings.

**License:** [MIT](LICENSE).
