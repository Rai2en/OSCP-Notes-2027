# Training and readiness

[Home](../README.md) · [Coverage](coverage.md) · [Progress template](../templates/progress.md)

Choose a pace you can sustain. These are practice suggestions, not official passing criteria or a guarantee. Use authorized labs and re-solve exercises without copying their walkthroughs.

## Four stages

| Stage | Practice | Exit evidence |
|---|---|---|
| Foundations | Linux/Windows administration, TCP/IP, DNS, Bash/PowerShell, HTTP/SQL | Explain and diagnose a failed connection or permission check |
| Individual skills | Enumeration, web flaws, credential handling, local escalation | Reproduce unfamiliar exercises and explain prerequisites |
| Connected environments | Domain enumeration, permissions, lateral movement, routing | Draw the network and explain every identity transition |
| Timed rehearsal | Mixed hosts, rest, evidence capture and report | Reconstruct a complete report from private notes within your planned window |

For an official study schedule, consult the [12-week plan](https://help.offsec.com/hc/en-us/articles/15541765522196-OffSec-PEN-200-Learning-Plan-12-Week) or [24-week plan](https://help.offsec.com/hc/en-us/articles/15545672357780-OffSec-PEN-200-Learning-Plan-24-Week). Adapt the workload rather than treating a calendar as proof of readiness.

## Suggested self-assessment

- [ ] Enumerate an unfamiliar host without a walkthrough and justify priorities.
- [ ] Distinguish transport, authentication and authorization failures.
- [ ] Verify a Linux and Windows escalation prerequisite manually.
- [ ] Explain why an AD graph edge enables the next step.
- [ ] Reach an internal service and establish a return connection through a pivot.
- [ ] Adapt a public exploit while documenting the exact changes.
- [ ] Capture complete evidence while solving, not afterward.
- [ ] Produce a report another reader can follow without asking what happened.
- [ ] Complete repeated mixed practice with declining hint dependence.

Record hint usage honestly. After reading a solution, close it, explain the missed observation, then reattempt later from a fresh state. Track time to first useful observation, time lost to environment issues, missing evidence and the cause of each failed hypothesis.

## Three bounded drills

| Drill | Do | Keep / exit condition |
|---|---|---|
| HTTP controls | Run [the local exercise](lab-validation.md#executed-record-http-truefalse-controls), then replay it manually | Baseline/true/false pair explained; no claim about data extraction or another database |
| Permission interpretation | Use a disposable lab and the [Windows](windows-services.md) or [Linux](linux-permissions.md) procedure | One permitted and one rejected hypothesis with actual permission/trigger evidence and resulting decision |
| Evidence handoff | Solve one authorized lab target using a private notebook; reconstruct the report from notes after a break | No missing command, identity, route or screenshot required for another reader to reproduce the path |

Record actual tool/target versions and results in [validation](lab-validation.md). Reattempt after addressing the cause of difficulty; merely rereading the explanation does not complete the drill.

## Turn a machine into a reusable lesson

Write a generic technique with synthetic names and clear prerequisites using [the technique template](../templates/technique.md). Keep credentials, flags, private lab screenshots and restricted exam material out of the public repository. A collection of machine-specific answers does not establish that you can solve a new machine.
