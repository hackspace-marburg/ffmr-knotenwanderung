% if len(hostname_len) == 0:
<div class="alert alert-warning" role="alert">
  Sorry, no hit for any hostname.
</div>
% end

<table class="table">
  <thead>
    <tr>
      <th scope="col">Hostname</th>
      <th scope="col">Matches</th>
    </tr>
  </thead>
  <tbody>
    % for (hostname, matches) in hostname_len.items():
    % if matches == 0:
    <tr class="table-danger">
    % elif matches > 1:
    <tr class="table-warning">
    % else:
    <tr>
    % end
      <td><a href="/s/{{hostname}}">{{hostname}}</a></td>
      <td>{{matches}}</td>
    </tr>
    % end
  </tbody>
</table>
