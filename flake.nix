{
	description = "Nix flake for shrimp check bot";

	inputs = {
		nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
		flake-utils.url = "github:numtide/flake-utils";
	};

	outputs = { self, nixpkgs, flake-utils }: 
		flake-utils.lib.eachDefaultSystem (
			system: let
				pkgs = nixpkgs.legacyPackages.${system};

				version =
					if (self ? rev)
					then builtins.substring 0 8 self.rev
					else "dev";

				package = pkgs.callPackage ./nix/package.nix {
					version = version;
				};
			in {
				packages.default = package;
				devShells.default = pkgs.callPackage ./nix/shell.nix {};
			}
		);
}
