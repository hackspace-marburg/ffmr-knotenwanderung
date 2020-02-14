{ config, lib, pkgs, ... }:

with lib;

let
  knotenwanderung = with pkgs.python3Packages; buildPythonPackage rec {
    pname = "knotenwanderung";
    version = "0.1.0";

    src = lib.cleanSource ./.;

    propagatedBuildInputs = [ bottle influxdb ];
  };

  cfg = config.services.knotenwanderung;

  configFile = pkgs.writeText "knotenwanderung.ini" (generators.toINI {} cfg.config);
in {
  options.services.knotenwanderung = {
    enable = mkEnableOption "knotenwanderung";

    config = mkOption {};
  };

  config = {
    systemd.services.knotenwanderung = mkIf cfg.enable {
      wantedBy = [ "multi-user.target" ];
      serviceConfig.ExecStart = "${knotenwanderung}/bin/knotenwanderung ${configFile}";
    };
  };
}
