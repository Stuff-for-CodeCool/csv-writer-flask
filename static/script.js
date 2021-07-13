const form = document.querySelector("form");
const modal = document.querySelector("#modal");
const links = document.querySelectorAll("table a");
const navs = document.querySelectorAll("nav a");

const buildModal = function ({ title, message, view_count }) {
    modal.innerHTML = `
            <h2>${title}</h2>
            <p><small>Viewed ${view_count} times</small></p>
            <p>${message}</p>`;

    const closeBtn = document.createElement("button");
    closeBtn.innerHTML = "&times;";
    closeBtn.addEventListener("click", closeModal);
    modal.insertAdjacentElement("afterbegin", closeBtn);

    modal.classList.add("open");
};

const submitHandler = async function (e) {
    e.preventDefault();
    const req = await fetch(e.target.action, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            title: e.target.title.value,
            message: e.target.message.value,
        }),
    });
    if (req.ok) {
        e.target.title.value = "";
        e.target.message.value = "";

        const res = await req.json();
        buildModal(res);
    }
};

const clickHandler = async function (e) {
    e.preventDefault();
    const req = await fetch(e.target.href, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
    });
    if (req.ok) {
        const res = await req.json();
        buildModal(res);
    }
};
const navHandler = async function (e) {
    e.preventDefault();
    const req = await fetch(e.target.href, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
    });
    if (req.ok) {
        const res = await req.json();

        const nav = document.querySelector("nav");
        const table = document.querySelector("table tbody");

        nav.innerHTML = "";
        if (res.prev) {
            nav.innerHTML += `<a href="${res.prev}">&lt;</a>`;
        }
        nav.innerHTML += `<span>${res.page}</span>`;
        if (res.next) {
            nav.innerHTML += `<a href="${res.next}">&gt;</a>`;
        }

        window.location.href = e.target.href;

        table.innerHTML = "";
        res.entries.forEach((e) => {
            table.innerHTML += `
            <tr>
                <td>
                    <a href="${e.link}">
                        ${e.title}
                    </a>
                </td>
                <td>${e.message}</td>
                <td>${e.view_count}</td>
            </tr>
            `;
        });
    }
};

if (form) {
    form.addEventListener("submit", submitHandler);
}

const closeModal = function (e) {
    e.preventDefault();

    modal.innerHTML = "";
    modal.classList.remove("open");
};

const escHandler = function (e) {
    if (e.keyCode === 27) {
        closeModal(e);
    }
};

if (modal) {
    document.body.addEventListener("keyup", escHandler);
}

if (links) {
    links.forEach((link) => link.addEventListener("click", clickHandler));
}

if (navs) {
    navs.forEach((nav) => nav.addEventListener("click", navHandler));
}
