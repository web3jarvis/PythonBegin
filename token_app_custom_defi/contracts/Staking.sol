// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./openzeppelin/token/ERC20/IERC20.sol";
import "./openzeppelin/utils/ReentrancyGuard.sol";

contract Staking is ReentrancyGuard {
    
    IERC20 public stakingToken;
    mapping(address => uint256) public stakingBalance;
    mapping(address => uint256) public stakingTime;

    constructor(address _stakingToken) {
        stakingToken = IERC20(_stakingToken);
    }

    function stake(uint256 _amount) public nonReentrant returns (bool) {
        require(stakingToken.transferFrom(msg.sender, address(this), _amount), "Transfer failed");
        stakingBalance[msg.sender] += _amount;
        stakingTime[msg.sender] = block.timestamp;
        return true;
    }

    function unstake(uint256 _amount) public nonReentrant returns (bool) {
        uint256 rewardAmount = reward(_amount);
        require(stakingBalance[msg.sender] >= _amount, "Insufficient staked balance");
        stakingBalance[msg.sender] -= _amount;
        require(stakingToken.transfer(msg.sender, _amount + rewardAmount), "Transfer failed");
        return true;
    }

    function reward(uint256 _amount) public pure returns (uint256) {
        return _amount / 10;
    }
}