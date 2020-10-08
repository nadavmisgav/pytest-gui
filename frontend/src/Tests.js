import React, { useState } from "react";
import Collapsible from "react-collapsible";

import "bootstrap/dist/css/bootstrap.min.css";
import "./Tests.css";
import { Row, Col } from "react-bootstrap";

function handleCheck(e, tests, setTests, selected) {
  e.stopPropagation();
  e.preventDefault();

  let newTests = tests.slice(0);
  let target_id = e.target.id;
  let foundIndex = tests.findIndex((x) => x.id === target_id);
  newTests[foundIndex].selected = !tests[foundIndex].selected;

  setTests(newTests);
}

function handleModuleCheck(e, tests, setTests, selected) {
  e.stopPropagation();
  e.preventDefault();

  let module = e.target.id;
  let newTests = tests.map((test) => {
    return {
      ...test,
      selected: test.file === module ? !selected : test.selected,
    };
  });

  setTests(newTests);
}

function TestItem({ name, selected, state, module, tests, setTests }) {
  let finalState = "";
  if (state) {
    state.forEach((s) => {
      if (s === "failed") {
        finalState = "failed";
      }
    });

    if (state.filter((s) => s !== "").length === 3) {
      finalState = "passed";
    }
  }

  let onClick = module ? handleModuleCheck : handleCheck;

  let stateFlagClass = "test-result fas fa-flag " + finalState;
  return (
    <div className="test-item">
      <label className="checkbox-container">
        <input type="checkbox" checked={selected} />
        <span
          id={name}
          className="checkmark"
          onClick={(e) => {
            onClick(e, tests, setTests, selected);
          }}
        ></span>
      </label>
      <i className={stateFlagClass}></i>
      <span>{name}</span>
    </div>
  );
}

function TestModule({ name, tests, setTests, selected }) {
  const test_items = tests.map(({ id, selected, state }) => {
    return (
      <TestItem
        key={id}
        name={id}
        selected={selected}
        tests={tests}
        setTests={setTests}
        state={state}
      />
    );
  });
  return (
    <Row className="row-12">
      <Col className="col-12">
        <Collapsible
          trigger={
            <TestItem
              name={name}
              module
              tests={tests}
              setTests={setTests}
              selected={selected}
            />
          }
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
  let file_list = new Set();

  tests.forEach((test) => {
    file_list.add(test.file);
  });

  file_list = Array.from(file_list);

  let modules = file_list.map((file) => {
    return {
      name: file,
      tests: [],
    };
  });

  tests.forEach((test) => {
    let idx = modules.findIndex((item) => item.name === test.file);
    modules[idx].tests.push(test);
  });

  const test_modules = modules.map((module) => {
    let is_selected = !module.tests.every((test) => !test.selected);
    return (
      <TestModule
        key={module["name"]}
        {...module}
        setTests={setTests}
        selected={is_selected}
      />
    );
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

function handleLock(e, lock, setLock) {
  e.preventDefault();
  setLock(!lock);
}

function Tests({ tests, setTests, logs, setLogs }) {
  let [lock, setLock] = useState(true);
  let mode = lock ? "lock" : "unlock";
  let logsItems = logs.map((log) => {
    return <span>{log}</span>;
  });
  return (
    <React.Fragment>
      <Row className="title-row">
        <Col className="col-8">
          <span>Tests</span>
        </Col>
        <Col className="col-4">
          <span>Logs</span>
          <i
            className={`fas fa-${mode}`}
            onClick={(e) => handleLock(e, lock, setLock)}
          ></i>
        </Col>
      </Row>
      <Row className="Tests mb-4">
        <Col className="tests col-8">
          <TestArea tests={tests} setTests={setTests} />
        </Col>
        <Col className="logs col-4">{logsItems}</Col>
      </Row>
    </React.Fragment>
  );
}

export default Tests;
