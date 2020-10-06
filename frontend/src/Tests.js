import React from "react";
import Collapsible from "react-collapsible";

import "bootstrap/dist/css/bootstrap.min.css";
import "./Tests.css";
import { Row, Col } from "react-bootstrap";

function handleCheck(e, tests, setTests) {
  e.stopPropagation();

  let newTests = tests.slice(0);
  let target_id = e.target.id;
  let foundIndex = tests.findIndex((x) => x.id === target_id);
  newTests[foundIndex].selected = !tests[foundIndex].selected;

  setTests(newTests);
}

function TestItem({ name, selected, module, tests, setTests }) {
  return (
    <div className="test-item">
      <label className="checkbox-container">
        <input type="checkbox" checked={selected} />
        <span
          id={name}
          className="checkmark"
          onClick={(e) => {
            handleCheck(e, tests, setTests);
          }}
        ></span>
      </label>
      <i className="test-result fas fa-flag"></i>
      <span>{name}</span>
    </div>
  );
}

function TestModule({ name, tests, setTests }) {
  const test_items = tests.map(({ id, selected }) => {
    return (
      <TestItem
        key={id}
        name={id}
        selected={selected}
        tests={tests}
        setTests={setTests}
      />
    );
  });
  return (
    <Row className="row-12">
      <Col className="col-12">
        <Collapsible
          trigger={<TestItem name={name} module={true} />}
          transitionTime={200}
          open={true}
        >
          {test_items}
        </Collapsible>
      </Col>
    </Row>
  );
}

function toggleModules(expand) {
  let modules = [...document.getElementsByClassName("Collapsible__trigger")];
  let class_name = expand ? "is-closed" : "is-open";
  modules.forEach((module) => {
    if (module.classList.contains(class_name)) {
      module.click();
    }
  });
}

function Modules({ tests, setTests }) {
  let modules = [];

  const test_modules = modules.map((module) => {
    return <TestModule key={module["name"]} {...module} setTests={setTests} />;
  });

  return test_modules;
}

function TestArea({ tests, setTests }) {
  if (tests.length === 0) {
    return <h4>No tests collected</h4>;
  }

  return (
    <React.Fragment>
      <Row id="toggle-buttons">
        <small onClick={() => toggleModules(true)}>expand</small>
        <small onClick={() => toggleModules(false)}>collapse</small>
      </Row>
      <Modules tests={tests} setTests={setTests} />
    </React.Fragment>
  );
}

function Tests({ tests, setTests, logs }) {
  return (
    <React.Fragment>
      <Row className="title-row">
        <Col className="col-8">
          <span>Tests</span>
        </Col>
        <Col className="col-4">
          <span>Logs</span>
        </Col>
      </Row>
      <Row className="Tests mb-4">
        <Col className="tests col-8">
          <TestArea tests={tests} setTests={setTests} />
        </Col>
        <Col className="logs col-4">
          <p id="log-area">{logs}</p>
        </Col>
      </Row>
    </React.Fragment>
  );
}

export default Tests;
