window.onload = (event) => {
    let keyparam = document.querySelectorAll("#key-param-tbdy tr");
    let key = document.getElementById("key-param-tbdy");
    let majparam = document.querySelectorAll("#maj-param-tbdy tr");
    let maj = document.getElementById("maj-param-tbdy");
    let minparam = document.querySelectorAll("#min-param-tbdy tr");
    let min = document.getElementById("min-param-tbdy");
    if (keyparam.length >= max_possible_key_params) {
        let addb = key.parentElement.querySelector(".addparam");
        addb.style.display = "none";
    }
    if(keyparam.length <= 1)
    {
        key.querySelectorAll(".rmvparam").forEach((rmv)=>{
            rmv.style.display = "none";
        });
    }
    if (majparam.length >= max_possible_major_params) {
        let addb = maj.parentElement.querySelector(".addparam");
        addb.style.display = "none";
    }
    if(majparam.length <= 1)
    {
        maj.querySelectorAll(".rmvparam").forEach((rmv)=>{
            rmv.style.display = "none";
        });
    }
    if (minparam.length >= max_possible_minor_params) {
        let addb = min.parentElement.querySelector(".addparam");
        addb.style.display = "none";
    }
    if(minparam.length <= 1)
    {
        min.querySelectorAll(".rmvparam").forEach((rmv)=>{
            rmv.style.display = "none";
        });
    }
};

let rmvbtns = document.querySelectorAll(".rmvparam");
rmvbtns.forEach((btn) => {
    btn.addEventListener("click", rmvParam);
});
let addbtns = document.querySelectorAll(".addparam");
addbtns.forEach((btn) => {
    btn.addEventListener("click", addParam);
});
document.querySelectorAll(".rejectedParameterRemove").forEach((rmv)=>{
    rmv.addEventListener("click",cancelParameter);
});
document.querySelectorAll(".server-rejected").forEach((val)=>{
    val.addEventListener("change",()=>{
        location.reload();
    });
})
function rmvParam(e) {
    let ptable = e.target.parentElement.parentElement.parentElement.parentElement;
    e.target.parentElement.parentElement.remove();
    validateParam(ptable);
}

function validateParam(ptable) {
    let max, str;
    let tbdy = ptable.querySelector("tbody");
    str = tbdy.getAttribute("id");

    (str == "key-param-tbdy") ? max = max_possible_key_params   : max;
    (str == "maj-param-tbdy") ? max = max_possible_major_params : max;
    (str == "min-param-tbdy") ? max = max_possible_minor_params : max;

    if (tbdy.childElementCount < max) {
        ptable.querySelector(".addparam").style.display = "block";
    } else {
        ptable.querySelector(".addparam").style.display = "none";
    }
    if (tbdy.childElementCount == 1) {
        tbdy.querySelectorAll(".rmvparam").forEach((btn) => {
            btn.style.display = "none";
        });
    } else {
        tbdy.querySelectorAll(".rmvparam").forEach((btn) => {
            btn.style.display = "block";
        });
    }
}

function addParam(e) {
    let ptable = e.target.parentElement.parentElement.parentElement.parentElement;
    let rmvbtns = ptable.querySelectorAll(".rmvparam");
    let newrow = document.createElement("tr");

    let kmax = 0;
    let kval = 0;
    let keyplaceholder;
    (ptable.children[2].id == "key-param-tbdy") ? (kmax = key_param.key,kval = key_param.value, keyplaceholder="Enter Key Parameter" ) : kmax;
    (ptable.children[2].id == "maj-param-tbdy") ? (kmax = maj_param.key,kval = maj_param.value, keyplaceholder="Enter Major Parameter")  : kmax;
    (ptable.children[2].id == "min-param-tbdy") ? (kmax = min_param.key,kval = min_param.value,  keyplaceholder="Enter Minor Parameter")  : kmax;

    newrow.innerHTML = `<td><textarea placeholder="${keyplaceholder}" class="form-control" rows="8" maxlength= "${kmax}"></textarea>
                                 <div class="charcount">
                                 <span>0</span>
                                 <span>/${kmax}</span>
                             </div>
                           <button type="button" id="tbl-btn" class="rmvparam btn btn-outline-danger">
                             <span class="tf-icons bx bx-trash-alt"></span>&nbsp; Remove
                           </button>
                         </td>
                         <td><textarea class="paraminput form-control" placeholder="First Parameter need to be approved" id="exampleFormControlTextarea1" rows="12" disabled maxlength="${kval}"></textarea>
                             <div class="charcount">
                                 <span>0</span>
                                 <span> /${kval}</span>
                             </div>
                         </td>`;
    let newRmvTemp = newrow.querySelector(".rmvparam");
    let newTxttemp = newrow.querySelectorAll("textarea");
    newRmvTemp.addEventListener("click", rmvParam);
    newTxttemp.forEach((ta)=>{
         ta.addEventListener("input", charactercount);
    });
    ptable.children[2].appendChild(newrow);

    rmvbtns.forEach((btn) => {
        btn.style.display = "block";
    });

    validateParam(ptable);
}

