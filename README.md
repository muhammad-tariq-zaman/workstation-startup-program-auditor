# workstation-startup-program-auditor

Audit startup programs on workstations for risk: the input CSV lists workstation, program, publisher, impact (high/medium/low) and enabled (yes/no) — REVIEW when the publisher is not a known publisher (Microsoft, Google, Adobe, Intel, Realtek, Cisco, Mozilla, Zoom, HP, Dell, Lenovo, Apple, TeamViewer), SLOW BOOT for a known publisher with high impact that is enabled, DISABLED when not enabled at startup, otherwise OK — REVIEW first, then SLOW BOOT, OK, DISABLED.

Sample input is included (sample.csv with nine startup programs).

## How to run

```sh
python3 main.py sample.csv
```

## Example output

```
WS-01 SpeedBooster Pro (UnknownSoft): REVIEW - unknown publisher, high impact
WS-02 CryptoMiner Helper (UnknownSoft): REVIEW - unknown publisher, high impact
WS-02 OldToolbar (UnknownSoft): REVIEW - unknown publisher
WS-03 HP Support Assistant (HP): SLOW BOOT - high startup impact
WS-01 Adobe Creative Cloud (Adobe): OK
WS-01 OneDrive (Microsoft): OK
WS-02 Zoom (Zoom): OK
WS-03 Teams (Microsoft): OK
WS-03 Skype (Microsoft): DISABLED - not enabled at startup
3 to review, 1 slowing boot, 4 ok, 1 disabled out of 9 program(s).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
