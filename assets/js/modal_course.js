function show2(event) {
    var headingId = event.target.parentNode.parentNode.id;
    


   
        //this gives id of tr whose button was clicked

    var data = document.getElementById(headingId).querySelectorAll(".course-data");
    
    var courseId = data[0].getAttribute("value")
    var courseName = data[1].getAttribute("value")
    var teachers = JSON.parse(data[2].getAttribute("value"))
    var isActive = data[3].getAttribute("value")
    var tid = data[4].getAttribute("value")
    var isActiveElem = document.getElementById("IIsActive")

    document.getElementById("c_name").value = courseName
    document.getElementById("c_id").value = courseId
//###############################################################################33
    var Tselect = document.getElementById("ITeacherSelect");
    
    var Tlength = Tselect.options.length;
    
    

    for (i = Tlength - 1; i >= 0; i--) {
        Tselect.options[i] = null;
    }

    for (element in teachers) {
        var opt = document.createElement("option");
        opt.value = teachers[element]["tid"];

        opt.innerHTML = teachers[element]["last_name"];
        Tselect.appendChild(opt)
        if (tid === opt.value) {
            opt.selected = true;
        }
// ################################################################################

var Cselect = document.getElementById("ITeacherSelect");
    
var Clength = Cselect.options.length;



for (i = Clength - 1; i >= 0; i--) {
    Cselect.options[i] = null;
}

for (element in teachers) {
    var opt = document.createElement("option");
    opt.value = teachers[element]["tid"];

    opt.innerHTML = teachers[element]["last_name"];
    Cselect.appendChild(opt)
    if (ncid === opt.value) {
        opt.selected = true;
    }
}
if (isActive == "True") {
    isActiveElem.checked = true;
  } else {
    isActiveElem.checked = false;
  }

}