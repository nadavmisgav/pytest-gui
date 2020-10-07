import React from "react";
import { useState } from "react";
import { Navbar, Nav, Container } from "react-bootstrap";
import Actions from "./Actions";
import Tests from "./Tests";

import "bootstrap/dist/css/bootstrap.min.css";

import "./App.css";

export const BASE_URL = "http://localhost:5000/api";

const log = (e) => {
  console.log(e);
};

function App() {
  const [tests, setTests] = useState([]);
  const [logs, setLogs] = useState([]);

  let logEvents = new EventSource(`${BASE_URL}/logs`);
  // let statusEvents = new EventSource(`${BASE_URL}/status`);

  logEvents.addEventListener("message", log, false);
  logEvents.addEventListener("open", log, false);
  logEvents.addEventListener("error", log, false);

  // statusEvents.addEventListener("message", log, false);
  // statusEvents.addEventListener("open", log, false);
  // statusEvents.addEventListener("error", log, false);

  return (
    <div className="App">
      <Navbar>
        <Navbar.Brand href="#">
          <img
            src="/assets/logo.png"
            width="92"
            height="92"
            className="d-inline-block align-top"
            alt="pytest logo"
          />
        </Navbar.Brand>
        {/* <Nav>
          <Nav.Item>
            <Nav.Link href="#reports">reports</Nav.Link>
          </Nav.Item>
        </Nav> */}
      </Navbar>
      <Container className="inner">
        <Actions tests={tests} setTests={setTests} />
        <Tests tests={tests} setTests={setTests} />
      </Container>
    </div>
  );
}

export default App;
