import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "jquery/dist/jquery.min.js";
import * as Popper from "popper.js";
import "../css/carbosem.css";
import CarboSem from './CarboSem';

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      data: {},
      searchParameter: 'data.json',
    };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.updateSearchParameter = this.updateSearchParameter.bind(this);
  }

  handleSubmit(event) {
    event.preventDefault();
    fetch('/getJSON?' + $.param({ filename: this.state.searchParameter }))
      .then((response) => {
        if (response.status == 200)
          return response.json()
      })
      .then(data => {
        console.log(data);
        console.log('ha');
        if (data)
          this.setState({ data: data });
      });
  }

  updateSearchParameter(updatedSearchParameter) {
    this.setState({ searchParameter: updatedSearchParameter.target.value });
  }

  render() {
    console.log('hum');
    const data = this.state.data;
    console.log(JSON.stringify(data));
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
              onSubmit={this.handleSubmit}
            >
              <input
                type="text"
                value={this.state.searchParameter}
                placeholder="Search for Sequences"
                className="form-control mr-sm-2"
                name="filename"
                onChange={updatedSearchParameter => this.updateSearchParameter(updatedSearchParameter)}
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
        <CarboSem data={data} />
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

export default App;
