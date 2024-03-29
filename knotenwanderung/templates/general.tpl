<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <link rel="stylesheet" href="/static/bootstrap.min.css">

    <title>{{title}} - Knotenwanderung</title>

    <style>
      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }

      body {
        padding-top: 4.5rem;
      }

      .form-control:focus{
        border-color: rgb(40, 167, 69);
        -webkit-box-shadow: none;
        box-shadow: none;
      }
    </style>
  </head>
  <body>
    <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <a class="navbar-brand">Knotenwanderung</a>

      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <a class="nav-link" href="/">Main</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/bulk">Bulk</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="https://github.com/hackspace-marburg/ffmr-knotenwanderung">GitHub</a>
        </li>
        </ul>

        <form class="form-inline mt-2 mt-md-0" action="/s" method="post">
          <input class="form-control mr-sm-2" type="text"
            name="hostname" placeholder="Hostname"
            value="{{search if search else ""}}" aria-label="Search">
          <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
        </form>
      </div>
    </nav>

    <main role="main" class="container">
      <div class="jumbotron">
        <h1>{{title}}</h1>
        <p class="lead">{{!content}}</p>
      </div>
    </main>

    <script src="/static/jquery.slim.min.js"></script>
    <script src="/static/bootstrap.min.js"></script>
  </body>
</html>
