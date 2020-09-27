import React from "react";
import { Navbar, Nav } from "react-bootstrap";
import Tests from "./Tests";
import Actions from "./Actions";

import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

function App() {
  return (
    <div className="App">
      <Navbar>
        <Navbar.Brand href="#">
          <img
            src="/logo.png"
            width="92"
            height="92"
            className="d-inline-block align-top"
            alt="pytest logo"
          />
        </Navbar.Brand>
        <Nav>
          <Nav.Item>
            <Nav.Link href="#reports">reports</Nav.Link>
          </Nav.Item>
        </Nav>
      </Navbar>
      <Actions />
      <Tests />
    </div>
  );
}

export default App;
