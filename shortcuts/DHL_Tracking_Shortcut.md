# DHL Tracking Shortcut for macOS 26.0.1 (25A362)

This guide walks you through building a macOS Shortcut that quickly opens the correct DHL tracking portal (Express vs. Parcel & eCommerce) for a given tracking number. It uses only built-in Shortcuts actions so it works on macOS 26.0.1 (25A362).

## Download the ready-made shortcut

If you just want to import everything that’s described below, grab the
[`shortcuts/DHL_Tracker.shortcut`](DHL_Tracker.shortcut) file that now lives in this
repository. macOS treats `.shortcut` bundles just like any other Shortcuts export. The
latest macOS builds (including 26.0.1) block double-clicking unsigned shortcut files,
so use **one** of the import options below:

### Option A – Import straight from Finder (works on macOS builds that still allow it)

If your Mac still lets you open unsigned exports directly, follow these exact steps:

1. **Download the shortcut file**
   - Click the `DHL_Tracker.shortcut` link above. In the GitHub preview page choose **Download raw file** (or press `⌘ + S`).
   - Save it somewhere easy to reach—your **Downloads** folder works fine.
2. **Open the file in Finder**
   - Open **Finder ▸ Downloads**, then double-click `DHL_Tracker.shortcut`.
   - (If Finder says it can’t open the file because it came from the internet, click **Open** when the security prompt appears.)
3. **Allow untrusted shortcuts (first-time step only)**
   - The first time you import a shortcut from outside Apple, Shortcuts may tell you it’s from an untrusted source.
   - Click **Open Settings**, enable **Allow Untrusted Shortcuts**, then return to Finder and double-click the file again.
4. **Add the shortcut to your library**
   - The Shortcuts gallery window appears showing every action inside the workflow. Scroll to the bottom and click **Add Shortcut**.
5. **Create the Reminders list when prompted**
   - On the first run the shortcut asks for a list named **DHL Tracking Favorites**. Click **Create List** so Reminders can store your saved shipments.
6. **Grant Reminders access**
   - macOS will request permission the first time the shortcut tries to read or write reminders. Choose **OK** so favorites keep working.

Once imported you can still tweak any of the actions described later, but you no longer need to assemble them one by one. Future updates are easy too—just download the newer `.shortcut` file and repeat these steps to replace the existing one.

### Option B – Import with the Shortcuts command-line tool (bypasses the unsigned warning)

1. Open **Terminal** and change into the folder that contains the downloaded shortcut.
   ```bash
   cd ~/Downloads
   ```
2. Use the built-in `shortcuts` command to import the workflow directly into the Shortcuts app:
   ```bash
   shortcuts import --filepath ./DHL_Tracker.shortcut
   ```
   - The flag is required—without `--filepath` the command exits with “unexpected arguments.”
   - If the shortcut lives somewhere else, replace `./DHL_Tracker.shortcut` with the correct path (for example, `~/Downloads/DHL_Tracker.shortcut`).
   - The first time you run the command macOS may ask for permission to control Shortcuts—grant it so the import can finish.
3. Open the Shortcuts app. The workflow appears in **All Shortcuts** with the name **DHL Tracker** (you can rename it if you like).
4. Run it once so Shortcuts can request access to the Reminders list that stores your favorites.

If you prefer not to keep the downloaded file, you can delete it after the command succeeds—the shortcut now lives inside the Shortcuts app.

> **Tip:** If an earlier copy of the shortcut only showed the tracking URL instead of opening it automatically, delete that version and import this updated file. The download now uses the dedicated **URL → Open URLs** action pair so picking **Express** or **Parcel & eCommerce** launches your browser immediately with the tracking number filled in.

## Overview

### Install & Set Up the Shortcut (for beginners)

1. **Open the Shortcuts app** on your Mac. You can find it via Spotlight (`⌘ + Space`) by typing “Shortcuts,” then pressing `Return` to launch it.
2. In the sidebar, pick **All Shortcuts** so you can see every shortcut you already have.
3. Click the **+** button in the toolbar (top-right corner). This creates a blank shortcut canvas.
4. At the top of the window, click the default name (usually “Shortcut”) and rename it to something like **“DHL Tracker.”** Press `Return` to save the name.
5. Follow the action list below to add each building block. Every action is available from the right-hand **Actions** panel—drag them into the main editor in the order shown.
6. When you’re finished, click the **Done** button in the top-right corner to save everything.

