# GraphQL API for User and Contract Management

This README provides information on how to use the GraphQL API implemented for managing users and contracts. The API allows you to perform CRUD operations on both `User` and `Contract` models.

## Queries

### Get All Users

**Query:**
```graphql
query {
  allUsers {
    id
    username
    email
  }
}
```
Description: Fetches a list of all users with their id, username, and email.

### Get All Contracts
***Query:***
```graphql
query {
  allContracts {
    id
    description
    userId
    createdAt
    fidelity
    amount
  }
}
```
Description: Fetches a list of all contracts with details including id, description, userId, createdAt, fidelity, and amount.

### Get a Single User by ID
***Query:***
```graphql
query {
  getUser(id: 1) {
    id
    username
    email
  }
}
```
Description: Fetches a single user by their id. Replace 1 with the actual user ID.

### Get a Single Contract by ID
***Query:***
```graphql
query {
  getContract(id: 1) {
    id
    description
    userId
    createdAt
    fidelity
    amount
  }
}
```
Description: Fetches a single contract by its id. Replace 1 with the actual contract ID.

### Get Contracts by User ID
***Query:***
```graphql
query {
  getContractsByUser(userId: 1) {
    contracts {
      id
      description
      userId
      createdAt
      fidelity
      amount
    }
    nextToken
  }
}
```
Description: Fetches contracts associated with a specific user by their userId. Replace 1 with the actual user ID.

## Mutations

### Create a User
***Mutation:***
```graphql
mutation {
  createUser(input: {
    username: "newuser",
    email: "newuser@example.com",
    password: "password123"
  }) {
    user {
      id
      username
      email
    }
    success
    message
  }
}
```
Description: Creates a new user. Replace username, email, and password with the desired values.

### Update a User
***Mutation:***
```graphql
mutation {
  updateUser(id: 1, input: {
    username: "updateduser",
    email: "updateduser@example.com",
    password: "newpassword123"
  }) {
    user {
      id
      username
      email
    }
    success
    message
  }
}
```
Description: Updates an existing user by id. Replace 1 with the user ID and provide the updated username, email, and password.

### Delete a User
***Mutation:***
```graphql
mutation {
  deleteUser(id: 1) {
    success
    message
  }
}
```
Description: Deletes a user by id. Replace 1 with the user ID.

### Create a Contract
***Mutation:***
```graphql
mutation {
  createContract(input: {
    description: "New contract",
    userId: 1,
    fidelity: 10,
    amount: 100.00
  }) {
    contract {
      id
      description
      userId
      createdAt
      fidelity
      amount
    }
  }
}
```
Description: Creates a new contract. Replace description, userId, fidelity, and amount with the desired values.

### Update a Contract
***Mutation:***
```graphql
mutation {
  updateContract(id: 1, input: {
    description: "Updated contract",
    fidelity: 20,
    amount: 150.00
  }) {
    contract {
      id
      description
      userId
      createdAt
      fidelity
      amount
    }
  }
}
```
Description: Updates an existing contract by id. Replace 1 with the contract ID and provide the updated description, fidelity, and amount.

### Delete a Contract
***Mutation:***
```graphql
mutation {
  deleteContract(id: 1) {
    success
    message
  }
}
```
Description: Deletes a contract by id. Rep