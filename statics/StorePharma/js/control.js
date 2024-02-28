  
    function myFunction() {
      var searchby;
      searchby =  document.getElementById("byInput").value;
      var inputID, filterID, tableID, trID, tdID, iID, jID, txtValueID; 
      inputID = document.getElementById("myInput");
      filterID = inputID.value.toUpperCase();
      tableID = document.getElementById("myTable");
      trID = tableID.getElementsByTagName("tr");
      for (iID = 0; iID < trID.length; iID++) { 
        tdID = trID[iID].getElementsByTagName("td")[searchby]; 
        if (tdID) {
          txtValueID = tdID.textContent || tdID.innerText;
          if (txtValueID.toUpperCase().indexOf(filterID) > -1) {
            trID[iID].style.display = "";
          } else {
            trID[iID].style.display = "none";
          }
        } 
    }
       
    } 
    
  
  $('#show').on('click', function () {
      $('.center').show();
      $(this).hide();
  })
  
  $('#close').on('click', function () {
      $('.center').hide();
      $('#show').show();
  }) 