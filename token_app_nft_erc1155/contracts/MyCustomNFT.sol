// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/token/common/ERC2981.sol";

contract MyCustomNFT is ERC1155, Ownable, ERC2981 {
    using Strings for uint256;
    mapping(uint256 => string) private _tokenURIs;
    constructor(address initialOwner) ERC1155("") Ownable(initialOwner){
        _setDefaultRoyalty(msg.sender, 1000);
    }

    function mintNFT(address to, uint256 id, uint256 amount, string memory tokenURI) external onlyOwner {
        _mint(to, id, amount, "");
        _tokenURIs[id] = tokenURI;
    }

    function uri(uint256 id) public view override returns (string memory) {
        return _tokenURIs[id];
    }

    function transferNFT(address from, address to, uint256 id, uint256 amount) external {
        safeTransferFrom(from, to, id, amount, "");
    }

    function supportsInterface(bytes4 interfaceId) public view override(ERC1155, ERC2981) returns (bool) {
        return super.supportsInterface(interfaceId);
    }
}