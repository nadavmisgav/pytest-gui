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
          ...test,
        };
      });

      setTests(tests);
      toast.success(`Discovered ${tests.length} tests`);
    })
    .catch((err) => {
      toast.error("Failed discovering tests, check log");
    })
    .finally(() => {
      target.classList.remove("disabled");
      target.onClick = (e) => discover(e, setTests);
    });
}

function handleLogs(e, logs, setLogs) {
  setLogs([...logs, e.data]);
}

const _translate = {
  setup: 0,
  call: 1,
  teardown: 2,
};
function handleStatus(e, tests, setTests) {
  let data = JSON.parse(e.data);
  if (data.when) {
    let status = data.outcome;
    let place = _translate[data.when];
    let newTests = Array.from(tests);
    let idx = newTests.findIndex((test) => test.nodeid === data.nodeid);
    newTests[idx].state[place] = status;
    setTests(newTests);
  }
}

function startTests(e, tests, setTests, logs, setLogs) {
  e.preventDefault();
  const target = e.target;
  target.classList.add("disabled");
  target.onClick = null;
  let cleanLogs = [];
  setLogs(cleanLogs);
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
      };
    }
  );
  setTests(newTests);

  const selected_tests = newTests.filter((test) => test.selected);
  if (selected_tests.length === 0) {
    toast.error("No tests selected");
    target.classList.remove("disabled");
    target.onClick = (e) =>
      startTests(e, newTests, setTests, cleanLogs, setLogs);
    return;
  }

  axios
    .post(`${BASE_URL}/run`, selected_tests)
    .then((res) => {
      let logEvents = new EventSource(`${BASE_URL}/logs`);
      let statusEvents = new EventSource(`${BASE_URL}/status`);

      logEvents.onmessage = (e) => handleLogs(e, cleanLogs, setLogs);
      statusEvents.onmessage = (e) => handleStatus(e, newTests, setTests);

      toast.success(`Started running tests`);
    })
    .catch((err) => {
      toast.error("Failed running tests, check log");
    })
    .finally(() => {
      target.classList.remove("disabled");
      target.onClick = (e) =>
        startTests(e, newTests, setTests, cleanLogs, setLogs);
    });
}

function stopTests(e) {
  e.preventDefault();
  const target = e.target;
  target.classList.add("disabled");
  target.onClick = null;

  axios
    .get(`${BASE_URL}/stop`)
    .then((res) => {
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

function ActionButtons({ tests, setTests, logs, setLogs }) {
  return (
    <Col>
      <Row className="action-buttons">
        <ActionButton
          icon="fa-play"
          description="Start tests"
          onClick={(e) => startTests(e, tests, setTests, logs, setLogs)}
        />
        <ActionButton
          icon="fa-stop"
          description="Stop tests"
          onClick={stopTests}
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

function Actions({ tests, setTests, logs, setLogs }) {
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
        <ActionButtons
          tests={tests}
          setTests={setTests}
          logs={logs}
          setLogs={setLogs}
        />
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
