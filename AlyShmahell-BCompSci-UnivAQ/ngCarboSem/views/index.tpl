<!DOCTYPE html>
<html lang="en" prefix="og: http://ogp.me/ns#" ng-app="ngApp">

<head>
    <base href="/">
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="CarboSem" />
    <meta property="og:description" content="Carbon Semantics" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://ngcarbosem.herokuapp.com/" />
    <meta property="og:image" content="static/image/logo.png" />
    <link rel="shortcut icon" href="static/image/favicon.ico" type="image/x-icon" />
    <link rel="icon" href="static/image/favicon.ico" type="image/x-icon" />
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.1/css/all.css" integrity="sha384-5sAR7xN1Nv6T6+dT2mhtzEpVJvfS3NScPQTrOxhwjIuvcA67KV2R5Jz6kr4abQsz" crossorigin="anonymous">
    <link type="text/css" rel="stylesheet" href="static/css/carbosem.css">
    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.7.5/angular.min.js"></script>
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://d3js.org/d3.v5.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
    <script type="text/javascript" src="static/js/carbosem.js"></script>
    <title>Carbon Semantics</title>
</head>

<body ng-controller="ngController">
<main class="main">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark static-top">
          <a class="navbar-brand" href="/">
            Carbon Semantics
              </a>
          <button
            class="navbar-toggler"
            type="button"
            data-toggle="collapse"
            data-target="#targetNavBar"
            aria-controls="targetNavBar"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span class="navbar-toggler-icon"></span>
          </button>
          <div
            class="collapse navbar-collapse customCollapse"
            id="targetNavBar"
          >
            <form
              role="search"
              class="form-inline mt-2 mt-md-0"
              id="search"
            >
              <input
                type="text"
                ng-model="ngFileName"
                placeholder="Search for Sequences"
                class="form-control mr-sm-2"
                name="filename"
              />
              <button
                class="btn btn-outline-success my-2 my-sm-0"
                type="submit"
                ng-click="ngSubmit()"
              >
                Search
                  </button>
            </form>
          </div>
        </nav>
        <canvas></canvas>
        <footer class="bg-dark fixed-bottom custom-footer">
          Copyright &copy; 2018 Aly Shmahell
              <a href="https://github.com/AlyShmahell/ngCarboSem" target="_blank">
              <i class="fab fa-github"></i>
          </a>
        </footer>
      </main>
</body>

</html>
