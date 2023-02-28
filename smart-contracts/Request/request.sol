// SPDX-License-Identifier: GPL-3.0 specifies the license for the Solidity code

// The pragma directive specifies the version of Solidity to be used for the contract
pragma solidity >=0.8.2 <0.9.0;

// RequestContract is a smart contract
contract RequestContract {
        // Private array of valid locations that only the contract can access
    string[] private valid_locations;

    // Public variable that stores the address of the manager
    address public manager;

    // Request is a struct that represents a request for inspection
    struct Request {
        address requester;
        string date;
        string location;
    }

    // Public array of inspection requests
    Request[] public requests;

    // Constructor function that initializes the contract with a list of valid locations and sets the manager's address to the creator of the contract
    constructor(string[] memory _valid_locations) {
        valid_locations = _valid_locations;
        manager = msg.sender;
    }

    // InpectionRequest function creates an inspection request and adds it to the requests array if the requested location is valid
    function InpectionRequest(string memory _InspectionPlace, string memory _date) public returns (bool) {
        bool isValidLocation = false;

        // Loop through the valid_locations array to see if the requested location is in the array
        for(uint i = 0; i < valid_locations.length; i++) {
            // Compare the hash of the current valid location with the hash of the requested location
            if(keccak256(bytes(valid_locations[i])) == keccak256(bytes(_InspectionPlace))) {
                // If the hashes match, set isValidLocation to true and exit the loop
                isValidLocation = true;
                break;
            }
        }

        // If the requested location is not valid, throw an error
        require(isValidLocation, "Invalid location");

        // Add a new Request to the requests array with the requester's address, date of inspection, and location of inspection
        requests.push(Request(msg.sender, _date, _InspectionPlace));
        return true;
    }

    // UpdateValidLocations function allows the manager to update the list of valid locations
    function updateValidLocations(string[] memory newLocations) public {
        // Only the manager can update the valid locations list
        require(msg.sender == manager, "Only manager can update valid locations");
        valid_locations = newLocations;
    }

    // GetValidLocations function returns the list of valid locations
    function getValidLocations() public view returns (string[] memory) {
        return valid_locations;
    }

    // GetRequests function returns the list of inspection requests
    function getRequests() public view returns (Request[] memory) {
        return requests;
    }

}