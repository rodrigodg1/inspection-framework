Specifications Contract
-----------------------

This is a Solidity smart contract that defines a Specifications contract. This contract allows a manufacturer to add and retrieve components with their respective specifications, such as component name, guidelines, and fabrication date.

Variables
---------

`manufacturer_address`
`address public manufacturer_address` is a public variable that stores the address of the manufacturer who deploys the contract.

Component Struct
-----------------

`struct Component` defines the specifications of a component with the following attributes:

* `component_name`: string that stores the name of the component.
* `guidelines`: string that stores the guidelines of the component.
* `fabrication_date`: string that stores the date when the component was fabricated.

`components`
`Component[] public components` is a public array that stores the list of components added by the manufacturer.

Constructor
-----------

The constructor function is called when the contract is deployed and initializes the components array with the initial component added by the manufacturer. The constructor takes in the following parameters:

* `_component_name`: string that stores the name of the initial component.
* `_guidelines`: string that stores the guidelines of the initial component.
* `_fabrication_date`: string that stores the date when the initial component was fabricated.

Functions
---------


`addComponent(string memory _component_name, string memory _guidelines, string memory _fabrication_date) public` is a public function that allows the manufacturer to add new components to the components array. The function takes in the following parameters:

* `_component_name`: string that stores the name of the new component.
* `_guidelines`: string that stores the guidelines of the new component.
* `_fabrication_date`: string that stores the date when the new component was fabricated.

`getComponents() public view returns (Component[] memory)` is a public function that allows anyone to view the list of components added by the manufacturer. The function returns an array of Component structs.
