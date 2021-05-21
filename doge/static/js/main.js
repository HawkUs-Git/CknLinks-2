var magic = {
  new: function () {
    fetch('/api/create/', {
        method: 'POST',
        body: JSON.stringify({
          slug: document.querySelector("#create-link-slug").value,
          url: document.querySelector("#create-link-url").value,
          private: document.querySelector("#create-link-checkbox").checked
        })
      })
      .then(response => response.json())
      .then(res => {
        // Print result
        if (res.status == true){
          document.querySelector("#create-link-success").innerHTML = `
          <div class="alert alert-success">`+res.message+`<br><a href="`+res.data.link+`">`+res.data.link+`</a>
          `
        }
        else{
          document.querySelector("#create-link-success").innerHTML = `
          <div class="alert alert-danger">`+res.message+`</div>`
        }
      });
  }
}