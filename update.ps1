# update.ps1 — Atualiza o squad qa-agents para a versão mais recente
#
# Uso:
#   .\update.ps1
#
# Se a política de execução bloquear o script:
#   powershell -ExecutionPolicy Bypass -File .\update.ps1

$ErrorActionPreference = "Stop"
$pluginJson = Join-Path $PSScriptRoot ".claude-plugin\plugin.json"

function Get-SquadVersion {
    if (Test-Path $pluginJson) {
        try {
            $meta = Get-Content $pluginJson -Raw | ConvertFrom-Json
            return $meta.version
        } catch {}
    }
    return "desconhecida"
}

# ── Banner ─────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "=================================================="
Write-Host "   Squad QA - Atualizador de versao"
Write-Host "=================================================="
Write-Host ""

# ── Versão antes do pull ───────────────────────────────────────────────────
$versionBefore = Get-SquadVersion
Write-Host "Versao atual : $versionBefore"

# ── Verificar se está num repositório git ─────────────────────────────────
$gitDir = Join-Path $PSScriptRoot ".git"
if (-not (Test-Path $gitDir)) {
    Write-Host ""
    Write-Host "ERRO: este diretorio nao e um repositorio git."
    Write-Host "Clone o repositorio antes de usar este script:"
    Write-Host "  git clone https://github.com/carminitti/Agentes.git"
    exit 1
}

# ── git pull ──────────────────────────────────────────────────────────────
Write-Host "Buscando atualizacoes..."
Write-Host ""

$pullOutput = git -C $PSScriptRoot pull 2>&1
$pullExitCode = $LASTEXITCODE

Write-Host $pullOutput

if ($pullExitCode -ne 0) {
    Write-Host ""
    Write-Host "ERRO: git pull falhou. Verifique sua conexao e permissoes de acesso."
    exit 1
}

Write-Host ""

# ── Versão após o pull ────────────────────────────────────────────────────
$versionAfter = Get-SquadVersion

if ($versionBefore -eq $versionAfter) {
    Write-Host "Voce ja esta na versao mais recente ($versionAfter)."
    Write-Host "Nenhuma instalacao necessaria."
    exit 0
}

Write-Host "Nova versao detectada : $versionBefore  ->  $versionAfter"
Write-Host ""

# ── O que mudou (últimos commits desde o pull) ────────────────────────────
Write-Host "Novidades nesta versao:"
$logOutput = git -C $PSScriptRoot log --oneline -5 2>&1
Write-Host $logOutput
Write-Host ""

# ── Reinstalar agentes ────────────────────────────────────────────────────
Write-Host "Instalando agentes atualizados..."
Write-Host ""

$installScript = Join-Path $PSScriptRoot "install.ps1"
if (-not (Test-Path $installScript)) {
    Write-Host "ERRO: install.ps1 nao encontrado em $PSScriptRoot"
    exit 1
}

& powershell -ExecutionPolicy Bypass -File $installScript
$installExitCode = $LASTEXITCODE

if ($installExitCode -ne 0) {
    Write-Host ""
    Write-Host "ERRO: instalacao falhou. Verifique as mensagens acima."
    exit 1
}

# ── Sucesso ───────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "=================================================="
Write-Host "   Atualizado: $versionBefore  ->  $versionAfter"
Write-Host "=================================================="
Write-Host ""
Write-Host "Reinicie o Claude Code para ativar os novos agentes."
Write-Host ""
