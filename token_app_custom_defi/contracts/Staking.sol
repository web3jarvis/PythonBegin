// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "./Token.sol";

contract Staking {
    
    Token public stakingToken;
    mapping(address => uint256) public stakingBalance;
    mapping(address => uint256) public stakingTime;

    constructor(address _stakingToken) {
        stakingToken = Token(_stakingToken); // Initialize the staking token contract
    }

    function stake(uint256 _amount) public returns (bool) {
        stakingToken.transferFrom(msg.sender, address(this), _amount); // Transfer tokens from user to staking contract
        stakingBalance[msg.sender] += _amount; // Update the user's staking balance
        stakingTime[msg.sender] = block.timestamp; // Record the time of staking for reward calculation
        return true;
    }

    function unstake(uint256 _amount) public returns (bool) {
        uint256 rewardAmount = reward(_amount);
        require(stakingBalance[msg.sender] >= _amount, "Insufficient staked balance");
        stakingBalance[msg.sender] -= _amount;
        stakingToken.transfer(msg.sender, _amount + rewardAmount);
        return true;
    }

    function reward(uint256 _amount) public pure returns (uint256) {
        return _amount / 10;
    }
}