let cancelledParameters = {key:[], major:[], minor:[]};
function cancelParameter(e)
{
    let input = e.target.parentElement.querySelector(".server-rejected");
    let value = input.value;
    (input.dataset.class === "key") ? cancelledParameters.key.push(value) : value;
    (input.dataset.class === "major") ? cancelledParameters.major.push(value) : value;
    (input.dataset.class === "minor") ? cancelledParameters.minor.push(value) : value;
}

function save(is_submit) {
    let keyparam = document.querySelectorAll("#key-param-tbdy tr");
    let majparam = document.querySelectorAll("#maj-param-tbdy tr");
    let minparam = document.querySelectorAll("#min-param-tbdy tr");
    let key_parameters = [];
    let major_parameters = [];
    let minor_parameters = [];
    let isValidate = true;
    keyparam.forEach((tr) => {
        let key = tr.children[0].children[0].value;
        let tempStr = key;
        if (!tempStr.replace(/\s/g, "").length && is_submit) {
            isValidate = false;

            let lis = document.querySelectorAll("button.nav-link");
            lis.forEach((li) => {
                li.classList.remove("active");
                if (li.dataset.bsTarget == "#navs-top-home") {
                    li.classList.add("active");
                }
            });
            document.getElementById("navs-top-profile").classList.remove("show");
            document.getElementById("navs-top-profile").classList.remove("active");
            document.getElementById("navs-top-messages").classList.remove("show");
            document.getElementById("navs-top-messages").classList.remove("active");
            document.getElementById("navs-top-home").classList.add("show");
            document.getElementById("navs-top-home").classList.add("active");
            alert("Key Parameter can't be empty");
            tr.children[0].children[0].focus();
            tr.children[0].children[0].scrollIntoView();
        }
        key_parameters.push(key);
    });
    majparam.forEach((tr) => {
        let key = tr.children[0].children[0].value;
        let tempStr = key;
        if (!tempStr.replace(/\s/g, "").length && is_submit) {
            isValidate = false;

            let lis = document.querySelectorAll("button.nav-link");
            lis.forEach((li) => {
                li.classList.remove("active");
                if (li.dataset.bsTarget == "#navs-top-profile") {
                    li.classList.add("active");
                }
            });

            document.getElementById("navs-top-home").classList.remove("show");
            document.getElementById("navs-top-home").classList.remove("active");
            document.getElementById("navs-top-messages").classList.remove("show");
            document.getElementById("navs-top-messages").classList.remove("active");
            document.getElementById("navs-top-profile").classList.add("show");
            document.getElementById("navs-top-profile").classList.add("active");

            alert("Major Parameter can't be empty");
            tr.children[0].children[0].focus();
            tr.children[0].children[0].scrollIntoView();
        }
        major_parameters.push(key);
    });
    minparam.forEach((tr) => {
        let key = tr.children[0].children[0].value;
        let tempStr = key;
        if (!tempStr.replace(/\s/g, "").length && is_submit) {
            isValidate = false;

            let lis = document.querySelectorAll("button.nav-link");
            lis.forEach((li) => {
                li.classList.remove("active");
                if (li.dataset.bsTarget == "#navs-top-messages") {
                    li.classList.add("active");
                }
            });

            document.getElementById("navs-top-profile").classList.remove("show");
            document.getElementById("navs-top-profile").classList.remove("active");
            document.getElementById("navs-top-home").classList.remove("show");
            document.getElementById("navs-top-home").classList.remove("active");
            document.getElementById("navs-top-messages").classList.add("show");
            document.getElementById("navs-top-messages").classList.add("active");

            alert("Minor Parameter can't be empty");
            tr.children[0].children[0].focus();
            tr.children[0].children[0].scrollIntoView();
        }
        minor_parameters.push(key);
    });
    let key_parameter_count = key_parameters.length;
    let major_parameter_count = major_parameters.length;
    let minor_parameter_count = minor_parameters.length;

    if (!isValidate) {
        return;
    }

    if (is_submit) {
        if (key_parameter_count < 1) {
            alert("Key Parameter must be greater than 1");
            return;
        }
        if (major_parameter_count < 1) {
            alert("Major Parameter must be greater than 0");
            return;
        }
        if (minor_parameter_count < 1) {
            alert("Minor Parameter must be greater than 0");
            return;
        }
    }

    let json = {
        key_parameter_count,
        major_parameter_count,
        minor_parameter_count,
        key_parameters,
        major_parameters,
        minor_parameters,
        cancelled_parameters: cancelledParameters,
        is_submit,
    };
    // console.log(cancelledParameters);
    // alert();
    $.ajax({
        url: window.location.href + "save/",
        type: "POST",
        data: {
            csrfmiddlewaretoken: csrf_token,
            json: JSON.stringify(json),
        },
        beforeSend: function (request) {
            request.setRequestHeader("phase", "Phase 1");
        },
        success: function (data) {
            if (is_submit) {
                alert("Successfully Submitted to RO");
            } else {
                alert("Successfully Saved");
            }
            location.reload();
        },
        failure: function (data) {
            alert("Failed to Save");
        }
    });
}