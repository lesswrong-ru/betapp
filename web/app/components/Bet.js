import React from 'react';

export default function (props) {
  return (
    <li>
      <button onClick={props.onRemove}>x</button>
      {' '}
      {props.title}
      {' '}
      ({props.confidence})
    </li>
  );
};
