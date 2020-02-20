with import <nixpkgs> {};

(pkgs.python3.withPackages (ps: with ps; [
  bjoern bottle cachetools influxdb
])).env
