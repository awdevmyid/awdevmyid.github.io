// Database alamat milik Anda (dari langkah sebelumnya)
const MY_REGISTERED_WALLETS = {
    eth: "0x5e8bade6e0bce65807db6327cb1d9eeb7c6a6a5b",
    solana: "CB4xnv7Mw23eJkbRBXvbLUDUDQVQsg5AUvfY5nu8Ny5W"
};

// Elemen DOM UI
const connectEthBtn = document.getElementById('connectEthBtn');
const connectSolBtn = document.getElementById('connectSolBtn');
const walletStatus = document.getElementById('walletStatus');
const matchStatus = document.getElementById('matchStatus');

// 1. Fungsi Koneksi Wallet Ethereum (MetaMask / Trust Wallet)
async function connectEthereum() {
    if (typeof window.ethereum !== 'undefined') {
        try {
            // Meminta akses akun ke MetaMask
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            const connectedAddress = accounts[0].toLowerCase();
            
            walletStatus.innerText = `ETH Terhubung: ${connectedAddress}`;
            
            // Verifikasi kecocokan data
            if (connectedAddress === MY_REGISTERED_WALLETS.eth.toLowerCase()) {
                matchStatus.innerText = "✓ Dompet Terverifikasi: Ini adalah wallet ETH Anda.";
                matchStatus.className = "text-emerald-400 text-xs font-semibold mt-1";
            } else {
                matchStatus.innerText = "⚠ Peringatan: Dompet tidak terdaftar dalam database.";
                matchStatus.className = "text-amber-400 text-xs font-semibold mt-1";
            }
        } catch (error) {
            walletStatus.innerText = "Koneksi dibatalkan oleh pengguna.";
        }
    } else {
        alert("MetaMask tidak terdeteksi! Silakan instal ekstensi browser MetaMask.");
    }
}

// 2. Fungsi Koneksi Wallet Solana (Phantom / Solflare)
async function connectSolana() {
    const isPhantomInstalled = window.solana && window.solana.isPhantom;
    
    if (isPhantomInstalled) {
        try {
            // Melakukan handshake koneksi ke Phantom
            const response = await window.solana.connect();
            const connectedAddress = response.publicKey.toString();
            
            walletStatus.innerText = `Solana Terhubung: ${connectedAddress}`;
            
            // Verifikasi kecocokan data
            if (connectedAddress === MY_REGISTERED_WALLETS.solana) {
                matchStatus.innerText = "✓ Dompet Terverifikasi: Ini adalah wallet Solana Anda.";
                matchStatus.className = "text-emerald-400 text-xs font-semibold mt-1";
            } else {
                matchStatus.innerText = "⚠ Peringatan: Dompet tidak cocok dengan database.";
                matchStatus.className = "text-amber-400 text-xs font-semibold mt-1";
            }
        } catch (error) {
            walletStatus.innerText = "Koneksi Solana gagal atau ditolak.";
        }
    } else {
        alert("Phantom Wallet tidak ditemukan! Silakan instal ekstensi Phantom.");
    }
}

// Event Listener tombol UI
connectEthBtn.addEventListener('click', connectEthereum);
connectSolBtn.addEventListener('click', connectSolana);
