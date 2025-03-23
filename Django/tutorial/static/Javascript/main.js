//Get search FORM and PAGE Links
let searchForm = document.getElementById('searchForm')
let pageLinks = document.getElementsByClassName('btn')

//ensure searchForm exists.
if(searchForm){
    for(let i=0; pageLinks.length > i; i++){
        pageLinks[i].addEventListener('click', function (e){
            e.preventDefault()
            
            //GET THE DATA ATTRIBUTE
            let page = this.dataset.page
            //console.log('PAGE',page)

            //ADD HIDDEN SEARCH INPUT TO FORM
            searchForm.innerHTML += `<input value=${page} name="page" hidden/>`
            
            
            //SUBMIT FORM
            searchForm.submit()
        })
    }
}
