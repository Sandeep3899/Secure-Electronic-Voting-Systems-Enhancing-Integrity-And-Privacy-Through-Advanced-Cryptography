# Secure-Electronic-Voting-Systems-Enhancing-Integrity-And-Privacy-Through-Advanced-Cryptography

# 🗳 Secure Electronic Voting System using BFV Homomorphic Encryption

## 📌 Project Overview
This project implements a **secure electronic voting system** using **Django** and **Pyfhel's BFV Homomorphic Encryption** to ensure voter privacy, vote integrity, and encrypted vote tallying. The system prevents unauthorized access, maintains data confidentiality, and guarantees a **tamper-proof election process**.

## 🚀 Features
- **Homomorphic Encryption**: Encrypts votes and allows computations without decryption.
- **Django-Based Secure Backend**: Manages authentication, CSRF protection, and encrypted vote storage.
- **Voter & Admin Dashboards**: Provides user-friendly interfaces for **casting votes, managing elections, and tallying results**.
- **Automatic Vote Tallying**: Uses **Pyfhel's homomorphic addition** to compute results securely.
- **PDF Generation for Reports**: Exports **election results** in PDF format.
- **Scalability**: Supports SQLite for development and **MySQL for production**.

---

## ⚙️ Technologies Used

### **Backend**
- **Django (3.1.1)** - Python web framework for secure authentication, CSRF protection, and data management.
- **MySQL Connector (2.2.9)** - Python driver for MySQL, used for **database interactions**.
- **Virtualenv (20.0.31)** - Isolated environment for managing project dependencies.

### **Frontend**
- **HTML5, CSS3, JavaScript** - UI development for voter and admin dashboards.
- **Bootstrap** - Responsive web design.

### **Database**
- **SQLite (Development)** - Default lightweight database.
- **MySQL (Production)** - Optional for scalability.

### **Encryption**
- **Pyfhel** - Python library for Fully Homomorphic Encryption (BFV scheme) to perform encrypted computations.

### **Other Libraries**
- **Pillow (7.2.0)** - Image processing for user profile pictures.
- **Django RenderPDF (3.0.1)** - PDF report generation for election results.
- **Requests (2.24.0)** - Handles API calls for external services.

---
