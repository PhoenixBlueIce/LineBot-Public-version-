# Raiden - LINE Bot System

Raiden is a personal software development platform built as a LINE Bot, designed to integrate multiple backend services such as weather queries, SQLite-based joke retrieval, and future draw-based features.

This project focuses on:
- Data processing
- Modular system design
- API integration
- Backend service development

## Features

- Weather Service
  - Query weather by city
  - Parse and format JSON weather data

- Joke Service
  - SQLite-based joke database
  - Random joke retrieval
  - Category-based design (extensible)

- Router System
  - Handles text and postback events
  - Routes user input to different services

## Tech Stack

- Python
- Flask
- SQLite
- JSON Data Processing
- LINE Messaging API

## Architecture

app.py → router → service layer → data layer

- app.py: handles LINE webhook
- router: routes user input
- services: business logic (weather, joke)
- data: JSON / SQLite

## Version History

- v0.1: LINE webhook + echo
- v0.2: router architecture
- v0.3: joke service (JSON)
- v0.4: weather service
- v0.5: weather system v1 completed
- v0.6: joke service migrated to SQLite

## Notes

The deployment setup was provided as a base template. 
This bot demonstrates backend logic including weather queries, joke retrieval, and modular service design.

This repository focuses on:
- Custom-developed services
- Data processing logic
- System architecture

All included code is fully understood and can be explained in detail.

## Future Work

- Category-based joke routing
- Full Taiwan weather aggregation
- Database expansion
- Advanced error handling
