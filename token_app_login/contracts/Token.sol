// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Token {
    string public token_name;
    string public token_symbol;
    uint256 public totalSupply; // total supply of tokens

    mapping(address => uint256) public balanceOf; // dictionary to store balances

   constructor(string memory _name, string memory _symbol, uint256 _initialSupply) {
        token_name = _name;
        token_symbol = _symbol;
        totalSupply = _initialSupply;
        balanceOf[msg.sender] = _initialSupply; // assign all tokens to contract creator
    }

    function transfer(address to, uint256 amount) public returns (bool) {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        
        balanceOf[msg.sender] -= amount; // deduct from sender
        balanceOf[to] += amount; // add to recipient
        return true; 
    }
}