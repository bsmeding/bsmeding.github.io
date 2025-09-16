---
authors: [bsmeding]
date: 2025-02-04
title: Import Nautobot Device Types
summary: Automatically import needed device-types
tags: ["nautobot", "nautobot job", "device-types"]
toc: true
layout: single
comments: true
---

# Automatically import device-types in Nautobot

To get device-types accurate, with the interface-templates, console templates, port numbers and modules I created a drop-inn Nautobot job that can sync the desired Device Types to your nautobot instance.


<!-- more -->
---

This Nautobot Job and repo is a for of Nautobot device-type library, i extended this with a Nautobot Job so it can be added and runned directly without the need for you to copy-past device types.

## Why automate device-type import?

Manually creating device-types in Nautobot is tedious and error-prone, especially for complex devices with many interfaces, modules, and console ports. By using a job that reads device-type YAML files (such as those from the [nautobot-device-type-library](https://github.com/bsmeding/nautobot_devicetype_library)), you can:

- **Save time:** Import dozens or hundreds of device-types in seconds.
- **Reduce errors:** YAML files are version-controlled and community-maintained.
- **Stay up-to-date:** Easily sync new or updated device-types as vendors release new hardware.

---

## 4. How it works

The included Nautobot Job (`SyncDeviceTypes`) scans the device-type YAML files in the repository. You can filter by manufacturer (vendor) and/or a text search (supports regex) to only import the device-types you need.

- **Dry-run mode:** See what would be imported/updated before making changes.
- **Commit mode:** Actually create or update device-types in your Nautobot instance.

The job will:
1. List all available manufacturers (vendors) based on the folder structure.
2. Allow you to filter device-types by name or regex.
3. Import the selected device-types, including interfaces, console ports, and module bays.

---

## 5. Example: Importing Cisco Catalyst 9300

Suppose you want to import only Cisco Catalyst 9300 device-types:

1. In the job form, select manufacturer: `cisco`
2. In the filter field, enter: `9300`
3. Run in dry-run mode to preview.
4. If the results look good, run again with commit enabled.

![Job Form Example](/images/nautobot/sync_device_types_form.png)
*Example: Selecting manufacturer and filter in the job form.*

---

## 6. Customizing or Extending

You can fork the repository and add your own device-type YAML files, or contribute improvements upstream. The job will automatically pick up any new files you add to the `device-types/<manufacturer>/` folders.

---

## 7. Troubleshooting

- **Device-types not appearing?**  
  Double-check your filter and manufacturer selection. Try running with no filter to see all available device-types.
- **Errors on import?**  
  Check the Nautobot job logs for details. Invalid YAML or missing required fields can cause failures.
- **Need more device-types?**  
  Contribute to the [see my nautobot-device-type-library](https://github.com/bsmeding/nautobot_devicetype_library) or add your own YAML files.

---

## 8. Security & Best Practices

- Always review device-type definitions before importing, especially from third-party sources.
- Use dry-run mode to preview changes.
- Keep your device-type library up-to-date for new hardware and bugfixes.

---

## 9. Resources

- [nautobot-device-type-library on GitHub (source of my fork, what is forked from Netbox device_type library)](https://github.com/nautobot/nautobot-device-type-library)
- [Nautobot documentation: Device Types](https://docs.nautobot.com/projects/core/en/stable/models/dcim/devicetype/)
- [How to write device-type YAML files](https://github.com/nautobot/nautobot-device-type-library#device-type-definition)

---

## 10. How to Get Started

### 1. Add the Git Repository

- Go to **Extensibility** → **Git repositories** in Nautobot.
- Click **Add** and enter the repo URL:  
  `https://github.com/bsmeding/nautobot_devicetype_library.git`
- Click **Dry-Run + Sync** to pull the device-types.

![Add Git Repository](/images/nautobot/import-device-types/add-git-repo.png)
*Adding the device-type library as a Git repository in Nautobot.*


---
### 2. Enable Job
- Go to **Jobs** → **Jobs** in Nautobot.
- Find **Sync device types** Job and click ![Edit](/images/nautobot/import-device-types/enable-nautobot-device-type-sync-job.png)
- Find **Enabled** and select this ![Enable](/images/nautobot/import-device-types/enable-nautobot-device-type-sync-job2.png)

---
### 3. Launch the Job

- Navigate to **Jobs** in Nautobot.
- Find and select the `Sync Device Types` job.
- (Optional) Enter a search filter or select a manufacturer.
- Run in **dry-run** mode first to preview changes.
- ![Start Dry-Run](/images/nautobot/import-device-types/dry-run.png)
- ![Results Dry-Run](/images/nautobot/import-device-types/dry-run2.png)
- If satisfied, run again with **commit** enabled to import device-types.
- ![Results Dry-Run](/images/nautobot/import-device-types/run.png)


*Running the Sync Device Types job with filter and manufacturer selection.*

> **Tip:** Please DO filter otherwise ALL devices will be added
> 
---

### 4. Verify Imported Device Types

- Go to **Devices** → **Device Types** to see the imported device-types.
- You can now use these when creating new devices in Nautobot.

![Device Types Imported](/images/nautobot/import-device-types/imported_device_example.png)
*Imported device-types now available in Nautobot.*

---

With this approach, you can keep your Nautobot device inventory accurate, consistent, and ready for automation!

---



### How to Contribute a New Device Type
Did you notice a device type missing from the library? You can help improve the ecosystem!

1. **Fork the Repository**  
   Go to [nautobot_devicetype_library on GitHub](https://github.com/bsmeding/nautobot_devicetype_library) and click **Fork**.

2. **Add Your Device Type YAML**  
   - Clone your fork locally.
   - Add your device type YAML file in the correct manufacturer folder under `device-types/`.
   - Follow the [device-type YAML format guidelines](https://github.com/nautobot/nautobot-device-type-library#device-type-definition).

3. **Commit and Push**  
   - Commit your changes with a clear message, e.g.  
     `Add device type: Cisco Catalyst 9500-24Y4C`
   - Push to your fork.

4. **Open a Pull Request**  
   - Go to your fork on GitHub.
   - Click **Compare & pull request**.
   - Describe your addition and submit the PR.

Your contribution will be reviewed and, once approved, merged into the main library for everyone to use!

> **Tip:** If you’re unsure about the YAML format, check out existing device types or open an issue for help.

---
