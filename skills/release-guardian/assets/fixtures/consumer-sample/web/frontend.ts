// Fixture: enum exhaustiveness and JSON.parse consumers.
const data = JSON.parse(responseBody);

switch (data.status) {
  case "active":
    renderActive(data);
    break;
  case "pending":
    renderPending(data);
    break;
  case "suspended":
    renderSuspended(data);
    break;
}
