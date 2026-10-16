# Coverage, audit and remaining work

[Home](../README.md) · [Start here](start-here.md)

Baseline reviewed: commit `24b4c1b`, 2026-09-10. The repository was a single README of about 2,300 lines. It already covered many enumeration, transfer, credential, privilege and AD commands. The main gaps were navigation, decision criteria, troubleshooting, reporting and explicit separation of training-only tools.

The table is a repository assessment, not a claim that all techniques are validated. The [official body of knowledge](https://help.offsec.com/hc/en-us/articles/38543335188756-OSCP-Body-of-knowledge) defines a broader curriculum than a command list. Course coverage and exam permission are different questions.

| Area | Current resource | Status / next improvement |
|---|---|---|
| Reporting and evidence | [Exam](exam.md), [report template](../templates/report.md) | Added; rehearse a full PDF export locally |
| Information gathering | [Methodology](methodology.md), README protocol sections | Broad command coverage; add annotated lab outputs |
| Web assessment | [Web](web.md) | Added manual workflow; expand API and XSS lab examples |
| SQL | README manual SQL and web workflow | Existing commands; training-only SQLMap explicitly labeled |
| Client-side topics | README contains limited material | Gap: structured authorized-lab exercises and prerequisites |
| Public exploit selection/adaptation | Methodology and troubleshooting | Added checklist; worked synthetic examples remain |
| Memory corruption | External references / scattered commands | Gap: tested cross-compilation and adaptation exercise |
| AV concepts | Existing payload notes | Partial; explain limitations and lab validation, not universal bypass claims |
| Password handling | README, AD workflow, private inventory | Covered in reference; add format-specific worked examples |
| Linux escalation | README and [prerequisite guide](privilege-escalation.md) | Broad reference; commands not all reproduced |
| Windows escalation | README and prerequisite guide | Broad reference; compatibility matrix still needs lab results |
| Tunneling | [Pivoting](pivoting.md) | Ligolo, SSH and Chisel examples; multi-hop lab rehearsal remains |
| Metasploit | README and exam restrictions | Restricted usage explained; separate training exercises remain |
| AD enumeration/authentication | [AD workflow](active-directory.md) and README | CE/legacy distinction and permission interpretation added |
| Lateral movement | AD workflow and README | Existing command coverage; synthetic end-to-end lab remains |
| Integrated practice | [Training](training.md) and progress template | Added measurable rehearsal process |

## Changes in this revision

- Situation-based navigation while preserving the original command reference and attribution.
- Exam-rule snapshot linked to official sources; SQLMap removed from setup aliases and labeled training-only.
- Setup variables and shortcuts clarified; avoid shadowing commands such as `nc` and `smbclient`.
- Ligolo console/host separation, return traffic and loopback access documented.
- AD permission, credential scope and collector compatibility guidance.
- Private note/report templates, an offline notebook initializer and a local Markdown path checker.

## Validation levels

### Field manual revision — 2026-10-17

The complete README at `d3496cf` was reviewed for this follow-up. It now serves as the **OSCP Ultimate Field Manual**, with stage-based navigation, consistent heading levels, ten service-specific checklists, Linux/Windows/AD checklists, concise Exam Tips and an Exam Mindset & Time Management section. Existing technical subjects and attribution remain; identified command changes are itemized in the [follow-up audit](command-audit.md#field-manual-follow-up-review). The exam snapshot was rechecked against the official guide and FAQ. These changes are source-reviewed and locally checked, not target-lab-tested.

### What each level means

**Source-reviewed** means documentation was compared with primary references. **Locally checked** applies to repository scripts and navigation. **Lab-tested** requires a dated, reproducible lab run with tool and target versions. The new attack workflows are source-reviewed, not lab-tested in this revision. The original README retains historical examples; this is not a line-by-line certification of every command.

## Maintenance priorities

The subsequent [command audit](command-audit.md) corrects identified CLI and chain prerequisites against current upstream references and adds a [CVE shortlist](cve-references.md). These changes are source-reviewed; offensive workflows remain untested in a target lab.

1. Add synthetic worked examples for uncovered topics and record their validation status.
2. Gradually split the original reference by topic while maintaining old anchors or redirect notes.
3. Replace stale third-party snippets only after checking their behavior and attribution.
4. Recheck exam policy and upstream tool syntax before each attempt or documentation release.
5. Add external-link auditing separately; the current offline checker validates local paths only.
