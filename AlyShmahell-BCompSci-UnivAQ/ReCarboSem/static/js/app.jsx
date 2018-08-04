/*
MIT License

Copyright (c) 2018 Aly Shmahell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

import React from "react";
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "jquery/dist/jquery.min.js";
import * as Popper from "popper.js";
import "../css/carbosem.css";

export default class App extends React.Component {
  render() {
    return (
      <main className="main">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark static-top">
          <a className="navbar-brand" href="/">
            Carbon Semantics
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-toggle="collapse"
            data-target="#targetNavBar"
            aria-controls="targetNavBar"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon" />
          </button>
          <div
            className="collapse navbar-collapse customCollapse"
            id="targetNavBar"
          >
            <form
              role="search"
              className="form-inline mt-2 mt-md-0"
              id="search"
            >
              <input
                type="text"
                value=""
                placeholder="Search for Sequences"
                className="form-control mr-sm-2"
                name="search"
              />
              <button
                className="btn btn-outline-success my-2 my-sm-0"
                type="submit"
              >
                Search
              </button>
            </form>
          </div>
        </nav>
        <canvas />
        <footer className="bg-dark fixed-bottom custom-footer">
          Copyright &copy; 2018 Aly Shmahell
          <a href="https://github.com/CarboSem">
            <i className="fa fa-github" aria-hidden="true" />
          </a>
        </footer>
      </main>
    );
  }
}
