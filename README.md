# GseCart Backend - Contact Management Service

This project implements a web service for  that identifies and manages customer identities across multiple purchases, even when different contact details (email and phone number) are used. The solution consolidates customer information and ensures primary and secondary contact records are linked and appropriately handled.

## Project Overview

The goal of this project is to create a Django-based API that resolves and consolidates customer contact details (emails and phone numbers) by linking them to a primary contact. The application supports managing primary and secondary contact records.

### Features:
- **Primary and Secondary Contact Management**: Consolidates contacts under a primary record with support for multiple secondary contacts.
- **Flexible Matching Logic**: Links contacts based on matching emails or phone numbers.
- **Error Handling**: Validates that either an email or phone is provided for each request.
- 
  This project is built using Django and Django Rest Framework (DRF) to create a robust and efficient API for managing data. The key features of the project include:

Django ORM: Utilized to interact with the database. Django ORM allows for seamless integration between the database and the Django models, providing a powerful way to query and manage data.
  
Django Rest Framework (DRF): Used for building RESTful APIs. In this project, serializers from DRF are utilized to efficiently handle querysets and convert them into JSON format for smooth communication between the server and the client.
## Technology Stack

- **Backend Framework**: Django, Django REST Framework
- **Database**: SQLite (used as the default database for simplicity)
- **Phone Number Handling**: `django-phonenumber-field`
- **Containerization**: Docker (optional, for deployment)
- **Version Control**: GitHub for source code management

## Setup Instructions

### Prerequisites
- Python 3.x
- Django 4.x
- Django REST Framework
- SQLite (default for development)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/gseCart.git
