var link = "/static/JsonFile/",
  oneDay = 24 * 60 * 60 * 1000,
  myChart,
  myChart2,
  myChart3,
  request = [],
  day = [],
  week = [],
  month = [],
  year = [],
  all = [],
  pending = [],
  accepted = [],
  rejected = [],
  cancelled = [],
  Userlabel = [],
  all_count = [],
  RequestLabel = [],
  pending_count = [],
  accepted_count = [],
  rejected_count = [],
  completed_count = [],
  cancelled_count = [],
  labeldata = [],
  newUserData = [],
  activeUserData = [],
  TxnLabel = [],
  TxnData = [];

// Main functions

//fucntion to fetch required data from json files
async function fetchData(link, file, p) {
  await fetch(link + file)
    .then((response) => response.json())
    .then((data) => {
      if (file === "user.json") {
        User(JSON.stringify(data), p);
      } else if (file === "trxn.json") {
        TxnChart(JSON.stringify(data), p);
      } else if (file === "request.json") {
        RequestChart(JSON.stringify(data), p);
      }
    })
    .then(function () {});
}

fetchData(link, "user.json", "day");
fetchData(link, "trxn.json", "day");
fetchData(link, "request.json", "day");

function dateRange(startDate, endDate, steps) {
  const dateArray = [];
  let currentDate = new Date(startDate);
  while (currentDate <= new Date(endDate)) {
    var d = new Date(currentDate);
    dateArray.push(d);
    currentDate.setUTCDate(currentDate.getUTCDate() + steps);
  }
  return dateArray;
}

function sortData(data, p) {
  var x = del(JSON.stringify(data), p);
  if (p == 1) {
    return x.sort((a, b) => new Date(a.date_joined) - new Date(b.date_joined));
  } else if (p == 2) {
    return x.sort((a, b) => new Date(a.last_login) - new Date(b.last_login));
  } else {
    return x.sort((a, b) => new Date(a.date_joined) - new Date(b.date_joined));
  }
}

function del(q, p) {
  w = JSON.parse(q);
  w.forEach(function (item, index) {
    if (p == 1) delete item.last_login;
    else if (p == 2) delete item.date_joined;
  });
  return w;
}

