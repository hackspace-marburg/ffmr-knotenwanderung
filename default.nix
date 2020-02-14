with import <nixpkgs> {};

with pkgs.python3Packages; buildPythonPackage rec {
  pname = "knotenwanderung";
  version = "unstable-2020-02-14";

  src = lib.cleanSource ./.;

  propagatedBuildInputs = [ bottle influxdb ];
}
