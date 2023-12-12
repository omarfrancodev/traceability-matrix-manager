# Traceability Matrix Manager API

## Description

The Traceability Matrix API is tool designed provide the functionality to manage projects, traceability of records, and users with different roles. It provides a flexible and secure environment for tracking project-related activities.

## Features and Highlights

- User roles: Admin, Team Member, Guest.
- Fine-grained permissions for each user role.
- Project and record management.
- Tracking record relationships by key.
- Event recording for user actions.
- API documentation using Postman collections.

## Technologies Used

- Django
- Django REST Framework
- Djoser
- Django REST framework simple JWT
- Postman (for API testing and documentation)

## Version

Current version of the release: [v1.0.0-beta](https://github.com/omarfrancodev/traceability-matrix-manager-API/releases/tag/v1.0.0-beta)

## API Documentation

API documentation is available in Postman collections:

- [Auth and User](https://restless-space-975505.postman.co/workspace/Tracability-Matrix-Manager~6b01404e-d807-4120-b704-6b66a7e6d756/collection/19039658-b999343e-bae2-4e5e-9cf6-e76d5fd2941a?action=share&creator=19039658)
- [Event Record History](https://restless-space-975505.postman.co/workspace/Tracability-Matrix-Manager~6b01404e-d807-4120-b704-6b66a7e6d756/collection/19039658-4d1a0b7b-db46-4ca1-bbd0-423617326fe6?action=share&creator=19039658)
- [Project](https://restless-space-975505.postman.co/workspace/Tracability-Matrix-Manager~6b01404e-d807-4120-b704-6b66a7e6d756/collection/19039658-c3b17e82-2bc1-400e-a7e8-198490822c13?action=share&creator=19039658)
- [Record](https://restless-space-975505.postman.co/workspace/Tracability-Matrix-Manager~6b01404e-d807-4120-b704-6b66a7e6d756/collection/19039658-5c5127c7-96a5-46e7-88d9-b1d4f1053258?action=share&creator=19039658)
- [User General for Admin](https://restless-space-975505.postman.co/workspace/Tracability-Matrix-Manager~6b01404e-d807-4120-b704-6b66a7e6d756/collection/19039658-701c31c2-8117-4efc-ba86-e6074c9f8200?action=share&creator=19039658)

## Getting Started

### Installation

1. Clone the repository.
  ```bash
  git clone https://github.com/omarfrancodev/traceability-matrix-manager-API.git
  ```
2. Install dependencies.
  ```bash
  cd traceability-matrix-manager-API
  pip install -r requirements.txt
  ```
3. Apply migrations.
  ```bash
  python manage.py migrate
  ```
4. Run the development server.
  ```bash
  python manage.py runserver
  ```
### Important
A `.env` file must be created in the root directory of the project and the environment variables must be configured according to the settings of the database to be used.

## Usage
Access the API documentation to explore available endpoints and actions.
