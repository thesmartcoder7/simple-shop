# Robust Bicycle Shop

## Introduction

This project is an e-commerce platform designed for Marcus, a bicycle shop owner, to expand his business into online sales. The platform is built with flexibility and customization in mind, allowing customers to create highly personalized bicycles while also providing Marcus with the tools to manage his inventory and pricing effectively.

## Key Features

1. **Product Customization**: Customers can build their own bicycles by selecting from a variety of options for different parts (e.g., frame type, frame finish, wheels, rim color, chain).

2. **Dynamic Pricing**: The system calculates the total price based on the selected options, taking into account complex pricing rules that may depend on combinations of choices.

3. **Inventory Management**: Marcus can mark certain options as "out of stock" to prevent orders for unavailable items.

4. **Compatibility Rules**: The platform enforces rules to prevent incompatible combinations of parts, ensuring that only valid configurations can be ordered.

5. **Expandable Product Range**: While initially focused on bicycles, the system is designed to accommodate future expansion into other sports-related items like skis, surfboards, and roller skates.

6. **Shopping Cart**: Customers can add customized products to their cart and manage their selections before placing an order.

7. **Order Processing**: The system handles the creation and management of orders based on the contents of the shopping cart.

## Technical Overview

The project is built using Django and Django Rest Framework, following a modular architecture that separates concerns into models, serializers, and views:

- **Models**: Define the data structure for products, parts, options, carts, and orders.
- **Serializers**: Handle the conversion of complex data types to Python native datatypes that can then be easily rendered into JSON.
- **Views**: Provide the logic for handling HTTP requests and returning appropriate responses.

The system uses session-based authentication to manage shopping carts and orders, allowing both logged-in and guest users to create and purchase customized bicycles.

The frontend is built using Angular 18.

- [ERD](documentation/ERD.md)
- [Installation](#Installation)
- [Description](documentation/description.md)

## Installation

Clone this project from this repository.

```bash
git clone https://github.com/thesmartcoder7/simple-shop.git
```

Make sure you have docker and docker compose installed as it will make the next step way easier.

Run the following command:

```bash
docker-compose up --build # to start the both the frontend and backend services

docker-compose run backend make test # to run the backend tests

docker-compose down # to stop the application form running.
```

If you run into any errors while running these commands, you might need root persmissions in case you installed docker and docker compose with super user.

Keep in mind that the required dependencies for this project are in their respective folders `frontend` i.e `package.json` and `backend` i.e `requirements.txt` . . . but that is why I decided to use Docker to setup the project with the build command and expose both the frontend and the backend.

