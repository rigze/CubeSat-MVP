# CubeSat MVP 

This repository contains a minimum viable prototype (MVP) for a CubeSat
communication and logging system.

## Purpose
The goal of this project is to explore how telemetry, commands, and logs
flow between a CubeSat and a ground station, with a focus on clarity,
fault visibility, and future security extensions.

## Structure
- cubesat/         : satellite-side logic and telemetry generation
- ground_station/  : ground-side reception and control logic
- attacker/        : simulated threat or interference scenarios
- shared/          : common data structures and utilities

## Current Status
Early-stage architecture and experimentation.

## Planned Extensions
- Communication security and authentication
- Fault injection and recovery testing
- More realistic channel simulation
