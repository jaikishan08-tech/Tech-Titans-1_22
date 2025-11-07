
function tracked(form) {
  fetch(form.action, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-Requested-With': 'XMLHttpRequest'
    },
    body: new URLSearchParams(new FormData(form))
  }).then(r => r.json()).then(d => {
    alert('Marked as completed!');
  }).catch(e => alert('Failed to mark.'));
  return false;
}
