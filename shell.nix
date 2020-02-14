with import <nixpkgs> {};

(pkgs.python3.withPackages (ps: with ps; [
  bottle
  influxdb
])).env
