// function deleteNote(noteId) {
//   fetch("/delete-note", {
//     method: "POST",
//     body: JSON.stringify({ noteId: noteId }),
//   }).then((_res) => {
//     window.location.href = "/";
//   });
// }


function deleteNote(noteId) {
  Swal.fire({
    title: "Do you confirm to delete?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Yes, delete it!",
    cancelButtonText: "No, cancel",
  }).then((result) => {
    if (result.isConfirmed) {
      // If user clicks "Yes, delete it!"
      fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
      }).then((_res) => {
        window.location.href = "/";
      });
    } else {
      // If user clicks "No, cancel"
      // Do nothing or handle as needed
    }
  });
}

function updateAsset(asset_Id) {
  alert('hi')
  var new_employee_id = document.getElementById('new_Employee_Id').value;
  
  fetch("/update", {
    method: "POST",
    body: JSON.stringify({ asset_Id: asset_Id, new_employee_id: new_employee_id }),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then((_res) => {
    window.location.href = "/";
  });
}



