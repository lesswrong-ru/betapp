import React from 'react';

export default function (props) {
  return (
    <li>
      {props.title}
      <button onClick={props.onRemove}>(remove)</button>
    </li>
  );
};
