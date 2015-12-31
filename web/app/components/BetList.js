import React from 'react';
import Bet from './Bet';

export default function (props) {
  return (
    <div>
      <ul>
        {props.bets.map(
          bet =>
          <Bet
            {...bet}
            key={bet.id}
            onRemove={() => props.onRemove(bet.id)}
            onResolve={(outcome) => props.onResolve(bet.id, outcome)}
          />
        )}
      </ul>
      {props.loading && <h1>Loading</h1>}
    </div>
  );
};
