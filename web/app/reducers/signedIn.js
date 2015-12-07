import { SIGN_IN } from '../actions';

export default function(state=false, action) {
  switch (action.type) {
    case SIGN_IN:
      return true;
    default:
      return state;
  }
}
