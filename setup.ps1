# setup.ps1 — Instalacao inicial do squad qa-agents (primeira vez)
#
# Execute este script em qualquer maquina para instalar o squad completo.
# Nao e necessario clonar o repositorio antes — este script faz tudo.
#
# Uso:
#   powershell -ExecutionPolicy Bypass -File .\setup.ps1
#
# Pre-requisitos:
#   - Git instalado (https://git-scm.com)
#   - Claude Code instalado

$ErrorActionPreference = "Stop"
$REPO_URL = "https://github.com/carminitti/Agentes.git"
$DEFAULT_DIR = "$env:USERPROFILE\Documents\qa-agents"

Write-Host ""
Write-Host "=================================================="
Write-Host "   Squad QA - Instalacao inicial"
Write-Host "=================================================="
Write-Host ""

# ── Verificar Git ─────────────────────────────────────────────────────────
$gitPath = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitPath) {
    Write-Host "ERRO: Git nao encontrado."
    Write-Host ""
    Write-Host "Instale o Git antes de continuar:"
    Write-Host "  winget install Git.Git"
    Write-Host "  (ou acesse https://git-scm.com e baixe o instalador)"
    Write-Host ""
    exit 1
}

# ── Diretorio de instalacao ───────────────────────────────────────────────
Write-Host "Onde deseja instalar o squad?"
Write-Host "  [Enter] para usar o padrao: $DEFAULT_DIR"
Write-Host ""
$inputDir = Read-Host "Diretorio"

if ([string]::IsNullOrWhiteSpace($inputDir)) {
    $installDir = $DEFAULT_DIR
} else {
    $installDir = $inputDir.Trim()
}

Write-Host ""
Write-Host "Diretorio escolhido: $installDir"
Write-Host ""

# ── Clonar ou atualizar ───────────────────────────────────────────────────
if (Test-Path (Join-Path $installDir ".git")) {
    Write-Host "Repositorio ja existe. Atualizando..."
    $pullOutput = git -C $installDir pull 2>&1
    Write-Host $pullOutput
} else {
    Write-Host "Clonando repositorio..."
    $cloneOutput = git clone $REPO_URL $installDir 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "ERRO: Falha ao clonar o repositorio."
        Write-Host $cloneOutput
        Write-Host ""
        Write-Host "Verifique sua conexao e tente novamente."
        exit 1
    }
    Write-Host $cloneOutput
}

Write-Host ""

# ── Versao instalada ──────────────────────────────────────────────────────
$pluginJson = Join-Path $installDir ".claude-plugin\plugin.json"
$version = "desconhecida"
if (Test-Path $pluginJson) {
    try {
        $meta = Get-Content $pluginJson -Raw | ConvertFrom-Json
        $version = $meta.version
    } catch {}
}

Write-Host "Versao: $version"
Write-Host ""

# ── Instalar agentes ──────────────────────────────────────────────────────
Write-Host "Instalando agentes no Claude Code..."
Write-Host ""

$installScript = Join-Path $installDir "install.ps1"
if (-not (Test-Path $installScript)) {
    Write-Host "ERRO: install.ps1 nao encontrado em $installDir"
    exit 1
}

& powershell -ExecutionPolicy Bypass -File $installScript
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERRO: Instalacao falhou. Verifique as mensagens acima."
    exit 1
}

# ── Sucesso ───────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "=================================================="
Write-Host "   Squad QA v$version instalado com sucesso!"
Write-Host "=================================================="
Write-Host ""
Write-Host "Proximo passo: reinicie o Claude Code."
Write-Host ""
Write-Host "Para atualizar no futuro, basta rodar:"
Write-Host "  powershell -ExecutionPolicy Bypass -File `"$installDir\update.ps1`""
Write-Host ""
