import React, { useState } from "react";
import {
  Row,
  Col,
  OverlayTrigger,
  Tooltip,
  Form,
  Button,
} from "react-bootstrap";
import axios from "axios";
import { BASE_URL } from "./App";

import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import "bootstrap/dist/css/bootstrap.min.css";
import "./Actions.css";

function discover(e, setTests) {
  e.preventDefault();
  const target = e.target;
  target.classList.add("disabled");
  target.onClick = null;

  axios
    .get(`${BASE_URL}/discover`)
    .then((res) => {
      const tests = res.data.map((test) => {
        return {
          selected: true,
          state: ["", "", ""],
          running: false,
          ...test,
        };
      });

      setTests(tests);
      toast.success(`Discovered ${tests.length} tests`);
    })
    .catch((err) => {
      setTests([]);
      toast.error("Failed discovering tests, check log");
    })
    .finally(() => {
      target.classList.remove("disabled");
      target.onClick = (e) => discover(e, setTests);
    });
}

function handleLogs(e) {
  let logArea = document.getElementById("log-area");
  let p = document.createElement("p");
  let text = document.createTextNode(`${e.data}`);
  p.appendChild(text);
  logArea.appendChild(p);
}

const _translate = {
  setup: 0,
  call: 1,
  teardown: 2,
};

function handleStatus(e, tests, setTests) {
  let data = JSON.parse(e.data);
  if (data.when) {
    let newTests = Array.from(tests);
    if (data.when === "started") {
      let started_idx = newTests.findIndex(
        (test) => test.nodeid === data.nodeid
      );
      newTests[started_idx].running = true;
    } else {
      let status = data.outcome;
      let place = _translate[data.when];
      let idx = newTests.findIndex((test) => test.nodeid === data.nodeid);
      newTests[idx].state[place] = status;
      if (data.when === "teardown") {
        let running_idx = newTests.findIndex(
          (test) => test.nodeid === data.nodeid
        );
        newTests[running_idx].running = false;
      }
    }
    setTests(newTests);
  }
}

function startTests(e, tests, setTests) {
  e.preventDefault();
  const target = e.target;
  target.classList.add("disabled");
  target.onClick = null;
  let logArea = document.getElementById("log-area");
  logArea.innerHTML = "";

  const newTests = tests.map(
    ({ file, id, markers, module, nodeid, selected }) => {
      return {
        file,
        id,
        markers,
        module,
        nodeid,
        selected,
        state: ["", "", ""],
        running: false,
      };
    }
  );

  const selected_tests = newTests.filter((test) => test.selected);
  if (selected_tests.length === 0) {
    toast.error("No tests selected");
    target.classList.remove("disabled");
    target.onClick = (e) => startTests(e, newTests, setTests);
    return;
  }

  axios
    .post(`${BASE_URL}/run`, selected_tests)
    .then((res) => {
      let logEvents = new EventSource(`${BASE_URL}/logs`);
      let statusEvents = new EventSource(`${BASE_URL}/status`);

      logEvents.onmessage = (e) => handleLogs(e);
      statusEvents.onmessage = (e) => handleStatus(e, newTests, setTests);
      // newTests[
      //   newTests.findIndex((test) => test === selected_tests[0])
      // ].running = true;
      setTests(newTests);
      toast.success(`Started running tests`);
    })
    .catch((err) => {
      toast.error("Failed running tests, check log");
    })
    .finally(() => {
      target.classList.remove("disabled");
      target.onClick = (e) => startTests(e, newTests, setTests);
    });
}

function stopTests(e, tests, setTests) {
  e.preventDefault();
  const target = e.target;
  target.classList.add("disabled");
  target.onClick = null;

  axios
    .get(`${BASE_URL}/stop`)
    .then((res) => {
      let newTests = tests.map((test) => {
        return {
          ...test,
          running: false,
        };
      });
      setTests(newTests);
      toast.success(`Stopped running tests`);
    })
    .catch((err) => {
      toast.error("Failed stopping tests, check log");
    })
    .finally(() => {
      target.classList.remove("disabled");
      target.onClick = stopTests;
    });
}

function selectAll(select, tests, setTests) {
  let newTests = tests.slice(0);
  newTests.forEach((test) => {
    test.selected = select;
  });

  setTests(newTests);
}

function ActionButton({ icon, onClick, description }) {
  const className = "fas action-img " + icon;
  return (
    <OverlayTrigger
      key={icon}
      placement="top"
      overlay={<Tooltip id={"tooltip-top"}>{description}</Tooltip>}
    >
      <i className={className} onClick={onClick}></i>
    </OverlayTrigger>
  );
}

function ActionButtons({ tests, setTests }) {
  return (
    <Col>
      <Row className="action-buttons">
        <ActionButton
          icon="fa-play"
          description="Start tests"
          onClick={(e) => startTests(e, tests, setTests)}
        />
        <ActionButton
          icon="fa-stop"
          description="Stop tests"
          onClick={(e) => stopTests(e, tests, setTests)}
        />
        <ActionButton
          icon="fa-search"
          description="Discover tests"
          onClick={(e) => discover(e, setTests)}
        />
      </Row>
    </Col>
  );
}

function formChange(e, setFilter) {
  setFilter(e.target.value);
}

function Actions({ tests, setTests }) {
  let [filter, setFilter] = useState("");
  let hidden = filter === "" ? "hidden" : "";
  return (
    <React.Fragment>
      <Row className="Actions mb-4">
        <Col className="filter col-8">
          <Row>
            <span className="header">filter</span>
          </Row>
          <Row>
            <Col className="col-8">
              <Form>
                <Form.Group controlId="formFilter">
                  <Form.Control
                    value={filter}
                    type="input"
                    placeholder="TEST NAME"
                    onChange={(e) => formChange(e, setFilter)}
                  />
                  <i
                    className={`fas fa-trash ${hidden}`}
                    onClick={() => setFilter("")}
                  ></i>
                </Form.Group>
              </Form>
            </Col>
            <Col>
              <div
                className="dark-button"
                onClick={() => selectAll(true, tests, setTests)}
              >
                select all
              </div>
              <div
                className="dark-button"
                onClick={() => selectAll(false, tests, setTests)}
              >
                clear all
              </div>
            </Col>
          </Row>
        </Col>
        <ActionButtons tests={tests} setTests={setTests} />
      </Row>

      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss={false}
        draggable
        pauseOnHover={false}
      />
    </React.Fragment>
  );
}

export default Actions;
