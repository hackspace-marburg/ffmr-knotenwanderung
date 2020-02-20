% if len(node_data) == 0:
<div class="alert alert-warning" role="alert">
  Sorry, no hit for this hostname.
</div>
% elif len(node_data) > 1:
<div class="alert alert-warning" role="alert">
  There are several nodes for this hostname. This means that different routers
  have shared the same hostname.
</div>
% end

% for node in node_data:
<div class="alert alert-dark" role="alert">
  <h2 class="alert-heading">Node {{node.node_id}}</h2>

  % if len(node.hosts) > 0:
  <p>
    This node appeared first at {{node.hosts[0].first.strftime("%Y-%m-%d")}} and
    last at {{node.hosts[-1].last.strftime("%Y-%m-%d")}} with
    {{len(node.hosts)}} hostnames.
  </p>

  <hr>

  <p>
  <table class="table table-striped">
    <thead>
      <tr>
        <th scrope="col">First</th>
        <th scrope="col">Last</th>
        <th scrope="col">Hostname</th>
        <th scrope="col"></th>
      </tr>
    </thead>
    <tbody>
    % for host in node.hosts:
      <tr>
        <td>{{host.first.strftime("%Y-%m-%d")}}</td>
        <td>{{host.last.strftime("%Y-%m-%d")}}</td>
        <td>{{host.hostname}}</td>
        <td>
          <a href="/s/{{host.hostname}}">Search</a>
          &middot;
          <a href="https://grafana.hsmr.cc/dashboard/db/ffmr-node-details?orgId=1&var-hostname={{host.hostname}}">Grafana</a>
          &middot;
          <a href="https://map.marburg.freifunk.net/#!v:m;n:{{node.node_id}}">Map</a>
        </td>
      </tr>
    % end
    </tbody>
  </table>
  </p>
  % else:
  <p>There are no hosts for this node. Something went wrong!</p>
  % end

</div>
% end
