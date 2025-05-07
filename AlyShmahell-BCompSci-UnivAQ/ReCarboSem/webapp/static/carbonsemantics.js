import { useD3 } from './used3';
import colormap from 'colormap'
import * as d3 from 'd3';
import React from 'react';

function untangle(graph, relations) {
    let links = [];
    let nodes = [];
    graph.links.forEach((link) => {
        if (link.type in relations) {
            links.push(
                {
                    'source': graph.nodes[link.source].id,
                    'target': graph.nodes[link.target].id,
                    'type': link.type
                }
            );
            nodes.push(
                graph.nodes[link.source].id
            );
            nodes.push(
                graph.nodes[link.target].id
            );
        }
    })
    nodes = Array.from(new Set(nodes));
    let tmp = links;
    links = [];
    tmp.forEach((link) => {
        links.push(
            {
                'source': nodes.indexOf(link.source),
                'target': nodes.indexOf(link.target),
                'type': link.type
            }
        )
    })
    tmp = nodes;
    nodes = [];
    tmp.forEach((node) => {
        nodes.push({
            'id': node
        })
    })
    return {
        'links': links, 'nodes': nodes, 'types': graph.types, 'roots': graph.roots
    };
}

var width = window.innerWidth,
    height = (90 * window.innerHeight) / 100;
function CarbonSemantics({ data, relations, roots }) {
    const ref = useD3(
        (canvas) => {
            /**
             * configure canvas parameters
             */
            var width = window.innerWidth,
                height = (90 * window.innerHeight) / 100;

            var canvas = document.querySelector("canvas"),
                context = canvas.getContext("2d");
            canvas.width = width;
            canvas.height = height;
            /**
             * configure simulation settings
             */
            var simulation = d3
                .forceSimulation()
                .force(
                    "link",
                    d3
                        .forceLink()
                        .distance(20)
                        .strength(1)
                )
                .force("charge", d3.forceManyBody())
                .force("center", d3.forceCenter(width / 2, height / 2))
                .force("x", d3.forceX(width / 2).strength(width > height ? 0.05 : 0.1))
                .force(
                    "y",
                    d3.forceY(height / 2).strength(width > height ? 0.1 : 0.05)
                );

            /**
             * initiating the simulation renderer
             */
             
            let subgraph = untangle(data, relations);
            console.log(roots);
            simulation.nodes(subgraph.nodes).on("tick", function () {
                context.clearRect(0, 0, width, height);
                subgraph.links.forEach(function (d) {
                    if (relations[d.type] === undefined) {
                        return;
                    }
                    context.beginPath();
                    context.strokeStyle = relations[d.type];
                    context.moveTo(d.source.x, d.source.y);
                    context.lineTo(d.target.x, d.target.y);
                    context.stroke();
                });
                subgraph.nodes.forEach(function (d) {
                    context.beginPath();                    
                    context.fillStyle = roots[d.id.replace(/\d+/g, '')];
                    d.x = Math.max(5, Math.min(width - 5, d.x));
                    d.y = Math.max(5, Math.min(height - 5, d.y));
                    context.moveTo(d.x, d.y);
                    context.arc(d.x, d.y, 5, 0, 2 * Math.PI);
                    context.fillText(
                        d.renderedText != null ? d.renderedText : "",
                        d.x + 5,
                        d.y + 5
                    );
                    context.fill();
                });

            });
            simulation.force("link").links(subgraph.links);
            /**
             * changing background parameters of elements as per mouse drag
             */
            d3.select(canvas).call(
                d3.drag()
                    .container(canvas)
                    .subject(function (event) {
                        return simulation.find(event.x, event.y);
                    })
                    .on("start", function (event) {
                        if (!event.active) simulation.alphaTarget(0.3).restart();
                        event.subject.fx = event.subject.x;
                        event.subject.fy = event.subject.y;
                        if (event.subject.renderedText)
                            event.subject.renderedText = null;
                        else event.subject.renderedText = event.subject.id;
                    })
                    .on("drag", function (event) {
                        event.subject.fx = Math.max(5, Math.min(width - 5, event.x));
                        event.subject.fy = Math.max(5, Math.min(height - 5, event.y));
                    })
                    .on("end", function (event) {
                        if (!event.active) simulation.alphaTarget(0);
                        event.subject.fx = null;
                        event.subject.fy = null;
                    })
            );
        },
        [data, relations]
    );

    return (
        <canvas width={width} height={height} ref={ref} className="canvas"/>
    );
}

export default CarbonSemantics;
