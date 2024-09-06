# GraphQL API for User and Contract Management

This README provides information on how to use the GraphQL API implemented for managing users and contracts. The API allows you to perform CRUD operations on both `User` and `Contract` models.
## Table of contents
1. [Application details](#applicatin-details)
   1. [Technology used](#technology-used)
   2. [Deployment](#deployment)
   3. [Queries and mutations](queries.md)
2. [How to run the application](#how-to-run-the-application)
3. [Authentication](#authentication)
    1. [Create user](#1-create-user)
    2. [Obtain token](#2-obtain-token)
    3. [List user with bearer token](#3-list-users-with-bearer-token)
4. [Database](#database)
5. [Deployment](#deployment)

## Applicatin details
This application provides a CRUD for table Users and Contracts in wich a user can have multiple contracts and contracts can have only a user.

### Technology used
For this appplication was obly used `python` and `django` to implement graphql using `graphene-django`package (bff) that facilitates the implementation. 

## How to run the application

To run the application there is no need to create a container or many configuration files. 
First you should create a virtual environment and activate it:
```bash
$ python3 -m venv venv
$ source venv/bin/activate
```
Then you should install the requirements:
```bash
(venv)/path/to/project/$ pip install -r requirements.txt 
```
After installed the packages run the application with the following command:
```bash
(venv)/path/to/project/$ python manage.py runserver
```
## Authentication

### 1. Create user
```bash
curl -X POST http://localhost:8000/graphql/ \
-H "Content-Type: application/json" \
-d '{"query": "mutation { createUser(input: {username: \"user1\", email: \"user1@example.com\", password: \"password123\"}) { user { id username email } success message } }"}'
```

### 2. Obtain token
```bash
curl -X POST http://localhost:8000/graphql/ \
-H "Content-Type: application/json" \
-d '{"query": "mutation { tokenAuth(username: \"user1\", password: \"password123\") { token } }"}'
```

### 3. List Users with Bearer Token
Replace `YOUR_JWT_TOKEN` with the token obtained from the previous step.
```bash
curl -X POST http://localhost:8000/graphql/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-d '{"query": "query { allUsers { id username email } }"}'
```
## Database 

For the database creation was used AWS RDS and with TCP connection from any IP address to facilitate and speed of the project. 
With it was used the `dj-database-url` package to use the database url to connect with the AWS RDS database. 

```bash
# example of variable with connection. 
DATABASE_URL=postgres://myuser:mypassword@myrdsinstance.amazonaws.com:5432/mydatabase
```
## Deployment

For deployment was used AWS ec2 service to deploy the application using Ubuntu instance. 
Where I did a clone directly into the ec2 terminal from aws.

