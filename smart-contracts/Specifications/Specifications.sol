// SPDX-License-Identifier: GPL-3.0 specifies the license for the Solidity code

// The pragma directive specifies the version of Solidity to be used for the contract
pragma solidity >=0.8.2 <0.9.0;


contract Specifications{

    address public manufacturer_address;

    struct Component{
        string component_name;
        string guidelines;
        string fabrication_date;
        
    }
    Component[] public components;



    constructor(string memory _component_name, string memory _guidelines, string memory _fabrication_date) {
        
        manufacturer_address = msg.sender;
        components.push(
            Component(_component_name, _guidelines, _fabrication_date)
        );
        
    }



    function addComponent(string memory _component_name, string memory _guidelines, string memory _fabrication_date) public {
        require(msg.sender == manufacturer_address, "Only manufacturer can add components");
        components.push(
            Component(_component_name, _guidelines, _fabrication_date)
        );
    }




    function getComponents() public view returns (Component[] memory) {
        return components;
    }



}