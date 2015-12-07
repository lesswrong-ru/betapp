import { OPEN_NEW_BET_FORM, CANCEL_NEW_BET_FORM, SUBMIT_NEW_BET } from '../actions';

const initialState = {
  open: false,
  posting: false,
};

export default function(state=initialState, action) {
  switch (action.type) {
    case OPEN_NEW_BET_FORM:
      return {
        ...state,
        open: true,
      };
    case CANCEL_NEW_BET_FORM:
      return {
        ...state,
        open: false,
      };
    case SUBMIT_NEW_BET:
      switch (action.status) {
        case 'initiated':
          return {
            ...state,
            posting: true,
          }
        case 'success':
          return {
            open: false,
            posting: false,
          }
        default:
          throw `Unknown action status ${action.status}`;
      }
    default:
      return state;
  }
}
