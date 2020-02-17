with import <nixpkgs> {};

(pkgs.python3.withPackages (ps: with ps; [
  bjoern bottle influxdb
])).env
