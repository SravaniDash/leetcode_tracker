# Leetcode Tracker

A simple backend API to track Leetcode problems and generate statistics
by difficulty and topic.

## Tech Stack
- FastAPI
- SQLite
- SQLAlchemy

## Features
- Log solved problems
- View all logged problems
- Aggregate stats by difficulty and topic

## What is FastAPI?
FastAPI - modern Python web framework used to build APIs. This project uses FastAPI to expose REST endpoints for logging Leetcode problems and retrieving stats. FastAPI provides automatic API documentation via Swagger UI. FastAPI only handles requests/responses, not the actual data. 