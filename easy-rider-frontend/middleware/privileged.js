export default function({ store, redirect }) {
  const currentUser = store.state.auth.user

  if (!store.state.auth.loggedIn || !currentUser) {
    return redirect('/account/signin')
  }

  if (currentUser.role < 2) {
    return redirect(`/users/${currentUser.id}/trips`)
  }
}