//User Graph functions
function User(data, p) {
  var user = JSON.parse(data);

  data = sortData(user, 1);
  var k = new Date();
  var j = new Date();
  j.setDate(j.getDate() - 10);
  var l = new Date();
  l.setDate(l.getDate() - 70);
  var days = dateRange(new Date(j), new Date(k), 1);
  var weeks = dateRange(
    new Date(l),
    new Date(data[Object.keys(data).length - 1].date_joined),
    7
  );
  var months = dateRange(
    new Date(data[0].date_joined),
    new Date(data[Object.keys(data).length - 1].date_joined),
    31
  );
  var years = dateRange(
    new Date(data[0].date_joined),
    new Date(data[Object.keys(data).length - 1].date_joined),
    365
  );

  Userlabel = [];
  newUserData = [];
  activeUserData = [];
  if (p == "day") {
    days.forEach(function (date) {
      var count = 0;
      data.forEach(function (user) {
        // console.log(new Date(date),new Date(user.date_joined), new Date(date).getDate() === new Date(user.date_joined).getDate());
        if (
          new Date(date).getDate() === new Date(user.date_joined).getDate() &&
          new Date(date).getMonth() === new Date(user.date_joined).getMonth() &&
          new Date(date).getFullYear() ===
            new Date(user.date_joined).getFullYear()
        ) {
          count++;
        }
      });
      var s = new Date(date);
      Userlabel.push(
        s.getDate() + " " + s.toLocaleString("en-us", { month: "short" })
      );
      newUserData.push(count);
    });
    data = sortData(user, 2);
    days.forEach(function (date) {
      var count = 0;
      data.forEach(function (user) {
        if (
          new Date(date).getDate() === new Date(user.last_login).getDate() &&
          new Date(date).getMonth() === new Date(user.last_login).getMonth() &&
          new Date(date).getFullYear() ===
            new Date(user.last_login).getFullYear()
        ) {
          count++;
        }
      });
      activeUserData.push(count);
    });
  } else if (p == "week") {
    weeks.forEach(function (date) {
      var count = 0;
      var s = new Date(date);
      var n = new Date(s);
      n.setDate(n.getDate() + 7);

      data.forEach(function (user) {
        if (
          new Date(n).getDate() <= new Date(user.date_joined).getDate() &&
          new Date(n).getMonth() <= new Date(user.date_joined).getMonth() &&
          new Date(date).getFullYear() ===
            new Date(user.date_joined).getFullYear()
        ) {
          count++;
        }
      });

      Userlabel.push(
        s.getDate() +
          " " +
          s.toLocaleString("en-us", { month: "short" }) +
          " - " +
          n.getDate() +
          " " +
          n.toLocaleString("en-us", { month: "short" })
      );
      newUserData.push(count);
    });
    data = sortData(user, 2);
    weeks.forEach(function (date) {
      var count = 0;
      var s = new Date(date);
      var n = new Date(s);
      n.setDate(n.getDate() + 7);
      data.forEach(function (user) {
        if (
          new Date(n).getDate() <= new Date(user.last_login).getDate() &&
          new Date(n).getMonth() <= new Date(user.last_login).getMonth() &&
          new Date(date).getFullYear() ===
            new Date(user.last_login).getFullYear()
        ) {
          count++;
        }
      });
      activeUserData.push(count);
    });
  } else if (p == "month") {
    months.forEach(function (date) {
      var count = 0;
      data.forEach(function (user) {
        if (
          new Date(date).getMonth() === new Date(user.date_joined).getMonth() &&
          new Date(date).getFullYear() ===
            new Date(user.date_joined).getFullYear()
        ) {
          count++;
        }
      });
      var s = new Date(date);

      Userlabel.push(s.toLocaleString("en-us", { month: "short" }));
      newUserData.push(count);
    });
    data = sortData(user, 2);
    months.forEach(function (date) {
      var count = 0;
      data.forEach(function (user) {
        if (
          new Date(date).getMonth() === new Date(user.last_login).getMonth() &&
          new Date(date).getFullYear() ===
            new Date(user.last_login).getFullYear()
        ) {
          count++;
        }
      });
      activeUserData.push(count);
    });
  } else if (p == "year") {
    years.forEach(function (date) {
      var count = 0;
      data.forEach(function (user) {
        if (
          new Date(date).getFullYear() ===
          new Date(user.date_joined).getFullYear()
        ) {
          count++;
        }
      });
      var s = new Date(date);

      Userlabel.push(s.getFullYear());
      newUserData.push(count);
    });
    data = sortData(user, 2);
    years.forEach(function (date) {
      var count = 0;
      data.forEach(function (user) {
        if (
          new Date(date).getFullYear() ===
          new Date(user.last_login).getFullYear()
        ) {
          count++;
        }
      });
      activeUserData.push(count);
    });
  }

  var ctx = document.getElementById("UserChart").getContext("2d");
  if (myChart != null) {
    myChart.destroy();
  }
  myChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: Userlabel,
      datasets: [
        {
          label: "New Users",
          data: newUserData,
          backgroundColor: ["rgba(255, 99, 132, 0.2)"],
          borderColor: ["rgba(255, 99, 132, 1)"],
          fill: false,
          borderWidth: 1,
        },
        {
          label: "Active Users",
          data: activeUserData,
          backgroundColor: ["rgba(54, 162, 235, 0.2)"],
          borderColor: ["rgba(54, 162, 235, 1)"],
          fill: false,
          borderWidth: 1,
        },
      ],
    },
  });
}

function sortTxn(data) {
  return data.sort((a, b) => new Date(a.datetime) - new Date(b.datetime));
}

