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
  var cid = data[0].getAttribute('value')
  var sid = data[1].getAttribute("value");
  var select = document.getElementById("ICourseSelect")
  var courses = JSON.parse(select.getAttribute("value"))

  console.log(cid)

  document.getElementById("Ifull_name").placeholder = fullName;

  for (element in courses) {
    console.log(courses);
    var opt = document.createElement("option");
    opt.value = courses[element]["cid"];
    
    opt.innerHTML = courses[element]["title"];
    if(cid === opt.value){

      opt.selected = true

    }
    
    
    // whatever property it has

    // then append it to the select element
    select.appendChild(opt);
    // index++;
  }
}
