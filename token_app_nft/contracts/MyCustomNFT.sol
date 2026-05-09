// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyCustomNFT is ERC721URIStorage, Ownable {

    uint256 private _nextTokenId;
    mapping(uint256 => string) private _tokenNames;

    event NFTMinted(
        address indexed to, 
        uint256 indexed tokenId, 
        string name, 
        string uri
    );

    constructor(address owner) 
    ERC721("MyNFT", "MYNFT")
    Ownable(owner)
    {
        _nextTokenId = 1;
    }

    function mintNFT(address to, string memory tokenURI, string memory tokenName) 
    external onlyOwner returns (uint256 tokenId)
    {
        tokenId = _nextTokenId++;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, tokenURI);
        _tokenNames[tokenId] = tokenName;
        emit NFTMinted(to, tokenId, tokenName, tokenURI);
    }
}