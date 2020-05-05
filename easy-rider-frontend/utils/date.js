import moment from 'moment'

export function dateToString(date) {
  const result = date ? moment(date).format('YYYY-MM-DD') : ''

  return result
}
