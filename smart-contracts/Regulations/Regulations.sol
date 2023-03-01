// SPDX-License-Identifier: GPL-3.0 specifies the license for the Solidity code

// The pragma directive specifies the version of Solidity to be used for the contract
pragma solidity >=0.8.2 <0.9.0;


contract Regulations{

    address public government_address;

    struct Standard{
        string standard_name;
        string description;        
    }

    Standard[] public standards;

    constructor() {
        government_address = msg.sender;
    }


    function addStandard(string memory _standard_name, string memory _description) public {
        require(msg.sender == government_address, "Only government can add standards");
        standards.push(Standard(_standard_name, _description));
    }

}