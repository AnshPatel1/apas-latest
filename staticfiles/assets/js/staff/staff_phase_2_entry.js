window.onload = (event) => {

    validateFileField(document.getElementById("file-input-form"));

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


function rmvParam(e) {
    let ptable = e.target.parentElement.parentElement.parentElement.parentElement;
    e.target.parentElement.parentElement.remove();
    validateParam(ptable);
}

function validateParam(ptable) {
    let max, str;
    let tbdy = ptable.querySelector("tbody");
    str = tbdy.getAttribute("id");
    (str == "key-param-tbdy") ? max = max_possible_key_params : max;
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

    newrow.innerHTML = `<td><input id="defaultInput" class="form-control" type="text" placeholder="Default input" />
                  <button type="button" id="tbl-btn" class="rmvparam btn btn-outline-danger">
                    <span class="tf-icons bx bx-trash-alt"></span>&nbsp; Remove
                  </button>
                </td>
                <td><textarea class="form-control paraminput" id="exampleFormControlTextarea1" rows="3" disabled></textarea></td>`;
    let newRmvTemp = newrow.querySelector(".rmvparam");
    newRmvTemp.addEventListener("click", rmvParam);
    ptable.children[2].appendChild(newrow);

    rmvbtns.forEach((btn) => {
        btn.style.display = "block";
    });

    validateParam(ptable);
}
function txtIsValid(val)
{
    if(!val.replace(/\s/g, "").length) {
        return false;
    }
    return true;
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
        let val = tr.children[1].children[0].value;
        let obj = {};
        obj[key] = val;
        let tempStr = val;
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
            tr.children[1].children[0].focus();
            return;
        }
        key_parameters.push(obj);
    });
    majparam.forEach((tr) => {
        let key = tr.children[0].children[0].value;
        let val = tr.children[1].children[0].value;
        let obj = {};
        obj[key] = val;
        let tempStr = val;
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
            tr.children[1].children[0].focus();
            return;
        }
        major_parameters.push(obj);
    });
    minparam.forEach((tr) => {
        let key = tr.children[0].children[0].value;
        let val = tr.children[1].children[0].value;
        let obj = {};
        obj[key] = val;
        let tempStr = val;
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
            tr.children[1].children[0].focus();
            return;
        }
        minor_parameters.push(obj);
    });
    let key_parameter_count = key_parameters.length;
    let major_parameter_count = major_parameters.length;
    let minor_parameter_count = minor_parameters.length;

    let self_development_check = document.getElementById("training-taken").checked;
    if(self_development_check && is_submit)
    {
        let self_development_form  = document.querySelector(".self-development-container");
        let fileInputs = self_development_form.querySelectorAll("input[type=file]");

        fileInputs.forEach((input)=>{
            if(input.files.length == 0){
                alert("Empty File Field !");
                isValidate = false;
                input.scrollIntoView();
                input.focus();
            }
        })
    }

    var mooc_completed = document.getElementById('mooc-taken').checked;
    var mooc_description = document.getElementById('mooc-description').value;
    if(mooc_completed && is_submit)
    {
        if(!txtIsValid(mooc_description))
        {
            alert("Empty Mooc Description");
            return;
        }
        let moocFile = document.getElementById("mooc-file-input");
        if(moocFile.files.length == 0 && requireFileValidation)
        {
            alert("Please Select Mooc File and Click Upload !")
            moocFile.focus();
            moocFile.scrollIntoView();
            isValidate = false;
            return;
        }
    }


    var other_activities_completed = document.getElementById('other-activity-check').checked;
    var other_activities_data = document.getElementById('other-activity-text').value;
    if(other_activities_completed)
    {
        if(!txtIsValid(other_activities_data) && is_submit)
        {
            document.getElementById("other-activity-check").focus();
            alert("Other Activities Description Cannot be Empty");
            isValidate = false;
            return;
        }
    }
    let self_evaluations = {
        key_highlights: document.getElementById('key-highlights'),
        challenges: document.getElementById('challenges'),
        areas_of_improvement: document.getElementById('areas-of-improvement'),
        areas_of_strength: document.getElementById('areas-of-strength'),
    }
    for(let el in self_evaluations)
    {
        if(!txtIsValid(self_evaluations[el].value) && is_submit)
        {
            alert(`${el} cannot be empty`);
            self_evaluations[el].scrollIntoView();
            self_evaluations[el].focus();
            isValidate = false;
            return;
        }
    }
    var self_eval = {
        "key_highlights": document.getElementById('key-highlights').value,
        "challenges": document.getElementById('challenges').value,
        "areas_of_improvement": document.getElementById('areas-of-improvement').value,
        "areas_of_strength": document.getElementById('areas-of-strength').value,
    }

    if (!isValidate) {
        return;
    }

    let json = {
        is_submit,
        key_parameter_count,
        major_parameter_count,
        minor_parameter_count,
        key_parameters,
        major_parameters,
        minor_parameters,
        // self_development,
        mooc_completed,
        mooc_description,
        other_activities_completed,
        other_activities_data,
        self_eval,
        "training_taken": document.getElementById("training-taken").checked
    };

    $.ajax({
        type: "POST", url: window.location.href + "save/", beforeSend: function (request) {
            request.setRequestHeader("phase", "Phase 2");
        }, data: {
            csrfmiddlewaretoken: csrf_token, json: JSON.stringify(json),
        }, success: function (response) {
            if (response === "Submitted") {
                alert("Congratulations! Your appraisal is submitted Successfully to RO. Please wait for further instructions");
                    location.reload()
            } else {
                alert("Saved successfully. You may logout now");
                // redirect to dashboard
                location.reload()
            }
        },
    });
}

