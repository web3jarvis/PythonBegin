// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Token {
    string public name;
    string public symbol;
    uint256 public totalSupply; // total supply of tokens

    mapping(address => uint256) public balanceOf; // dictionary to store balances
    mapping(address => mapping(address => uint256)) public allowance; // for approvals

   constructor(string memory _name, string memory _symbol, uint256 _initialSupply) {
        name = _name;
        symbol = _symbol;
        totalSupply = _initialSupply;
        balanceOf[msg.sender] = _initialSupply; // assign all tokens to contract creator
    }

    function transfer(address to, uint256 amount) public returns (bool) {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        
        balanceOf[msg.sender] -= amount; // deduct from sender
        balanceOf[to] += amount; // add to recipient
        return true; 
    }

    function approve(address spender, uint256 amount) public returns (bool) {
    allowance[msg.sender][spender] = amount;
    return true;
}
    function transferFrom(address from, address to, uint256 amount) public returns (bool) {
        require(balanceOf[from] >= amount, "Insufficient balance");
        
        allowance[from][msg.sender] -= amount; // deduct from allowance
        balanceOf[from] -= amount; // deduct from sender
        balanceOf[to] += amount; // add to recipient
        return true; 
    }
    
}