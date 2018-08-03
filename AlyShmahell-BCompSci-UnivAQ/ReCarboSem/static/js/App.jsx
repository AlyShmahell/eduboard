import React from 'react';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'jquery/dist/jquery.min.js';
import * as Popper from 'popper.js';
import '../css/App.css';
import CarboSem from './carbosem';

export default class App extends React.Component {
  render() {
    return (
      <main className="main">
          <nav className="navbar navbar-expand-lg navbar-dark bg-dark static-top">
                  <a className="navbar-brand" href="/">Carbon Semantics</a>
                  <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#targetNavBar" aria-controls="targetNavBar" aria-expanded="false" aria-label="Toggle navigation">
                      <span className="navbar-toggler-icon"></span>
                  </button>
                  <div className="collapse navbar-collapse customCollapse" id="targetNavBar">
                        <form role="search" className="form-inline mt-2 mt-md-0" id="search">
                              <input type="text" value="" placeholder="Search for Sequences" className="form-control mr-sm-2" name="search"/>
                              <button className="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
                        </form>
                  </div>
          </nav>
          <div>
          <CarboSem />
        </div>
        <footer className="bg-dark fixed-bottom custom-footer">
            Copyright &copy; 2018 Aly Shmahell
            <a href="https://github.com/CarboSem">
                <i className="fa fa-github" aria-hidden="true">
                </i>
            </a>
        </footer>
      </main>
    );
  }
}
