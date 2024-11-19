{ pkgs ? import <nixpkgs> {} }:
let
  nixpkgs.config.allowUnfreePredicate = pkg: builtins.elem (nixpkgs.lib.getName pkg) [
    "cuda-merged"
  ];
in
(pkgs.buildFHSUserEnv {
  name = "pipzone";
  targetPkgs = pkgs: (with pkgs; [
    python311
    python311Packages.pip
    python311Packages.virtualenv
    cudaPackages.cudatoolkit

    ffmpeg
    libGL
    glib
    #glibc
  ]);
  runScript = "bash";


  profile = ''
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${pkgs.libGL.out}/lib:${pkgs.glib.out}/lib
 '';
 # :${pkgs.glibc}/lib
}).env
