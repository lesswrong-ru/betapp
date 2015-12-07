import React from 'react';
import Bet from './Bet';

export default function (props) {
  if (props.loading) {
    return <h1>Loading</h1>;
  }
  return (
    <ul>
      {props.bets.map(
        bet =>
        <Bet
          {...bet}
          key={bet.id}
          onRemove={() => props.onRemove(bet.id)}
        />
      )}
    </ul>
  );
};
