# Contributing / Contribuire

Community reports, corrections and repeatable hardware tests are welcome.

## What to submit

1. **OS** (Windows Server edition/build), GPU model, NVIDIA driver and RTX Desktop Manager versions.
2. **Monitor configuration**: no physical monitor / real monitor, EDID source (File/Monitor), which port and digital signal type.
3. **Desktop configuration**: identify which monitor is primary, resolution, refresh rate, scaling, and Extend/Duplicate state.
4. **Before/after symptoms** in Windows Settings, Server Manager, Start and remote-support tools.
5. **Evidence status**: PASS, FAIL, SKIP or NOT RUN. Explicitly label results that are only user-reported.
6. **Recovery**: how you preserved access and safely rolled back.

Use the repository's bug-report issue template. For changes to documentation, open a pull request from a branch; **never force-push someone else's branch**. Include links to the official NVIDIA/Microsoft sources for any claims about supported drivers or Windows behavior.

## Privacy and security

**Do not upload raw screenshots or logs containing:** machine/host names, GPU or monitor serial numbers, EDID serial strings, usernames, remote-support IDs, IP addresses, tokens, passwords or customer data. Remove these before sharing.

Do not add opaque executables, redistributable proprietary EDID blobs of unclear provenance, or unreviewed installer scripts. Any future code must be checked and tested before merging.

## Documentation style

- Keep English README as the canonical overview; update the Italian guide when the procedure changes.
- Avoid claiming compatibility or reboot persistence unless somebody has actually reproduced it.
- Explain the **critical difference** between NVIDIA **EDID (File)** and a correctly configured **Windows primary display**.

## License

Contributions to repository text are accepted under the [MIT License](LICENSE).
