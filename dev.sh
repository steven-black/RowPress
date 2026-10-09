#!/usr/bin/env bash
case "$1" in
  clean)   rm -rf bin obj ;;
  build)   dotnet build Xemplate.csproj ;;
  run)     dotnet run --project Xemplate.csproj ;;
  fresh)   rm -rf bin obj && dotnet build Xemplate.csproj && dotnet run --project Xemplate.csproj ;;
  publish) dotnet publish Xemplate.csproj -c Release ;;
  open)
    dir="$(cygpath -w "$PWD/bin/Release/net10.0-windows/win-x64/publish")"
    if [ -d "$dir" ]; then
      explorer "$dir"
    else
      echo "Publish folder not found. Run: bash dev.sh publish"
    fi
    ;;
  *)       echo "usage: ./dev.sh clean|build|run|fresh|publish|open" ;;
esac
