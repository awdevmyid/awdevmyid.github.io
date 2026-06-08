```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20 {
    function transfer(
        address to,
        uint256 amount
    ) external returns (bool);

    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) external returns (bool);

    function balanceOf(
        address account
    ) external view returns (uint256);
}

contract MultiChainVault {

    // =====================================
    // OWNER
    // =====================================

    address public owner;

    modifier onlyOwner() {
        require(
            msg.sender == owner,
            "Not owner"
        );
        _;
    }

    // =====================================
    // MULTICHAIN ADDRESS BOOK
    // =====================================

    mapping(string => string) private chainAddress;

    // =====================================
    // EVENTS
    // =====================================

    event ETHReceived(
        address indexed from,
        uint256 amount
    );

    event TokenReceived(
        address indexed token,
        address indexed from,
        uint256 amount
    );

    event OwnershipTransferred(
        address indexed oldOwner,
        address indexed newOwner
    );

    event ChainAddressUpdated(
        string chain,
        string wallet
    );

    // =====================================
    // CONSTRUCTOR
    // =====================================

    constructor() {
        owner = msg.sender;

        chainAddress["BTC"] =
            "bc1qfwn7lfntn5jyl9yxgcrnhu4gaz8w5mnua0acyt";

        chainAddress["SOL"] =
            "CB4xnv7Mw23eJkbRBXvbLUDUDQVQsg5AUvfY5nu8Ny5W";

        chainAddress["DOGE"] =
            "DSTbQeqpCajXu8BYmririjJ8b8Lx92Lvov";

        chainAddress["LTC"] =
            "ltc1qz7ccrlkkv5qxrmlenr67jtqe3dy5k5w09sznvf";

        chainAddress["XRP"] =
            "rUT9m6CoZqdNWKFm7q2zo8Htsy1cvfSuk";
    }

    // =====================================
    // RECEIVE ETH
    // =====================================

    receive() external payable {
        emit ETHReceived(
            msg.sender,
            msg.value
        );
    }

    // =====================================
    // TOKEN DEPOSIT
    // =====================================

    function depositToken(
        address token,
        uint256 amount
    ) external {

        require(
            IERC20(token).transferFrom(
                msg.sender,
                address(this),
                amount
            ),
            "Transfer failed"
        );

        emit TokenReceived(
            token,
            msg.sender,
            amount
        );
    }

    // =====================================
    // MULTICHAIN LOOKUP
    // =====================================

    function getChainAddress(
        string calldata chain
    )
        external
        view
        returns (string memory)
    {
        return chainAddress[chain];
    }

    function setChainAddress(
        string calldata chain,
        string calldata wallet
    )
        external
        onlyOwner
    {
        chainAddress[chain] = wallet;

        emit ChainAddressUpdated(
            chain,
            wallet
        );
    }

    // =====================================
    // BALANCES
    // =====================================

    function ethBalance()
        external
        view
        returns (uint256)
    {
        return address(this).balance;
    }

    function tokenBalance(
        address token
    )
        external
        view
        returns (uint256)
    {
        return IERC20(token)
            .balanceOf(address(this));
    }

    // =====================================
    // WITHDRAW ETH
    // =====================================

    function withdrawETH()
        external
        onlyOwner
    {
        uint256 amount =
            address(this).balance;

        (bool success,) =
            payable(owner).call{
                value: amount
            }("");

        require(
            success,
            "Withdraw failed"
        );
    }

    // =====================================
    // WITHDRAW TOKEN
    // =====================================

    function withdrawToken(
        address token
    )
        external
        onlyOwner
    {
        IERC20 erc20 =
            IERC20(token);

        uint256 balance =
            erc20.balanceOf(
                address(this)
            );

        require(
            erc20.transfer(
                owner,
                balance
            ),
            "Withdraw failed"
        );
    }

    // =====================================
    // OWNERSHIP
    // =====================================

    function transferOwnership(
        address newOwner
    )
        external
        onlyOwner
    {
        require(
            newOwner != address(0),
            "Zero address"
        );

        emit OwnershipTransferred(
            owner,
            newOwner
        );

        owner = newOwner;
    }
}
```