function hideSpinner() {
    document.getElementById("file-spinner").style.display = "none";
}

function showSpinner() {
    document.getElementById("file-spinner").style.display = "inline-block";
}

function submitMooc() {
    var fd = new FormData();
    file_urls = document.querySelectorAll(".file-input-custom");
    var files = $('#mooc-file-input')[0].files;
    let filediv = document.getElementById("file-input-form");

    // console.log($('#mooc-file-input').checkValidity());

    // Check file selected or not 
    if (files.length > 0) {
        for (let i = 0; i < filediv.children.length; i++) {
            fd.append('file', files[i]);
        }
        fd.append('csrfmiddlewaretoken', csrf_token);
        // alert(window.origin + '/appraisee/mooc/upload/')
        let spinner = document.getElementById("file-spinner");
        $.ajax({
            url: window.origin + '/appraisee/mooc/upload/',
            type: 'post',
            data: fd,
            contentType: false,
            processData: false,
            beforeSend: showSpinner,
            complete: hideSpinner,
            success: function (response) {
                if (response) {
                    // $("#img").attr("src", response);
                    // $(".preview img").show(); // Display image element
                    response_json = JSON.parse(response);
                    var file_link_area = document.getElementById("file-link-area");
                    file_link_area.innerHTML = "File uploaded  " + response_json.filename + "<a target='_blank' href=\"" + response_json.file_url + "\"> view</a>";
                    // alert(JSON.stringify(response));
                } else {
                    alert('file not uploaded');
                }
            },
        });
    } else {
        alert("Please select a file.");
    }
}


let rmvfilebtns = document.querySelectorAll(".rmvfile");
rmvfilebtns.forEach((btn) => {
    btn.addEventListener("click", removeFileField);
});

function removeFileField(e) {
    let filecontainer = e.target.closest(".file-container");
    let formfloating = filecontainer.parentElement;
    if (filecontainer.querySelectorAll('input[type="file"]').length == 0) {
        let id = filecontainer.querySelector('input[type="hidden"]').getAttribute("value");
        let fd = new FormData();
        fd.append("file_id", id);
        fd.append("csrfmiddlewaretoken", csrf_token);
        $.ajax({
            url: window.origin + "/appraisee/staff/certifications/delete/",
            type: 'post',
            data: fd,
            processData: false,
            contentType: false,
            success: () => {
                alert("File Deleted Successfully");
            }
        });
        filecontainer.remove();
    } else {
        filecontainer.remove();
    }
    validateFileField(formfloating);
}

