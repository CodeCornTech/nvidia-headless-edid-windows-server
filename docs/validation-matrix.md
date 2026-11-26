# Validation matrix — evidence and limits

This table separates **observed** results from configurations that were not tested. Case date: **2026-11-26**. Values represent the source troubleshooting session only.

| Check | Evidence | Status |
| --- | --- | --- |
| Windows Server 2022 + NVIDIA Quadro P620 recognized | Win32_VideoController / nvidia-smi output | **PASS** |
| Driver 582.99 loaded, GPU in WDDM | Driver output / NVIDIA System Topology | **PASS** |
| No physical PnP monitor initially present | PnP output + operator confirmation | **PASS** |
| Temporary USB Mobile Monitor virtual display works | All affected apps restored when enabled | **PASS** — user reported |
| Forced EDID accepted by NVIDIA | NVIDIA topology: DisplayPort 4 connected, **EDID (File)** | **PASS** |
| Emulated monitor mode | Advanced display: 1920×1080, 60.000 Hz, RGB 8-bit, SDR | **PASS** |
| EDID loading **by itself** fixes every UI symptom | Scroll/scaling still broken after loading EDID | **FAIL** — important finding |
| Windows main-display/layout corrections restore UI | Operator reported final resolution after configuration | **PASS** — user reported |
| All software remains healthy without temporary display | Operator final report that issue is resolved | **PASS** — user reported; not independently instrumented |
| Persistent working display through unattended reboot | No complete post-reboot evidence provided | **NOT RUN** |
| Display survives pre-login / lock-screen conditions | No evidence | **NOT RUN** |
| Physical monitor hot-plug and automatic switching | No evidence | **NOT RUN** |
| Other Quadro / RTX GPUs, Windows Server versions | No evidence | **NOT RUN** |
| Local automated tests / driver-level tests | No execution on the source server from this repository | **NOT RUN** |

## Reproduction checklist

For new reports, record separately:

- Windows edition/build, GPU model, driver version and WDDM mode;
- physical connected outputs and presence/absence of EDID (File);
- which display is actually **primary**, resolution, refresh rate and DPI scale;
- behavior with and without an indirect display driver;
- status of **Settings scroll**, **Start sizing**, **Server Manager**, **AnyDesk image**, **Supremo**, **RustDesk**;
- tested reboot persistence and real-monitor hot-plug (only when performed).

Do not convert **NOT RUN** to **PASS** without observed evidence.
