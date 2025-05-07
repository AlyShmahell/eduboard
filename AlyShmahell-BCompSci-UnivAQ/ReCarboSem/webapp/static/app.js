import React, { useState } from 'react';
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "jquery/dist/jquery.min.js";
import "./carbonsemantics.css";
import Draggable, { DraggableCore } from 'react-draggable'; // Both at the same time
import CarbonSemantics from './carbonsemantics';
import Dynamicheckbox from './dynamicheckbox';


function App() {
  const [filename, setFilename] = useState('simulated#1.json');
  const [relations, setRelations] = useState({});
  const [roots, setRoots] = useState({});
  const [data, setData] = useState({
    'nodes': [],
    'links': [],
    'types': [],
    'roots': []
  });
  function handleSubmit(event) {
    
    event.preventDefault();
    fetch('/getJSON?' + $.param({ filename: filename }))
      .then((response) => {
        setRelations({});
        setRoots({});
        setData({
          'nodes': [],
          'links': [],
          'types': [],
          'roots': []
        })
        if (response.status == 200)
          return response.json()
      })
      .then(data => {
        if (data)
          setData(data);
      });
  }
  return (

    <main className="main">
      <Draggable>
        <div className='card'>
          <div className='header'>
          <a href="/" className='title'>
            Carbon Semantics
          </a>
          </div>
          <form
            role="search"
            className="search"
            id="search"
            onSubmit={handleSubmit}
          >
            <input
              type="text"
              className="textbox"
              value={filename}
              placeholder="Search for Sequences"
              name="filename"
              onChange={(event) => setFilename(event.target.value)}
            />
            <button
              type="submit"
            >
              Search
            </button>
          </form>
          <Dynamicheckbox className='checkbox' data={data} relations={relations} setRelations={setRelations} roots={roots} setRoots={setRoots} />
          <footer className="footer">
            Copyright &copy; 2018 -2023 <br /> Aly Shmahell <br />
            <a href="https://github.com/AlyShmahell/ReCarboSem" target="_blank">
              <i className="fab fa-github"></i>
            </a>
          </footer>
        </div>
      </Draggable>
      <CarbonSemantics data={data} relations={relations} roots={roots} />
    </main>
  );
}

export default App;