const fs = require('fs');
const path = require('path');

async function syncDNS() {
    const domainsDir = path.join(__dirname, '../domains');
    if (!fs.existsSync(domainsDir)) return;

    const files = fs.readdirSync(domainsDir);
    const token = process.env.CF_API_TOKEN;
    const zoneId = process.env.CF_ZONE_ID;

    for (const file of files) {
        if (path.extname(file) === '.json') {
            const filePath = path.join(domainsDir, file);
            const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
            const subdomainName = path.basename(file, '.json') + '.awdev.my.id';

            console.log(`Processing ${subdomainName} -> ${data.record.value}`);

            // Kirim request ke Cloudflare API untuk membuat/memperbarui CNAME
            const response = await fetch(`https://api.cloudflare.com/client/v4/zones/${zoneId}/dns_records`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    type: data.record.type || 'CNAME',
                    name: subdomainName,
                    content: data.record.value,
                    ttl: 1,
                    proxied: true
                })
            });

            const result = await response.json();
            if (result.success) {
                console.log(`Berhasil mendaftarkan: ${subdomainName}`);
            } else {
                console.log(`Gagal/Sudah ada: ${subdomainName}`, result.errors);
            }
        }
    }
}

syncDNS();
