{ pkgs }:

pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
      pandas
      requests
      discordpy
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
