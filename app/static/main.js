function required() {
  var empt = document.forms["form1"]["content"].value;
  if (empt == "") {
    alert("Please input a valid name.");
    return false;
  }
  else {
    return true;
  }
}
