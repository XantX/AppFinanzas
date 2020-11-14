function perfilImg() {
  if (document.getElementById("perfimg").value == "hombre-01.png") {
    document.getElementById("perfimg").value = "mujer-01.png";
    console.log(document.getElementById("perfimg").value);
  } else {
    document.getElementById("perfimg").value = "hombre-01.png";
    console.log(document.getElementById("perfimg").value);
  }
}
function activacion(id) {
  moverse = document.getElementById(id);
  link = document.getElementById("linkCuenta");
  moverse.classList.remove("active");
  link.classList.remove("active");

  algo = document.getElementById("cuentaDni");
  algo.innerHTML = id;
}
function DNI(dni) {
  confir = document.getElementById("comfirDNI");
  confir.innerHTML = dni;
  advertencia = document.getElementById("advertencia");
  advertencia.style.display = "none";
}
function confirmar() {
  input = document.getElementById("inputDNI");
  dni = document.getElementById("comfirDNI");
  if (input.value === dni.innerHTML) {
    location.href = "/delete/" + dni.innerHTML;
    console.log("/delete/" + dni.innerHTML);
  } else {
    input.value = "";
    advertencia = document.getElementById("advertencia");
    advertencia.style.display = "block";
  }
}
function pasar() {
  Cobrar = document.getElementById("cobrar");
  Retiro = document.getElementById("retiro");
  Regreso = document.getElementById("regreso");
  Cobrar.classList.remove("active");
  Retiro.classList.remove("active");
  Regreso.classList.remove("active");
}
