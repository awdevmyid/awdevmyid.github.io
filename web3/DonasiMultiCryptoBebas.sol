// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DonasiMultiCryptoBebas {
    // Alamat admin/pemilik kontrak yang menerima ETH
    address public immutable admin;

    // Alamat koin non-EVM sebagai data informasi resmi (hemat gas dengan 'constant')
    string public constant alamatSolana = "CB4xnv7Mw23eJkbRBXvbLUDUDQVQsg5AUvfY5nu8Ny5W";
    string public constant alamatBitcoin = "bc1qfwn7lfntn5jyl9yxgcrnhu4gaz8w5mnua0acyt";
    string public constant alamatInjective = "inj1t696mehqhnn9sp7mvvnuk8v7ad7x56jm5gslj6";
    string public constant alamatDogecoin = "DSTbQeqpCajXu8BYmririjJ8b8Lx92Lvov";
    string public constant alamatLitecoin = "ltc1qz7ccrlkkv5qxrmlenr67jtqe3dy5k5w09sznvf";
    string public constant alamatFio = "FIO67SRBSYY42urrjvN11AWuuTWHQzo47jH8LE1nrthe48EBxDo9e";
    string public constant alamatIcp = "8a92cb3db92beacc8982e1425c3c25b8f80381249d77ce19bf66c306d8727053";
    string public constant alamatIotx = "io1p7ej7yufhsc7fwqv5vngde5llse00a4zsrs83w";
    string public constant alamatZilliqa = "zil1de4766z0f9mm9psyflk3tcrxc562cw068y863d";
    string public constant alamatEgld = "erd1rgznaj8fvvy6jq80xyvnzjk0amv5t63l9vm276r0kf939gjy2p0sfakxj8";
    string public constant alamatOsmosis = "osmo148ds6u09ywv0d2zswjdcp0h9krs7f8eaf60gw5";
    string public constant alamatFlux = "t1LKNhr6hitag9QwTk7sGgBnwyyQYxFqMbv";
    string public constant alamatJuno = "juno148ds6u09ywv0d2zswjdcp0h9krs7f8eahnlrl6";
    string public constant alamatFiro = "aE7PmZpWuW7aXBqCXhpGmaF2XLSYert4DR";
    string public constant alamatRipple = "rUT9m6CoZqdNWKFm7q2zo8Htsy1cvfSuk";
    string public constant alamatTron = "TBh1vo5wazVxz5FCqmkVZSDAG2RgXJRPbo";

    // Event mencatat siapa yang mengirim dan berapa jumlahnya
    event PembayaranSukses(address indexed pengirim, uint256 jumlah);

    constructor() {
        admin = 0x5E8BaDE6E0BcE65807Db6327cB1d9eEB7c6a6A5b;
    }

    /**
     * @dev Fungsi untuk mengirim donasi dengan jumlah bebas.
     */
    function kirimDonasi() external payable {
        // Validasi agar pengirim tidak mengirimkan 0 ETH (transaksi kosong)
        require(msg.value > 0, "Jumlah ETH harus lebih besar dari 0");

        // Meneruskan berapapun ETH yang dikirim langsung ke admin
        (bool sukses, ) = payable(admin).call{value: msg.value}("");
        require(sukses, "Transfer dana ke admin gagal");

        emit PembayaranSukses(msg.sender, msg.value);
    }

    // Fungsi fallback: Jika orang mengirim ETH langsung ke alamat kontrak ini tanpa panggil fungsi,
    // kontrak akan otomatis mengarahkan dana tersebut ke fungsi kirimDonasi().
    receive() external payable {
        // Langsung teruskan ke admin
        (bool sukses, ) = payable(admin).call{value: msg.value}("");
        require(sukses, "Transfer dana langsung gagal");

        emit PembayaranSukses(msg.sender, msg.value);
    }
}
