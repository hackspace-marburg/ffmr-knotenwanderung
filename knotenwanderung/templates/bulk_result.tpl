% if len(hostname_map) == 0:
<div class="alert alert-warning" role="alert">
  Sorry, no hit for any hostname.
</div>
% end

<table class="table table-striped">
  <thead>
    <tr>
      <th scope="col">Requested Hostname</th>
      <th scope="col">Current Hostname</th>
      <th scope="col">Last seen</th>
      <th scope="col"></th>
    </tr>
  </thead>
  <tbody>
    % for (hostname, nodes) in hostname_map.items():
    % if len(nodes) != 1 or len(nodes[0].hosts) == 0:
    <tr class="table-warning">
      <td>{{hostname}}</td>
      <td colspan="2">
      % if len(nodes) == 0:
      Unknown hostname
      % elif len(nodes) > 1:
      Multiple nodes for this hostname
      % else:
      oof.
      % end
      </td>
      <td><a href="/s/{{hostname}}">Details</a></td>
    </tr>
    % else:
    <tr>
      <td>{{hostname}}</td>
      <td>{{nodes[0].hosts[-1].hostname}}</td>
      <td>{{nodes[0].hosts[-1].last.strftime("%Y-%m-%d")}}</td>
      <td><a href="/s/{{hostname}}">Details</a></td>
    </tr>
    % end
    % end
  </tbody>
</table>
