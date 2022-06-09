import React from "react";

const Radio = ({ selected, name, value, label, option, onChange }) => (
  <label
    className={`radio-label${
      (selected === value && " selected") || " not-selected"
    }`}
  >
    <div className={`input-radio${option ? "" : " no-option"}`}>
      <input
        type="radio"
        name={name}
        value={value}
        checked={selected === value}
        onChange={onChange}
      />{" "}
      {option ? option + ". " : ""}
    </div>
    <div className="text-radio">{label}</div>
  </label>
);

export default Radio;
