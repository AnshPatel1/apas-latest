const tooltipOptions = {
    title: "Please Check The Value",
    trigger: 'manual'
};
$(function () {
    $('[data-toggle="tooltip"]').tooltip(tooltipOptions);
})
window.onload = ()=>{
    let cannotBeZeroOnAccept = document.querySelectorAll(".cannotBeZeroOnAccept");
    cannotBeZeroOnAccept.forEach((input)=>{
        let parentTr = input.closest("td");
        let acceptBtn = parentTr.querySelector("input[type=radio][value='accept']");
        if(input.value == 0 && acceptBtn.checked) {
            input.value = "";
        }
    })
};

window.onscroll = ()=>{
    let individualMax = document.querySelectorAll(".individual-max");
    individualMax.forEach((el)=>{
        let dimensions = el.getBoundingClientRect();
        if(dimensions.top < 0 || dimensions.bottom > window.innerHeight)
        {
            if(Number(el.value) > Number(el.getAttribute("max")))
            {
                const scrollPosition = dimensions.top + (dimensions.height / 2) - (window.innerHeight / 2);
                window.scrollBy({
                  top: scrollPosition
                })
                el.dispatchEvent(new Event("change"));
            }
        }
    })
}

document.querySelectorAll(".form-control").forEach((e) => {
    e.dispatchEvent(new Event("input"));
})

let sectionMaxInputs = document.querySelectorAll(".section-max");
sectionMaxInputs.forEach((input) => {
    input.addEventListener("input", sectionMax);
    input.addEventListener("change", (e) => {
        e.target.value = Number(e.target.value).toFixed(2)
        let table = input.closest("table");
        let card = table.closest(".card");
        let max = Number(table.dataset.maxmarks);
        let sum = 0;
        let siblings = table.querySelectorAll(".section-max");
        siblings.forEach((marks) => {
            sum += Number(marks.value);
        })
        if (sum > max) {
            input.value = Number(Number(input.value) - (sum - max)).toFixed(2);
            alert("you have exceeded the maximum marks for this section. Please check the marks again.");
            card.style.border = "1px solid #d9dee3";
            table.setAttribute("aria-invalid", false);
            input.dispatchEvent(new Event("input"))
        }
    });
    input.dispatchEvent(new Event("input"))
    input.dispatchEvent(new Event("change"))
});

let individualMaxInputs = document.querySelectorAll(".individual-max");
individualMaxInputs.forEach((input) => {
    input.setAttribute("placeholder", "Max: " + input.getAttribute("max"))
    input.dataset.toggle = "tooltip";
    input.addEventListener("change", (e) => {
        individualMax(e.target);
    });
});

function sectionMax(e) {
    let table = e.target.closest("table");
    let card = table.closest(".card");
    let max = Number(table.dataset.maxmarks);
    let sum = 0;
    let siblings = table.querySelectorAll(".section-max");
    siblings.forEach((marks) => {
        sum += Number(marks.value);
    })
    if (sum > max) {
        card.style.border = "3px solid red";
        table.setAttribute("aria-invalid", true);
    } else {
        card.style.border = "1px solid #d9dee3";
        table.setAttribute("aria-invalid", false);
    }
    // table.querySelector(".totalmarks").children[0].innerText = sum.toFixed(2);
    table.closest(".card").querySelector(".totalmarks").children[0].innerText = sum.toFixed(2);
}

function individualMax(e) {
    let max = Number(e.getAttribute("max"));
    let min = Number(e.getAttribute("min"));
    if (e.value > max) {
        e.value = max;
        $(e).tooltip('show');
    }
    if (e.value < min) {
        e.value = min;
        $(e).tooltip('show');
    }
    setTimeout(() => {
        $(e).tooltip('hide');
    }, 1500)
    e.value = Number(e.value).toFixed(2);
}


function initializeAcceptRejectDisable(acceptBtnID, rejectBtnID, inputID) {
    // If acceptBtn/rejectBtn are radio btn. When acceptBtn is checked, input is enabled. When rejectBtn is checked, input is disabled.

    let acceptBtn = document.getElementById(acceptBtnID);
    let rejectBtn = document.getElementById(rejectBtnID);
    let input = document.getElementById(inputID);

    if (acceptBtn.checked) {
        input.readOnly = false;

    }
    if (rejectBtn.checked) {
        input.readOnly = true;
    }

    acceptBtn.addEventListener("change", (e) => {
        if (e.target.checked) {
            input.readOnly = false;
            input.value = Number(input.dataset.old);
            if (input.value == 0) {
                input.value = "";
            }
        }
    });
    rejectBtn.addEventListener("change", (e) => {
        if (e.target.checked) {
            input.readOnly = true;
            input.dataset.old = input.value;
            input.value = 0;

        }
    });

}

document.querySelectorAll("input.btn-check").forEach((btn) => {
    if (btn.value == "reject") {
        btn.addEventListener("change", clearRemarksOnReject)
        btn.addEventListener("change",(e) => {
            let marks = e.target.closest("td").querySelector("input[type=\"number\"]");
            if (marks) {
                marks.dispatchEvent(new Event("change"));
            }
        });
    }
})

function clearRemarksOnReject(e) {
    let parentTr = e.target.closest("tr");
    parentTr.querySelector("textarea.form-control.count").value = "";
    parentTr.querySelector("textarea.form-control.count").dispatchEvent(new Event("input"));
}

let cannotBeZeroOnAccept = document.querySelectorAll(".cannotBeZeroOnAccept");
cannotBeZeroOnAccept.forEach((mark) => {
    mark.addEventListener("input",validate0OnAccept);
    mark.addEventListener("change",validate0OnAccept);
    // mark.dispatchEvent(new Event("input"));
    // mark.dispatchEvent(new Event("change"));
})

function validate0OnAccept(e) {
    let parentTr = e.target.closest("td");
    let table = e.target.closest("table");
    let acceptBtn = parentTr.querySelector("input[type=radio][value='accept']");
    let rejectBtn = parentTr.querySelector("input[type=radio][value='reject']");
    let warning = document.createElement("div");
    warning.innerHTML = `
          <div class="alert alert-warning zwarning mt-2" role="alert">
              Marks cannot be 0 when accept is checked. If you want to give 0 marks, please check reject.
          </div>
    `;
    if (Number(e.target.value == 0) && acceptBtn.checked) {
        parentTr.querySelectorAll(".zwarning").forEach((e) => {
            e.remove();
        });
        parentTr.appendChild(warning);
        e.target.style.border = "1px solid red";
        table.setAttribute("aria-invalid", true);
        e.target.setCustomValidity("Marks cannot be 0 when accepted. Please check reject instead");
    } else{
        parentTr.querySelectorAll(".zwarning").forEach(function (e) {
            e.remove();
        });
        e.target.style.border = "1px solid #d9dee3";
        table.setAttribute("aria-invalid", false);
        e.target.setCustomValidity("");

    }
}

let variableData = document.querySelectorAll(".variable-data");
variableData.forEach((div)=>{
    let tbody = div.querySelector("tbody");
    if (tbody.children.length < 1) {
        let table = div.querySelector('table');
        table.style.display="none";
        let el = document.createElement("div");
        el.innerHTML = `<div class="alert alert-warning ms-3 me-3">You have not achieved any data in this parameter</div>`;
        let card_body = div.querySelector(".card-body");
        if (card_body) {
            card_body.appendChild(el);
        } else {
            div.appendChild(el);
        }

        if(div.querySelector(".totalmarks")) {
            div.querySelector(".totalmarks").children[0].innerText = 0 ;
        }
    }
});