//Txn Graph functions
function TxnChart(data, p) {
  var data = JSON.parse(data);
  data = sortTxn(data);
  var k = new Date();
  var j = new Date();
  j.setDate(j.getDate() - 10);
  var l = new Date();
  l.setDate(l.getDate() - 70);
  var days = dateRange(new Date(j), new Date(k), 1);
  var weeks = dateRange(new Date(l), new Date(k), 7);
  var months = dateRange(new Date(data[0].datetime), new Date(k), 31);
  console.log(months);
  var years = dateRange(
    new Date(data[0].datetime),
    new Date(data[Object.keys(data).length - 1].datetime),
    365
  );

  TxnLabel = [];
  TxnData = [];

  if (p == "day") {
    days.forEach(function (date) {
      var count = 0;
      var s = new Date(date);
      var n = new Date(date);
      n.setDate(n.getDate() + 7);
      data.forEach(function (user) {
        if (
          new Date(date).getDate() === new Date(user.datetime).getDate() &&
          new Date(date).getMonth() === new Date(user.datetime).getMonth() &&
          new Date(date).getFullYear() === new Date(user.datetime).getFullYear()
        ) {
          count++;
        }
      });
      TxnLabel.push(
        s.getDate() + " " + s.toLocaleString("en-us", { month: "short" })
      );
      TxnData.push(count);
    });
  } else if (p == "week") {
    weeks.forEach(function (date) {
      var count = 0;
      var s = new Date(date);
      var n = new Date(date);
      n.setDate(n.getDate() + 7);
      data.forEach(function (user) {
        if (
          new Date(n).getDate() <= new Date(user.datetime).getDate() &&
          new Date(n).getMonth() <= new Date(user.datetime).getMonth() &&
          new Date(date).getFullYear() === new Date(user.datetime).getFullYear()
        ) {
          count++;
        }
      });

      TxnLabel.push(
        s.getDate() +
          " " +
          s.toLocaleString("en-us", { month: "short" }) +
          " - " +
          n.getDate() +
          " " +
          n.toLocaleString("en-us", { month: "short" })
      );
      TxnData.push(count);
    });
    TxnLabel.pop();
  } else if (p == "month") {
    months.forEach(function (date) {
      var count = 0;
      data.forEach(function (user) {
        if (new Date(date).getMonth() === new Date(user.datetime).getMonth()) {
          count++;
        }
      });
      var s = new Date(date);

      TxnLabel.push(s.toLocaleString("en-us", { month: "short" }));
      TxnData.push(count);
    });
  } else if (p == "year") {
    years.forEach(function (date) {
      var count = 0;
      data.forEach(function (user) {
        if (
          new Date(date).getFullYear() === new Date(user.datetime).getFullYear()
        ) {
          count++;
        }
      });
      var s = new Date(date);

      TxnLabel.push(s.getFullYear());
      TxnData.push(count);
    });
  }

  var ctx = document.getElementById("TxnChart").getContext("2d");
  if (myChart2 != null) {
    myChart2.destroy();
  }

  myChart2 = new Chart(ctx, {
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
        x: {
          beginAtZero: true,
          ticks: {
            max: 10,
          },
        },
      },
    },
    data: {
      labels: TxnLabel,
      datasets: [
        {
          type: "bar",
          label: "Txns",
          data: TxnData,
          backgroundColor: "skyblue",
          borderWidth: 1,
        },
      ],
    },
  });
}

//function for request graph

