{ pkgs ? import <nixpkgs> {} }:
(pkgs.buildFHSUserEnv {
  name = "pipzone";
  targetPkgs = pkgs: (with pkgs; [
    python311
    python311Packages.pip
    python311Packages.virtualenv
    cudaPackages.cudatoolkit

    ffmpeg
    libGL
    glibc
  ]);
  runScript = "zsh";

  profile = ''
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${pkgs.libGL}/lib:${pkgs.glibc}/lib:/nix/store/pjxrn2wn0sn533p48jz5qxgjld84hn3i-glib-2.80.4/lib
 '';
}).env
