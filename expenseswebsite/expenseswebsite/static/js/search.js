const searchBar = document.querySelector("#searchBar");
const newTable = document.querySelector(".table-output");
const oldTalbe = document.querySelector(".app-table");
const noResults = document.querySelector(".no-results");
const tableBody = document.querySelector("#table-body");
newTable.style.display = "none";
oldTalbe.style.display = "block";
noResults.style.display = "none";

searchBar.addEventListener('keyup',(e)=>{
    const searchTxt = e.target.value;
    console.log(searchTxt)
    if(searchTxt.length>0){
        // console.log(searchTxt.length)
        newTable.style.display = "block";
        oldTalbe.style.display = "none";
        fetch('/search-data',{
            body:JSON.stringify({search_text:searchTxt}),
            method:"POST",
        }).then(res=>res.json())
        .then(data=>{
            console.log('data',data);
            if(data.length===0){
                noResults.style.display = "block";
                newTable.style.display = "none";
            }
            else{
                noResults.style.display = "none";
                newTable.style.display = "block";

                let tableHTML = "";

                data.forEach((element) => {
                    // Build the table rows in the string variable
                    tableHTML += `
                        <tr>
                            <td>${element.amount}</td>
                            <td>${element.category}</td>
                            <td>${element.description}</td>
                            <td>${element.date}</td>
                        </tr>`;
                });
                tableBody.innerHTML = tableHTML;
                
                
                
            }
            // console.log('data',data);

        });
    }
    else{
        newTable.style.display = "none";
        oldTalbe.style.display = "block";
        noResults.style.display = "none";
    }
});