function RequestChart(k, p) {
  var data = JSON.parse(k);

  RequestLabel = [];
  all_count = [];
  pending_count = [];
  rejected_count = [];
  accepted_count = [];
  all = [];
  pending = [];
  rejected = [];
  accepted = [];

  for (var i = 0; i < data.length; i++) {
    all.push(data[i]);
    if (data[i].status === "Pending") {
      pending.push(data[i]);
    } else if (data[i].status === "Rejected") {
      rejected.push(data[i]);
    } else if (data[i].status === "Accepted") {
      accepted.push(data[i]);
    }
  }

  var k = new Date();
  var j = new Date();
  j.setDate(j.getDate() - 10);
  var l = new Date();
  l.setDate(l.getDate() - 70);
  var days = dateRange(new Date(j), new Date(k), 1);
  var weeks = dateRange(
    new Date(l),
    new Date(data[Object.keys(data).length - 1].date),
    7
  );
  var months = dateRange(
    new Date(data[0].date),
    new Date(data[Object.keys(data).length - 1].date),
    31
  );
  var years = dateRange(
    new Date(data[0].date),
    new Date(data[Object.keys(data).length - 1].date),
    365
  );

  if (p == "day") {
    days.forEach(function (date) {
      var count = 0;
      all.forEach(function (user) {
        if (
          new Date(date).getDate() === new Date(user.date).getDate() &&
          new Date(date).getMonth() === new Date(user.date).getMonth() &&
          new Date(date).getFullYear() === new Date(user.date).getFullYear()
        ) {
          count++;
        }
      });
      var s = new Date(date);
      RequestLabel.push(
        s.getDate() + " " + s.toLocaleString("en-us", { month: "short" })
      );
      all_count.push(count);

      count = 0;
      pending.forEach(function (user) {
        if (
          new Date(date).getDate() === new Date(user.date).getDate() &&
          new Date(date).getMonth() === new Date(user.date).getMonth() &&
          new Date(date).getFullYear() === new Date(user.date).getFullYear()
        ) {
          count++;
        }
      });

      pending_count.push(count);

      count = 0;
      accepted.forEach(function (user) {
        if (
          new Date(date).getDate() === new Date(user.date).getDate() &&
          new Date(date).getMonth() === new Date(user.date).getMonth() &&
          new Date(date).getFullYear() === new Date(user.date).getFullYear()
        ) {
          count++;
        }
      });

      accepted_count.push(count);

      count = 0;
      rejected.forEach(function (user) {
        if (
          new Date(date).getDate() === new Date(user.date).getDate() &&
          new Date(date).getMonth() === new Date(user.date).getMonth() &&
          new Date(date).getFullYear() === new Date(user.date).getFullYear()
        ) {
          count++;
        }
      });

      rejected_count.push(count);
    });
  } else if (p == "week") {
    weeks.forEach(function (date) {
      var count = 0;
      var s = new Date(date);
      var n = new Date(date);
      n.setDate(n.getDate() + 7);
      all.forEach(function (user) {
        if (
          new Date(n).getDate() <= new Date(user.date).getDate() &&
          new Date(n).getMonth() <= new Date(user.date).getMonth() &&
          new Date(date).getFullYear() === new Date(user.date).getFullYear()
        ) {
          count++;
        }
      });

      RequestLabel.push(
        s.getDate() +
          " " +
          s.toLocaleString("en-us", { month: "short" }) +
          " - " +
          n.getDate() +
          " " +
          n.toLocaleString("en-us", { month: "short" })
      );
      all_count.push(count);
      console.log(RequestLabel);
      count = 0;
      pending.forEach(function (user) {
        if (
          new Date(n).getDate() <= new Date(user.date).getDate() &&
          new Date(n).getMonth() <= new Date(user.date).getMonth() &&
          new Date(date).getFullYear() === new Date(user.date).getFullYear()
        ) {
          count++;
        }
      });

      pending_count.push(count);

      count = 0;
      accepted.forEach(function (user) {
        if (
          new Date(n).getDate() <= new Date(user.date).getDate() &&
          new Date(n).getMonth() <= new Date(user.date).getMonth() &&
          new Date(date).getFullYear() === new Date(user.date).getFullYear()
        ) {
          count++;
        }
      });

      accepted_count.push(count);
      count = 0;
      rejected.forEach(function (user) {
        if (
          new Date(n).getDate() <= new Date(user.date).getDate() &&
          new Date(n).getMonth() <= new Date(user.date).getMonth() &&
          new Date(date).getFullYear() === new Date(user.date).getFullYear()
        ) {
          count++;
        }
      });

      rejected_count.push(count);
    });
  } else if (p == "month") {
    months.forEach(function (date) {
      var count = 0;

      all.forEach(function (user) {
        if (new Date(date).getMonth() == new Date(user.date).getMonth()) {
          count++;
        }
      });
      var s = new Date(date);
      RequestLabel.push(s.toLocaleString("en-us", { month: "short" }));
      all_count.push(count);
      count = 0;
      pending.forEach(function (user) {
        if (new Date(date).getMonth() == new Date(user.date).getMonth()) {
          count++;
        }
      });
      var s = new Date(date);
      pending_count.push(count);

      count = 0;
      accepted.forEach(function (user) {
        if (new Date(date).getMonth() == new Date(user.date).getMonth()) {
          count++;
        }
      });
      var s = new Date(date);
      accepted_count.push(count);
      count = 0;
      rejected.forEach(function (user) {
        if (new Date(date).getMonth() === new Date(user.date).getMonth()) {
          count++;
        }
      });
      var s = new Date(date);
      rejected_count.push(count);
    });
  } else if (p == "year") {
    years.forEach(function (date) {
      var count = 0;

      all.forEach(function (user) {
        if (
          new Date(date).getFullYear() === new Date(user.date).getFullYear()
        ) {
          count++;
        }
      });
      var s = new Date(date);

      RequestLabel.push(s.getFullYear());
      all_count.push(count);
      count = 0;
      pending.forEach(function (user) {
        if (
          new Date(date).getFullYear() === new Date(user.date).getFullYear()
        ) {
          count++;
        }
      });

      pending_count.push(count);

      count = 0;
      accepted.forEach(function (user) {
        if (
          new Date(date).getFullYear() === new Date(user.date).getFullYear()
        ) {
          count++;
        }
      });

      accepted_count.push(count);
      count = 0;
      rejected.forEach(function (user) {
        if (
          new Date(date).getFullYear() === new Date(user.date).getFullYear()
        ) {
          count++;
        }
      });
      rejected_count.push(count);
    });
  }

  var ctx = document.getElementById("RequestChart").getContext("2d");
  if (myChart3 != null) {
    myChart3.destroy();
  }

  myChart3 = new Chart(ctx, {
    data: {
      labels: RequestLabel,
      datasets: [
        {
          type: "bar",
          label: "All",
          data: all_count,
          backgroundColor: "rgba(54, 162, 235, 1)",
          borderColor: "rgba(54, 162, 235, 1)",
          borderWidth: 1,
        },
        {
          label: "Pending",
          type: "bar",
          data: pending_count,
          borderColor: "orange",
          backgroundColor: "gold",
          borderWidth: 1,
        },
        {
          label: "Accepted",
          type: "bar",
          data: accepted_count,
          borderColor: "green",
          backgroundColor: "lightgreen",
          borderWidth: 1,
        },
        {
          label: "Rejected",
          type: "bar",
          data: rejected_count,
          borderColor: "red",
          backgroundColor: "#d20d308f",
          borderWidth: 1,
        },
      ],
    },
  });
}
$(document).ready(function () {
  $(".select_period").change(function () {
    var period = $(this).val();
    var id = $(this).attr("id");
    if (id === "user") {
      if (myChart != null) {
        myChart.destroy();
      }
      fetchData(link, "user.json", period);
    } else if (id === "request") {
      if (myChart3 != null) {
        myChart3.destroy();
      }
      fetchData(link, "request.json", period);
    } else if (id === "txn") {
      if (myChart2 != null) {
        myChart2.destroy();
      }
      fetchData(link, "trxn.json", period);
    }
  });

  $(".download-report").click(function () {
    if (this.classList[2] === "csv") {
      if (this.classList[1] === "users") {
        DataToExcel(link + "user.json", 1);
      } else if (this.classList[1] === "txns") {
        DataToExcel(link + "trxn.json", 2);
      } else if (this.classList[1] === "requests") {
        DataToExcel(link + "request.json", 3);
      }
    } else if (this.classList[2] === "pdf") {
      if (this.classList[1] === "users") {
        DataToPDF(link + "user.json", 1);
      } else if (this.classList[1] === "txns") {
        DataToPDF(link + "trxn.json", 2);
      } else if (this.classList[1] === "requests") {
        DataToPDF(link + "request.json", 3);
      }
    }
  });
});

