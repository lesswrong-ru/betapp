import React from 'react';

export default function (props) {
  return (
    <li>
      <button onClick={props.onRemove}>x</button>
      {' '}
      {props.title}
      {' '}
      ({props.confidence})
      <button onClick={() => props.onResolve(true)}>y</button>
      <button onClick={() => props.onResolve(false)}>n</button>
    </li>
  );
};
