# MAMAN-TRACKER

An educational project exploring browser geolocation behavior and privacy boundaries

### Overview

This project is a small, educational web application built to demonstrate how modern browsers expose location-related information at different levels of precision.

The goal is to help developers, security practitioners, and privacy engineers understand:

- What location data is implicitly available during a web request

- What location data is explicitly protected by browser permission models

- How secure origins and user interaction affect sensitive API access

This project is intended strictly for learning, demonstration, and defensive research.

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

### Why This Matters

Many users assume that denying a location permission prompt fully hides their location.
In reality, permissions control precision, not existence.

Understanding this distinction is important for:

- Privacy engineering and consent design

- Threat modeling and risk assessment

- Secure web application development

- Browser security education and training

### Ethical Use Statement

This project:

- Is designed for educational and awareness purposes only

- Must be used only on systems you own or have permission to test

- Is not intended for surveillance, tracking, or misuse

All demonstrations should be conducted responsibly and transparently.

#### Technologies Used

- Python (Flask)

- HTML / JavaScript

- Browser Geolocation API

- Secure transport (HTTPS via tunneling or certificates)

### Related Write-Up

A detailed explanation of the concepts and lessons from this project is available here:
Medium Article: <https://abhayal.medium.com/what-browser-location-access-really-exposes-an-educational-security-perspective-82537cb74fa0>

### Disclaimer

This repository is provided “as is” for educational purposes.
The author assumes no responsibility for misuse or policy violations.
