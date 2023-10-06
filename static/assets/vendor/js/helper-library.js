let limitInputs = document.querySelectorAll(".count");
limitInputs.forEach((div) => {
    let divspan = document.createElement("div");
    divspan.setAttribute("class", "charcount me-0 ms-0 ps-2 pe-2");
    divspan.innerHTML = `<span class="minimum-characters">Min. ${div.getAttribute("minlength")} characters</span><span class="counter justify-se"><span>0</span><span>/${div.getAttribute("maxlength")}</span></span>`;
    div.after(divspan);
    divspan.style.cssText = "display: flex;justify-content: space-between;text-align: right;margin: 5px 10px;";
    div.addEventListener("input", (e) => {
        characterCount(e.target)
    });
    div.dispatchEvent(new Event("input"));
});

document.querySelectorAll('.add-type-table')
    .forEach(function (table) {
        initializeAddTableForm(table);
    });


document.querySelectorAll(".rmvbtn").forEach((btn) => {
    btn.addEventListener("click", deleteRow);
});

function initializeAddTableForm(div_element) {
    div_element.querySelector('.addbtn').addEventListener('click', addSkeleton);
    let table = div_element.querySelector('table');
    for (let i = table.querySelector('tbody').children.length; i < Number(table.dataset.min); i++) {
        addSkeleton({target: div_element.querySelector('.addbtn')});

    }
    validateTable(table);

}

function addSkeleton(e) {
    var table = e.target.closest('div.add-type-table').querySelector('table');
    var tbody = table.getElementsByTagName('tbody')[0];
    var clone = table.querySelector(".skeleton").cloneNode(true);
    clone.classList.remove("skeleton");
    clone.querySelectorAll(":is(textarea,input,select)").forEach((input) => {
        input.setAttribute("required", "");
    });
    let sr_cell = clone.querySelector(".sr-no");
    sr_cell.innerHTML = tbody.childElementCount + 1;
    clone.style.display = "";
    clone.querySelector(".rmvbtn").addEventListener('click', deleteRow);
    clone.querySelectorAll(".count").forEach((input) => {
        input.addEventListener("input", (e) => {
            characterCount(e.target)
        });
    });
    tbody.appendChild(clone);
    validateTable(table);
    clone.querySelectorAll(".individual-integer").forEach((input) => {
        addIntegerInputValidator(input);
    });
}

function deleteRow(e) {
    let table = e.target.closest("table");
    e.target.closest("tr").remove();
    validateTable(table);
}

function validateTable(table) {
    var tbody = table.getElementsByTagName('tbody')[0];
    if (table.querySelector("tbody").children.length >= Number(table.dataset.max)) {
        table.closest('div.add-type-table').querySelectorAll(".addbtn").forEach((btn) => {
            btn.disabled = true;
        })
    } else {
        table.closest('div.add-type-table').querySelectorAll(".addbtn").forEach((btn) => {
            btn.disabled = false;
        })
    }
    if (tbody.children.length <= Number(table.dataset.min)) {
        table.querySelectorAll(".rmvbtn").forEach((btn) => {
            btn.style.display = "none";
        });
    } else {
        table.querySelectorAll(".rmvbtn").forEach((btn) => {
            btn.style.display = "";
        });
    }
    let counter = 1;
    tbody.querySelectorAll("tr").forEach((tr) => {
        tr.querySelectorAll("input").forEach((input) => {
            input.name = input.dataset.prefix + counter;
            input.required = true;
            if (input.classList.contains('individual-integer')) {
                input.setAttribute("placeholder", "Max " + input.getAttribute("max"));
            }
        });
        tr.querySelectorAll("textarea").forEach((input) => {
            input.name = input.dataset.prefix + counter;
            input.required = true;
        });
        tr.querySelectorAll("select").forEach((input) => {
            input.name = input.dataset.prefix + counter;
            input.required = true;
        });

        tr.querySelector(".sr-no").innerHTML = counter;
        counter++;
    });
}

function characterCount(e) {
    let min = Number(e.getAttribute("minlength"));

    let span = e.parentElement.querySelector(".counter").children[0];
    span.innerText = e.value.length;
    if (e.value.length >= min) {
        e.parentElement.querySelector(".minimum-characters").style.visibility = "hidden";
    } else {
        e.parentElement.querySelector(".minimum-characters").style.visibility = "visible";
    }
}

