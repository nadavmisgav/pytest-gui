import React, { useEffect } from "react";
import { useState } from "react";
import { Navbar, Nav, Container } from "react-bootstrap";
import Actions from "./Actions";
import Tests from "./Tests";

import "bootstrap/dist/css/bootstrap.min.css";

import "./App.css";

export const BASE_URL = "http://localhost:5000/api";

function App() {
  let cache = localStorage.getItem("cache");

  let init_tests = cache ? JSON.parse(cache).tests : [];
  let init_logs = cache ? JSON.parse(cache).logs : [];

  const [tests, setTests] = useState(init_tests);
  const [logs, setLogs] = useState(init_logs);

  localStorage.setItem(
    "cache",
    JSON.stringify({
      tests,
      logs,
    })
  );

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
        <Actions
          tests={tests}
          setTests={setTests}
          logs={logs}
          setLogs={setLogs}
        />
        <Tests
          tests={tests}
          setTests={setTests}
          logs={logs}
          setLogs={setLogs}
        />
      </Container>
    </div>
  );
}

export default App;
