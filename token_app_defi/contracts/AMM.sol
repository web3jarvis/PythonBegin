// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Token.sol";

contract AMM {
    Token public tokenA;
    Token public tokenB;
    uint256 public reserveA; // amount of tokenA in the pool
    uint256 public reserveB; // amount of tokenB in the pool

    constructor(address _tokenA, address _tokenB) {
        tokenA = Token(_tokenA);
        tokenB = Token(_tokenB);
    }

    function addLiquidity(uint256 amountA, uint256 amountB) public {
        require(tokenA.transferFrom(msg.sender, address(this), amountA), "Transfer of tokenA failed");
        require(tokenB.transferFrom(msg.sender, address(this), amountB), "Transfer of tokenB failed");
        
        reserveA += amountA;
        reserveB += amountB;
    }

    function swapAForB(uint256 amountA) public {
        require(tokenA.transferFrom(msg.sender, address(this), amountA), "Transfer of tokenA failed");
        
        uint256 amountB = (amountA * reserveB) / (reserveA + amountA);

        require(amountB > 0, "Insufficient output amount");
        require(tokenB.transfer(msg.sender, amountB), "Transfer of tokenB failed");
        
        reserveA += amountA;
        reserveB -= amountB;
    }

    function swapBForA(uint256 amountB) public {
        require(tokenB.transferFrom(msg.sender, address(this), amountB), "Transfer of tokenB failed");
        
        uint256 amountA = (amountB * reserveA) / (reserveB + amountB);
        
        require(amountA > 0, "Insufficient output amount");
        require(tokenA.transfer(msg.sender, amountA), "Transfer of tokenA failed");
        
        reserveB += amountB;
        reserveA -= amountA;
    }
}