function DataToExcel(url, n) {
  fetch(url)
    .then((response) => response.json())
    .then((data1) => {
      var data = data1;
      var csv = "";
      var filename = "Curropted Data.csv";
      if (n == 1) {
        filename = "Users' Analytics.csv";
        var row = "ID, Last Login, Date Joined";
        row += "\n";
        for (var i = 0; i < data.length; i++) {
          var x = new Date(data[i].date_joined);
          data[i].date_joined =
            x.getDate() +
            " " +
            new Date(x).toLocaleString("en-us", { month: "short" });

          var y = new Date(data[i].last_login);
          data[i].last_login =
            y.getDate() +
            " " +
            new Date(y).toLocaleString("en-us", { month: "short" });

          row += data[i].id + ",";
          row += data[i].last_login + ",";
          row += data[i].date_joined + ",";
          row += "\n";
        }
      } else if (n == 2) {
        filename = "Txns' Analytics.csv";
        var row = "Date, Amount,";
        row += "\n";
        console.log(data);
        for (var i = 0; i < data.length; i++) {
          var d = new Date(data[i].datetime);
          data[i].datetime =
            d.getDate() +
            " " +
            new Date(d).toLocaleString("en-us", { month: "short" }) +
            " " +
            d.getFullYear();
          row += data[i].datetime + ",";
          row += data[i].amount + ",";
          row += "\n";
        }
      } else if (n == 3) {
        filename = "Requests' Analytics.csv";
        var row = "Token, Status, Date";
        row += "\n";
        for (var i = 0; i < data.length; i++) {
          var d = new Date(data[i].date);
          data[i].date =
            d.getDate() +
            " " +
            new Date(d).toLocaleString("en-us", { month: "short" }) +
            " " +
            d.getFullYear();
          row += data[i].token + ",";
          row += data[i].status + ",";
          row += data[i].date + ",";
          row += "\n";
        }
      }

      csv += row;
      console.log(csv);
      var hiddenElement = document.createElement("a");
      hiddenElement.href = "data:text/csv;charset=utf-8," + encodeURI(csv);
      hiddenElement.target = "_blank";
      hiddenElement.download = filename;
      hiddenElement.click();
      data = null;
    });
}