function validateFileField(formfloating) {

    if (formfloating.childElementCount <= 1) {
        formfloating.querySelectorAll(".rmvfile").forEach((rmbtn) => {
            rmbtn.setAttribute("disabled", "");
        });
    } else {
        formfloating.querySelectorAll(".rmvfile").forEach((rmbtn) => {
            rmbtn.removeAttribute("disabled");
        });
    }
    if (formfloating.childElementCount >= max_trainings) {
        document.querySelector("#file-add-btn").style.display = "none";
    } else {
        document.querySelector("#file-add-btn").style.display = "inline-block";
    }
}

let addbtn = document.getElementById("file-add-btn");
addbtn.addEventListener("click", addFileField);

function addFileField(e) {
    let addbtn = e.target;
    let div = addbtn.parentElement.parentElement.parentElement;
    let form = div.children[2];
    let field = document.createElement("div");
    field.setAttribute("class", "file-container");
    file_count++;
    file_index_list.push(file_count);
    field.innerHTML = `
                         <input
                            type="text"
                            name="name"
                            class="course-input form-control"
                            id="course-name-` + file_count + `"
                            value=""
                            placeholder="Name of the Course, Course Code"
                            />
                    <div class="row mb-3">
                        <div class="col-md-8">
                            <input
                                    class="form-control"
                                    type="file"
                                    value=""
                                    style="margin:10px 0px"
                                    placeholder="Upload File"
                                    id="course-file-input-` + file_count + `"
                                    accept=".pdf,image/*"
                            />
                            <div class="ms-3 mb-3">
                                <small id="file-link-area-` + file_count + `">
                                        No file uploaded
                                </small>
                            </div>
                            <input type="hidden" name="file-id" value=""/>
    
                        </div>
    
    
                        <div class="col-md-4">
    
                            <button type="button" id="tbl-btn"
                                    class="rmvfile btn btn-outline-danger">
                                <span class="tf-icons bx bx-trash-alt"></span>&nbsp;
                                Remove
                            </button>
                            <input type="hidden"  id="rmv-id" name="rmv-id" value="` + file_count + `"/>
                        </div>
                        <hr>
                    </div>
                    `;

    form.appendChild(field);
    let rmfile = field.querySelector(".rmvfile");
    rmfile.addEventListener("click", removeFileField);
    validateFileField(form);
}

function multiFileBeforeSend() {
    let spinner = document.getElementById("cert-file-spinner");
    spinner.style.display = "inline-block";
}

function multiFileAfterSend() {
    let spinner = document.getElementById("cert-file-spinner");
    spinner.style.display = "none";
}

