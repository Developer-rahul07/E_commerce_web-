$('#slider1, #slider2, #slider3 , #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function (){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    // console.log(id)
    $.ajax({
        type: "GET",
        url : "/plusecart",
        data : {
            prod_id : id
        },
        success: function(data){
            // console.log(data)
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})

$('.minus-cart').click(function (){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    console.log(id)
    $.ajax({
        type: "GET",
        url : "/minusecart",
        data : {
            prod_id : id
        },
        success: function(data){
            // console.log(data)
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})


// remove cart  is not working ! see video 5.00 -5.40 ===https://www.youtube.com/watch?v=I6rR3Se72BU
$('.remove-cart').click(function (){
    var id = $(this).attr("pid").toString();
    var eml = this 
    // console.log(id)
    $.ajax({
        type: "GET", 
        url : "/removecart",
        data : {
            prod_id : id
        },
        success: function(data){
            console.log("delete")
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})

const order_box = document.getElementsByClassName("order_box");

const order = () => {
//   document.getElementsByClassName("order_box").innerText = " NO MONEY 😂!! NO PRODUCT 😂!!"
order_box.innerText =  " NO MONEY 😂!! NO PRODUCT 😂!!"
}

setTimeout(order() ,1000);