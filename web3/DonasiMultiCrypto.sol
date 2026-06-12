// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DonasiMultiCrypto {
    // Alamat admin/pemilik kontrak yang menerima ETH
    address public immutable admin;
    
    // Biaya wajib yang harus dikirimkan pengguna (0.09 ETH dalam satuan Wei)
    uint256 public constant BIAYA_WAJIB = 0.09 ether;

    // Penyimpanan alamat koin non-EVM sebagai data informasi resmi
    string public alamatSolana;
    string public alamatBitcoin;
    string public alamatInjective;
    string public alamatDogecoin;
    string public alamatLitecoin;
    string public alamatFio;
    string public alamatIcp;
    string public alamatIotx;
    string public alamatZilliqa;
    string public alamatEgld;
    string public alamatOsmosis;
    string public alamatFlux;
    string public alamatJuno;
    string public alamatFiro;
    string public alamatRipple;
    string public alamatTron;

    // Event yang dipicu setiap kali pengguna berhasil mengirimkan 0.09 ETH
    event PembayaranSukses(address indexed pengirim, uint256 jumlah);

    // Constructor otomatis menetapkan dompet ETH Anda sebagai admin penerima dana
    constructor() {
        admin = 0x5E8BaDE6E0BcE65807Db6327cB1d9eEB7c6a6A5b;
        
        // Inisialisasi data alamat koin non-EVM milik Anda
        alamatSolana = "CB4xnv7Mw23eJkbRBXvbLUDUDQVQsg5AUvfY5nu8Ny5W";
        alamatBitcoin = "bc1qfwn7lfntn5jyl9yxgcrnhu4gaz8w5mnua0acyt";
        alamatInjective = "inj1t696mehqhnn9sp7mvvnuk8v7ad7x56jm5gslj6";
        alamatDogecoin = "DSTbQeqpCajXu8BYmririjJ8b8Lx92Lvov";
        alamatLitecoin = "ltc1qz7ccrlkkv5qxrmlenr67jtqe3dy5k5w09sznvf";
        alamatFio = "FIO67SRBSYY42urrjvN11AWuuTWHQzo47jH8LE1nrthe48EBxDo9e";
        alamatIcp = "8a92cb3db92beacc8982e1425c3c25b8f80381249d77ce19bf66c306d8727053";
        alamatIotx = "io1p7ej7yufhsc7fwqv5vngde5llse00a4zsrs83w";
        alamatZilliqa = "zil1de4766z0f9mm9psyflk3tcrxc562cw068y863d";
        alamatEgld = "erd1rgznaj8fvvy6jq80xyvnzjk0amv5t63l9vm276r0kf939gjy2p0sfakxj8";
        alamatOsmosis = "osmo148ds6u09ywv0d2zswjdcp0h9krs7f8eaf60gw5";
        alamatFlux = "t1LKNhr6hitag9QwTk7sGgBnwyyQYxFqMbv";
        alamatJuno = "juno148ds6u09ywv0d2zswjdcp0h9krs7f8eahnlrl6";
        alamatFiro = "aE7PmZpWuW7aXBqCXhpGmaF2XLSYert4DR";
        alamatRipple = "rUT9m6CoZqdNWKFm7q2zo8Htsy1cvfSuk";
        alamatTron = "TBh1vo5wazVxz5FCqmkVZSDAG2RgXJRPbo";
    }

    /**
     * @dev Fungsi utama bagi pengguna untuk mengirim dana.
     * Pengguna HARUS mengirimkan tepat 0.09 ETH, jika tidak transaksi akan ditolak.
     */
    function kirimDonasi() external payable {
        // Validasi jumlah transfer harus tepat 0.09 ETH
        require(msg.value == BIAYA_WAJIB, "Anda harus mengirimkan tepat 0.09 ETH");

        // Dana langsung diteruskan secara otomatis ke alamat admin ETH Anda
        payable(admin).transfer(msg.value);

        // Mencatat log transaksi di blockchain
        emit PembayaranSukses(msg.sender, msg.value);
    }

    // Fungsi fallback untuk menolak pengiriman dana langsung tanpa memanggil fungsi resmi
    receive() external payable {
        revert("Gunakan fungsi kirimDonasi() dan sertakan 0.09 ETH");
    }
}
