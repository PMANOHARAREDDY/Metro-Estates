function calcPayment(){
    let p = document.getElementById("price").value;
    let p1=0;
    if (p){
        p = parseFloat(p);
        p1 = (3/100)*p;
        p1 = p1.toFixed(2);
    }
    document.getElementById("rp").innerText="Your PAYMENT AMOUNT IS "+p1+" Rs";
}
