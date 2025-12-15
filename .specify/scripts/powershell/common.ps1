#!/usr/bin/env pwsh
# Common PowerShell functions analogous to common.sh

function Get-RepoRoot {
    # Always use the project root where the .specify directory is located
    # This ensures consistency even if the git repo root is higher up
    return (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path
}

function Get-CurrentBranch {
    # First check if SPECIFY_FEATURE environment variable is set
    if ($env:SPECIFY_FEATURE) {
        return $env:SPECIFY_FEATURE
    }
    
    # Then check git if available
    try {
        $result = git rev-parse --abbrev-ref HEAD 2>$null
        if ($LASTEXITCODE -eq 0) {
            return $result
        }
    } catch {
        # Git command failed
    }
    
    # For non-git repos, try to find the latest feature directory
    $repoRoot = Get-RepoRoot
    $specsDir = Join-Path $repoRoot "specs"
    
    if (Test-Path $specsDir) {
        $latestFeature = ""
        $highest = 0
        
        Get-ChildItem -Path $specsDir -Directory | ForEach-Object {
            if ($_.Name -match '^(\d{3})-') {
                $num = [int]$matches[1]
                if ($num -gt $highest) {
                    $highest = $num
                    $latestFeature = $_.Name
                }
            }
        }
        
        if ($latestFeature) {
            return $latestFeature
        }
    }
    
    # Final fallback
    return "main"
}

function Test-HasGit {
    try {
        git rev-parse --show-toplevel 2>$null | Out-Null
        return ($LASTEXITCODE -eq 0)
    } catch {
        return $false
    }
}

function Test-FeatureBranch {
    param(
        [string]$Branch,
        [bool]$HasGit = $true
    )
    
    # For non-git repos, we can't enforce branch naming but still provide output
    if (-not $HasGit) {
        Write-Warning "[specify] Warning: Git repository not detected; skipped branch validation"
        return $true
    }
    
    if ($Branch -notmatch '^[0-9]{3}-') {
        Write-Output "ERROR: Not on a feature branch. Current branch: $Branch"
        Write-Output "Feature branches should be named like: 001-feature-name"
        return $false
    }
    return $true
}

function Get-FeatureDir {
    param([string]$RepoRoot, [string]$Branch)
    Join-Path $RepoRoot "specs/$Branch"
}

function Get-FeaturePathsEnv {
    $repoRoot = Get-RepoRoot
    $currentBranch = Get-CurrentBranch
    $hasGit = Test-HasGit
    $featureDir = Get-FeatureDir -RepoRoot $repoRoot -Branch $currentBranch
    
    [PSCustomObject]@{
        REPO_ROOT     = $repoRoot
        CURRENT_BRANCH = $currentBranch
        HAS_GIT       = $hasGit
        FEATURE_DIR   = $featureDir
        FEATURE_SPEC  = Join-Path $featureDir 'spec.md'
        IMPL_PLAN     = Join-Path $featureDir 'plan.md'
        TASKS         = Join-Path $featureDir 'tasks.md'
        RESEARCH      = Join-Path $featureDir 'research.md'
        DATA_MODEL    = Join-Path $featureDir 'data-model.md'
        QUICKSTART    = Join-Path $featureDir 'quickstart.md'
        CONTRACTS_DIR = Join-Path $featureDir 'contracts'
    }
}

function Extract-PlanField {
    param(
        [Parameter(Mandatory=$true)]
        [string]$FieldPattern,
        [Parameter(Mandatory=$true)]
        [string]$PlanFile
    )
    Write-Host "DEBUG: Extract-PlanField called for FieldPattern: '$FieldPattern', PlanFile: '$PlanFile'"
    if (-not (Test-Path $PlanFile)) { 
        Write-Host "DEBUG: PlanFile '$PlanFile' not found."
        return '' 
    }
    # Lines like **Language/Version**: Python 3.12
    # Simplified regex for debugging
    $regex = "\*\*$( $FieldPattern )\*\*: (.+)" 
    Write-Host "DEBUG: Regex: '$regex'"
    $matches = @()
    $content = Get-Content -LiteralPath $PlanFile -Encoding utf8
    foreach ($line in $content) {
        Write-Host "DEBUG: Checking line: '$line'"
        if ($line -match $regex) { 
            Write-Host "DEBUG: Line matched regex."
            Write-Host "DEBUG: Matches[0]: '$($Matches[0])'"
            Write-Host "DEBUG: Matches[1]: '$($Matches[1])'"
            $val = $Matches[1].Trim() 
            Write-Host "DEBUG: Extracted value: '$val'"
            if ($val -notin @('NEEDS CLARIFICATION','N/A')) { 
                $matches += $val 
                Write-Host "DEBUG: Added value to matches array."
            } else {
                Write-Host "DEBUG: Value was 'NEEDS CLARIFICATION' or 'N/A', not added."
            }
        }
    }
    if ($matches.Count -gt 0) {
        Write-Host "DEBUG: Returning first match: '$($matches[0])'"
        return $matches[0]
    }
    Write-Host "DEBUG: No valid match found, returning empty string."
    return ''
}

function Test-FileExists {
    param([string]$Path, [string]$Description)
    if (Test-Path -Path $Path -PathType Leaf) {
        Write-Output "  ✓ $Description"
        return $true
    } else {
        Write-Output "  ✗ $Description"
        return $false
    }
}

function Test-DirHasFiles {
    param([string]$Path, [string]$Description)
    if ((Test-Path -Path $Path -PathType Container) -and (Get-ChildItem -Path $Path -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer } | Select-Object -First 1)) {
        Write-Output "  ✓ $Description"
        return $true
    } else {
        Write-Output "  ✗ $Description"
        return $false
    }
}

function Test-ExtractPlanField {
    param(
        [string]$PlanFile
    )
    Write-Host "--- Testing Extract-PlanField ---"
    $lang = Extract-PlanField -FieldPattern 'Language/Version' -PlanFile $PlanFile
    Write-Host "Extracted Language/Version: '$lang'"
    $framework = Extract-PlanField -FieldPattern 'Primary Dependencies' -PlanFile $PlanFile
    Write-Host "Extracted Primary Dependencies: '$framework'"
    $storage = Extract-PlanField -FieldPattern 'Storage' -PlanFile $PlanFile
    Write-Host "Extracted Storage: '$storage'"
    Write-Host "--- Test Complete ---"
}
