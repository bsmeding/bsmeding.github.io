---
title: How to Enable Windows Subsystem for Linux (WSL)
tags:
    - wsl
    - basics
    - tutorial
---
# How to Enable Windows Subsystem for Linux (WSL)

The Windows Subsystem for Linux (WSL) allows you to run a Linux environment directly on Windows without the need for a virtual machine or dual-boot setup. It’s a powerful tool for developers who want the best of both worlds: Windows and Linux.

---

## Step 1: Check System Requirements

- **OS Version**: WSL is available on Windows 10 (version 1903 or later) and Windows 11.
- **Hardware**: Ensure your system supports virtualization (check in your BIOS/UEFI).

---

## Step 2: Enable WSL

1. Open **PowerShell** as Administrator.
2. Run the following command to enable the WSL feature:

    ```powershell
    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
    ```

3. Enable the Virtual Machine Platform (required for WSL 2):

    ```powershell
    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
    ```

4. Restart your computer to apply the changes.

---

## Step 3: Set WSL 2 as the Default Version (Optional)

WSL 2 offers better performance and full system call compatibility compared to WSL 1.

1. Update your WSL kernel to the latest version. Download it from [Microsoft’s WSL page](https://aka.ms/wsl2kernel).
2. Open **PowerShell** as Administrator and set WSL 2 as the default version:

    ```powershell
    wsl --set-default-version 2
    ```

---

## Step 4: Install a Linux Distribution

1. Open the **Microsoft Store**.
2. Search for your preferred Linux distribution (e.g., Ubuntu, Debian, Kali Linux).
3. Click **Install**.
4. Once installed, launch the distribution and complete the setup (create a username and password).

---

## Step 5: Verify Your WSL Installation

To check the installed Linux distributions and their WSL versions, run:

```powershell
wsl -l -v
```

You should see a list of installed distributions and their version (WSL 1 or WSL 2).

---

## Step 6: Start Using Linux on Windows

Launch your Linux distribution from the Start menu or by typing `wsl` in PowerShell or Command Prompt.

Example:
```bash
# Update package lists
sudo apt update

# Install essential tools
sudo apt install build-essential
```

---

## Additional Tips

- **File Access**: Access Windows files from Linux via `/mnt/c`.
- **Customizations**: Modify WSL settings in the `.wslconfig` file in your user directory.
- **GUI Applications**: On Windows 11, WSL supports Linux GUI applications natively.

---

## Conclusion

WSL bridges the gap between Windows and Linux, making it an excellent tool for developers, system administrators, and enthusiasts. With these steps, you can set up and start using WSL to enhance your productivity.
