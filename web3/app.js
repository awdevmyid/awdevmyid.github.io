// Database Alamat Kripto Milik Anda
const CRYPTO_DATABASE = {
    eth: "0x5e8bade6e0bce65807db6327cb1d9eeb7c6a6a5b",
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
};

const JUMLAH_DONASI_ETH = "0.001"; // Nominal donasi instan MetaMask

// Elemen UI
const cryptoSelect = document.getElementById("crypto-select");
const cryptoLabel = document.getElementById("crypto-label");
const walletAddressText = document.getElementById("wallet-address");
const btnCopy = document.getElementById("btn-copy");
const ethWeb3Section = document.getElementById("eth-web3-section");

const btnConnect = document.getElementById("btn-connect");
const btnSend = document.getElementById("btn-send");
const walletStatus = document.getElementById("wallet-status");

let provider, signer, userAddress;

// Fungsi Ganti Tampilan Koin Saat dropdown Dipilih
cryptoSelect.addEventListener("change", (e) => {
    const selectedCoin = e.target.value;
    const address = CRYPTO_DATABASE[selectedCoin];
    
    cryptoLabel.innerText = `Alamat ${selectedCoin.toUpperCase()}`;
    walletAddressText.innerText = address;
    btnCopy.innerText = "📋 Salin Alamat";

    // Menyembunyikan/Menampilkan fitur MetaMask Web3 jika koinnya adalah ETH
    if (selectedCoin === "eth") {
        ethWeb3Section.classList.remove("hidden");
    } else {
        ethWeb3Section.classList.add("hidden");
    }
});

// Fitur Copy to Clipboard
btnCopy.addEventListener("click", () => {
    navigator.clipboard.writeText(walletAddressText.innerText);
    btnCopy.innerText = "✅ Tersalin!";
    setTimeout(() => { btnCopy.innerText = "📋 Salin Alamat"; }, 2000);
});

// LOGIKA WEB3 ETHEREUM (MetaMask)
async function connectWallet() {
    if (typeof window.ethereum !== "undefined") {
        try {
            const accounts = await window.ethereum.request({ method: "eth_requestAccounts" });
            userAddress = accounts[0];
            
            provider = new ethers.providers.Web3Provider(window.ethereum);
            signer = provider.getSigner();

            walletStatus.innerText = `Terhubung: ${userAddress.substring(0, 6)}...${userAddress.substring(userAddress.length - 4)}`;
            walletStatus.className = "text-xs font-mono text-emerald-400 mb-2";
            
            btnSend.disabled = false;
            btnSend.classList.remove("opacity-50", "cursor-not-allowed");
            btnSend.classList.add("cursor-pointer");
            
            btnConnect.innerText = "🔄 Terhubung";
            btnConnect.disabled = true;
            btnConnect.className = "bg-gray-700 text-gray-400 text-sm font-medium py-3 px-4 rounded-xl cursor-not-allowed";
        } catch (error) {
            alert("Koneksi dompet dibatalkan.");
        }
    } else {
        alert("Silakan pasang ekstensi MetaMask di browser Anda.");
    }
}

async function sendCrypto() {
    if (!signer) return;
    try {
        walletStatus.innerText = "Menunggu konfirmasi transaksi...";
        walletStatus.className = "text-xs font-mono text-amber-400 mb-2";

        const tx = await signer.sendTransaction({
            to: CRYPTO_DATABASE.eth,
            value: ethers.utils.parseEther(JUMLAH_DONASI_ETH)
        });

        walletStatus.innerText = "Memproses transaksi di jaringan...";
        await tx.wait();
        
        walletStatus.innerText = "Donasi Sukses! Terima kasih.";
        walletStatus.className = "text-xs font-mono text-emerald-400 mb-2";
        alert(`Sukses dikirim! Hash: ${tx.hash}`);
    } catch (error) {
        walletStatus.innerText = "Transaksi Gagal/Dibatalkan";
        walletStatus.className = "text-xs font-mono text-rose-400 mb-2";
    }
}

btnConnect.addEventListener("click", connectWallet);
btnSend.addEventListener("click", sendCrypto);
