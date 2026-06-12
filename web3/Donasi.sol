// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Donation {
    // Alamat publik pemilik kontrak (menggunakan tipe data address)
    address public immutable owner;

    // Event untuk mencatat riwayat donasi di blockchain
    event DonationReceived(address indexed donor, uint256 amount);

    constructor() {
        // Menetapkan pembuat kontrak sebagai pemilik yang berhak menerima dana
        owner = msg.sender;
    }

    // Fungsi untuk menerima dana dari pengguna
    function sendDonation() external payable {
        require(msg.value > 0, "Jumlah donasi harus lebih dari 0");
        
        // Mentransfer dana yang diterima langsung ke dompet pemilik
        payable(owner).transfer(msg.value);
        
        emit DonationReceived(msg.sender, msg.value);
    }
}
