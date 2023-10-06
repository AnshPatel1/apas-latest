const tooltipOptions = {
    title: "Please Check The Value",
    trigger: 'manual'
};
$(function () {
  $('[data-toggle="tooltip"]').tooltip(tooltipOptions);
})

let remarks = document.querySelectorAll("textarea").forEach((e)=>{
    e.dispatchEvent(new Event("input"));
})

let sectionMaxInputs = document.querySelectorAll(".section-max");
sectionMaxInputs.forEach((input) => {
    input.addEventListener("input", sectionMax);
    input.addEventListener("change", (e) => {
        e.target.value = Number(e.target.value).toFixed(2)
    });
});

let individualMaxInputs = document.querySelectorAll(".individual-max");
individualMaxInputs.forEach((input) => {
    input.dataset.toggle = "tooltip";
    input.setAttribute("placeholder", "Max " + input.getAttribute("max"));
    input.addEventListener("change", (e) => {
        individualMax(e.target);
    });
});

let agreeWithR1Check = document.querySelectorAll(".agree-with-r1");
agreeWithR1Check.forEach((check)=>{
    check.addEventListener("change",(e)=>{ resetToR1Input(e.target) })
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
        card.style.border = "1px solid red";
        table.setAttribute("aria-invalid", "true");
    } else {
        card.style.border = "1px solid #d9dee3";
        table.setAttribute("aria-invalid", "false");
    }
    table.querySelector(".totalmarks").children[0].innerText = sum.toFixed(2);
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
    setTimeout(()=>{
        $(e).tooltip('hide');
    },1500)
    e.value = Number(e.value).toFixed(2);
}


function resetToR1Input(self)
{
    let parent = self.closest("td");
    let r1input = parent.querySelector(".r1-input");
    let r2input = parent.querySelector(".r2-input");

    if(self.checked)
    {
        if(r1input.hasAttribute("data-check"))
        {
            let r1Action = r1input.dataset.check;
            if(r1Action === "accept")
            {
                parent.querySelector(".checkbox-accept").checked = true;
                parent.querySelector(".checkbox-reject").checked = false;
            }
            else
            {
                parent.querySelector(".checkbox-reject").checked = true;
                parent.querySelector(".checkbox-accept").checked = false;
            }
            parent.querySelector(".checkbox-accept").setAttribute("disabled","");
            parent.querySelector(".checkbox-reject").setAttribute("disabled","");
            return;
        }

        r2input.value = r1input.value;
        r2input.setAttribute("disabled","");
    }
    else
    {
        if(r1input.hasAttribute("data-check"))
        {
            parent.querySelector(".checkbox-accept").removeAttribute("disabled");
            parent.querySelector(".checkbox-reject").removeAttribute("disabled");
            return;
        }

        r2input.disabled = "false";
        r2input.removeAttribute("disabled");
    }
}

let agreeCheckbox = document.querySelectorAll(".agreeCheckbox");
agreeCheckbox.forEach((check)=>{
    check.addEventListener("change",r1_remarks_marks);
});
function r1_remarks_marks(e) {
    let wrap = e.target.closest(".action-wrap");
    if (e.target.checked) {
        let r1 = wrap.querySelector(".r1-action");
        if(r1.classList.contains("marks") || r1.classList.contains("select"));
        {
            let r2 = wrap.querySelector(".r2-action");
            r2.value = r1.value;
        }
        if(r1.classList.contains("action"))
        {
            let r2 = wrap.querySelectorAll(".r2-action");
            r2.forEach((check)=>{
               if(check.value == r1.value)
               {
                   check.checked = true;
               }
               else
               {
                   check.checked = false;
               }
            });
        }
        wrap.querySelectorAll('.r2-action').forEach((element)=>{
            element.setAttribute("disabled", true);
        })
    } else {
        e.target.closest(".action-wrap").querySelectorAll('.r2-action').forEach((element)=>{
            element.removeAttribute("disabled");
        })
    }
}