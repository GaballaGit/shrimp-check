{ pkgs }:

pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
      requests
      discordpy
      ruff
    ]))
  ];

  shellHook = ''
  	if [ -f .env ]; then
		set -a
		source .env
		set +a
	fi
	'';
}
