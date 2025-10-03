# Inventory Management System

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