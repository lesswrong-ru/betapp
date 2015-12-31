import { INTERNAL_ERROR } from '../actions';

const initialState = null;

export default function(state=initialState, action) {
  if (action.type == INTERNAL_ERROR) {
    return 'oops';
  }
  return null;
}