function DataToPDF(url, n) {
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      var x = [],
        filename = "";
      for (let i = 0; i < data.length; i++) {
        x.push(data[i]);
      }
      if (n == 1) {
        filename = "Users'";
      } else if (n == 2) {
        filename = "Txns'";
      } else if (n == 3) {
        filename = "Requests'";
        console.log(x);
      }

      var docDefinition = {
        userPassword: "123",
        ownerPassword: "123456",
        permissions: {
          printing: "highResolution", //'lowResolution'
          modifying: false,
          copying: false,
          annotating: true,
          fillingForms: true,
          contentAccessibility: true,
          documentAssembly: true,
        },
        info: {
          title: filename + " Report - MPayz Admin",
          author: "MPayz",
          subject: "A summary of all " + filename,
        },
        content: [
          {
            text: "MPayz Admin Report",
            bold: true,
            fontSize: 25,
            alignment: "center",
          },
          {
            image: "logo",
            width: 100,
            height: 100,
            alignment: "center",
            margin: [0, 0, 0, 10],
            fit: [100, 100],
          },
          {
            text: filename + " Report",
            bold: true,
            fontSize: 15,
            alignment: "center",
            margin: [0, 0, 0, 10],
          },
        ],
        images: {
          logo: "https://wallet.mpayz.io/static/images/adminpanellogo.png",
        },
        footer: {
          columns: [
            {
              text: "Copyright @MPayz Inc",
              alignment: "center",
            },
          ],
        },
      };

      if (n == 1) {
        docDefinition.content.push({
          table: {
            headerRows: 1,
            widths: [20, "*", "*"],

            body: [
              [
                {
                  text: "ID",
                  alignment: "center",
                  bold: true,
                },
                {
                  text: "Last Login",
                  alignment: "center",
                  bold: true,
                },
                {
                  text: "Date Joined",
                  alignment: "center",
                  bold: true,
                },
              ],
            ],
          },
        });

        for (var i = 0; i < x.length; i++) {
          var y = new Date(x[i].last_login);
          var z = new Date(x[i].date_joined);
          docDefinition.content.push({
            table: {
              headerRows: 1,
              widths: [20, "*", "*"],

              body: [
                [
                  {
                    text: x[i].id,
                    alignment: "center",
                  },
                  {
                    text:
                      y.getDate() +
                      "/" +
                      (y.getMonth() + 1) +
                      "/" +
                      y.getFullYear(),
                    alignment: "center",
                  },
                  {
                    text:
                      z.getDate() +
                      "/" +
                      (z.getMonth() + 1) +
                      "/" +
                      z.getFullYear(),
                    alignment: "center",
                  },
                ],
              ],
            },
          });
        }
      } else if (n == 2) {
        docDefinition.content.push({
          table: {
            headerRows: 1,
            widths: ["*", "*"],

            body: [
              [
                {
                  text: "Date",
                  alignment: "center",
                  bold: true,
                },
                {
                  text: "Amount",
                  alignment: "center",
                  bold: true,
                },
              ],
            ],
          },
        });
        for (var i = 0; i < x.length; i++) {
          var y = new Date(x[i].datetime);

          docDefinition.content.push({
            table: {
              headerRows: 1,
              widths: ["*", "*"],

              body: [
                [
                  {
                    text:
                      y.getDate() +
                      "/" +
                      (y.getMonth() + 1) +
                      "/" +
                      y.getFullYear(),
                    alignment: "center",
                  },
                  {
                    text: x[i].amount,
                    alignment: "center",
                  },
                ],
              ],
            },
          });
        }
      } else if (n == 3) {
        docDefinition.content.push({
          table: {
            headerRows: 1,
            widths: ["*", "*", "*"],

            body: [
              [
                {
                  text: "Date",
                  alignment: "center",
                  bold: true,
                },
                {
                  text: "Status",
                  alignment: "center",
                  bold: true,
                },
                {
                  text: "Token",
                  alignment: "center",
                  bold: true,
                },
              ],
            ],
          },
        });
        for (var i = 0; i < x.length; i++) {
          var y = new Date(x[i].date);
          docDefinition.content.push({
            table: {
              headerRows: 1,
              widths: ["*", "*", "*"],

              body: [
                [
                  {
                    text:
                      y.getDate() +
                      "/" +
                      (y.getMonth() + 1) +
                      "/" +
                      y.getFullYear(),
                    alignment: "center",
                  },
                  {
                    text: x[i].status,
                    alignment: "center",
                  },
                  {
                    text: x[i].token,
                    alignment: "center",
                  },
                ],
              ],
            },
          });
        }
      }

      var a = new Date();

      console.log(docDefinition);
      pdfMake
        .createPdf(docDefinition)
        .download(
          filename +
            " Report " +
            a.getDate() +
            "-" +
            (a.getMonth() + 1) +
            "-" +
            a.getFullYear()
        ) + ".pdf";
    });
}
