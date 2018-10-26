import groupBy from 'lodash/groupBy';
import forEach from 'lodash/forEach';

/**
 * Transformers the users events into a map of repos and their events
 * 
 * @param {Object} repos
 * @returns {Object}
 */
export default (repos) => {
  const reposGroupedByName = groupBy(repos, ({repo_name}) => repo_name);

  const reposGroupedByNameAndEventType = {}

  forEach(reposGroupedByName, (events, repoName) => {
    reposGroupedByNameAndEventType[repoName] = groupBy(events, ({ type }) => type)
  })

  return reposGroupedByNameAndEventType;
}
