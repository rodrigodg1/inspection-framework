# Inspection Request Smart Contract

This Solidity smart contract provides a system for requesting inspections of certain locations. It also allows the site manager to manage the list of valid locations.

## Usage

To use this contract, follow these steps:

1. Deploy the contract to an Ethereum network using a Solidity compiler.
2. Call the constructor function with a list of valid locations.
3. Users can call the `InpectionRequest` function to submit an inspection request for a valid location. They must provide the date of the inspection and the location they want to inspect.
4. The manager can call the `updateValidLocations` function to update the list of valid locations.
5. Anyone can call the `getValidLocations` function to retrieve the list of valid locations.
6. Anyone can call the `getRequests` function to retrieve the list of inspection requests.

## Smart Contract Explanation

The smart contract consists of the following elements:

### Variables

- `valid_locations`: a private array of valid locations that only the contract can access.
- `manager`: a public variable that stores the address of the manager.
- `requests`: a public array of inspection requests.

### Struct

The `Request` struct represents a request for inspection. It contains the following elements:

- `requester`: the address of the user who submitted the request.
- `date`: the date of the inspection.
- `location`: the location to be inspected.

### Constructor

The constructor function initializes the contract with a list of valid locations and sets the manager's address to the creator of the contract.

### Functions

- `InpectionRequest`: creates an inspection request and adds it to the requests array if the requested location is valid.
- `updateValidLocations`: allows the manager to update the list of valid locations.
- `getValidLocations`: returns the list of valid locations.
- `getRequests`: returns the list of inspection requests.

Each function is documented with a brief description of what it does, the input parameters it requires, and what it returns. 

## Prerequisites

- Basic knowledge of Solidity programming language
- Understanding of blockchain technology and smart contracts
- Access to a Solidity compiler and Ethereum network to deploy and interact with the contract
