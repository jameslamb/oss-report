/**
 * Converts raw user data into a format we can use
 * Might be overkill, but we might need to transform this further at some point
 * 
 * @param {String} userData
 * 
 * @returns {Object}
 */
export default (userData) => {
  return JSON.parse(userData);
};
