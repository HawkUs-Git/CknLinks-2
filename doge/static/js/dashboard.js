function error(m) {
  var template = document.querySelector("#templates-error").innerHTML
  var id = Math.floor(Math.random() * 1000000)
  template = template.replace("message", m).replace("idi", id)
  document.querySelector(".errors").innerHTML = template + document.querySelector(".errors").innerHTML
  setTimeout(function () {
    console.log(id)
    document.getElementById(id).remove()
  }, 5000)
}

function hide_c_l() {
  document.querySelector(".dashboard-link-info").innerHTML = `
    `
  document.querySelector("#create-link-success").innerHTML = ""
  document.querySelector("#h5a-6").value = ""
  document.querySelector("#slug").value = ""
  if (document.querySelector('.dashboard-create-link').style.opacity == '' || document.querySelector('.dashboard-create-link').style.opacity == '0') {
    document.querySelector('.dashboard-create-link').style.opacity = '100%';
    document.querySelector('.dashboard-create-link').style.display = 'block'
  } else {
    document.querySelector('.dashboard-create-link').style.opacity = '0%';
    document.querySelector('.dashboard-create-link').style.display = 'none'
  };
}

function hide_c_l_l() {
  document.querySelector('.dashboard-create-link').style.opacity = '0%'
}

var dash = {
  new: function () {
    fetch('/api/create/', {
        method: 'POST',
        body: JSON.stringify({
          slug: document.querySelector("#slug").value,
          url: document.querySelector("#h5a-6").value,
          private: false
        })
      })
      .then(response => response.json())
      .then(res => {
        // Print result
        if (res.status == true) {
          dash.link(res.data.link)
          dash.load()
        } else {
          document.querySelector("#create-link-success").innerHTML = `
          <div class="alert alert-danger dash-message">` + res.message + `</div>`
        }
      });
  },
  load: function () {
    document.querySelector(".dashboard-links-view").innerHTML = `
    <Br><br><center><div class="spinner-border text-light" role="status">
     <span class="visually-hidden">Loading...</span>
    </div></center>
    `

    fetch('/api/get/?type=links')
      .then(response => response.json())
      .then(res => {
        document.querySelector(".dashboard-links-view").innerHTML = ``
        res.forEach(function (item, index) {
          document.querySelector(".dashboard-links-view").innerHTML += `
            <div class="dashboard-link" onClick="dash.link('` + item.slug + `')">
              <h4>` + item.title + `</h4>
              <a href="https://https://CknLinks-2.arjun418.repl.co/l/` + item.slug + `" class="dashboard-link-link" target="_blank">https://https://CknLinks-2.arjun418.repl.co/l/<b>` + item.slug + `</b></a>
              <Br><br>
            </div>          
          `
        })
      });
  },
  link: function (id) {
    hide_c_l_l()
    document.querySelector(".dashboard-link-info").innerHTML = `
    <div class="spinner-border text-light" role="status">
     <span class="visually-hidden">Loading...</span>
    </div>
    `
    fetch('/api/link/?id=' + id)
      .then(response => response.json())
      .then(item => {
        document.querySelector(".dashboard-link-info").innerHTML = `
            <h3 class="text-info">` + item.title + `</h3>
            <a class="text-muted" href="` + item.url + `">` + item.url + `</a><br><br>
            <input value="https://https://CknLinks-2.arjun418.repl.co/l/` + item.slug + `" class="dashboard-link-link"  id="current-copy-text" onClick="this.select()" readonly> <button class="link-view-button" onClick="CopyToClipboard()">copy</button><button class="link-view-button" onClick="dash.delete('` + item.slug + `')">delete</button><hr>
            <span style="font-size: 24px;">` + item.clicks + `</span> total clicks<br><img src="https://chart.googleapis.com/chart?cht=qr&chl=`+item.url+`&chs=100x100" class="rounded">
       `
      });
  },
  delete: function (id) {
    fetch('/api/delete/?id=' + id, {
        method: 'POST'
      })
      .then(response => response.json())
      .then(res => {
        document.querySelector(".dashboard-link-info").innerHTML = `
successfully deleted!
       `
        dash.load()
      });
  },
  def_graph: function () {
    fetch('/api/stat')
    .then(response => response.json())
    .then(res => {
          // Graphs
    var ctx = document.getElementById('chart')
    // eslint-disable-next-line no-unused-vars
    ctx.height = "30vh";
    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: [
          '1AM',
          '2AM',
          '3AM',
          '4AM',
          '5AM',
          '6AM',
          '7AM',
          '8AM',
          '9AM',
          '10AM',
          '11AM',
          '12AM',
          '1PM',
          '2PM',
          '3PM',
          '4PM',
          '5PM',
          '6PM',
          '7PM',
          '8PM',
          '9PM',
          '10PM',
          '11PM',
          '12PM'
        ],
        datasets: [{
          data: res,
          backgroundColor: 'transparent',
          borderColor: '#68D696',
          borderWidth: 4,
          pointBackgroundColor: '#68D696'
        }]
      },
      options: {
        maintainAspectRatio: false,
      }
    })
    })
  }
}

function CopyToClipboard() {
  /* Get the text field */
  var copyText = document.getElementById("current-copy-text");

  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */

  /* Copy the text inside the text field */
  document.execCommand("copy");
}

dash.load()
dash.def_graph()