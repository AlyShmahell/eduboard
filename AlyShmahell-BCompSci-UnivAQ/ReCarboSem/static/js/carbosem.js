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
import React from 'react';
import * as d3 from 'd3';
import $ from 'jquery/dist/jquery.min.js';
import {withFauxDOM} from 'react-faux-dom';

class CarboSem extends React.Component {

  constructor() {
      super();
      /*
       * Global Variables (YUI Module Variables)
       */
      this.checkbox = {
              "states": [],
              "vals": [],
              "colors": []
          };
      this.ledger = {
              "elements": [],
              "colors": []
          };
  }

   submitQuery(){
    /*
     * resetting the checkbox area
     */
     this.checkbox["states"] = [];
     this.checkbox["vals"] = [];
     this.checkbox["colors"] = [];

     /*
      * resetting the ledger area
      */
     this.ledger["elements"] = [];
     this.ledger["colors"] = [];
  }

   drawGraph(){
    const semCanvas = this.props.connectFauxDOM('canvas', 'semCanvas');
    const semDivAddedCheckbox = this.props.connectFauxDOM('div', 'semDivAddedCheckbox');
    const semDivAddedLedger = this.props.connectFauxDOM('div', 'semDivAddedLedger');
    /*
     * defining color arrays
     */
    const linkColor = d3.scaleOrdinal(d3.schemeCategory10);
    const nodeColor = d3.scaleOrdinal(d3.schemeCategory20);
    d3.json('/getJSON', function (error, graph) {
        if (error) {
            alert("Error, no JSON file found!");
            console.log(graph);
            return;
        }
        else {
          console.log(graph);
        }

        /*
         * cleaning up previously rendered checkboxes and ledger elements
         */
        d3.selectAll(semDivAddedCheckbox).remove();
        d3.selectAll(semDivAddedLedger).remove();

        /*
         * initiating checkboxes after submitting a new query
         */
        if (this.checkbox["states"].length == 0)
            for (var i = 0; i < graph.nodes.length; i++) {
                if (graph.nodes[i].targets)
                    for (var j = 0; j < graph.nodes[i].targets.length; j++) {
                        var pushState = this.checkbox["vals"].indexOf(graph.nodes[i].targets[j].type);
                        if (pushState == -1) {
                            this.checkbox["vals"].push(graph.nodes[i].targets[j].type);
                            this.checkbox["states"].push(true);
                            this.checkbox["colors"].push(linkColor(this.checkbox["states"].length - 1));
                        }
                    }
            }
        /*
         * rendering checkboxes as per their current states
         */
        var addedCheckbox = d3.select(".form-group").append("div").attr("class", "checkbox").attr("id", semDivAddedCheckbox);
        var addedLabels = [];
        var addedBoxes = [];
        var beginCheckbox = addedCheckbox.append("label").text("{")
            .style("color", "floralwhite").style("padding-right", "10px");
        for (var i = 0; i < this.checkbox["states"].length; i++) {
            addedLabels[i] = addedCheckbox.append("label").attr("for", this.checkbox["vals"][i]).text(this.checkbox["vals"][i])
                .style("color", this.checkbox["colors"][i]);
            addedBoxes[i] = addedCheckbox.append("input")
                .attr("type", "checkbox")
                .attr("name", "function")
                .attr("value", this.checkbox["vals"][i])
                .attr("id", this.checkbox["vals"][i])
                .style("opacity", 0)
                .property("checked", this.checkbox["states"][i]);
        }
        var endCheckbox = addedCheckbox.append("label").text("}")
            .style("color", "floralwhite");
        addedCheckbox.on("change", function () {
            for (var i = 0; i < this.checkbox["states"].length; i++) {
                this.checkbox["states"][i] = addedBoxes[i].property("checked");
                this.checkbox["colors"][i] = this.checkbox["states"][i] ? linkColor(i) : "#FFFFFF";
            }
            drawGraph();
            return;
        });
        /*
         * creating local arrays according to checkbox states
         */
        var nodes = new Array();
        var links = new Array();
        for (var i = 0, len = graph.nodes.length; i < len; i++) {
            if (graph.nodes[i].targets) {
                nodes.push({
                    "label": graph.nodes[i].label,
                    "title": graph.nodes[i].title
                });
                var ledgerInsertibility = false;
                var ledgerIndex = this.ledger["elements"].findIndex(x => x == graph.nodes[i].label);
                if (ledgerIndex < 0) {
                    this.ledger["elements"].push(graph.nodes[i].label);
                    this.ledger["colors"].push(nodeColor(this.ledger["elements"].length - 1));
                    ledgerInsertibility = true;
                }
                var source = nodes.length - 1;
                var nodeValidity = 0;
                for (var j = 0; j < graph.nodes[i].targets.length; j++) {

                    var checkboxIndex = this.checkbox["vals"].findIndex(x => x == graph.nodes[i].targets[j].type);
                    var checkboxIndexValidity = this.checkbox["states"][checkboxIndex];
                    if (!checkboxIndexValidity)
                        continue;
                    else
                        nodeValidity++;
                    var nodeIndex = nodes.findIndex(x => x.title == graph.nodes[graph.nodes[i].targets[j].target].title);
                    var target;
                    if (nodeIndex > -1) {
                        target = nodeIndex;
                    } else {
                        nodes.push({
                            "label": graph.nodes[graph.nodes[i].targets[j].target].label,
                            "title": graph.nodes[graph.nodes[i].targets[j].target].title
                        });
                        target = nodes.length - 1;
                        var ledgerIndex = this.ledger["elements"].findIndex(x => x == graph.nodes[graph.nodes[i].targets[j].target].label);
                        if (ledgerIndex < 0) {
                            this.ledger["elements"].push(graph.nodes[graph.nodes[i].targets[j].target].label);
                            this.ledger["colors"].push(nodeColor(this.ledger["elements"].length - 1));
                        }
                    }
                    links.push({
                        "source": source,
                        "target": target,
                        "type": graph.nodes[i].targets[j].type
                    });
                }
                if (nodeValidity == 0) {
                    nodes.pop();
                    if (ledgerInsertibility) {
                        this.ledger["elements"].pop();
                        this.ledger["colors"].pop();
                    }
                }
            }
        }
        /*
         * pushing arrays to local graph
         */
        var localGraph = {
            "nodes": nodes,
            "links": links
        };

        /*
         * rendering ledger elements as per their current states
         */
        if (this.ledger["elements"].length > 0) {
            var addedLedger = d3.select(".form-group").append("div").attr("class", "checkbox").attr("id", semDivAddedLedger).style(
                "display", "inline");
            var beginledger = addedLedger.append("label").text("{")
                .style("color", "floralwhite")
                .style("padding-left", "10px");
            var addedLedgerElements = [];
            for (var i = 0; i < this.ledger["elements"].length; i++) {
                addedLedgerElements[i] = addedLedger.append("label").text(this.ledger["elements"][i] + (i < this.ledger["elements"].length - 1 ? ", " : "")).style("color", this.ledger["colors"][i]);
            }
            var endLedger = addedLedger.append("label").text("}")
                .style("color", "floralwhite");
        }

        /*
         * configure canvas parameters
         */
        var width = window.innerWidth,
            height = (90 * window.innerHeight) / 100;

        var canvas = document.querySelector(canvas),
            context = canvas.getContext("2d");
        canvas.width = width;
        canvas.height = height;

        /*
         * configure simulation settings
         */
        var simulation = d3.forceSimulation()
            .force("link", d3.forceLink().distance(10).strength(1))
            .force("charge", d3.forceManyBody())
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force('x', d3.forceX(width / 2).strength(width > height ? 0.1 : 0.25))
            .force('y', d3.forceY(height / 2).strength(width > height ? 0.25 : 0.1));


        /*
         * initiating the simulation renderer
         */
        simulation
            .nodes(localGraph.nodes)
            .on("tick", function () {
                context.clearRect(0, 0, width, height);
                localGraph.links.forEach(function (d) {
                    context.beginPath();
                    context.strokeStyle = this.checkbox["colors"][this.checkbox["vals"].findIndex(x => x == d.type)];
                    context.moveTo(d.source.x, d.source.y);
                    context.lineTo(d.target.x, d.target.y);
                    context.stroke();
                });
                localGraph.nodes.forEach(function (d) {
                    context.beginPath();
                    context.fillStyle = ledger["colors"][ledger["elements"].findIndex(x => x == d.label)];
                    d.x = Math.max(5, Math.min(width - 5, d.x));
                    d.y = Math.max(5, Math.min(height - 5, d.y));
                    context.moveTo(d.x, d.y);
                    context.arc(d.x, d.y, 5, 0, 2 * Math.PI);
                    context.fillText(d.renderedText != null ? d.renderedText : "", d.x + 5, d.y + 5);
                    context.fill();
                });
            });

        simulation.force("link")
            .links(localGraph.links);

        /*
         * changing background parameters of elements as per mouse drag
         */
        d3.select(canvas)
            .call(d3.drag()
                .container(node)
                .subject(function () {
                    return simulation.find(d3.event.x, d3.event.y);
                })
                .on("start", function () {
                    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
                    d3.event.subject.fx = d3.event.subject.x;
                    d3.event.subject.fy = d3.event.subject.y;
                    if (d3.event.subject.renderedText)
                        d3.event.subject.renderedText = null;
                    else
                        d3.event.subject.renderedText = d3.event.subject.title;
                })
                .on("drag", function () {
                    d3.event.subject.fx = Math.max(5, Math.min(width - 5, d3.event.x));
                    d3.event.subject.fy = Math.max(5, Math.min(height - 5, d3.event.y));
                })
                .on("end", function () {
                    if (!d3.event.active) simulation.alphaTarget(0);
                    d3.event.subject.fx = null;
                    d3.event.subject.fy = null;
                }));
    });
    this.props.animateFauxDOM(800)
  }

  render () {
    $("#search").submit(this.submitQuery());
    $("#search").submit(this.drawGraph());
    return (
            <div className="suggar">
              {this.props.semCanvas}
            </div>
        );
 }
}

CarboSem.defaultProps = {
  semCanvas: 'loading canvas',
  semDivAddedLedger: 'loading ledger',
  semDivAddedCheckbox: 'loading checkboxes'
}

export default withFauxDOM(CarboSem);
