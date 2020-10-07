import React from "react";
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

const notify = () => toast.success("Wow so easy !");

function discover(e, setTests) {
  e.preventDefault();
  axios
    .get(`${BASE_URL}/discover`)
    .then((res) => {
      const tests = res.data;
      setTests(tests);
      toast.success(`Discovered ${tests.length} tests`);
    })
    .catch((err) => {
      toast.error("Failed discovering tests");
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
          onClick={notify}
        />
        <ActionButton
          icon="fa-stop"
          description="Stop tests"
          onClick={notify}
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

function Actions({ tests, setTests }) {
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
                  <Form.Control type="input" />
                  {/* <Form.Text className="text-muted">
                  Example
                </Form.Text> */}
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
