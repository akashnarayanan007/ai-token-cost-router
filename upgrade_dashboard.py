import json
import os

# 1. Parse and clean dataset
with open('openrouter_final.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

cleaned_models = []
for m in raw_data:
    inp = m.get('input_price')
    outp = m.get('output_price')
    if inp and isinstance(inp, dict) and 'value' in inp and outp and isinstance(outp, dict) and 'value' in outp:
        try:
            inp_val = float(inp['value'])
            outp_val = float(outp['value'])
            
            ctx_str = str(m.get('context_length', '0')).upper().strip()
            ctx_tokens = 0
            if 'M' in ctx_str:
                ctx_tokens = int(float(ctx_str.replace('M', '')) * 1_000_000)
            elif 'K' in ctx_str:
                ctx_tokens = int(float(ctx_str.replace('K', '')) * 1_000)
            elif ctx_str.isdigit():
                ctx_tokens = int(ctx_str)
                
            cache_val = 0.0
            cache_p = m.get('cache_read_price')
            if cache_p and isinstance(cache_p, dict) and 'value' in cache_p:
                try:
                    cache_val = float(cache_p['value'])
                except (ValueError, TypeError):
                    cache_val = 0.0

            model_id_str = m.get('model_id', 'unknown')
            provider_name = model_id_str
            if '/' in model_id_str:
                provider_name = model_id_str.split('/')[0]
            elif model_id_str.startswith('~'):
                provider_name = model_id_str.replace('~', '')

            cleaned_models.append({
                'model_id': model_id_str,
                'provider': provider_name,
                'model_name': m.get('model_name', 'Unknown Model'),
                'context_length': m.get('context_length', 'N/A'),
                'context_tokens': ctx_tokens,
                'input_price': inp_val,
                'output_price': outp_val,
                'cache_price': cache_val,
                'release_date': m.get('release_date', ''),
                'product_page_url': m.get('product_page_url', '#')
            })
        except (ValueError, TypeError):
            continue

json_embed = json.dumps(cleaned_models, separators=(',', ':'))

# 2. Build HTML template
html_template = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Token Cost Router | Enterprise LLM Cost Optimization</title>
    
    <!-- Professional Google Fonts: Inter & JetBrains Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            /* WCAG AAA High-Contrast Dark Palette */
            --bg-primary: #090d16;
            --bg-secondary: #0f1626;
            --bg-subtle: #141c2e;
            
            --card-bg: #111a2e;
            --card-bg-elevated: #16223b;
            --card-border: #1e2c47;
            --card-border-hover: #33486f;
            --card-border-strong: #405785;
            --card-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);

            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --text-dim: #64748b;

            /* Strict Accessible Primary & Accents */
            --accent-primary: #3b82f6;
            --accent-primary-hover: #2563eb;
            --accent-primary-subtle: rgba(59, 130, 246, 0.12);
            --accent-primary-border: rgba(59, 130, 246, 0.35);

            --accent-emerald: #10b981;
            --accent-emerald-hover: #059669;
            --accent-emerald-subtle: rgba(16, 185, 129, 0.12);
            --accent-emerald-border: rgba(16, 185, 129, 0.35);

            --accent-amber: #f59e0b;
            --accent-amber-subtle: rgba(245, 158, 11, 0.12);
            --accent-amber-border: rgba(245, 158, 11, 0.35);

            --accent-rose: #f43f5e;
            --accent-rose-subtle: rgba(244, 63, 94, 0.12);
            --accent-rose-border: rgba(244, 63, 94, 0.35);

            --accent-cyan: #06b6d4;
            --accent-cyan-subtle: rgba(6, 182, 212, 0.12);

            --accent-indigo: #6366f1;
            --accent-indigo-subtle: rgba(99, 102, 241, 0.12);

            --input-bg: #0b1120;
            --input-border: #233352;
            --input-border-focus: #3b82f6;

            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 14px;
            --radius-xl: 18px;

            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            --font-mono: 'JetBrains Mono', SFMono-Regular, Menlo, Monaco, Consolas, monospace;

            --transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }

        /* Light Theme Overrides (High-Contrast Slate) */
        [data-theme="light"] {
            --bg-primary: #f8fafc;
            --bg-secondary: #f1f5f9;
            --bg-subtle: #e2e8f0;

            --card-bg: #ffffff;
            --card-bg-elevated: #f8fafc;
            --card-border: #e2e8f0;
            --card-border-hover: #cbd5e1;
            --card-border-strong: #94a3b8;
            --card-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05);

            --text-primary: #0f172a;
            --text-secondary: #334155;
            --text-muted: #64748b;
            --text-dim: #94a3b8;

            --accent-primary: #2563eb;
            --accent-primary-hover: #1d4ed8;
            --accent-primary-subtle: rgba(37, 99, 235, 0.08);
            --accent-primary-border: rgba(37, 99, 235, 0.25);

            --accent-emerald: #059669;
            --accent-emerald-hover: #047857;
            --accent-emerald-subtle: rgba(5, 150, 105, 0.08);
            --accent-emerald-border: rgba(5, 150, 105, 0.25);

            --accent-amber: #d97706;
            --accent-amber-subtle: rgba(217, 119, 6, 0.08);
            --accent-amber-border: rgba(217, 119, 6, 0.25);

            --accent-rose: #e11d48;
            --accent-rose-subtle: rgba(225, 29, 72, 0.08);
            --accent-rose-border: rgba(225, 29, 72, 0.25);

            --input-bg: #ffffff;
            --input-border: #cbd5e1;
            --input-border-focus: #2563eb;
        }

        *, *::before, *::after {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        html, body {
            width: 100%;
            min-height: 100%;
            font-family: var(--font-sans);
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        /* Enterprise Subtle Dot Grid Background */
        body {
            background-image: radial-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px);
            background-size: 24px 24px;
        }

        [data-theme="light"] body {
            background-image: radial-gradient(rgba(0, 0, 0, 0.04) 1px, transparent 1px);
        }

        .container {
            max-width: 1320px;
            margin: 0 auto;
            padding: 0 24px;
        }

        /* ================= NAVIGATION HEADER ================= */
        header.app-header {
            position: sticky;
            top: 0;
            z-index: 50;
            background: rgba(9, 13, 22, 0.85);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-bottom: 1px solid var(--card-border);
            padding: 14px 0;
            transition: var(--transition);
        }

        [data-theme="light"] header.app-header {
            background: rgba(248, 250, 252, 0.88);
            border-color: var(--card-border);
        }

        .header-inner {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
        }

        .brand-section {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
            color: inherit;
            cursor: pointer;
        }

        .brand-logo-icon {
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-emerald));
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.35);
        }

        .brand-text {
            display: flex;
            flex-direction: column;
        }

        .brand-title {
            font-size: 1.05rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .brand-pill {
            font-size: 0.68rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            background: var(--accent-primary-subtle);
            color: var(--accent-primary);
            border: 1px solid var(--accent-primary-border);
            padding: 2px 7px;
            border-radius: 12px;
        }

        .brand-sub {
            font-size: 0.75rem;
            color: var(--text-muted);
            font-weight: 500;
        }

        /* Top Nav Tabs */
        .nav-tabs {
            display: flex;
            align-items: center;
            gap: 6px;
            background: var(--bg-secondary);
            padding: 4px;
            border-radius: var(--radius-md);
            border: 1px solid var(--card-border);
        }

        .nav-tab-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 7px 16px;
            border-radius: var(--radius-sm);
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: var(--transition);
        }

        .nav-tab-btn:hover {
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.04);
        }

        [data-theme="light"] .nav-tab-btn:hover {
            background: rgba(0, 0, 0, 0.04);
        }

        .nav-tab-btn.active {
            background: var(--card-bg);
            color: var(--text-primary);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            border: 1px solid var(--card-border);
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
            background: var(--accent-emerald-subtle);
            color: var(--accent-emerald);
            border: 1px solid var(--accent-emerald-border);
        }

        .status-dot-pulse {
            width: 7px;
            height: 7px;
            background: var(--accent-emerald);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--accent-emerald);
            animation: pulseDot 2s infinite;
        }

        @keyframes pulseDot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.85); }
        }

        .btn-icon {
            width: 38px;
            height: 38px;
            border-radius: var(--radius-md);
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            color: var(--text-secondary);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: var(--transition);
        }

        .btn-icon:hover {
            background: var(--card-bg-elevated);
            color: var(--text-primary);
            border-color: var(--card-border-hover);
            transform: translateY(-1px);
        }

        .btn-secondary {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            color: var(--text-primary);
            padding: 8px 14px;
            border-radius: var(--radius-md);
            font-size: 0.82rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
            transition: var(--transition);
        }

        .btn-secondary:hover {
            background: var(--card-bg-elevated);
            border-color: var(--card-border-hover);
        }

        /* ================= MAIN CONTENT VIEWS ================= */
        main.main-content {
            padding: 32px 0 64px;
        }

        .tab-panel {
            display: none;
        }

        .tab-panel.active {
            display: block;
            animation: fadeIn 0.25s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* ================= HERO WINNER CARD ================= */
        .hero-banner {
            background: linear-gradient(135deg, rgba(20, 29, 49, 0.95) 0%, rgba(13, 20, 36, 0.98) 100%);
            border: 1px solid var(--accent-emerald-border);
            border-radius: var(--radius-xl);
            padding: 32px 36px;
            margin-bottom: 24px;
            box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.08);
            position: relative;
            overflow: hidden;
        }

        [data-theme="light"] .hero-banner {
            background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
            border-color: rgba(5, 150, 105, 0.3);
            box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.08);
        }

        .hero-banner::after {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 380px;
            height: 100%;
            background: radial-gradient(circle at 80% 20%, rgba(16, 185, 129, 0.12) 0%, transparent 70%);
            pointer-events: none;
        }

        .hero-grid {
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 32px;
            align-items: center;
            position: relative;
            z-index: 2;
        }

        .hero-badge-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }

        .badge-winner {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: var(--accent-emerald-subtle);
            border: 1px solid var(--accent-emerald-border);
            color: var(--accent-emerald);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .hero-model-title {
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: var(--text-primary);
            margin-bottom: 12px;
            line-height: 1.2;
        }

        .hero-meta-strip {
            display: flex;
            align-items: center;
            gap: 20px;
            color: var(--text-secondary);
            font-size: 0.88rem;
            flex-wrap: wrap;
        }

        .hero-meta-item {
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .hero-meta-item strong {
            color: var(--text-primary);
            font-weight: 600;
        }

        .hero-cost-box {
            text-align: right;
            background: var(--input-bg);
            border: 1px solid var(--card-border);
            border-radius: var(--radius-lg);
            padding: 24px 32px;
            min-width: 280px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        }

        .hero-cost-label {
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 6px;
        }

        .hero-cost-figure {
            font-family: var(--font-mono);
            font-size: 2.7rem;
            font-weight: 800;
            color: var(--accent-emerald);
            line-height: 1.1;
            letter-spacing: -0.03em;
        }

        .hero-savings-subtitle {
            margin-top: 8px;
            font-size: 0.82rem;
            color: var(--accent-emerald);
            font-weight: 600;
        }

        /* Volume Multiplier Bar */
        .volume-scale-banner {
            margin-top: 18px;
            padding-top: 16px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 14px;
        }

        [data-theme="light"] .volume-scale-banner {
            border-top-color: rgba(0, 0, 0, 0.08);
        }

        .scale-selector {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .scale-label {
            font-size: 0.78rem;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-right: 6px;
        }

        .scale-btn {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            color: var(--text-secondary);
            padding: 5px 12px;
            border-radius: 16px;
            font-size: 0.78rem;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
        }

        .scale-btn:hover {
            color: var(--text-primary);
            border-color: var(--card-border-hover);
        }

        .scale-btn.active {
            background: var(--accent-primary);
            border-color: var(--accent-primary);
            color: #ffffff;
        }

        .projected-savings-pill {
            font-size: 0.84rem;
            font-weight: 600;
            color: var(--text-secondary);
        }

        .projected-savings-pill strong {
            color: var(--accent-emerald);
            font-family: var(--font-mono);
        }

        /* ================= KPI STATS CARDS ================= */
        .stats-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }

        .stat-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: var(--radius-lg);
            padding: 20px 22px;
            transition: var(--transition);
            box-shadow: var(--card-shadow);
        }

        .stat-card:hover {
            border-color: var(--card-border-hover);
            transform: translateY(-2px);
        }

        .stat-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 8px;
        }

        .stat-heading {
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
        }

        .stat-icon-wrap {
            width: 32px;
            height: 32px;
            border-radius: var(--radius-sm);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .icon-emerald { background: var(--accent-emerald-subtle); color: var(--accent-emerald); }
        .icon-blue { background: var(--accent-primary-subtle); color: var(--accent-primary); }
        .icon-rose { background: var(--accent-rose-subtle); color: var(--accent-rose); }
        .icon-cyan { background: var(--accent-cyan-subtle); color: var(--accent-cyan); }

        .stat-number {
            font-family: var(--font-mono);
            font-size: 1.65rem;
            font-weight: 800;
            color: var(--text-primary);
            line-height: 1.2;
            letter-spacing: -0.02em;
        }

        .stat-detail {
            font-size: 0.78rem;
            color: var(--text-muted);
            margin-top: 6px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* ================= CALCULATOR & WORKLOAD PRESETS ================= */
        .panel-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: var(--radius-xl);
            padding: 28px 32px;
            margin-bottom: 24px;
            box-shadow: var(--card-shadow);
        }

        .panel-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 14px;
        }

        .panel-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 10px;
            letter-spacing: -0.01em;
        }

        .workload-chips {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }

        .chip-label {
            font-size: 0.76rem;
            font-weight: 700;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .preset-chip {
            background: var(--bg-secondary);
            border: 1px solid var(--card-border);
            color: var(--text-secondary);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
        }

        .preset-chip:hover {
            color: var(--text-primary);
            border-color: var(--card-border-hover);
            background: var(--card-bg-elevated);
        }

        .preset-chip.active {
            background: var(--accent-primary-subtle);
            border-color: var(--accent-primary-border);
            color: var(--accent-primary);
            font-weight: 700;
        }

        .calculator-controls-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1.2fr;
            gap: 18px;
        }

        .control-group {
            display: flex;
            flex-direction: column;
            gap: 7px;
        }

        .control-label {
            font-size: 0.78rem;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.04em;
            display: flex;
            justify-content: space-between;
        }

        .control-label span.metric-val {
            font-family: var(--font-mono);
            color: var(--accent-primary);
            font-weight: 600;
            text-transform: none;
        }

        .input-text, .select-control {
            width: 100%;
            background: var(--input-bg);
            border: 1px solid var(--input-border);
            border-radius: var(--radius-md);
            padding: 12px 14px;
            color: var(--text-primary);
            font-size: 0.92rem;
            font-family: var(--font-mono);
            font-weight: 600;
            outline: none;
            transition: var(--transition);
        }

        .select-control {
            font-family: var(--font-sans);
            cursor: pointer;
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 14px center;
            padding-right: 40px;
        }

        .input-text:focus, .select-control:focus {
            border-color: var(--input-border-focus);
            box-shadow: 0 0 0 3px var(--accent-primary-subtle);
        }

        .search-box {
            position: relative;
        }

        .search-icon {
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-dim);
            pointer-events: none;
        }

        .search-input {
            padding-left: 40px;
            font-family: var(--font-sans);
            font-weight: 500;
        }

        /* ================= COMPARISON BAR CHART ================= */
        .chart-toggle-group {
            display: flex;
            gap: 4px;
            background: var(--bg-secondary);
            padding: 3px;
            border-radius: var(--radius-sm);
            border: 1px solid var(--card-border);
        }

        .toggle-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.74rem;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
        }

        .toggle-btn.active {
            background: var(--card-bg);
            color: var(--text-primary);
            box-shadow: 0 1px 4px rgba(0,0,0,0.2);
        }

        .comparison-bars-container {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 14px;
        }

        .bar-row {
            display: grid;
            grid-template-columns: 260px 1fr 140px;
            align-items: center;
            gap: 16px;
            padding: 8px 12px;
            border-radius: var(--radius-md);
            background: rgba(255, 255, 255, 0.015);
            border: 1px solid transparent;
            transition: var(--transition);
        }

        .bar-row:hover {
            background: var(--card-bg-elevated);
            border-color: var(--card-border);
        }

        .bar-model-col {
            display: flex;
            align-items: center;
            gap: 10px;
            overflow: hidden;
            white-space: nowrap;
        }

        .bar-rank-badge {
            font-family: var(--font-mono);
            font-size: 0.74rem;
            font-weight: 700;
            width: 22px;
            height: 22px;
            border-radius: 6px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: var(--bg-secondary);
            color: var(--text-muted);
            flex-shrink: 0;
        }

        .bar-rank-1 {
            background: var(--accent-emerald-subtle);
            color: var(--accent-emerald);
            border: 1px solid var(--accent-emerald-border);
        }

        .bar-model-name {
            font-size: 0.86rem;
            font-weight: 600;
            color: var(--text-primary);
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .bar-track {
            height: 24px;
            background: var(--bg-secondary);
            border-radius: 6px;
            position: relative;
            overflow: hidden;
            border: 1px solid var(--card-border);
        }

        .bar-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--accent-primary), #60a5fa);
            border-radius: 5px;
            transition: width 0.5s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
        }

        .bar-fill.winner {
            background: linear-gradient(90deg, var(--accent-emerald), #34d399);
        }

        .bar-cost-col {
            text-align: right;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 2px;
        }

        .bar-cost-val {
            font-family: var(--font-mono);
            font-size: 0.92rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        .bar-multiplier {
            font-size: 0.72rem;
            font-weight: 600;
            color: var(--text-muted);
        }

        .bar-multiplier.baseline {
            color: var(--accent-emerald);
            font-weight: 700;
        }

        /* ================= FULL PRICING MATRIX TABLE ================= */
        .table-filter-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 18px;
            flex-wrap: wrap;
            gap: 12px;
        }

        .provider-pills {
            display: flex;
            align-items: center;
            gap: 6px;
            flex-wrap: wrap;
        }

        .provider-pill {
            background: var(--bg-secondary);
            border: 1px solid var(--card-border);
            color: var(--text-secondary);
            padding: 5px 12px;
            border-radius: 16px;
            font-size: 0.76rem;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
        }

        .provider-pill:hover {
            border-color: var(--card-border-hover);
            color: var(--text-primary);
        }

        .provider-pill.active {
            background: var(--text-primary);
            color: var(--bg-primary);
            border-color: var(--text-primary);
            font-weight: 700;
        }

        .table-responsive {
            overflow-x: auto;
            border: 1px solid var(--card-border);
            border-radius: var(--radius-lg);
            background: var(--card-bg);
        }

        table.pricing-table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.88rem;
        }

        table.pricing-table th {
            background: var(--bg-secondary);
            color: var(--text-muted);
            padding: 12px 16px;
            font-size: 0.74rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 1px solid var(--card-border);
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
            transition: var(--transition);
        }

        table.pricing-table th:hover {
            color: var(--text-primary);
            background: var(--card-bg-elevated);
        }

        table.pricing-table th.active-sort {
            color: var(--accent-primary);
        }

        table.pricing-table td {
            padding: 14px 16px;
            border-bottom: 1px solid var(--card-border);
            color: var(--text-secondary);
            vertical-align: middle;
            transition: var(--transition);
        }

        table.pricing-table tr.table-row:hover td {
            background: var(--card-bg-elevated);
            color: var(--text-primary);
        }

        table.pricing-table tr.row-winner td {
            background: rgba(16, 185, 129, 0.04);
        }

        /* Provider Badges */
        .provider-tag {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 3px 10px;
            border-radius: 14px;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            text-transform: uppercase;
            border: 1px solid transparent;
            white-space: nowrap;
        }

        .tag-openai { background: rgba(16, 163, 127, 0.15); color: #34d399; border-color: rgba(16, 163, 127, 0.4); }
        .tag-anthropic { background: rgba(217, 119, 6, 0.15); color: #fbbf24; border-color: rgba(217, 119, 6, 0.4); }
        .tag-google { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border-color: rgba(59, 130, 246, 0.4); }
        .tag-deepseek { background: rgba(2, 132, 199, 0.15); color: #38bdf8; border-color: rgba(2, 132, 199, 0.4); }
        .tag-qwen { background: rgba(139, 92, 246, 0.15); color: #c084fc; border-color: rgba(139, 92, 246, 0.4); }
        .tag-meta { background: rgba(6, 182, 212, 0.15); color: #22d3ee; border-color: rgba(6, 182, 212, 0.4); }
        .tag-mistral { background: rgba(244, 63, 94, 0.15); color: #fb7185; border-color: rgba(244, 63, 94, 0.4); }
        .tag-default { background: rgba(100, 116, 139, 0.15); color: #cbd5e1; border-color: rgba(100, 116, 139, 0.3); }

        .price-mono {
            font-family: var(--font-mono);
            font-size: 0.86rem;
            color: var(--text-secondary);
        }

        .cost-highlight {
            font-family: var(--font-mono);
            font-size: 0.92rem;
            font-weight: 700;
            color: var(--accent-emerald);
        }

        .btn-inspect {
            background: transparent;
            border: 1px solid var(--card-border);
            color: var(--text-muted);
            padding: 4px 10px;
            border-radius: var(--radius-sm);
            font-size: 0.76rem;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
        }

        .btn-inspect:hover {
            color: var(--text-primary);
            border-color: var(--accent-primary);
            background: var(--accent-primary-subtle);
        }

        /* ================= TAB 3: SELF-HEALING ARCHITECTURE ================= */
        .story-hero {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: var(--radius-xl);
            padding: 36px;
            margin-bottom: 24px;
        }

        .story-title {
            font-size: 1.8rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 12px;
            color: var(--text-primary);
        }

        .story-lead {
            font-size: 1.05rem;
            color: var(--text-secondary);
            line-height: 1.6;
            max-width: 900px;
            margin-bottom: 24px;
        }

        .timeline-container {
            display: flex;
            flex-direction: column;
            gap: 16px;
            margin-top: 24px;
        }

        .timeline-step {
            display: grid;
            grid-template-columns: 48px 1fr auto;
            gap: 20px;
            align-items: center;
            background: var(--bg-secondary);
            border: 1px solid var(--card-border);
            border-radius: var(--radius-lg);
            padding: 18px 22px;
            transition: var(--transition);
        }

        .timeline-step:hover {
            border-color: var(--card-border-hover);
            transform: translateX(4px);
        }

        .step-number {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: var(--font-mono);
            font-size: 1.1rem;
            font-weight: 800;
            color: var(--accent-primary);
        }

        .step-content h4 {
            font-size: 0.98rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 4px;
        }

        .step-content p {
            font-size: 0.85rem;
            color: var(--text-muted);
            line-height: 1.5;
        }

        .step-badge {
            font-family: var(--font-mono);
            font-size: 0.8rem;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: 20px;
            white-space: nowrap;
        }

        .badge-fail { background: var(--accent-rose-subtle); color: var(--accent-rose); border: 1px solid var(--accent-rose-border); }
        .badge-progress { background: var(--accent-amber-subtle); color: var(--accent-amber); border: 1px solid var(--accent-amber-border); }
        .badge-success { background: var(--accent-emerald-subtle); color: var(--accent-emerald); border: 1px solid var(--accent-emerald-border); }

        .proof-gallery {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 24px;
        }

        .proof-card {
            background: var(--bg-secondary);
            border: 1px solid var(--card-border);
            border-radius: var(--radius-lg);
            padding: 20px;
            overflow: hidden;
        }

        .proof-card h4 {
            font-size: 0.92rem;
            font-weight: 700;
            margin-bottom: 12px;
            color: var(--text-primary);
        }

        .proof-img {
            width: 100%;
            height: auto;
            border-radius: var(--radius-md);
            border: 1px solid var(--card-border);
            cursor: pointer;
            transition: var(--transition);
        }

        .proof-img:hover {
            transform: scale(1.02);
        }

        /* ================= MODAL / DRAWER ================= */
        .modal-backdrop {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(8px);
            z-index: 100;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }

        .modal-backdrop.active {
            display: flex;
            animation: fadeIn 0.2s ease-out;
        }

        .modal-window {
            background: var(--card-bg);
            border: 1px solid var(--card-border-strong);
            border-radius: var(--radius-xl);
            max-width: 640px;
            width: 100%;
            padding: 32px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7);
            position: relative;
        }

        .modal-close-btn {
            position: absolute;
            top: 20px;
            right: 20px;
            background: transparent;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            padding: 6px;
            border-radius: 6px;
        }

        .modal-close-btn:hover {
            color: var(--text-primary);
            background: var(--card-bg-elevated);
        }

        .code-snippet-box {
            background: var(--input-bg);
            border: 1px solid var(--card-border);
            border-radius: var(--radius-md);
            padding: 16px;
            font-family: var(--font-mono);
            font-size: 0.8rem;
            color: var(--text-secondary);
            overflow-x: auto;
            margin: 16px 0;
            position: relative;
        }

        .copy-snippet-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            color: var(--text-muted);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 600;
            cursor: pointer;
        }

        .copy-snippet-btn:hover {
            color: var(--text-primary);
            border-color: var(--accent-primary);
        }

        /* Toast notifications */
        .toast-shelf {
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 200;
            display: flex;
            flex-direction: column;
            gap: 10px;
            pointer-events: none;
        }

        .toast-item {
            background: var(--card-bg);
            border: 1px solid var(--accent-emerald-border);
            color: var(--text-primary);
            padding: 12px 20px;
            border-radius: var(--radius-md);
            font-size: 0.85rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            animation: toastEnter 0.25s ease-out;
        }

        @keyframes toastEnter {
            from { opacity: 0; transform: translateY(12px) scale(0.96); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Responsive Breakpoints */
        @media (max-width: 1080px) {
            .calculator-controls-grid { grid-template-columns: 1fr 1fr; }
            .stats-row { grid-template-columns: repeat(2, 1fr); }
            .hero-grid { grid-template-columns: 1fr; }
            .hero-cost-box { text-align: left; }
            .proof-gallery { grid-template-columns: 1fr; }
        }

        @media (max-width: 720px) {
            .calculator-controls-grid { grid-template-columns: 1fr; }
            .stats-row { grid-template-columns: 1fr; }
            .bar-row { grid-template-columns: 140px 1fr 90px; }
            .hero-banner { padding: 24px; }
            .hero-model-title { font-size: 1.6rem; }
            .nav-tabs { display: none; }
        }
    </style>
</head>
<body>

    <!-- ================= APP HEADER ================= -->
    <header class="app-header">
        <div class="container header-inner">
            <div class="brand-section" onclick="switchTab('router')">
                <div class="brand-logo-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
                </div>
                <div class="brand-text">
                    <div class="brand-title">
                        AI Token Cost Router
                        <span class="brand-pill">Scraper Studio v2</span>
                    </div>
                    <span class="brand-sub">Enterprise Model Cost Intelligence</span>
                </div>
            </div>

            <!-- Central Navigation Tabs -->
            <nav class="nav-tabs">
                <button class="nav-tab-btn active" id="tab-btn-router" onclick="switchTab('router')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2"></rect><line x1="8" y1="6" x2="16" y2="6"></line><line x1="16" y1="14" x2="16" y2="18"></line></svg>
                    Router & Presets
                </button>
                <button class="nav-tab-btn" id="tab-btn-matrix" onclick="switchTab('matrix')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                    Pricing Matrix
                </button>
                <button class="nav-tab-btn" id="tab-btn-story" onclick="switchTab('story')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                    Self-Healing Architecture
                </button>
            </nav>

            <div class="header-actions">
                <div class="status-pill">
                    <div class="status-dot-pulse"></div>
                    <span id="model-count-header">388 Models Indexed</span>
                </div>

                <!-- Theme Toggle Button -->
                <button class="btn-icon" onclick="toggleTheme()" title="Toggle Light/Dark Theme">
                    <svg id="icon-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: none;"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
                    <svg id="icon-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
                </button>

                <!-- Export CSV Button -->
                <button class="btn-secondary" onclick="exportCSV()" title="Export current dataset as CSV">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                    Export
                </button>
            </div>
        </div>
    </header>

    <!-- ================= MAIN CONTENT ================= -->
    <main class="main-content">
        <div class="container">

            <!-- ================= TAB 1: ROUTER & CALCULATOR ================= -->
            <section id="panel-router" class="tab-panel active">
                
                <!-- Hero Optimal Winner Card -->
                <div class="hero-banner" id="hero-winner-card">
                    <div class="hero-grid">
                        <div>
                            <div class="hero-badge-row">
                                <span class="badge-winner">
                                    <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                                    Recommended Optimal Route
                                </span>
                                <span id="hero-provider-tag"></span>
                            </div>
                            <h2 class="hero-model-title" id="hero-model-name">Loading optimal route...</h2>
                            <div class="hero-meta-strip">
                                <div class="hero-meta-item">
                                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect></svg>
                                    Context: <strong id="hero-context">-</strong>
                                </div>
                                <div class="hero-meta-item">
                                    Input / 1M: <strong id="hero-input-rate">-</strong>
                                </div>
                                <div class="hero-meta-item">
                                    Output / 1M: <strong id="hero-output-rate">-</strong>
                                </div>
                                <div class="hero-meta-item">
                                    Release: <strong id="hero-release-date">-</strong>
                                </div>
                            </div>
                        </div>

                        <div class="hero-cost-box">
                            <div class="hero-cost-label" id="hero-cost-label">Cost (1 Request)</div>
                            <div class="hero-cost-figure" id="hero-total-cost">$0.0000</div>
                            <div class="hero-savings-subtitle" id="hero-savings-sub">Rank #1 across all filtered models</div>
                        </div>
                    </div>

                    <!-- Volume Scale Multiplier -->
                    <div class="volume-scale-banner">
                        <div class="scale-selector">
                            <span class="scale-label">Production Scale:</span>
                            <button class="scale-btn active" onclick="setVolumeMultiplier(1, this)">1 Request</button>
                            <button class="scale-btn" onclick="setVolumeMultiplier(1000, this)">1,000 Reqs</button>
                            <button class="scale-btn" onclick="setVolumeMultiplier(50000, this)">50k Reqs / Month</button>
                            <button class="scale-btn" onclick="setVolumeMultiplier(500000, this)">500k Reqs / Month</button>
                        </div>
                        <div class="projected-savings-pill">
                            Scale Savings: <strong id="hero-scale-savings">$0.00 / month</strong> vs expensive alternative
                        </div>
                    </div>
                </div>

                <!-- KPI Metric Cards -->
                <div class="stats-row">
                    <div class="stat-card">
                        <div class="stat-top">
                            <span class="stat-heading">Cheapest Option</span>
                            <div class="stat-icon-wrap icon-emerald">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                            </div>
                        </div>
                        <div class="stat-number" id="stat-cheapest-num">$0.0000</div>
                        <div class="stat-detail" id="stat-cheapest-label">-</div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-top">
                            <span class="stat-heading">Market Average</span>
                            <div class="stat-icon-wrap icon-blue">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                            </div>
                        </div>
                        <div class="stat-number" id="stat-avg-num">$0.0000</div>
                        <div class="stat-detail">Across matching tier models</div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-top">
                            <span class="stat-heading">Max Cost Option</span>
                            <div class="stat-icon-wrap icon-rose">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                            </div>
                        </div>
                        <div class="stat-number" id="stat-max-num">$0.0000</div>
                        <div class="stat-detail" id="stat-max-label">-</div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-top">
                            <span class="stat-heading">Efficiency Delta</span>
                            <div class="stat-icon-wrap icon-cyan">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
                            </div>
                        </div>
                        <div class="stat-number" id="stat-savings-num">0.0%</div>
                        <div class="stat-detail">Cheapest vs Most Expensive</div>
                    </div>
                </div>

                <!-- Calculator Panel -->
                <div class="panel-card">
                    <div class="panel-header">
                        <div class="panel-title">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--accent-primary)" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2"></rect><line x1="8" y1="6" x2="16" y2="6"></line><line x1="16" y1="14" x2="16" y2="18"></line></svg>
                            Payload Calculator & Workload Presets
                        </div>
                        <div class="workload-chips">
                            <span class="chip-label">Presets:</span>
                            <button class="preset-chip active" onclick="applyPreset(100000, 20000, this)">100k In / 20k Out</button>
                            <button class="preset-chip" onclick="applyPreset(10000, 2000, this)">Support Chat (10k/2k)</button>
                            <button class="preset-chip" onclick="applyPreset(50000, 10000, this)">Code Review (50k/10k)</button>
                            <button class="preset-chip" onclick="applyPreset(250000, 25000, this)">RAG / Enterprise (250k/25k)</button>
                            <button class="preset-chip" onclick="applyPreset(100000, 50000, this)">Deep Reasoning (100k/50k)</button>
                        </div>
                    </div>

                    <div class="calculator-controls-grid">
                        <div class="control-group">
                            <div class="control-label">
                                <span>Input Tokens</span>
                                <span class="metric-val" id="input-tokens-display">100,000</span>
                            </div>
                            <input type="number" id="input-tokens" class="input-text" value="100000" min="0" step="5000">
                        </div>

                        <div class="control-group">
                            <div class="control-label">
                                <span>Output Tokens</span>
                                <span class="metric-val" id="output-tokens-display">20,000</span>
                            </div>
                            <input type="number" id="output-tokens" class="input-text" value="20000" min="0" step="1000">
                        </div>

                        <div class="control-group">
                            <div class="control-label">
                                <span>Min Context Window</span>
                            </div>
                            <select id="context-select" class="select-control">
                                <option value="0">Any Window Size</option>
                                <option value="32000">32K+ Tokens</option>
                                <option value="128000">128K+ Tokens</option>
                                <option value="256000">256K+ Tokens</option>
                                <option value="1000000">1M+ Tokens</option>
                            </select>
                        </div>

                        <div class="control-group">
                            <div class="control-label">
                                <span>Search Model or Provider</span>
                            </div>
                            <div class="search-box">
                                <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                                <input type="text" id="search-filter" class="input-text search-input" placeholder="e.g. OpenAI, Claude, Llama, Flash...">
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Top Models Comparison Chart -->
                <div class="panel-card">
                    <div class="panel-header">
                        <div class="panel-title">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--accent-emerald)" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                            Cheapest Models Comparison Benchmark
                        </div>
                        <div class="chart-toggle-group">
                            <button class="toggle-btn active" id="btn-chart-5" onclick="setChartLimit(5)">Top 5</button>
                            <button class="toggle-btn" id="btn-chart-8" onclick="setChartLimit(8)">Top 8</button>
                            <button class="toggle-btn" id="btn-chart-12" onclick="setChartLimit(12)">Top 12</button>
                        </div>
                    </div>
                    <div class="comparison-bars-container" id="bar-chart-list">
                        <!-- Bars injected via JS -->
                    </div>
                </div>

            </section>

            <!-- ================= TAB 2: FULL PRICING MATRIX ================= -->
            <section id="panel-matrix" class="tab-panel">
                <div class="panel-card">
                    <div class="panel-header">
                        <div class="panel-title">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--accent-primary)" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="3" y1="15" x2="21" y2="15"></line><line x1="9" y1="3" x2="9" y2="21"></line><line x1="15" y1="3" x2="15" y2="21"></line></svg>
                            Complete LLM Pricing & Parameter Matrix
                        </div>
                        <div style="display: flex; gap: 8px;">
                            <button class="btn-secondary" onclick="exportCSV()">Export CSV</button>
                            <button class="btn-secondary" onclick="exportJSON()">Export JSON</button>
                        </div>
                    </div>

                    <!-- Provider Filter Bar -->
                    <div class="table-filter-bar">
                        <div class="provider-pills" id="provider-pills-bar">
                            <button class="provider-pill active" onclick="filterByProvider('all', this)">All Providers</button>
                            <button class="provider-pill" onclick="filterByProvider('openai', this)">OpenAI</button>
                            <button class="provider-pill" onclick="filterByProvider('google', this)">Google</button>
                            <button class="provider-pill" onclick="filterByProvider('anthropic', this)">Anthropic</button>
                            <button class="provider-pill" onclick="filterByProvider('deepseek', this)">DeepSeek</button>
                            <button class="provider-pill" onclick="filterByProvider('meta', this)">Meta</button>
                            <button class="provider-pill" onclick="filterByProvider('mistralai', this)">Mistral</button>
                            <button class="provider-pill" onclick="filterByProvider('qwen', this)">Qwen</button>
                            <button class="provider-pill" onclick="filterByProvider('ibm-granite', this)">IBM</button>
                        </div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);" id="matrix-count-display">
                            Showing 388 models
                        </div>
                    </div>

                    <!-- Table -->
                    <div class="table-responsive">
                        <table class="pricing-table">
                            <thead>
                                <tr>
                                    <th style="width: 60px;" onclick="handleTableSort('cost')">Rank <span id="th-sort-cost">▲</span></th>
                                    <th onclick="handleTableSort('name')">Model Name <span id="th-sort-name"></span></th>
                                    <th onclick="handleTableSort('provider')">Provider <span id="th-sort-provider"></span></th>
                                    <th onclick="handleTableSort('context')">Context Window <span id="th-sort-context"></span></th>
                                    <th onclick="handleTableSort('input_price')">Input / 1M <span id="th-sort-input_price"></span></th>
                                    <th onclick="handleTableSort('output_price')">Output / 1M <span id="th-sort-output_price"></span></th>
                                    <th style="text-align: right;" onclick="handleTableSort('cost')">Payload Cost <span id="th-sort-cost2"></span></th>
                                    <th style="text-align: right;">Action</th>
                                </tr>
                            </thead>
                            <tbody id="pricing-table-body">
                                <!-- Injected rows -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>

            <!-- ================= TAB 3: SELF-HEALING ARCHITECTURE ================= -->
            <section id="panel-story" class="tab-panel">
                <div class="story-hero">
                    <div class="brand-pill" style="margin-bottom: 12px; display: inline-block;">Into the Scrape-Verse Hackathon</div>
                    <h2 class="story-title">The Self-Healing Scraper Studio Architecture</h2>
                    <p class="story-lead">
                        OpenRouter lists 500+ AI models across dozens of providers. Capturing this volatile, dynamic dataset required building an automated, self-healing pipeline using <strong>Bright Data Scraper Studio</strong>. Here is the verified technical progression from DOM scraper failure to API discovery.
                    </p>

                    <!-- Technical Timeline -->
                    <div class="timeline-container">
                        <div class="timeline-step">
                            <div class="step-number">1</div>
                            <div class="step-content">
                                <h4>First Attempt — Direct Webpage Scraping (openrouter.ai/models)</h4>
                                <p>Initial AI scraper built targeting the rendered web table. Captured only 15 models due to client-side infinite scroll & lazy loading.</p>
                            </div>
                            <span class="step-badge badge-fail">15 Records</span>
                        </div>

                        <div class="timeline-step">
                            <div class="step-number">2</div>
                            <div class="step-content">
                                <h4>Self-Healing Attempt #1 — bdata scraper heal</h4>
                                <p>Dispatched instruction: "Wait for elements and scroll down to load infinite list". Scraper regenerated selector rules. Result: 15 → 16 models.</p>
                            </div>
                            <span class="step-badge badge-progress">16 Records</span>
                        </div>

                        <div class="timeline-step">
                            <div class="step-number">3</div>
                            <div class="step-content">
                                <h4>Self-Healing Attempt #2 — Aggressive scroll targeting</h4>
                                <p>Instructed deeper scrolling down DOM. Improved to 18 models, but proved that fighting client-side hydration in HTML was suboptimal.</p>
                            </div>
                            <span class="step-badge badge-progress">18 Records</span>
                        </div>

                        <div class="timeline-step">
                            <div class="step-number">4</div>
                            <div class="step-content">
                                <h4>Strategic Pivot — Discovering OpenRouter Public API</h4>
                                <p>Identified underlying JSON endpoint (<code>openrouter.ai/api/v1/models</code>). Pointed Bright Data Scraper Studio directly at the API payload.</p>
                            </div>
                            <span class="step-badge badge-success">421 Records</span>
                        </div>

                        <div class="timeline-step">
                            <div class="step-number">5</div>
                            <div class="step-content">
                                <h4>Final Optimization — Modality Parameter Query</h4>
                                <p>Discovered default API excludes multimodal models. Appended <code>?output_modalities=all</code>. Landed at full 558 model catalogue.</p>
                            </div>
                            <span class="step-badge badge-success">558 Records (100%)</span>
                        </div>
                    </div>

                    <!-- Visual Proof Cards -->
                    <div class="proof-gallery">
                        <div class="proof-card">
                            <h4>Bright Data Scraper Studio Collectors Proof</h4>
                            <img src="scraper-proof.png" alt="Bright Data Collectors Proof" class="proof-img" onclick="openProofModal(this.src)">
                            <p style="font-size: 0.78rem; color: var(--text-muted); margin-top: 8px;">
                                Collector IDs: <code>c_mt1syvpq8qmnfk802</code> (initial) → <code>c_mt5lqt7s21ptwuiesf</code> (final 558 models).
                            </p>
                        </div>
                        <div class="proof-card">
                            <h4>Local CLI Verification & Count Progression</h4>
                            <img src="data-count-proof.png" alt="Local Data Count Proof" class="proof-img" onclick="openProofModal(this.src)">
                            <p style="font-size: 0.78rem; color: var(--text-muted); margin-top: 8px;">
                                Terminal audit confirming dataset model growth across iterations.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

        </div>
    </main>

    <!-- ================= MODEL DETAIL INSPECT MODAL ================= -->
    <div class="modal-backdrop" id="inspect-modal">
        <div class="modal-window">
            <button class="modal-close-btn" onclick="closeInspectModal()">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
            <div id="modal-content-target">
                <!-- Dynamically populated -->
            </div>
        </div>
    </div>

    <!-- Toast Shelf -->
    <div class="toast-shelf" id="toast-shelf"></div>

    <!-- Embedded Scraped Dataset -->
    <script id="models-data" type="application/json">
__JSON_DATA__
    </script>

    <!-- Application Script Logic -->
    <script>
        const MODELS = JSON.parse(document.getElementById('models-data').textContent);

        let activeTab = 'router';
        let volumeMultiplier = 1;
        let chartLimit = 5;
        let currentSort = { key: 'cost', asc: true };
        let selectedProviderFilter = 'all';
        let debounceTimer = null;
        let currentFilteredList = [];

        // Tab Switching
        function switchTab(tabId) {
            activeTab = tabId;
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav-tab-btn').forEach(b => b.classList.remove('active'));

            const targetPanel = document.getElementById('panel-' + tabId);
            const targetBtn = document.getElementById('tab-btn-' + tabId);
            if (targetPanel) targetPanel.classList.add('active');
            if (targetBtn) targetBtn.classList.add('active');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Theme Toggle
        function toggleTheme() {
            const html = document.documentElement;
            const current = html.getAttribute('data-theme') || 'dark';
            const next = current === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', next);

            document.getElementById('icon-sun').style.display = next === 'light' ? 'block' : 'none';
            document.getElementById('icon-moon').style.display = next === 'dark' ? 'block' : 'none';
            triggerToast('Switched to ' + next.toUpperCase() + ' theme');
        }

        // Production Volume Scale
        function setVolumeMultiplier(multiplier, btnElem) {
            volumeMultiplier = multiplier;
            document.querySelectorAll('.scale-btn').forEach(b => b.classList.remove('active'));
            if (btnElem) btnElem.classList.add('active');
            
            const labelMap = {
                1: 'Cost (1 Request)',
                1000: 'Cost (1,000 Requests)',
                50000: 'Cost (50k Reqs / Mo)',
                500000: 'Cost (500k Reqs / Mo)'
            };
            document.getElementById('hero-cost-label').textContent = labelMap[multiplier] || 'Cost';
            updateAllCalculations();
        }

        // Format Currency
        function formatCost(val) {
            if (val === 0) return "$0.0000";
            if (val < 0.001) return "$" + val.toFixed(5);
            if (val < 0.01) return "$" + val.toFixed(4);
            if (val < 10) return "$" + val.toFixed(4);
            return "$" + val.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        }

        function formatTokens(num) {
            return num.toLocaleString();
        }

        // Provider Badge Helper
        function getProviderTagHTML(provider) {
            const p = (provider || 'default').toLowerCase();
            let tagClass = 'tag-default';
            if (p.includes('openai')) tagClass = 'tag-openai';
            else if (p.includes('google')) tagClass = 'tag-google';
            else if (p.includes('anthropic')) tagClass = 'tag-anthropic';
            else if (p.includes('deepseek')) tagClass = 'tag-deepseek';
            else if (p.includes('qwen')) tagClass = 'tag-qwen';
            else if (p.includes('meta')) tagClass = 'tag-meta';
            else if (p.includes('mistral')) tagClass = 'tag-mistral';

            return '<span class="provider-tag ' + tagClass + '">' + provider + '</span>';
        }

        // Main Calculation Loop
        function updateAllCalculations() {
            const inputTokens = parseFloat(document.getElementById('input-tokens').value) || 0;
            const outputTokens = parseFloat(document.getElementById('output-tokens').value) || 0;
            const minContext = parseInt(document.getElementById('context-select').value) || 0;
            const searchQuery = document.getElementById('search-filter').value.toLowerCase().trim();

            document.getElementById('input-tokens-display').textContent = formatTokens(inputTokens);
            document.getElementById('output-tokens-display').textContent = formatTokens(outputTokens);

            let filtered = MODELS.filter(m => {
                if (m.context_tokens < minContext) return false;
                if (selectedProviderFilter !== 'all') {
                    if (!m.provider.toLowerCase().includes(selectedProviderFilter)) return false;
                }
                if (searchQuery) {
                    const matchName = (m.model_name || '').toLowerCase().includes(searchQuery);
                    const matchId = (m.model_id || '').toLowerCase().includes(searchQuery);
                    const matchProv = (m.provider || '').toLowerCase().includes(searchQuery);
                    if (!matchName && !matchId && !matchProv) return false;
                }
                return true;
            });

            // Calculate cost per model
            filtered.forEach(m => {
                const singleCost = ((inputTokens / 1000000) * m.input_price) + ((outputTokens / 1000000) * m.output_price);
                m.unitCost = singleCost;
                m.totalScaledCost = singleCost * volumeMultiplier;
            });

            // Sort
            filtered.sort((a, b) => {
                let vA, vB;
                if (currentSort.key === 'cost') { vA = a.totalScaledCost; vB = b.totalScaledCost; }
                else if (currentSort.key === 'name') { vA = a.model_name; vB = b.model_name; }
                else if (currentSort.key === 'provider') { vA = a.provider; vB = b.provider; }
                else if (currentSort.key === 'context') { vA = a.context_tokens; vB = b.context_tokens; }
                else if (currentSort.key === 'input_price') { vA = a.input_price; vB = b.input_price; }
                else if (currentSort.key === 'output_price') { vA = a.output_price; vB = b.output_price; }

                if (vA < vB) return currentSort.asc ? -1 : 1;
                if (vA > vB) return currentSort.asc ? 1 : -1;
                return 0;
            });

            currentFilteredList = filtered;
            document.getElementById('matrix-count-display').textContent = 'Showing ' + filtered.length + ' of ' + MODELS.length + ' models';

            if (filtered.length === 0) {
                document.getElementById('hero-model-name').textContent = "No matching models found";
                document.getElementById('hero-total-cost').textContent = "$0.0000";
                return;
            }

            const winner = [...filtered].sort((a, b) => a.totalScaledCost - b.totalScaledCost)[0];
            const maxOption = [...filtered].sort((a, b) => b.totalScaledCost - a.totalScaledCost)[0];
            const sumCost = filtered.reduce((acc, m) => acc + m.totalScaledCost, 0);
            const avgCost = sumCost / filtered.length;
            const savingsPercent = maxOption.totalScaledCost > 0 ? 
                ((maxOption.totalScaledCost - winner.totalScaledCost) / maxOption.totalScaledCost) * 100 : 0;
            const scaleSavingsDollars = (maxOption.unitCost - winner.unitCost) * Math.max(volumeMultiplier, 50000);

            // Populate Hero
            document.getElementById('hero-model-name').textContent = winner.model_name;
            document.getElementById('hero-provider-tag').innerHTML = getProviderTagHTML(winner.provider);
            document.getElementById('hero-context').textContent = winner.context_length;
            document.getElementById('hero-input-rate').textContent = '$' + winner.input_price.toFixed(4);
            document.getElementById('hero-output-rate').textContent = '$' + winner.output_price.toFixed(4);
            document.getElementById('hero-release-date').textContent = winner.release_date || 'Active';
            document.getElementById('hero-total-cost').textContent = formatCost(winner.totalScaledCost);
            document.getElementById('hero-scale-savings').textContent = formatCost(scaleSavingsDollars) + ' / mo';

            // Populate KPIs
            document.getElementById('stat-cheapest-num').textContent = formatCost(winner.totalScaledCost);
            document.getElementById('stat-cheapest-label').textContent = winner.model_name;
            document.getElementById('stat-avg-num').textContent = formatCost(avgCost);
            document.getElementById('stat-max-num').textContent = formatCost(maxOption.totalScaledCost);
            document.getElementById('stat-max-label').textContent = maxOption.model_name;
            document.getElementById('stat-savings-num').textContent = savingsPercent.toFixed(1) + '%';

            renderComparisonBars(filtered, winner);
            renderMatrixTable(filtered, winner);
        }

        // Render Comparison Bar Chart
        function renderComparisonBars(models, winner) {
            const listElem = document.getElementById('bar-chart-list');
            listElem.innerHTML = '';

            const sortedCheapest = [...models].sort((a, b) => a.totalScaledCost - b.totalScaledCost).slice(0, chartLimit);
            const maxCostInSlice = Math.max(...sortedCheapest.map(m => m.totalScaledCost), 0.00001);

            sortedCheapest.forEach((m, idx) => {
                const isWinner = idx === 0;
                const pct = Math.max((m.totalScaledCost / maxCostInSlice) * 100, 3);
                const multiplier = winner.totalScaledCost > 0 ? (m.totalScaledCost / winner.totalScaledCost) : 1;

                const row = document.createElement('div');
                row.className = 'bar-row';
                row.innerHTML = 
                    '<div class="bar-model-col">' +
                        '<span class="bar-rank-badge ' + (isWinner ? 'bar-rank-1' : '') + '">' + (idx + 1) + '</span>' +
                        getProviderTagHTML(m.provider) +
                        '<span class="bar-model-name" title="' + m.model_name + '">' + m.model_name + '</span>' +
                    '</div>' +
                    '<div class="bar-track">' +
                        '<div class="bar-fill ' + (isWinner ? 'winner' : '') + '" style="width: ' + pct + '%"></div>' +
                    '</div>' +
                    '<div class="bar-cost-col">' +
                        '<span class="bar-cost-val">' + formatCost(m.totalScaledCost) + '</span>' +
                        '<span class="bar-multiplier ' + (isWinner ? 'baseline' : '') + '">' +
                            (isWinner ? '1.0x (Optimal)' : multiplier.toFixed(1) + 'x cost') +
                        '</span>' +
                    '</div>';
                listElem.appendChild(row);
            });
        }

        // Render Matrix Table
        function renderMatrixTable(models, winner) {
            const tbody = document.getElementById('pricing-table-body');
            tbody.innerHTML = '';

            models.forEach((m, idx) => {
                const isWinner = m.model_id === winner.model_id;
                const tr = document.createElement('tr');
                tr.className = 'table-row ' + (isWinner ? 'row-winner' : '');

                tr.innerHTML = 
                    '<td><span class="bar-rank-badge ' + (idx === 0 ? 'bar-rank-1' : '') + '">' + (idx + 1) + '</span></td>' +
                    '<td><strong>' + m.model_name + '</strong></td>' +
                    '<td>' + getProviderTagHTML(m.provider) + '</td>' +
                    '<td>' + m.context_length + '</td>' +
                    '<td class="price-mono">$' + m.input_price.toFixed(4) + '</td>' +
                    '<td class="price-mono">$' + m.output_price.toFixed(4) + '</td>' +
                    '<td style="text-align: right;" class="cost-highlight">' + formatCost(m.totalScaledCost) + '</td>' +
                    '<td style="text-align: right;"><button class="btn-inspect" onclick="inspectModel(\\'' + m.model_id.replace(/'/g, "\\\\'") + '\\')">Inspect</button></td>';

                tbody.appendChild(tr);
            });
        }

        // Sort Table
        function handleTableSort(key) {
            if (currentSort.key === key) {
                currentSort.asc = !currentSort.asc;
            } else {
                currentSort.key = key;
                currentSort.asc = true;
            }

            document.querySelectorAll('table.pricing-table th span').forEach(s => s.textContent = '');
            const targetSpan = document.getElementById('th-sort-' + key) || document.getElementById('th-sort-' + key + '2');
            if (targetSpan) {
                targetSpan.textContent = currentSort.asc ? '▲' : '▼';
            }

            updateAllCalculations();
        }

        // Chart Limit Toggle
        function setChartLimit(limit) {
            chartLimit = limit;
            document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('btn-chart-' + limit)?.classList.add('active');
            updateAllCalculations();
        }

        // Workload Presets
        function applyPreset(inTokens, outTokens, chipElem) {
            document.getElementById('input-tokens').value = inTokens;
            document.getElementById('output-tokens').value = outTokens;
            document.querySelectorAll('.preset-chip').forEach(c => c.classList.remove('active'));
            if (chipElem) chipElem.classList.add('active');
            updateAllCalculations();
            triggerToast('Applied preset: ' + formatTokens(inTokens) + ' In / ' + formatTokens(outTokens) + ' Out');
        }

        // Provider Filter Pills
        function filterByProvider(provider, btnElem) {
            selectedProviderFilter = provider.toLowerCase();
            document.querySelectorAll('.provider-pill').forEach(p => p.classList.remove('active'));
            if (btnElem) btnElem.classList.add('active');
            updateAllCalculations();
        }

        // Inspect Model Drawer Modal
        function inspectModel(modelId) {
            const m = MODELS.find(x => x.model_id === modelId);
            if (!m) return;

            const modal = document.getElementById('inspect-modal');
            const target = document.getElementById('modal-content-target');

            const pySnippet = 
`from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="your_openrouter_api_key",
)

response = client.chat.completions.create(
    model="${m.model_id}",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)`;

            target.innerHTML = 
                '<div style="margin-bottom: 16px;">' +
                    getProviderTagHTML(m.provider) +
                    '<h3 style="font-size: 1.4rem; font-weight: 800; margin-top: 8px;">' + m.model_name + '</h3>' +
                    '<p style="font-size: 0.85rem; color: var(--text-muted); font-family: var(--font-mono);">' + m.model_id + '</p>' +
                '</div>' +
                '<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 16px 0;">' +
                    '<div style="background: var(--bg-secondary); padding: 12px; border-radius: 8px; border: 1px solid var(--card-border);">' +
                        '<div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase;">Context Window</div>' +
                        '<div style="font-size: 1.1rem; font-weight: 700;">' + m.context_length + '</div>' +
                    '</div>' +
                    '<div style="background: var(--bg-secondary); padding: 12px; border-radius: 8px; border: 1px solid var(--card-border);">' +
                        '<div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase;">Input / 1M</div>' +
                        '<div style="font-size: 1.1rem; font-weight: 700; color: var(--accent-primary);">$' + m.input_price.toFixed(4) + '</div>' +
                    '</div>' +
                    '<div style="background: var(--bg-secondary); padding: 12px; border-radius: 8px; border: 1px solid var(--card-border);">' +
                        '<div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase;">Output / 1M</div>' +
                        '<div style="font-size: 1.1rem; font-weight: 700; color: var(--accent-emerald);">$' + m.output_price.toFixed(4) + '</div>' +
                    '</div>' +
                '</div>' +
                '<div style="font-size: 0.85rem; font-weight: 700; color: var(--text-primary); margin-top: 16px;">OpenAI-Compatible Python Integration</div>' +
                '<div class="code-snippet-box">' +
                    '<button class="copy-snippet-btn" onclick="copySnippetText(this)">Copy</button>' +
                    '<pre style="margin: 0;">' + escapeHtml(pySnippet) + '</pre>' +
                '</div>' +
                '<div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 16px;">' +
                    '<a href="' + m.product_page_url + '" target="_blank" class="btn-secondary" style="text-decoration: none;">View on OpenRouter ↗</a>' +
                    '<button class="btn-secondary" onclick="closeInspectModal()">Close</button>' +
                '</div>';

            modal.classList.add('active');
        }

        function closeInspectModal() {
            document.getElementById('inspect-modal').classList.remove('active');
        }

        function escapeHtml(text) {
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }

        function copySnippetText(btn) {
            const pre = btn.parentElement.querySelector('pre');
            navigator.clipboard.writeText(pre.textContent).then(() => {
                btn.textContent = "Copied!";
                setTimeout(() => btn.textContent = "Copy", 1500);
            });
        }

        function openProofModal(src) {
            window.open(src, '_blank');
        }

        // Export Data
        function exportCSV() {
            if (!currentFilteredList || currentFilteredList.length === 0) return;
            let rows = ["Rank,Model Name,Provider,Context Window,Input Price (USD per 1M),Output Price (USD per 1M),Calculated Cost (USD)"];
            currentFilteredList.forEach((m, idx) => {
                rows.push([
                    idx + 1,
                    '"' + m.model_name.replace(/"/g, '""') + '"',
                    '"' + m.provider + '"',
                    '"' + m.context_length + '"',
                    m.input_price,
                    m.output_price,
                    m.totalScaledCost.toFixed(6)
                ].join(','));
            });

            downloadBlob(rows.join(String.fromCharCode(10)), 'text/csv;charset=utf-8;', 'ai_model_costs.csv');
            triggerToast('Exported CSV with ' + currentFilteredList.length + ' models');
        }

        function exportJSON() {
            if (!currentFilteredList || currentFilteredList.length === 0) return;
            const dataStr = JSON.stringify(currentFilteredList, null, 2);
            downloadBlob(dataStr, 'application/json;charset=utf-8;', 'ai_model_costs.json');
            triggerToast('Exported JSON dataset');
        }

        function downloadBlob(content, mimeType, filename) {
            const blob = new Blob([content], { type: mimeType });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }

        // Toast Messages
        function triggerToast(msg) {
            const shelf = document.getElementById('toast-shelf');
            if (!shelf) return;
            const toast = document.createElement('div');
            toast.className = 'toast-item';
            toast.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent-emerald)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg><span>' + msg + '</span>';
            shelf.appendChild(toast);
            setTimeout(() => {
                if (toast.parentNode) toast.parentNode.removeChild(toast);
            }, 2600);
        }

        // Setup Event Listeners
        window.addEventListener('DOMContentLoaded', () => {
            const inputs = ['input-tokens', 'output-tokens', 'search-filter'];
            inputs.forEach(id => {
                document.getElementById(id).addEventListener('input', () => {
                    clearTimeout(debounceTimer);
                    debounceTimer = setTimeout(() => updateAllCalculations(), 120);
                });
            });

            document.getElementById('context-select').addEventListener('change', () => updateAllCalculations());
            
            if (window.location.hash) {
                const h = window.location.hash.replace('#', '');
                if (['router', 'matrix', 'story'].includes(h)) {
                    switchTab(h);
                }
            }
            
            updateAllCalculations();
        });
    </script>
</body>
</html>
"""

html_final = html_template.replace("__JSON_DATA__", json_embed)

# Write to root index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_final)

# Write to final-submission/index.html
with open(os.path.join('final-submission', 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_final)

print("Successfully generated high-contrast enterprise index.html in root and final-submission!")
