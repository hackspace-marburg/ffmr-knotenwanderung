Enter one hostname per line. The system checks each hostname separately when
you send the data.

<form action="" method="post">
  <div class="form-group">
    <label for="bulkTextarea">Hostnames</label>
    <textarea class="form-control" id="bulkTextarea" name="hostnames" rows="7"></textarea>
  </div>
  <button type="submit" class="btn btn-outline-success">Search</button>
</form>

<script>
  var placeholders = ["35000-examples", "35037-hsmr-1", "35037-the-wired", "35043-Spiegelslustturm-00"];
  var bulkArea = document.getElementById("bulkTextarea");
  bulkArea.placeholder=placeholders.join("\n");
</script>
