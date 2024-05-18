const searchField = document.querySelector("#searchField");
const searchOutput=document.querySelector(".new_output")
const originalOutput=document.querySelector(".original_output")
const newBody=document.querySelector(".new_body")
const header=document.querySelector(".header-rounded-images")

searchOutput.style.display = "none";

searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0){
        console.log("searchValue", searchValue);
        newBody.innerHTML = "";
        

        fetch("/search", {
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data", data);
                originalOutput.style.display = "none";
                searchOutput.style.display = "block";

                if(data.length===0){
                    searchOutput.innerHTML = "No results found";
                }else{
                    header.style.display = "block";
                    data.forEach((item) => {
                        newBody.innerHTML += `
                        <div class="row row-cols-1 row-cols-md-4 g-4 big">

                                    <img class="card-img-top" src="${item.img_url}" alt="Result Image">
                                    <a class="card-body" href="/products/${item.id}" style="background-color:antiquewhite; display:flex"><h5 class="card-title" style="background-color:antiquewhite;">${item.product_name}</h5></a>
                                
                        </div>
                        
                        
                        `;
                        

                    });
                }
            });
    }else{
        searchOutput.style.display = "none";
        originalOutput.style.display = "block";

        
    }
});