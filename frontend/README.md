# Darukaa.Earth

Environmental project management dashboard for monitoring restoration projects, geographic sites, carbon storage, and biodiversity.

## Features

- Administrator login
- Environmental project management
- Geographic site management
- Interactive map using Leaflet
- Polygon-based site boundaries
- PostgreSQL database
- PostGIS geospatial storage
- Carbon and biodiversity indicators
- Environmental analytics dashboard

## Technology Stack

### Frontend
- HTML
- CSS
- JavaScript
- Leaflet
- Chart.js

### Backend
- Python
- Flask
- Flask-SQLAlchemy

### Database
- PostgreSQL
- PostGIS

## Architecture

The frontend communicates with the Flask REST API.

The Flask backend stores project and site information in PostgreSQL.

Geographic site boundaries are stored as PostGIS geometry polygons.

Frontend → Flask API → PostgreSQL/PostGIS

## Database

Main tables:

- `project`
- `site`
- `location`
- `place`
- `review`
- `user`

The `site` table stores geographic boundaries using PostGIS geometry.

## Run Locally

### Backend

```bash
cd backend
python app.py