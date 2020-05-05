export default class User {
  constructor(id, email, password, role = 1) {
    this.id = id
    this.email = email
    this.password = password
    this.role = role
  }
}
