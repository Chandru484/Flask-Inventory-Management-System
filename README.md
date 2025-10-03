# Inventory Management System - StockMaster

A Flask-based web application for managing inventory across multiple locations. This system allows tracking of products, locations, and product movements between locations.This application does a CRUD operations of Create,Read,Update,Delete in inventory system.

## Features

- Product management (Add, Edit, View, Delete)
- Location management (Add, Edit, View, Delete)
- Product Movement tracking (Add, Edit, View, Delete)
- Inventory Balance Report showing product quantities at each location
- Bootstrap-based responsive UI

## Database Schema

- **Product**: product_id (text/varchar as primary key)
- **Location**: location_id (text/varchar as primary key)
- **ProductMovement**: movement_id, timestamp, from_location, to_location, product_id, qty
  - from_location or to_location can be NULL
  - If from_location is NULL → product moved into location
  - If to_location is NULL → product moved out of location

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository or download the source code

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate

3. To Run this project:
   ```bash
   python app.py


<img width="1907" height="968" alt="image" src="https://github.com/user-attachments/assets/537cbb6a-11ef-4fbf-ba36-fbb571b45f70" />
<img width="1888" height="977" alt="image" src="https://github.com/user-attachments/assets/3f2a7ebc-d745-4465-9e25-6cf9908a09be" />
<img width="1895" height="975" alt="image" src="https://github.com/user-attachments/assets/8dfa028a-7386-471c-a322-4352b6ed81c1" />
<img width="1880" height="970" alt="image" src="https://github.com/user-attachments/assets/8913f639-7618-4e71-9f4c-6bfaadc86ea5" />
<img width="1886" height="976" alt="image" src="https://github.com/user-attachments/assets/59334570-d88b-4af5-afca-3766d48ea378" />
<img width="1878" height="974" alt="image" src="https://github.com/user-attachments/assets/8cd7c664-6081-4ba6-a0ca-df3c3a0ac6f4" />










