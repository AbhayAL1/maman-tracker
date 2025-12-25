# MAMAN-TRACKER

An educational project exploring browser geolocation behavior and privacy boundaries

---

### Overview

This project is a small, educational web application built to demonstrate how modern browsers expose location-related information at different levels of precision.

The goal is to help developers, security practitioners, and privacy engineers understand:

- What location data is implicitly available during a web request

- What location data is explicitly protected by browser permission models

- How secure origins and user interaction affect sensitive API access

This project is intended strictly for learning, demonstration, and defensive research.

---

### What This Project Demonstrates

The application highlights two distinct layers of location exposure:

#### 1. Network-Level Location (IP-Based, Approximate)

- Derived from the client’s IP address

- Does not require user permission

- Provides coarse geographic information (e.g., city or region)

#### 2. Browser-Gated Location (GPS / Sensor-Based, Precise)

- Requires explicit user consent

- Protected by browser security policies

- Only accessible on secure origins (HTTPS) and after user interaction

By presenting both side by side, the project illustrates that location access is not binary, but layered.

---

### Why This Matters

Many users assume that denying a location permission prompt fully hides their location.
In reality, permissions control precision, not existence.

Understanding this distinction is important for:

- Privacy engineering and consent design

- Threat modeling and risk assessment

- Secure web application development

- Browser security education and training

Here is a **professional, clear, and repository-ready rewrite** of your installation section.
This is suitable for GitHub and aligns with the tone of the rest of your project documentation.

---

### Installation and Setup

Follow the steps below to run the application locally.

#### Prerequisites

* Python 3.x
* `pip`
* Git
* (Optional) ngrok account for HTTPS tunneling

---

#### Step 1: Clone the Repository

```
git clone https://github.com/AbhayAL1/maman-tracker.git
cd maman-tracker
```

---

#### Step 2: Set Execute Permissions

```
chmod +x maman_tracker.py
```

---

#### Step 3: Install Dependencies

```
pip3 install flask
```

---

#### Step 4: Run the Application

```
python3 maman_tracker.py
```

By default, the application starts on the configured port and is accessible via `http://localhost`.

---

### Accessing Precise Location Data (Important)

Modern browsers restrict access to precise geolocation data to **secure origins (HTTPS)**.

If precise location access is not prompted or is blocked when running locally, use **ngrok** to expose the application over HTTPS.

#### Using ngrok

1. Start the application locally.
2. In a new terminal window, run:

   ```
   ngrok http <port>
   ```
3. Open the **HTTPS URL** provided by ngrok in your browser.

This ensures the browser allows geolocation permission prompts as intended.

---

### Notes

* Location access always requires explicit user consent.
* This project is intended for educational and defensive research purposes only.
* Test only on systems and networks you own or have permission to use.

---

### Ethical Use Statement

This project:

- Is designed for educational and awareness purposes only

- Must be used only on systems you own or have permission to test

- Is not intended for surveillance, tracking, or misuse

All demonstrations should be conducted responsibly and transparently.

---

#### Technologies Used

- Python (Flask)

- HTML / JavaScript

- Browser Geolocation API

- Secure transport (HTTPS via tunneling or certificates)

---

### Related Write-Up

A detailed explanation of the concepts and lessons from this project is available here:
Medium Article: <https://abhayal.medium.com/what-browser-location-access-really-exposes-an-educational-security-perspective-82537cb74fa0>

---

### Disclaimer

This repository is provided “as is” for educational purposes.
The author assumes no responsibility for misuse or policy violations.
