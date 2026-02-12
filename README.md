Developer Details

Name: Anshul Hiremath
University: Dayananda Sagar University
Year: Fourth Year Engineering Student

Departure Times Service

This repository contains my submission for the KJBN Labs coding assessment. I selected the Departure Times problem statement and completed it under the Back end track.

The goal of this project is to build a backend service that provides real time public transportation departure information based on a user’s location. The service integrates with the Transport for London public Unified API and returns nearby transport stops along with upcoming departures in a structured and readable format.

Problem Selection

Chosen question: Departure Times
Track: Back end track

The service accepts geographic coordinates and returns the nearest transport stations and their upcoming departures.

Live Deployment

Public URL
https://departure-time.onrender.com

Opening the link automatically redirects to the API documentation where the endpoint can be tested interactively.

Main endpoint example
/departures?lat=51.5074&lon=-0.1278

Project Overview

The application is built using FastAPI and is structured as a clean backend service. When a request is received, the system performs the following steps:

The user sends latitude and longitude
The server finds nearby transport stops using the TfL StopPoint API
The server fetches arrival predictions for each stop
The response is filtered, sorted and formatted
A structured JSON response is returned

The service currently supports multiple transport modes including Underground, Bus and DLR.

Architecture

The codebase is separated into logical layers to keep the system maintainable and clear.

main.py initializes the application and registers routes
config.py loads environment variables
logger.py configures structured logging
routes/departures.py handles request processing
services/tfl_client.py communicates with the TfL API
tests/test_departures.py validates endpoint behavior

This separation ensures the API layer is independent from the external data provider.

Technology Stack

Python
FastAPI
httpx for async HTTP requests
Uvicorn ASGI server
Pytest for testing
Render for deployment

Running the Project Locally

1 Install dependencies
pip install -r requirements.txt

2 Create environment file
Create a .env file in the project root and add

TFL_API_KEY=your_api_key_here
TFL_BASE_URL=https://api.tfl.gov.uk

3 Start the server
uvicorn app.main:app --reload

4 Open documentation
http://127.0.0.1:8000/docs

API Usage

Example request
GET /departures?lat=51.5074&lon=-0.1278

A few values for testing:

Central London 
51.5074, -0.1278

Bank financial district
51.5133, -0.0890

London Bridge
51.5055, -0.0865

The response includes the location, nearby stations and upcoming departures sorted by time.

Testing

Tests verify the endpoint contract and input validation.

Run tests with
pytest

The tests check
Valid request returns success
Missing parameters return validation error
Invalid parameters return validation error

Logging and Error Handling

The application includes structured logging for incoming requests and external API calls. Network errors, invalid API responses and unexpected conditions are handled gracefully and mapped to meaningful HTTP responses.

Deployment

The service is deployed on Render as an ASGI application. The root route redirects to the API documentation so reviewers can immediately interact with the endpoint without additional setup.

Environment variables are securely configured in the hosting platform and not stored in the repository.



