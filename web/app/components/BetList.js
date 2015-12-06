import React from 'react';
import Bet from './Bet';

export default function (props) {
  return (
    <ul>
      {props.bets.map((bet, index) =>
        <Bet
          {...bet}
          key={index}
        />
      )}
    </ul>
  );
};
