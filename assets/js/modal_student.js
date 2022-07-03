//   $("#submit").click(function () {

//     var fullName = document.getElementById("Mfull_name").getAttribute("value")
//     var s = document.getElementById("Ifull_name")
//     s.placeholder = fullName
//       var str = "You Have Entered "
//           + "Name: " +  " and Marks: " ;
//         console.log(fullName)
//       $("#modal_body").html(str);
//   });

function show(event) {
  var rowId = event.target.parentNode.id;

  // console.log(rowId)
  //this gives id of tr whose button was clicked
  var data = document.getElementById(rowId).querySelectorAll(".row-data");
  /*returns array of all elements with 
              "row-data" class within the row with given id*/

  var fullName = data[0].innerHTML;
  var cid = data[1].getAttribute("value");
  var sid = data[2].getAttribute("value");
  var is_registered = data[3].getAttribute("value");
  var select = document.getElementById("ICourseSelect");
  var length = select.options.length;

  var registered_elem = document.getElementById("IIsRegistered");
  var courses = JSON.parse(select.getAttribute("value"));
  if (is_registered == "True") {
    registered_elem.checked = true;
  } else {
    registered_elem.checked = false;
  }

  document.getElementById("Ifull_name").placeholder = fullName;
  document.getElementById("Isid").value = sid;
  for (i = length - 1; i >= 0; i--) {
    select.options[i] = null;
  }
  for (element in courses) {
    var opt = document.createElement("option");
    opt.value = courses[element]["cid"];

    opt.innerHTML = courses[element]["title"];
    if (cid === opt.value) {
      opt.selected = true;
    }

    // whatever property it has

    // then append it to the select element
    select.appendChild(opt);
    // index++;
  }
}
