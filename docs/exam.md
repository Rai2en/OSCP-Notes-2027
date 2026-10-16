# Exam checklist

[Home](../README.md) · [Mindset & time management](../README.md#exam-mindset--time-management) · [Report template](../templates/report.md)

Rules checked on **2026-10-17**. Re-read the official guide before your attempt; the exam panel supplies target-specific requirements.

## Current format and restrictions

The practical window is 23h45, followed by 24 hours for documentation. Passing requires 70/100. Three standalone hosts total 60 points (10 initial access + 10 privilege escalation each); the three-host AD set totals 40 (10 + 10 + 20), with starting credentials supplied. The panel defines each objective; partial AD milestones can count. Metasploit modules and Meterpreter are limited to one chosen host, including failed attempts and `check`; Metasploit pivoting is prohibited. SQLMap, mass vulnerability scanners, spoofing and commercial tools are prohibited. Follow the complete [official exam guide](https://help.offsec.com/hc/en-us/articles/360040165632-OSCP-Exam-Guide).

There are no bonus points. AI chatbots are prohibited during both the exam and reporting phase. A tool being taught in PEN-200 does not make every feature usable in the exam. See the [official FAQ](https://help.offsec.com/hc/en-us/articles/4412170923924-OSCP-Exam-FAQ).

## Before the attempt

- [ ] Read guide, FAQ, proctoring instructions and exam email.
- [ ] Test VPN, keyboard layout, screenshot capture and VM recovery.
- [ ] Keep a local, searchable copy of these notes and required tools.
- [ ] Complete a full practice report, PDF export and archive rehearsal.
- [ ] Plan food, rest and connection/power contingencies.
- [ ] Record which host, if any, consumes the Metasploit/Meterpreter allowance.

## Evidence at each milestone

- [ ] Record the command, result, identity and hostname in private notes.
- [ ] Capture proof contents from their original location with `cat`/`type` in an interactive target shell, alongside the target IP shown with `ipconfig`, `ifconfig` or `ip addr`. A web-based shell is not accepted for this proof.
- [ ] Submit proof values to the panel before the practical window closes.
- [ ] Document the exact path to the required privilege level.
- [ ] Keep screenshots legible and linked to the appropriate finding.

## Before submission

- [ ] Another competent reader could reproduce each documented step.
- [ ] Modified exploits include source URL, changes and rationale.
- [ ] Export and visually inspect the PDF, including images and code.
- [ ] Follow the exact PDF/7z naming, size and packaging requirements in the guide.
- [ ] Complete the upload and checksum verification within the deadline.

Do not treat a retrieved flag as a substitute for the required shell, privileges or documentation. Details and exceptions belong to the [official guide](https://help.offsec.com/hc/en-us/articles/360040165632-OSCP-Exam-Guide).
