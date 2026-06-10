{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      python = pkgs.python3.withPackages (ps: [
        ps.wxpython
        ps.tabulate
      ]);
    in
    {
      packages.${system}.default = pkgs.writeShellApplication {
        name = "area";
        runtimeInputs = [ python ];
        text = ''
          exec python ${self}/area/gui.py
        '';
      };
    };
}
