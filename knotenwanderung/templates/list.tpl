% if len(node_data) == 0:
<div class="alert alert-warning" role="alert">
  Sorry, no hit for this hostname.
</div>
% elif len(node_data) > 1:
<div class="alert alert-info" role="alert">
  There are multiple <i>node_ids</i> for this hostname.
</div>
% end

% for node in node_data:
<h2>{{node.node_id}}</h2>
<ul>
  %for host in sorted(node.hosts):
    <li><a href="https://grafana.hsmr.cc/dashboard/db/ffmr-node-details?orgId=1&var-hostname={{host.hostname}}">{{host.hostname}}</a></li>
  %end
</ul>
% end
