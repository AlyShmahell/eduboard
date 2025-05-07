
import React, { useMemo, useState } from 'react';
import colormap from 'colormap'


function Dynamicheckbox({ data, relations, setRelations, roots, setRoots }) {
    function check(event) {
        if (event.target.checked) {
            let tmp = {};
            tmp[event.target.value] = event.target.id;
            setRelations( prev => ({
                ...prev,
                ...tmp
            })
                
            )
        }
        else {
            let tmp = { ...relations };
            delete tmp[event.target.value];
            setRelations(prev => ({
                ...tmp
            })
                
            )
        }
    }
    let relcolors = colormap({
        colormap: 'hot',
        nshades: Math.max(6, data.types.length),
        format: 'hex',
        alpha: 1
    })
    let rootcolors = colormap({
        colormap: 'jet',
        nshades: Math.max(6, data.roots.length),
        format: 'hex',
        alpha: 1
    })
    let checkboxes = [<h3>Links</h3>];
    let legend = [<h3>Nodes</h3>];
    data.types.forEach((typename, index) => {
        checkboxes.push(<span style={{ color: relcolors[index] }}> <input onChange={check} defaultChecked={true} type="checkbox" id={relcolors[index]} name="dynamiccheckbox" value={typename} /> {typename} </span>);
    });
    data.roots.forEach((rootname, index) => {
        legend.push(<span style={{ color: rootcolors[index] }}>  {rootname} </span>);
    });
    useMemo(() => {
        data.types.forEach((typename, index) => {
            let tmp = {};
            tmp[typename] = relcolors[index];
            setRelations(prev => ({
                ...prev,
                ...tmp
            })
            )
        });
        
    }, [data.types]);
    useMemo(() => {
        data.roots.forEach((rootname, index) => {
            let tmp = {};
            tmp[rootname] = rootcolors[index];
            setRoots(prev => ({
                ...prev,
                ...tmp
            })
            )
        });
        
    }, [data.roots]);
    if (checkboxes.length<=1)
        checkboxes = [];
    if (legend.length<=1)
        legend = [];
    return (
        <div className="checkbox">
            {checkboxes}
            {legend}
        </div>
    );
}

export default Dynamicheckbox;