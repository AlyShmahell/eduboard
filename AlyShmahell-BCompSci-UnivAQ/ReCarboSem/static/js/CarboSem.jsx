import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import * as d3 from 'd3';

class CarboSem extends Component{

    state = {

    };

    static getDerivedStateFromProps(nextProps, prevState){
        if (!nextProps.data) return null;
        const {data} = nextProps.data;
        const {xScale, yScale} = prevState;
    }

    render() {
        return (
          <svg>
          </svg>
        );
    }
}

export default CarboSem;