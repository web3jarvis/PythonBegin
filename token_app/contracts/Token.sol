// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Token {
    string public name = "MyToken";
    string public symbol = "MTK";
    uint256 public totalSupply; // total supply of tokens

    mapping(address => uint256) public balanceOf; // dictionary to store balances

    constructor(uint _supply) {
        totalSupply = _supply; // set total supply
        balanceOf[msg.sender] = _supply; // assign all tokens to the contract deployer
    }

    function transfer(address to, uint256 amount) public returns (bool) {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        
        balanceOf[msg.sender] -= amount; // deduct from sender
        balanceOf[to] += amount; // add to recipient
        return true; 
    }
}