function show2(event) {
    var heading = event.target.closest("div");
    


   
        //this gives id of tr whose button was clicked
   
    

    var data = heading.querySelectorAll(".course-data");
    
    var courseId = data[0].getAttribute("value")
    var courseName = data[1].getAttribute("value")
    var teachers = JSON.parse(data[2].getAttribute("value"))
    var isActive = data[3].getAttribute("value")
    var tid = data[4].getAttribute("value")
    var next_course_select = document.getElementById("INextCourse")
    var courses = JSON.parse(next_course_select.getAttribute("value"))
    var isActiveElem = document.getElementById("IIsActive")
    var ncid = data[5].getAttribute("value")
    var cid_num = data[6].getAttribute("value")

    document.getElementById("Ic_name").value = courseName
    document.getElementById("Icid_num").value = cid_num
    document.getElementById("course-idd").value = courseId
    console.log(courseId)
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


    
var Clength = next_course_select.options.length;



for (i = Clength - 1; i >= 0; i--) {
    next_course_select.options[i] = null;
}

for (element in courses) {
    var opt = document.createElement("option");
    opt.value = courses[element]["cid"];

    opt.innerHTML = courses[element]["title"];
    next_course_select.appendChild(opt)
    if (ncid === opt.value) {
        opt.selected = true;
    }
}
if (isActive == "True") {
    isActiveElem.checked = true;
  } else {
    isActiveElem.checked = false;
  }

}}