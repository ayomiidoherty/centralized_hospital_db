# centralized_hospital_db
A Flask-based API for managing hospital data, providing secure access to patient medical records, and facilitating inter-hospital data sharing.

## Table of Contents
- [About](#about)
- [Features](#features)
- [Technologies](#technologies)
- [Setup](#setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Future Improvements](#future-improvements)
- [License](#license)
- [Contact](#contact)

## About
The Centralized Hospital Database API is a RESTful API designed to manage patient medical records, facilitate access requests between hospitals, and ensure secure access to sensitive data. This API is built with Flask and MongoDB, enabling smooth integration with hospital systems.

## Features
- **Secure Access**: Hospitals must request and get approval to access patient records.
- **Medical Records Management**: Create, update, delete, and fetch patient medical records.
- **Role-Based Access Control**: Administrators can approve access requests and manage records.
- **Inter-Hospital Collaboration**: Hospitals can request access to records, which are granted upon approval.

## Technologies
- **Flask**: Lightweight web framework for building the API.
- **MongoDB**: NoSQL database for storing patient records and access requests.
- **Python**: Programming language used to implement the backend.
- **Postman**: Used for testing the API endpoints.
- **Render**: Platform for deploying the Flask application.

## Setup

### 1. Clone the repository:
```bash
git clone https://github.com/ayomiidoherty/hospital-db-api.git
