# Inventory Management System - StockMaster

A Flask-based web application for managing inventory across multiple locations. This system allows tracking of products, locations, and product movements between locations.

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



  <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/431951bc-3b34-447d-b1d3-72954dab563f" />
  <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a35ac618-2d4a-4a84-8d93-4160cc5b7519" />
  <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a6609829-b65a-4cfa-ab79-72a6bc18bd3c" />
  <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/2f18fe13-7d15-49d7-95d0-c1e3a80c9d0c" />
  <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c005639a-e8af-4953-ba71-c1b53e944f43" />