You can run the shortcut right away by double-clicking it in the Shortcuts app or by pressing the **Play** ▶️ button inside the editor.

The shortcut:

1. Prompts you for a DHL tracking number (or lets you pick a saved favorite).
2. Lets you choose whether the shipment is **Express** or **Parcel & eCommerce**.
3. Opens the corresponding DHL tracking page in your default browser with the tracking number prefilled.
4. Offers to save the number as a favorite for future sessions.

## Actions List

1. **Get File**
   - After dropping the action on the canvas, click **Show More** to reveal the additional controls.
   - **Service**: `iCloud Drive`. (If you only see a pop-up button labeled “App Store App,” “Contact,” etc., change it to **File** first—this tells Shortcuts you want a file path. The **Show More** disclosure triangle then exposes the **Service** menu.)
   - Path: `Shortcuts/DHL Favorites.json`
   - Turn **Create if not found** on so the file is generated automatically.
   - When Shortcuts asks where to save, pick **iCloud Drive > Shortcuts** so the file sits alongside your other shortcut data. If you still don’t see iCloud Drive in the **Service** menu, open **System Settings ▸ [your Apple ID] ▸ iCloud**, confirm **iCloud Drive** is turned on, then return to Shortcuts and try again.
   - **No iCloud Drive available?** Skip ahead to [Favorites without iCloud Drive](#cant-access-icloud-drive-use-reminders-for-favorites-instead) for a Reminders-based setup that keeps working offline.

2. **Get Contents of File**
   - File: The result of step 1.

3. **If** (to guarantee you always have valid JSON)
   - Condition: `If Contents of File is Provided`
   - In the **If** (true) branch you can leave it empty—the existing file contents will flow through.
   - In the **Otherwise** branch add a **Text** action that contains `{}`. This seeds the favorites file the first time you run the shortcut.

4. **Get Dictionary from Input**
   - This converts the JSON text into a dictionary. Name the resulting Magic Variable `Favorites Dictionary`.

5. **Choose from Menu**
   - Menu Prompt: `How do you want to track?`
   - Menu Items:
     - `Pick Favorite`
     - `Track New`

6. Inside the **Pick Favorite** branch:
   1. **Get Dictionary Keys**
      - Dictionary: `Favorites Dictionary`
   2. **If**
      - Condition: `If Dictionary Keys is Empty`
      - If True: **Show Alert** with `No favorites saved yet. Pick “Track New” instead.` and then **Stop Shortcut**.
   3. **Choose from List**
      - List: `Dictionary Keys`
      - Prompt: `Select a saved shipment`
   4. **Get Dictionary Value**
      - Key: `Chosen Item` (from the previous step)
      - Dictionary: `Favorites Dictionary`
   5. Rename the Magic Variable from this step to `Tracking Number` for reuse below.

7. Inside the **Track New** branch:
   1. **Ask for Input**
      - Prompt: `Enter your DHL tracking number`
      - Input Type: `Text`
      - Rename the Magic Variable to `Tracking Number`.

8. **Choose from Menu**
   - Menu Prompt: `Select the DHL service`
   - Menu Items:
     - `Express`
     - `Parcel & eCommerce`

9. Inside the **Express** menu branch:
   1. **URL**
      - URL value: `https://www.dhl.com/global-en/home/tracking/tracking-express.html?submit=1&tracking-id=`
      - Place the cursor at the end of the field, tap the variable button, and choose the `Tracking Number` Magic Variable to append it directly after the equals sign (no extra spaces).
   2. **Open URLs**
      - URL: Leave it set to **Provided Input** so it opens the URL action immediately above.

10. Inside the **Parcel & eCommerce** menu branch:
   1. **URL**
      - URL value: `https://www.dhl.com/global-en/home/tracking/tracking-parcel.html?submit=1&tracking-id=`
      - Append the same `Tracking Number` Magic Variable right after the equals sign.
   2. **Open URLs**
      - URL: Leave the default **Provided Input** so the link opens instantly.

11. **Choose from Menu** (appears after both tracking branches)
   - Menu Prompt: `Save this tracking number as a favorite?`
   - Menu Items:
     - `Yes`
     - `No`

12. Inside the **Yes** branch:
    1. **Ask for Input**
       - Prompt: `Give this favorite a short name (e.g., “Laptop Repair”)`
       - Input Type: `Text`
    2. **Set Dictionary Value**
       - Key: `Provided Input`
       - Value: `Tracking Number`
       - Dictionary: `Favorites Dictionary`
    3. **Get Text from Dictionary**
       - Dictionary: `Favorites Dictionary`
       - Format: `JSON`
    4. **Save File**
       - Destination: `Shortcuts/DHL Favorites.json`
       - Turn **Overwrite If File Exists** on so the favorites list persists.
    5. (Optional) **Show Notification** confirming the favorite was saved.

13. The **No** branch can stay empty (the shortcut simply ends).

### Can’t access iCloud Drive? Use Reminders for favorites instead

If iCloud Drive is disabled or you’re using a managed Mac that hides the **Service** picker, you can keep your saved shipments inside the Reminders app instead of a JSON file. The tracking experience stays the same—you’ll still pick a favorite or enter a new number—but Reminders stores the list for you. The downloadable shortcut file above already uses this Reminders-based layout so you can start here immediately.

1. **Create a dedicated list**
   - Open **Reminders** and click the **+** button under **My Lists**.
   - Name the list **DHL Favorites** (or something similar) and make sure it lives **On My Mac** so it doesn’t require iCloud.

2. **Swap in Reminders actions before the “Pick Favorite” menu**
   - Remove the `Get File`, `Get Contents of File`, `If`, and `Get Dictionary from Input` actions.
   - Add **Find Reminders** and configure it to:
     - **List**: `DHL Favorites`
     - **Sort By**: `Creation Date (Newest First)` (optional but keeps your latest saves at the top)
     - Toggle **Limit** off so you fetch every reminder.
   - Rename the Magic Variable that comes out of `Find Reminders` to `Favorites List`.

3. **Update the “Pick Favorite” branch**
   - Insert an **If** action right after the branch opens.
   - Condition: `If Favorites List is Empty`
   - If True: **Show Alert** with `No favorites saved yet. Pick “Track New” instead.` followed by **Stop Shortcut**.
   - Otherwise: add **Choose from List** with **List** set to `Favorites List` and **Prompt** `Select a saved shipment`.
   - Follow it with **Get Details of Reminder** and set **Detail** to `Notes`. Rename the Magic Variable from this action to `Tracking Number` so the later steps keep working.
   - (Optional) If you prefer to keep the DHL service type alongside each favorite, turn on **Select Multiple** in `Choose from List` and use **Get Details of Reminder** twice—once for `Notes` (tracking number) and once for `Tags` (service labels).

4. **Update the “Save favorite” branch**
   - After asking for the friendly name, replace the dictionary and file actions with **Add New Reminder**.
   - Configure **Title**: `Provided Input` (the nickname you just collected).
   - Set **Notes** to the existing `Tracking Number` Magic Variable.
   - (Optional) Add **Add Tags to Reminder** right after and type `Express` or `Parcel` so the service is remembered too.
   - Finish with an optional **Show Notification** confirming the reminder was added.

When you run the shortcut again, `Find Reminders` retrieves every item in **DHL Favorites**, so your saved numbers show up instantly—no iCloud Drive needed.

## Optional Enhancements

- **Validate tracking number length**: Insert an `If` action after the first step to ensure the input isn’t empty. If empty, show an alert and stop the shortcut.
- **Auto-copy tracking number**: Add a `Copy to Clipboard` action before opening the URL so the number is available for other apps.
- **Share sheet support**: Change the shortcut type to “Quick Action” in the shortcut settings to surface it in Finder and the Services menu.
- **Manage favorites**: Add another menu after tracking that lets you remove a saved shipment by deleting its key from `Favorites Dictionary` and re-saving the file.

## Exporting the Shortcut

After assembling the shortcut:

1. Click the shortcut name in the toolbar.
2. Choose **Share > Export File…**.
3. Save the `.shortcut` file so you can reuse or share it.

Importing later is as simple as double-clicking the exported file.
