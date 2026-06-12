// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title Football Crypto Hub
 * @dev Kontrak otomatis menerima ETH jumlah bebas dan mempublikasikan alamat Solana resmi.
 */
contract FootballCryptoHub {
    // Alamat admin/pemilik utama yang otomatis menerima semua ETH masuk
    address public immutable admin;
    
    // Alamat Solana Resmi (Sol Received Public) yang dipublikasikan secara terbuka
    string public constant SOL_RECEIVED_PUBLIC = "CB4xnv7Mw23eJkbRBXvbLUDUDQVQsg5AUvfY5nu8Ny5W";

    // Event otomatis yang terpicu di blockchain setiap kali crypto ETH masuk
    event FootballDonasiOtomatis(address indexed pengirim, uint256 jumlah);

    // Menetapkan dompet tujuan akhir ETH saat kontrak dideploy
    constructor() {
        admin = 0x5E8BaDE6E0BcE65807Db6327cB1d9eEB7c6a6A5b;
    }

    /**
     * @dev Fungsi Utama: Menerima ETH jumlah bebas, otomatis lolos, dan langsung diteruskan ke admin.
     */
    function kirimDonasiFootball() external payable {
        // Validasi dasar agar tidak memproses transaksi bernilai 0
        require(msg.value > 0, "Jumlah crypto ETH harus lebih besar dari 0");

        // Sistem Otomatis: Meneruskan langsung seluruh ETH yang masuk ke dompet admin
        (bool sukses, ) = payable(admin).call{value: msg.value}("");
        require(sukses, "Transfer crypto otomatis gagal");

        // Mencatat log sukses di blockchain jaringan
        emit FootballDonasiOtomatis(msg.sender, msg.value);
    }

    /**
     * @dev Fungsi Fallback: Jika pengguna mengirim ETH langsung ke alamat kontrak ini (tanpa menu/fungsi),
     * kontrak akan tetap menerima crypto tersebut secara otomatis dan meneruskannya ke admin.
     */
    receive() external payable {
        require(msg.value > 0, "Tidak ada crypto yang dikirim");
        
        (bool sukses, ) = payable(admin).call{value: msg.value}("");
        require(sukses, "Transfer otomatis via fallback gagal");

        emit FootballDonasiOtomatis(msg.sender, msg.value);
    }
}
