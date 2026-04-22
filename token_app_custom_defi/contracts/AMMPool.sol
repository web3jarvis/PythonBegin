// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Token.sol";

contract AMMPool{
    Token public tokenA;
    Token public tokenB;
    uint256 public reserveA;
    uint256 public reserveB;

    constructor(address _tokenA, address _tokenB){
        tokenA = Token(_tokenA);
        tokenB = Token(_tokenB);
    }

    function addLiquidity(uint amountA, uint amountB) public returns (bool){
        tokenA.transferFrom(msg.sender, address(this), amountA);
        tokenB.transferFrom(msg.sender, address(this), amountB);
        reserveA += amountA;
        reserveB += amountB;
        return true;
    }

    function swapAforB(uint amountA) public returns (uint){
        uint amountB = (amountA * reserveB) / (reserveA + amountA);
        require(amountB > 0, "Insufficient output amount");
        tokenA.transferFrom(msg.sender, address(this), amountA);
        tokenB.transfer(msg.sender, amountB);
        reserveA += amountA;
        reserveB -= amountB;
        return amountB;
    }

    function swapBforA(uint amountB) public returns (uint){
        uint amountA = (amountB * reserveA) / (reserveB + amountB);
        require(amountA > 0, "Insufficient output amount");
        tokenB.transferFrom(msg.sender, address(this), amountB);
        tokenA.transfer(msg.sender, amountA);
        reserveB += amountB;
        reserveA -= amountA;
        return amountA;
    }
}