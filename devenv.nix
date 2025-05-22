{ pkgs, ... }:

{
  # Python 3.12 and uv package manager
  packages = [
    pkgs.uv
    pkgs.gnumake
  ];

  # Set up Python environment
  languages.python = {
    enable = true;
    version = "3.12";
    uv.enable = true;
  };

  # Shell hook to activate the environment
  enterShell = ''
    echo "PyGridFight development environment"
    echo "Python: $(python --version)"
    echo "uv: $(uv --version)"
  '';
}