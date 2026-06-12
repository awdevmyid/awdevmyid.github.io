// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MultiChainWalletRegistry {
    address public owner;

    // Struktur untuk menyimpan alamat non-EVM (disimpan sebagai string)
    struct NonEVMWallets {
        string solana;
        string btc;
        string inj;
        string doge;
        string ltc;
        string fio;
        string icp;
        string iotx;
        string zil;
        string egld;
        string osmo;
        string flux;
        string juno;
        string firo;
        string xrp;
        string trx;
    }

    address public ethWallet;
    NonEVMWallets public externalWallets;

    constructor() {
        owner = msg.sender;
        
        // Input alamat ETH milik Anda
        ethWallet = 0x5e8bade6B0bCE65807Db6327cB1d9Eeb7C6a6A5b;

        // Input daftar alamat multi-chain Anda
        externalWallets = NonEVMWallets({
            solana: "CB4xnv7Mw23eJkbRBXvbLUDUDQVQsg5AUvfY5nu8Ny5W",
            btc: "bc1qfwn7lfntn5jyl9yxgcrnhu4gaz8w5mnua0acyt",
            inj: "inj1t696mehqhnn9sp7mvvnuk8v7ad7x56jm5gslj6",
            doge: "DSTbQeqpCajXu8BYmririjJ8b8Lx92Lvov",
            ltc: "ltc1qz7ccrlkkv5qxrmlenr67jtqe3dy5k5w09sznvf",
            fio: "FIO67SRBSYY42urrjvN11AWuuTWHQzo47jH8LE1nrthe48EBxDo9e",
            icp: "8a92cb3db92beacc8982e1425c3c25b8f80381249d77ce19bf66c306d8727053",
            iotx: "io1p7ej7yufhsc7fwqv5vngde5llse00a4zsrs83w",
            zil: "zil1de4766z0f9mm9psyflk3tcrxc562cw068y863d",
            egld: "erd1rgznaj8fvvy6jq80xyvnzjk0amv5t63l9vm276r0kf939gjy2p0sfakxj8",
            osmo: "osmo148ds6u09ywv0d2zswjdcp0h9krs7f8eaf60gw5",
            flux: "t1LKNhr6hitag9QwTk7sGgBnwyyQYxFqMbv",
            juno: "juno148ds6u09ywv0d2zswjdcp0h9krs7f8eahnlrl6",
            firo: "aE7PmZpWuW7aXBqCXhpGmaF2XLSYert4DR",
            xrp: "rUT9m6CoZqdNWKFm7q2zo8Htsy1cvfSuk",
            trx: "TBh1vo5wazVxz5FCqmkVZSDAG2RgXJRPbo"
        });
    }
}
