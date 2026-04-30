// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./openzeppelin/token/ERC20/IERC20.sol";
import "./openzeppelin/utils/ReentrancyGuard.sol";

contract AMMPool is ReentrancyGuard {
    IERC20 public tokenA;
    IERC20 public tokenB;
    uint256 public reserveA;
    uint256 public reserveB;

    constructor(address _tokenA, address _tokenB){
        tokenA = IERC20(_tokenA);
        tokenB = IERC20(_tokenB);
    }

    function addLiquidity(uint amountA, uint amountB) public nonReentrant returns (bool){
        require(tokenA.transferFrom(msg.sender, address(this), amountA), "Transfer failed");
        require(tokenB.transferFrom(msg.sender, address(this), amountB), "Transfer failed");
        reserveA += amountA;
        reserveB += amountB;
        return true;
    }

    function swapAforB(uint amountA) public nonReentrant returns (uint){
        uint amountB = (amountA * reserveB) / (reserveA + amountA);
        require(amountB > 0, "Insufficient output amount");
        require(tokenA.transferFrom(msg.sender, address(this), amountA), "Transfer failed");
        require(tokenB.transfer(msg.sender, amountB), "Transfer failed");
        reserveA += amountA;
        reserveB -= amountB;
        return amountB;
    }

    function swapBforA(uint amountB) public nonReentrant returns (uint){
        uint amountA = (amountB * reserveA) / (reserveB + amountB);
        require(amountA > 0, "Insufficient output amount");
        require(tokenB.transferFrom(msg.sender, address(this), amountB), "Transfer failed");
        require(tokenA.transfer(msg.sender, amountA), "Transfer failed");
        reserveB += amountB;
        reserveA -= amountA;
        return amountA;
    }
}