function submitMultiFiles() {
    // take description from id course-input-1, course-input-2, course-input-3 ... based on variable file_count
    // take file from id course-file-input-1, course-file-input-2, course-file-input-3 ... based on variable file_count
    // add it to formdata
    // send it to server
    // code begins below
    let formdata = new FormData();
    formdata.append("csrfmiddlewaretoken", csrf_token);

    let fileform = document.getElementById("file-input-form");
    let fcontainers = fileform.querySelectorAll(".file-container");

    for (let i = 0; i < fcontainers.length; i++) {
        let name = fcontainers[i].querySelector(".course-input");
        let field = fcontainers[i].querySelectorAll('input[type="file"]');
        if (field.length == 0) {
            continue;
        } else {
            let tempStr = name.value;
            if (!tempStr.replace(/\s/g, '').length) {
                alert("name cannot be empty");
                return;
            }
            if (field[0].files.length == 0) {
                alert("no files selected");
                return;
            }
            formdata.append("name", name.value);
            formdata.append("file", field[0].files[0]);
        }
    }
    $.ajax({
        url: window.origin + "/appraisee/staff/certifications/upload/",
        type: "post",
        data: formdata,
        contentType: false,
        processData: false,
        // add header

        beforeSend: multiFileBeforeSend,
        complete: multiFileAfterSend,
        success: function (response) {
            if (response) {
                response_json = JSON.parse(response);
                let index = 0;
                for (let i = 0; i < fcontainers.length; i++) {
                    let filefield = fcontainers[i].querySelector(`input[type="file"]`);
                    if (filefield) {

                        let name = fcontainers[i].querySelector(`input[type="text"]`);
                        let link = fcontainers[i].querySelector("small");
                        let fileid = fcontainers[i].querySelector(`input[name="file-id"]`);
                        filefield.remove();
                        name.innerText = response_json[index].name;
                        name.setAttribute("disabled", "disabled");
                        link.innerHTML = `File Uploaded ` + response_json[index].filename + ` <a href="` + response_json[index].url + `">view</a>`;
                        fileid.value = response_json[index].id;
                        index++;
                    }
                }
                alert("Files Uploaded Successfully");
            } else {
                alert('file not uploaded');
            }
        },
    });
}


document.getElementById("training-taken").addEventListener("click", (e) => {
    if (e.target.checked) {
        document.getElementById("file-input-form").style.display = "block";
        document.getElementById("cert-submit-area").style.display = "inline-block";
    } else {
        document.getElementById("file-input-form").style.display = "none";
        document.getElementById("cert-submit-area").style.display = "none";
    }
});

let checkb = document.querySelectorAll(".form-check-input");

$(document).ready(function () {
    if (need_to_show) {
        for (let i = 0; i < min_trainings; i++) {
            document.getElementById("file-add-btn").click();
        }
    }

    let addbtn = document.getElementById("file-add-btn");
    let div = addbtn.parentElement.parentElement.parentElement;
    let form = div.children[2];
    if (form.children.length >= max_trainings) {
        document.getElementById("file-add-btn").style.display = "none";
    } else {
        document.getElementById("file-add-btn").style.display = "inline-block";
    }
    if (document.getElementById("training-taken").checked) {
        document.getElementById("file-input-form").style.display = "block";
        document.getElementById("cert-submit-area").style.display = "inline-block";
    } else {
        document.getElementById("file-input-form").style.display = "none";
        document.getElementById("cert-submit-area").style.display = "none";
    }
    if (document.getElementById("other-activity-check").checked) {
        document.getElementById("other-activity-text").style.display = "inline-block";
    } else {
        document.getElementById("other-activity-text").style.display = "none";
    }
    if (document.getElementById("mooc-taken").checked) {
        document.getElementById("mooc-div").style.display = "block";
        document.getElementById("mooc-submit-area").style.display = "block";
    } else {
        document.getElementById("mooc-div").style.display = "none";
        document.getElementById("mooc-submit-area").style.display = "none";
    }
    // document.getElementById("other-activity-check").addEventListener("change",(e)=>{
    //    if(e.target.style.display = "inline-block") {
    //     document.getElementById("other-activity-text").style.display = "inline-block";
    //     } else {
    //         document.getElementById("other-activity-text").style.display = "none";
    //     }
    // });
    document.getElementById("other-activity-check").addEventListener("change", () => {
        if (document.getElementById("other-activity-check").checked) {
            document.getElementById("other-activity-text").style.display = "inline-block";
        } else {
            document.getElementById("other-activity-text").style.display = "none";
        }
    });
    checkb.forEach((chk) => {
        chk.addEventListener("change", (e) => {
            let parentDiv = e.target.parentElement.parentElement;
            let forms = parentDiv.querySelectorAll(".form-floating");
            if (chk.checked) {
                forms.forEach(element => {
                    element.style.display = "block";
                });
            } else {
                forms.forEach(element => {
                    element.style.display = "none";
                });
            }
        });
    });
});
