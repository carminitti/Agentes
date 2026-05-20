# Instala o plugin qa-agents no perfil do usuário atual
# Modo preferencial: plugin install (requer Claude Code >= versão com suporte a plugins)
# Fallback: cópia manual dos agentes para ~/.claude/agents/
#
# Se a política de execução bloquear o script, rode:
#   powershell -ExecutionPolicy Bypass -File .\install.ps1

$pluginDir = $PSScriptRoot

Write-Host "Tentando instalar via plugin..."
$result = & claude plugin install --scope user $pluginDir 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "Plugin qa-agents instalado com sucesso."
    Write-Host "Reinicie o Claude Code para que os agentes fiquem disponíveis."
    exit 0
}

Write-Host "Plugin install não disponível. Instalando manualmente..."
Write-Host ""

$destination = "$env:USERPROFILE\.claude\agents"
$source = Join-Path $pluginDir "agents"

if (-not (Test-Path $source)) {
    Write-Host "Pasta agents/ não encontrada em $pluginDir"
    exit 1
}

if (-not (Test-Path $destination)) {
    New-Item -ItemType Directory -Path $destination -Force | Out-Null
}

$installed = 0
$updated = 0

# Instala agents da raiz de agents/ e de subpastas nomeadas (ex: genericos/).
# Exclui suites/ — são fixtures de teste, não agents.
Get-ChildItem -Path $source -Filter "*.md" -Recurse |
    Where-Object { $_.DirectoryName -notmatch '\\suites($|\\)' } |
    ForEach-Object {
    $target = Join-Path $destination $_.Name
    $isNew = -not (Test-Path $target)
    Copy-Item $_.FullName -Destination $destination -Force
    if ($isNew) {
        Write-Host "Instalado:  $($_.Name)"
        $installed++
    } else {
        Write-Host "Atualizado: $($_.Name)"
        $updated++
    }
}

Write-Host ""
Write-Host "$installed novo(s), $updated atualizado(s) em $destination"
Write-Host "Reinicie o Claude Code para que os agentes fiquem disponíveis."