function addIntegerInputValidator(input) {
    // validate an input in such a way that it only allows integer values from min and max attributes. doesnt allow characted input and floating point values
    input.addEventListener("change", (e) => {
        let value = e.target.value;
        let min = Number(e.target.getAttribute("min"));
        let max = Number(e.target.getAttribute("max"));
        let regex = new RegExp(`^\\d{${min},${max}}$`);
        console.log(regex.test(value));
        if (!(e.target.value <= max && e.target.value >= min) && !e.target.classList.contains("roundException")) {
            if (e.target.value > max) {
                e.target.value = max;
            } else if (e.target.value < min) {
                e.target.value = min;
            } else {
                e.target.value = "";
            }
        } else {
            e.target.value = Math.round(e.target.value)
        }
    });
}

let integerInputs = document.querySelectorAll(".individual-integer");
integerInputs.forEach((input) => {
    addIntegerInputValidator(input);
});

var node_clipboard = {
    'bachelors': null,
    'masters': null,
};

function hideInitialize(checkbox_id, gayabable) {
    let checkbox = document.getElementById(checkbox_id);
    let gayab = document.getElementById(gayabable);
    if (checkbox.checked) {
        gayab.style.display = "none";
        // add .ignore class to all inputs and textareas in gayabable
        let objectsToBEHidden = gayab.querySelector('tbody').querySelectorAll(":is(input,textarea,select)");
        objectsToBEHidden.forEach((object) => {
            object.required = false;

        });
    } else {
        gayab.style.display = "";
        let objectsToBEHidden = gayab.querySelector('tbody').querySelectorAll(":is(input,textarea,select)");
        objectsToBEHidden.forEach((object) => {
            object.required = true;
        });
    }
    checkbox.addEventListener("change", (e) => {
        if (e.target.checked) {
            gayab.style.display = "none";
            let objectsToBEHidden = gayab.querySelector('tbody').querySelectorAll(":is(input,textarea,select)");
            objectsToBEHidden.forEach((object) => {
                object.required = false;
            });
        } else {
            gayab.style.display = "";
            let objectsToBEHidden = gayab.querySelector('tbody').querySelectorAll(":is(input,textarea,select)");
            objectsToBEHidden.forEach((object) => {
                object.required = true;

            });
        }
    });
}

function hideInitializeSimple(checkbox_id, gayabable) {
    let checkbox = document.getElementById(checkbox_id);
    let gayab = document.getElementById(gayabable);
    if (checkbox.checked) {
        gayab.style.display = "none";
        // add .ignore class to all inputs and textareas in gayabable
        let objectsToBEHidden = gayab.querySelectorAll("input,textarea,select");
        objectsToBEHidden.forEach((object) => {
            object.classList.add("ignore");

        });
    } else {
        gayab.style.display = "";
        let objectsToBEHidden = gayab.querySelectorAll("input,textarea,select");
        objectsToBEHidden.forEach((object) => {
            object.classList.remove("ignore");

        });
    }
    checkbox.addEventListener("change", (e) => {
        if (e.target.checked) {
            gayab.style.display = "none";
            let objectsToBEHidden = gayab.querySelectorAll(":is(input,textarea,select)");
            objectsToBEHidden.forEach((object) => {
                object.required = false;
            });
        } else {
            gayab.style.display = "";
            let objectsToBEHidden = gayab.querySelectorAll(":is(input,textarea,select)");
            objectsToBEHidden.forEach((object) => {
                object.required = true;

            });
        }
    });
}

function disableAllInputs()
{
    let inputs = document.querySelectorAll("input, textarea");
    inputs.forEach((input)=>{
        if(input.type == "checkbox" || input.type == "radio" || input.type =="file")
        {
            input.disabled = true;
        }
        else{
            input.setAttribute("readonly","readonly");
        }
    })
    let select = document.querySelectorAll("select");
    select.forEach((sel)=>{
        let parent = sel.parentElement;
        let p = document.createElement("p");
        p.innerHTML = `${sel.value}`;
        sel.remove();
        parent.appendChild(p);
    })
    let btn = document.querySelectorAll(".rmvbtn , .addbtn");
    btn.forEach((b)=>{
        let clone = b.cloneNode(true);
        b.replaceWith(clone);
    })
}

let prepopulated = document.querySelectorAll(".prepopulated");
prepopulated.forEach((div)=>{
    let header = div.querySelector(".card-header")
    header.innerHTML += `<span class="badge bg-label-success ms-2"><i class="bx bx-check-circle"></i> PREPOPULATED & VALIDATED</span>`;
    let tbody = div.querySelector("tbody");
    if (tbody.children.length < 1) {
        let table = div.querySelector('table');
        table.remove();
        let el = document.createElement("div");
        el.innerHTML = `<div class="alert alert-warning ms-3 me-3">You have not achieved any data in this parameter</div>`;
        let card_body = div.querySelector(".card-body");
        if (card_body) {
            card_body.appendChild(el);
        } else {
            div.appendChild(el);
        }
    }
});
