// SPDX-License-Identifier: GPL-3.0 specifies the license for the Solidity code

// The pragma directive specifies the version of Solidity to be used for the contract
pragma solidity >=0.8.2 <0.9.0;


// ResultsContract is a smart contract that stores the results of inspections
contract ResultsContract {
    // Private array of valid locations that only the contract can access
    string[] private valid_locations;

    // Public variable that stores the address of the manager
    address public manager;

    // Result is a struct that represents the results of an inspection
    struct Result {
        address inspector;
        string location;
        string result;
    }

    // Public array of inspection results
    Result[] public results;

    // Constructor function that initializes the contract with a list of valid locations and sets the manager's address to the creator of the contract
    constructor(string[] memory _valid_locations) {
        valid_locations = _valid_locations;
        manager = msg.sender;
    }

    // InspectionResult function creates an inspection result and adds it to the results array if the location is valid
    function InspectionResult(string memory _InspectionPlace, string memory _result) public returns (bool) {
        bool isValidLocation = false;

        // Loop through the valid_locations array to see if the location is in the array
        for(uint i = 0; i < valid_locations.length; i++) {
            // Compare the hash of the current valid location with the hash of the location
            if(keccak256(bytes(valid_locations[i])) == keccak256(bytes(_InspectionPlace))) {
                // If the hashes match, set isValidLocation to true and exit the loop
                isValidLocation = true;
                break;
            }
        }

        // If the location is not valid, throw an error
        require(isValidLocation, "Invalid location");

        // Add a new Result to the results array with the inspector's address, location of inspection, and the result of the inspection
        results.push(Result(msg.sender, _InspectionPlace, _result));
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
}