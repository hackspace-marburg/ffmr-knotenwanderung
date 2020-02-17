{ config, lib, pkgs, ... }:

with lib;

let
  knotenwanderung = with pkgs.python3Packages; buildPythonPackage rec {
    pname = "knotenwanderung";
    version = "unstable";

    #src = pkgs.fetchFromGitHub {
    #  owner = "hackspace-marburg";
    #  repo = "ffmr-knotenwanderung";
    #  rev = "v0.1.0";
    #  sha256 = "0yywfpk9qzr2pbi9g1ld34gggmngg1ir1vyw6n26zpmf4vv8250p";
    #};
    src = lib.cleanSource ./.;

    propagatedBuildInputs = [ bottle influxdb ];
  };

  cfg = config.services.knotenwanderung;

  configFile = pkgs.writeText "knotenwanderung.ini" (generators.toINI {} cfg.config);
in {
  options.services.knotenwanderung = {
    enable = mkEnableOption ''
      knotenwanderung, web service to check whether FFMR nodes have been renamed
    '';

    config = mkOption {
      type = types.attrs;
      description = "A set to mimic knotenwanderung's configuration INI file.";
      example = {
        InfluxDBClient = {
          host = "influx.example.com"; port = 1312; database = "ff";
        };
        Bottle = {
          host = "localhost"; port = 8080;
        };
      };
    };
  };

  config = {
    systemd.services.knotenwanderung = mkIf cfg.enable {
      description = "Web service to check whether FFMR nodes have been renamed";

      after = [ "network.target" ];
      wantedBy = [ "multi-user.target" ];

      serviceConfig = {
        ExecStart = "${knotenwanderung}/bin/knotenwanderung ${configFile}";
        DynamicUser = true;
      };
    };
  };
}
