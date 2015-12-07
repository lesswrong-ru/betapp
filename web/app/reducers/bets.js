import { FETCH_BETS } from '../actions';

const initialState = {
  items: [],
  fetching: false,
};

export default function(state=initialState, action) {
  switch (action.type) {
    case FETCH_BETS:
      switch (action.status) {
        case 'success':
          return {
            ...state,
            items: action.bets,
            fetching: false,
          };
        case 'initiated':
          return {
            ...state,
            fetching: true,
          };
        default:
          return state;
      }

    default:
      return state;
  }
}
