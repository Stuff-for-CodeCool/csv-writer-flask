async function getting(url) {
    const req = await fetch(url, { headers: { "Content-Type": "application/json" } })

    if (req.ok) {
        const res = await req.json();
        //  do something
    }
}

async function posting(url, data) {
    const req = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (req.ok) {
        const res = await req.json();
        //  do something
    }
}