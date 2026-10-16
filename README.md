# 🛡️ SENTINEL
## Network Traffic Monitoring & Intrusion Detection System Using Python and Machine Learning

**Author:** Bidyadhar Jena  
**Project type:** Educational cybersecurity prototype  
**Platform:** Windows 11 (primary setup guide)  
**Interface:** Flask web dashboard

SENTINEL is a student-built network monitoring prototype that captures IPv4 packets, displays observed traffic in a local web dashboard, and uses an Isolation Forest machine-learning model to flag potentially unusual traffic patterns. Alerts can be stored in a local SQLite database.

> **Important limitation:** The current model was trained on synthetic data. Its results are experimental; an anomaly is not proof of an attack, and the system may produce false positives or miss suspicious activity. This project is for learning and authorized testing, not production security monitoring.

---

## 📚 Table of contents

- [Features](#-features)
- [How it works](#-how-it-works)
- [Technology stack](#-technology-stack)
- [Project structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation on Windows](#-installation-on-windows)
- [Run SENTINEL](#-run-sentinel)
- [Test the project](#-test-the-project)
- [Train or replace the model](#-train-or-replace-the-model)
- [Troubleshooting](#-troubleshooting)
- [Fork this repository](#-fork-this-repository)
- [Contributing](#-contributing)
- [Responsible use and privacy](#-responsible-use-and-privacy)
- [Limitations and future improvements](#-limitations-and-future-improvements)
- [Author](#-author)
- [License](#-license)

---

## ✨ Features

- **IPv4 packet capture:** Uses Scapy to observe packets on a selected network interface.
- **Live dashboard:** A Flask application serves a local browser dashboard.
- **Traffic table:** Shows timestamp, source/destination IP addresses, protocol, destination port, and packet size for captured packets.
- **Anomaly assessment:** Uses an Isolation Forest model to flag observations that differ from its training data.
- **Alert history:** Saves alert records in a local SQLite database.
- **JSON APIs:** Provides endpoints for live traffic, live alerts, alert history, and summary statistics.
- **Responsive interface:** HTML, CSS, and JavaScript dashboard with a dark security-operations theme.

## 🔎 How it works

1. Scapy captures IPv4 packets from the selected interface.
2. The monitor extracts a small set of packet features: packet size, packets per second for a source IP, and destination port.
3. The saved Isolation Forest model assesses the feature values.
4. If the model flags an observation as anomalous, the application may create an alert (with a cooldown to reduce repeated alerts).
5. Alerts are stored in SQLite and displayed on the dashboard.

This is a basic demonstration pipeline. It is not a complete intrusion prevention system and does not block traffic.

## 🧰 Technology stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Scapy | Packet capture and packet-field inspection |
| Npcap | Packet-capture support on Windows |
| Flask | Local web server and JSON APIs |
| scikit-learn | Isolation Forest anomaly model |
| NumPy | Numeric feature handling |
| joblib | Saving/loading the trained model |
| SQLite | Local alert storage |
| HTML, CSS, JavaScript | Dashboard interface |

`pandas` may also be used by the model-training script, depending on the version of `train_model.py` in the repository.

## 🗂️ Project structure

The exact files can vary as the project develops. The structure below reflects the expected layout:

```text
Network-Intrusion-Detection/
├── app.py
├── packet_monitor.py
├── detector.py
├── train_model.py
├── test_detector.py
├── test_dashboard.py
├── test_alert_storage.py
├── check_model.py
├── requirements.txt
├── README.md
├── .gitignore
├── database/
│   └── db_manager.py
├── detection/
│   └── ml_detector.py
├── models/
│   └── anomaly_model.joblib
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── sentinel-logo.png
└── logs/
```

Some test files shown above may be optional. Include only files that actually exist in your local project. The SQLite database is created locally when the application initializes; it is usually not committed to Git.

---

## 💻 Prerequisites

Before installation, prepare the following:

1. **Windows 10/11** (this guide uses Windows 11).
2. **Python 3.10 or newer** recommended. Use a Python version compatible with the installed scikit-learn release.
3. **Git** (optional for running locally, required for the Git workflow below).
4. **Visual Studio Code** or another editor (recommended).
5. **Npcap** installed on Windows for Scapy packet capture. Get it from the official website: <https://npcap.com/>.
6. **Administrator privileges may be required** to install Npcap or capture traffic, depending on system configuration.
7. A network connection and permission to monitor the device/network being tested.

---

## ⚙️ Installation on Windows

### Option 1: Download the repository ZIP

1. Open this repository on GitHub.
2. Click **Code → Download ZIP**.
3. Extract the ZIP file to a folder, for example:

   `C:\Projects\Network-Intrusion-Detection`

4. Open that folder in VS Code (**File → Open Folder**).
5. Continue with [Create a virtual environment](#create-a-virtual-environment).

### Option 2: Clone with Git

Open a terminal in the directory where you want to keep the project. Replace `YOUR-GITHUB-USERNAME` with the repository owner's GitHub username and use the actual repository name if it differs:

```powershell
git clone https://github.com/YOUR-GITHUB-USERNAME/sentinel-network-intrusion-detection.git
cd sentinel-network-intrusion-detection
```

Open the folder in VS Code:

```powershell
code .
```

If `code` is not recognized, open VS Code and choose **File → Open Folder** instead.

### Install Python

1. Download Python from the official site: <https://www.python.org/downloads/>.
2. Run the installer.
3. If offered, select **Add Python to PATH**.
4. Open a new terminal and check:

```powershell
python --version
python -m pip --version
```

If `python` is not recognized, try `py --version` and use `py` instead of `python` in the commands below.

### Install Npcap

1. Visit <https://npcap.com/>.
2. Download and run the Npcap installer.
3. Follow the installer instructions.
4. Restart VS Code after installation.

Npcap is a Windows application/driver, **not** a VS Code extension. Only capture traffic you are authorized to monitor.

### Create a virtual environment

From the project's root folder in the VS Code terminal:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

Or run Python from the environment without activating it:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

### Install dependencies

With the virtual environment activated:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If `requirements.txt` is missing or incomplete, the project's main dependencies are:

```powershell
python -m pip install Flask scapy scikit-learn numpy joblib pandas
```

Install only packages needed by the actual source files. If dependency installation fails, note the full error and your Python version before trying a different version.

### Confirm that the model file exists

The application expects a trained model at:

```text
models/anomaly_model.joblib
```

If the file is included in the repository, it should be present after cloning/downloading. Check the model loader and `train_model.py` instructions if it is missing. Do not assume a newly trained model is accurate merely because it loads.

---

## ▶️ Run SENTINEL

1. Open a terminal at the project root.
2. Activate the virtual environment if needed.
3. Start the app:

```powershell
python app.py
```

4. If packet capture requires elevated privileges, close the app and reopen VS Code/terminal as Administrator only when appropriate for your own device. Do not run untrusted code with elevated privileges.
5. Keep the terminal open while the application is running.
6. Open your browser and visit:

   **Dashboard:** <http://127.0.0.1:5000>

The server is configured to bind to `127.0.0.1`, so it is intended to be accessible only from your own computer.

### Dashboard API endpoints

| Endpoint | Description |
|---|---|
| `/api/traffic` | Recent in-memory captured packet records |
| `/api/alerts` | Recent in-memory alerts |
| `/api/alerts/history` | Recent alerts saved in SQLite |
| `/api/stats` | Counts for in-memory traffic/alerts and stored alerts |

Example: <http://127.0.0.1:5000/api/traffic>

Stop the application by returning to its terminal and pressing **Ctrl + C**.

---

## 🧪 Test the project

Run the tests that exist in your copy of the project from the root directory:

```powershell
python test_detector.py
python test_dashboard.py
python test_alert_storage.py
```

If a test file is not present, skip that command. If the repository includes a model-checking script, you can run:

```powershell
python check_model.py
```

A successful test means the tested code path ran successfully; it does not establish detection accuracy or security effectiveness.

### Safe packet-capture check

You can make ordinary browser requests or visit normal websites while monitoring your own computer. If the dashboard remains empty:

- Confirm Npcap is installed.
- Check the VS Code terminal for capture errors.
- Confirm the correct network interface is selected if your configuration requires it.
- Check permissions and any endpoint-security software settings.
- Do not capture networks or devices without authorization.

---

## 🧠 Train or replace the model

The expected model features are:

1. `packet_size`
2. `packets_per_second`
3. `destination_port`

The current Isolation Forest model is trained on synthetic example data. For meaningful evaluation, collect or obtain an appropriately licensed and labelled dataset, document its source, split it into training and test sets, and evaluate precision, recall, false-positive rate, and other suitable metrics. Avoid using private packet captures without consent and remove identifying information where appropriate.

If you run `train_model.py`, review its source first to understand what data it uses and which model file it overwrites. Keep a backup of the current model before replacing it.

---

## 🛠️ Troubleshooting

### `python` is not recognized

Install Python and enable PATH, or use the Windows launcher:

```powershell
py --version
py -m pip install -r requirements.txt
py app.py
```

### `ModuleNotFoundError`

Activate the project's virtual environment, then install dependencies:

```powershell
python -m pip install -r requirements.txt
```

### Scapy reports that packet capture is unavailable

- Install Npcap from <https://npcap.com/>.
- Restart VS Code/terminal after installation.
- Check capture permissions and the selected interface.
- Follow the official Scapy/Npcap guidance for your Windows configuration.

### Model file not found

Confirm that `models/anomaly_model.joblib` exists. If it does not, inspect `train_model.py` and the expected training data before creating a replacement.

### Dashboard opens but shows no traffic

- Confirm the monitor thread starts without an error.
- Generate ordinary traffic from the same computer.
- Check `/api/traffic`.
- Verify packet capture is using the intended interface.
- Check the terminal for errors.

### Dashboard APIs work but a panel is empty

Open the relevant API endpoint in your browser. If it returns data but the panel is empty, hard-refresh the dashboard with **Ctrl + F5** and inspect the browser developer console for JavaScript errors.

### Port 5000 is already in use

Stop the other process using port 5000, or change the port in `app.py` and visit the matching local URL.

---

## 🍴 Fork this repository

Forking creates your own GitHub copy of a repository so you can experiment without changing the original project.

1. Sign in to GitHub.
2. Open the original SENTINEL repository page.
3. Click **Fork** near the top-right.
4. Choose your GitHub account as the owner.
5. Review the repository name and click **Create fork**.
6. Open your forked repository. Its URL will look like:

   `https://github.com/YOUR-GITHUB-USERNAME/sentinel-network-intrusion-detection`

7. To download your fork to your computer, open a terminal and run:

```powershell
git clone https://github.com/YOUR-GITHUB-USERNAME/sentinel-network-intrusion-detection.git
cd sentinel-network-intrusion-detection
```

Replace `YOUR-GITHUB-USERNAME` with your username and adjust the repository name if you renamed it.

### If you want to contribute changes back

1. Create a new branch.
2. Make and test your changes.
3. Commit and push the branch to your fork.
4. Open a **Pull request** from your fork to the original repository.
5. Describe what changed and what you tested.

If you are the owner of your own fork, you can commit and push directly to it if you prefer.

---

## 🤝 Contributing

Suggestions and improvements are welcome. For substantial changes:

1. Open an issue describing the proposed change.
2. Create a branch for the work.
3. Keep changes focused and document new dependencies.
4. Add or update tests where practical.
5. Clearly document limitations and test results.

Do not submit credentials, personal packet captures, API keys, or other sensitive data.

---

## 🔐 Responsible use and privacy

- Use SENTINEL only on devices and networks you own or are explicitly authorized to monitor.
- Packet metadata can contain sensitive information such as IP addresses and destinations. Handle logs and captures responsibly.
- Do not commit private captures, credentials, secrets, or personal information to GitHub.
- This application is a monitoring prototype; it does not block packets or replace a firewall, endpoint protection, or a professionally validated IDS.
- Alerts are heuristic/model-based indicators, not confirmed incidents.
- Do not expose the development server publicly without a security review.

## ⚠️ Limitations and future improvements

Current limitations:

- The model uses synthetic training data and has not been validated on representative labelled real-world traffic.
- Only a small set of packet features is used.
- The capture code currently focuses on IPv4 packets.
- Anomaly detection may generate false positives and false negatives.
- The dashboard status indicates API connectivity, not necessarily that packet capture is healthy.
- The project is not intended for production deployment.

Possible future improvements:

- Add capture-health status and interface selection.
- Evaluate the model using a documented, labelled dataset.
- Add model evaluation metrics and a reproducible training workflow.
- Improve alert prioritization and configurable thresholds.
- Add structured logging, configuration files, and more automated tests.
- Add data retention controls and a privacy-conscious export function.

---

## 👨‍💻 Author

**Bidyadhar Jena**

Project: **SENTINEL — Network Traffic Monitoring & Intrusion Detection System Using Python and Machine Learning**

To add your verified profiles, edit this section with your own profile URLs:

- GitHub: `https://github.com/Bidyadhar-Jena`
- LinkedIn: `https://www.linkedin.com/in/bidyadhar-jena-919593379`

Replace the placeholders with your actual profile links before publishing. Do not include private contact information unless you intentionally want it public.

---

## 📄 License

No license is specified by this README. Before publishing, choose a license if you want others to have explicit permission to use, modify, and redistribute the code. For example, you can add an MIT License by creating a `LICENSE` file containing the appropriate license text and your chosen copyright notice.

Until a license is added, do not assume that the repository is open-source licensed.
