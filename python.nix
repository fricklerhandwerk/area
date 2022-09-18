with (import ./inputs.nix);
mach-nix.mkPython {
  requirements = builtins.readFile ./requirements.txt + builtins.readFile ./requirements-test.txt;
}
