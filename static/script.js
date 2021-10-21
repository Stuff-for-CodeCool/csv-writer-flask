const buildForm = () => {
    const form = document.createElement("form");
    form.action = "/add/";
    form.method = "POST";

    const titleLabel = document.createElement("label");
    titleLabel.for = "title";
    titleLabel.innerText = "Title";
    form.appendChild(titleLabel);

    const titleInput = document.createElement("input");
    titleInput.type = "text";
    titleInput.id = "title";
    titleInput.name = "title";
    titleInput.required = true;
    form.appendChild(titleInput);

    const messageLabel = document.createElement("label");
    messageLabel.for = "message";
    messageLabel.innerText = "Message";
    form.appendChild(messageLabel);

    const message = document.createElement("textarea");
    message.id = "message";
    message.name = "message";
    message.cols = 30;
    message.rows = 10;
    message.required = true;
    form.appendChild(message);

    const button = document.createElement("button");
    button.type = "submit";
    button.innerText = "Submit";
    form.appendChild(button);

    return form;

    // <form action="/add/" method="POST">
    //     <label for="title">Title</label>
    //     <input type="text" id="title" name="title" required="">

    //     <label for="message">Message</label>
    //     <textarea name="message" id="message" cols="30" rows="10" required=""></textarea>

    //     <button type="submit">Submit</button>
    // </form>
};

const loadApiContentPage = async (id) => {
    const req = await fetch("/entry/" + id, {
        headers: { "Content-Type": "application/json" },    //  tells server this is a json request
    });

    if (req.ok) {   //  request was successful
        const res = await req.json();   //  convert response to json

        //  inject code
        document.querySelector("#content").innerHTML = `
            <h2>${res.title}</h2>
            <p><small>Viewed ${res.view_count} times</small></p>
            <p>${res.message}</p>
        `;
    }
};

const loadApiPage = async (e) => {
    e.preventDefault();

    const req = await fetch(e.target.href, {    //  don't bother specifying an endpoint, get it from the form itself
        headers: { "Content-Type": "application/json" },    //  json
    });

    if (req.ok) {
        //  elements
        const table = document.querySelector("tbody");
        const nav = {
            prev: document.querySelector("nav a:first-child"),
            page: document.querySelector("nav span"),
            next: document.querySelector("nav span + a"),
        };
        table.innerHTML = "";

        //  json response
        const res = await req.json();

        res.entries.forEach((item) => {
            //  table row, cells, link
            const tr = document.createElement("tr");
            const td1 = document.createElement("td");
            const td2 = document.createElement("td");
            const td3 = document.createElement("td");
            const a = document.createElement("a");

            tr.appendChild(td1);
            tr.appendChild(td2);
            tr.appendChild(td3);

            td1.appendChild(a);

            a.href = "/entry/" + item.id;
            a.innerText = item.title;
            //  add link behavior by default
            a.addEventListener("click", (e) => {
                e.preventDefault();
                loadApiContentPage(item.id);
            });

            td2.innerText = item.message;
            td3.innerText = item.view_count;

            table.appendChild(tr);
        });

        // nav links
        if (res.prev) {
            nav.prev.classList.remove("hidden");
            nav.prev.href = "/page/" + res.prev;
        } else {
            nav.prev.classList.add("hidden");
        }

        if (res.next) {
            nav.next.classList.remove("hidden");
            nav.next.href = "/page/" + res.next;
        } else {
            nav.next.classList.add("hidden");
        }

        nav.page.innerText = res.page;
    }
};

const handleSubmit = async (e) => {
    e.preventDefault();

    const req = await fetch(e.target.action, {
        method: "POST",                                     //  make a POST request
        headers: { "Content-Type": "application/json" },    //  make it json
        body: JSON.stringify({                              //  send json string with what the server expects
            title: e.target.title.value,
            message: e.target.message.value,
        }),
    });

    if (req.ok) {
        const res = await req.json();

        if (res.message) {
            //  error message
            document.querySelector(".flashes").innerHTML = `<li>${res.message}</li>`;
        } else {
            //  success behavior
            loadApiContentPage(res.id);
        }
    }
};

//  handle bottom navigation
const navLinks = document.querySelectorAll("nav a");
navLinks.forEach((a) => a.addEventListener("click", loadApiPage));

//  load entries
const indexLinks = document.querySelectorAll("table a");
indexLinks.forEach((a) =>
    a.addEventListener("click", (e) => {
        e.preventDefault();

        const id = e.target.href    //  get the link
            .split("/")             //  split it by /
            .filter((x) => !!x)     //  get non-empty elements
            .pop();                 //  get last element

        loadApiContentPage(id);
    })
);

//  handle form submission
const form = document.querySelector("form");
form.addEventListener("submit", handleSubmit);
