

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
        var rowId = 
            event.target.parentNode.id;

            // console.log(rowId)
              //this gives id of tr whose button was clicked
            var data = document.getElementById(rowId).querySelectorAll(".row-data"); 
              /*returns array of all elements with 
              "row-data" class within the row with given id*/

           
  
                var fullName = data[0].innerHTML;
                var idNum = data[1].value;
                console.log(fullName,idNum)
  
                
            }
