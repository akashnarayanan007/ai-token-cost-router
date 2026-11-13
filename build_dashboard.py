import json, os

with open('openrouter_final.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# Filter models to only those with valid numeric input_price and output_price
cleaned_models = []
for m in raw_data:
    inp = m.get('input_price')
    outp = m.get('output_price')
    if inp and isinstance(inp, dict) and 'value' in inp and outp and isinstance(outp, dict) and 'value' in outp:
        try:
            inp_val = float(inp['value'])
            outp_val = float(outp['value'])
            
            # Helper to parse context length to integer tokens
            ctx_str = str(m.get('context_length', '0')).upper().strip()
            ctx_tokens = 0
            if 'M' in ctx_str:
                ctx_tokens = int(float(ctx_str.replace('M', '')) * 1_000_000)
            elif 'K' in ctx_str:
                ctx_tokens = int(float(ctx_str.replace('K', '')) * 1_000)
            elif ctx_str.isdigit():
                ctx_tokens = int(ctx_str)
                
            cleaned_models.append({
                'model_id': m.get('model_id', 'unknown'),
                'model_name': m.get('model_name', 'Unknown Model'),
                'context_length': m.get('context_length', 'N/A'),
                'context_tokens': ctx_tokens,
                'input_price': inp_val,
                'output_price': outp_val,
                'release_date': m.get('release_date', ''),
                'product_page_url': m.get('product_page_url', '#')
            })
        except (ValueError, TypeError):
            continue

print(f"Loaded {len(cleaned_models)} valid models")

json_embed = json.dumps(cleaned_models, indent=None)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Token Cost Router | LLM Price & Performance Optimizer</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --bg-dark: #090d16;
            --bg-card: rgba(18, 26, 43, 0.7);
            --bg-card-hover: rgba(26, 38, 64, 0.8);
            --border-color: rgba(255, 255, 255, 0.08);
            --border-glow: rgba(99, 102, 241, 0.3);
            
            --primary: #6366f1;
            --primary-light: #818cf8;
            --primary-glow: rgba(99, 102, 241, 0.4);
            
            --accent-emerald: #10b981;
            --accent-emerald-glow: rgba(16, 185, 129, 0.3);
            
            --accent-amber: #f59e0b;
            --accent-cyan: #06b6d4;
            --accent-purple: #a855f7;
            --accent-rose: #f43f5e;

            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
            
            --radius-lg: 16px;
            --radius-md: 12px;
            --radius-sm: 8px;
            --transition-fast: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-normal: 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            min-height: 100vh;
            line-height: 1.5;
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 85% 25%, rgba(16, 185, 129, 0.08) 0%, transparent 35%),
                radial-gradient(circle at 50% 80%, rgba(168, 85, 247, 0.08) 0%, transparent 45%);
            background-attachment: fixed;
            padding-bottom: 60px;
        }}

        .container {{
            max-width: 1280px;
            margin: 0 auto;
            padding: 0 24px;
        }}

        /* Header */
        header {{
            padding: 24px 0 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 32px;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .brand-icon {{
            width: 42px;
            height: 42px;
            background: linear-gradient(135deg, var(--primary), #a855f7);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 20px var(--primary-glow);
        }}

        .brand-icon svg {{
            width: 24px;
            height: 24px;
            fill: none;
            stroke: #fff;
            stroke-width: 2.2;
            stroke-linecap: round;
            stroke-linejoin: round;
        }}

        .brand-title {{
            font-size: 1.4rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #ffffff 30%, #a5b4fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .brand-subtitle {{
            font-size: 0.8rem;
            color: var(--text-muted);
            font-weight: 500;
        }}

        .header-badges {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.25);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 600;
            color: #34d399;
        }}

        .status-dot {{
            width: 8px;
            height: 8px;
            background-color: #34d399;
            border-radius: 50%;
            box-shadow: 0 0 10px #34d399;
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.5; transform: scale(0.85); }}
        }}

        /* Hero Section */
        .hero-card {{
            position: relative;
            background: linear-gradient(135deg, rgba(30, 41, 70, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
            border: 1px solid rgba(99, 102, 241, 0.35);
            border-radius: 24px;
            padding: 36px 40px;
            margin-bottom: 32px;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.1);
            overflow: hidden;
            backdrop-filter: blur(16px);
        }}

        .hero-card::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 450px;
            height: 450px;
            background: radial-gradient(circle, rgba(16, 185, 129, 0.15) 0%, rgba(99, 102, 241, 0.1) 40%, transparent 70%);
            pointer-events: none;
            z-index: 0;
        }}

        .hero-content {{
            position: relative;
            z-index: 1;
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 24px;
            align-items: center;
        }}

        .hero-label {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: #000;
            font-size: 0.75rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 4px 12px;
            border-radius: 20px;
            margin-bottom: 14px;
            box-shadow: 0 0 12px rgba(245, 158, 11, 0.4);
        }}

        .hero-model-title {{
            font-size: 2.2rem;
            font-weight: 800;
            color: #fff;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 14px;
            letter-spacing: -0.02em;
        }}

        .hero-meta {{
            display: flex;
            align-items: center;
            gap: 16px;
            color: var(--text-muted);
            font-size: 0.9rem;
        }}

        .hero-meta-item {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .hero-price-box {{
            text-align: right;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px 28px;
            border-radius: 18px;
            min-width: 260px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        }}

        .hero-price-label {{
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            font-weight: 600;
            margin-bottom: 4px;
        }}

        .hero-price-value {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 2.6rem;
            font-weight: 800;
            color: #34d399;
            text-shadow: 0 0 20px rgba(52, 211, 153, 0.4);
            line-height: 1.1;
        }}

        .hero-savings-tag {{
            margin-top: 6px;
            font-size: 0.8rem;
            color: #a7f3d0;
            font-weight: 600;
        }}

        /* Stats Row */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 32px;
        }}

        .stat-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 20px;
            backdrop-filter: blur(12px);
            transition: var(--transition-fast);
        }}

        .stat-card:hover {{
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }}

        .stat-title {{
            font-size: 0.78rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
            margin-bottom: 8px;
        }}

        .stat-value {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.5rem;
            font-weight: 700;
            color: #fff;
        }}

        .stat-sub {{
            font-size: 0.78rem;
            color: var(--text-dim);
            margin-top: 4px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        /* Calculator Controls Panel */
        .calculator-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 28px 32px;
            margin-bottom: 32px;
            backdrop-filter: blur(16px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
        }}

        .calc-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
        }}

        .calc-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .preset-buttons {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .preset-btn {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition-fast);
        }}

        .preset-btn:hover {{
            background: rgba(99, 102, 241, 0.15);
            border-color: var(--primary-light);
            color: #fff;
        }}

        .preset-btn.active {{
            background: var(--primary);
            border-color: var(--primary);
            color: #fff;
            box-shadow: 0 0 12px var(--primary-glow);
        }}

        .calc-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1.2fr;
            gap: 20px;
        }}

        .input-group {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .input-label {{
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
        }}

        .input-wrapper {{
            position: relative;
        }}

        .form-control {{
            width: 100%;
            background: rgba(10, 15, 26, 0.7);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 12px 16px;
            color: #fff;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.95rem;
            font-weight: 600;
            outline: none;
            transition: var(--transition-fast);
        }}

        .form-control:focus {{
            border-color: var(--primary-light);
            box-shadow: 0 0 0 3px var(--primary-glow);
        }}

        select.form-control {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            cursor: pointer;
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%94a3b8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 14px center;
            padding-right: 40px;
        }}

        select.form-control option {{
            background: #0f172a;
            color: #fff;
        }}

        .search-wrapper {{
            position: relative;
        }}

        .search-icon {{
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            width: 18px;
            height: 18px;
            stroke: var(--text-dim);
            fill: none;
            stroke-width: 2;
        }}

        .search-control {{
            padding-left: 42px;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}

        /* Chart Section */
        .chart-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 28px 32px;
            margin-bottom: 32px;
            backdrop-filter: blur(16px);
        }}

        .chart-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
        }}

        .chart-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #fff;
        }}

        .chart-controls {{
            display: flex;
            gap: 6px;
        }}

        .toggle-btn {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 4px 12px;
            border-radius: var(--radius-sm);
            font-size: 0.75rem;
            font-weight: 600;
            cursor: pointer;
        }}

        .toggle-btn.active {{
            background: rgba(99, 102, 241, 0.2);
            border-color: var(--primary-light);
            color: #fff;
        }}

        .bar-chart-list {{
            display: flex;
            flex-direction: column;
            gap: 14px;
        }}

        .chart-item {{
            display: grid;
            grid-template-columns: 240px 1fr 110px;
            align-items: center;
            gap: 16px;
        }}

        .chart-model-info {{
            display: flex;
            align-items: center;
            gap: 8px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .chart-model-name {{
            font-size: 0.88rem;
            font-weight: 600;
            color: var(--text-main);
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .bar-track {{
            background: rgba(255, 255, 255, 0.04);
            border-radius: 8px;
            height: 28px;
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            padding: 0 10px;
        }}

        .bar-fill {{
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            background: linear-gradient(90deg, var(--primary), #818cf8);
            border-radius: 8px;
            width: 0%;
            transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 0 12px rgba(99, 102, 241, 0.3);
        }}

        .bar-fill.rank-1 {{
            background: linear-gradient(90deg, #10b981, #34d399);
            box-shadow: 0 0 12px rgba(16, 185, 129, 0.4);
        }}

        .chart-cost {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.88rem;
            font-weight: 700;
            text-align: right;
            color: #fff;
        }}

        /* Table Section */
        .table-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 24px;
            backdrop-filter: blur(16px);
            overflow: hidden;
        }}

        .table-wrapper {{
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}

        th {{
            padding: 14px 16px;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-muted);
            font-weight: 700;
            border-bottom: 1px solid var(--border-color);
            cursor: pointer;
            user-select: none;
            transition: var(--transition-fast);
        }}

        th:hover {{
            color: #fff;
            background: rgba(255, 255, 255, 0.02);
        }}

        th .sort-icon {{
            display: inline-block;
            margin-left: 4px;
            opacity: 0.4;
        }}

        th.active-sort .sort-icon {{
            opacity: 1;
            color: var(--primary-light);
        }}

        td {{
            padding: 16px;
            font-size: 0.9rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            transition: var(--transition-fast);
        }}

        tr.table-row {{
            transition: background var(--transition-fast), transform var(--transition-fast);
        }}

        tr.table-row:hover {{
            background: var(--bg-card-hover);
        }}

        tr.rank-1-row {{
            background: rgba(16, 185, 129, 0.05);
        }}

        .rank-badge {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.82rem;
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-muted);
        }}

        .rank-1-row .rank-badge {{
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: #000;
            box-shadow: 0 0 10px rgba(245, 158, 11, 0.4);
        }}

        /* Provider Badges */
        .provider-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 14px;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            border: 1px solid transparent;
            white-space: nowrap;
        }}

        .badge-openai {{ background: rgba(16, 163, 127, 0.15); color: #34d399; border-color: rgba(16, 163, 127, 0.3); }}
        .badge-anthropic {{ background: rgba(217, 119, 6, 0.15); color: #fbbf24; border-color: rgba(217, 119, 6, 0.3); }}
        .badge-google {{ background: rgba(59, 130, 246, 0.15); color: #60a5fa; border-color: rgba(59, 130, 246, 0.3); }}
        .badge-deepseek {{ background: rgba(2, 132, 199, 0.15); color: #38bdf8; border-color: rgba(2, 132, 199, 0.3); }}
        .badge-qwen {{ background: rgba(139, 92, 246, 0.15); color: #c084fc; border-color: rgba(139, 92, 246, 0.3); }}
        .badge-meta {{ background: rgba(6, 182, 212, 0.15); color: #22d3ee; border-color: rgba(6, 182, 212, 0.3); }}
        .badge-mistralai {{ background: rgba(244, 63, 94, 0.15); color: #fb7185; border-color: rgba(244, 63, 94, 0.3); }}
        .badge-nvidia {{ background: rgba(132, 204, 22, 0.15); color: #a3e635; border-color: rgba(132, 204, 22, 0.3); }}
        .badge-default {{ background: rgba(100, 116, 139, 0.15); color: #cbd5e1; border-color: rgba(100, 116, 139, 0.3); }}

        .model-cell {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}

        .model-link {{
            color: #fff;
            font-weight: 600;
            text-decoration: none;
            transition: var(--transition-fast);
        }}

        .model-link:hover {{
            color: var(--primary-light);
        }}

        .price-val {{
            font-family: 'JetBrains Mono', monospace;
            font-weight: 500;
            color: var(--text-muted);
        }}

        .total-cost-val {{
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            color: #34d399;
            font-size: 0.95rem;
        }}

        /* Empty State */
        .empty-state {{
            padding: 60px 20px;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}

        .empty-icon {{
            width: 64px;
            height: 64px;
            background: rgba(255, 255, 255, 0.04);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 16px;
            color: var(--text-dim);
        }}

        .empty-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 8px;
        }}

        .empty-desc {{
            font-size: 0.88rem;
            color: var(--text-muted);
            max-width: 400px;
            margin-bottom: 20px;
        }}

        .reset-btn {{
            background: var(--primary);
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: var(--radius-md);
            font-size: 0.88rem;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition-fast);
        }}

        .reset-btn:hover {{
            background: var(--primary-light);
            box-shadow: 0 0 16px var(--primary-glow);
        }}

        /* Fade/Slide animation for table */
        .fade-in {{
            animation: fadeIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Responsive Design */
        @media (max-width: 1024px) {{
            .calc-grid {{ grid-template-columns: 1fr 1fr; }}
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .hero-content {{ grid-template-columns: 1fr; }}
            .hero-price-box {{ text-align: left; }}
        }}

        @media (max-width: 640px) {{
            .calc-grid {{ grid-template-columns: 1fr; }}
            .stats-grid {{ grid-template-columns: 1fr; }}
            .chart-item {{ grid-template-columns: 140px 1fr 80px; }}
            .hero-card {{ padding: 24px; }}
            .hero-model-title {{ font-size: 1.6rem; }}
        }}
    </style>
</head>
<body>

    <div class="container">
        <!-- Header -->
        <header>
            <div class="brand">
                <div class="brand-icon">
                    <svg viewBox="0 0 24 24">
                        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                    </svg>
                </div>
                <div>
                    <h1 class="brand-title">AI Token Cost Router</h1>
                    <div class="brand-subtitle">Smart LLM Price & Performance Optimizer</div>
                </div>
            </div>
            <div class="header-badges">
                <div class="status-badge">
                    <div class="status-dot"></div>
                    <span id="model-count-badge">388 Models Active</span>
                </div>
            </div>
        </header>

        <!-- Hero Section: #1 Winner -->
        <section class="hero-card" id="hero-winner-card">
            <div class="hero-content">
                <div>
                    <div class="hero-label">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                        Optimal Cost Router Winner
                    </div>
                    <h2 class="hero-model-title" id="hero-model-name">Loading...</h2>
                    <div class="hero-meta">
                        <span id="hero-provider-badge"></span>
                        <div class="hero-meta-item">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg>
                            Context Window: <strong id="hero-context" style="color: #fff; margin-left: 4px;">-</strong>
                        </div>
                        <div class="hero-meta-item">
                            Input: <strong id="hero-input-price" style="color: #fff; margin-left: 4px;">-</strong>
                        </div>
                        <div class="hero-meta-item">
                            Output: <strong id="hero-output-price" style="color: #fff; margin-left: 4px;">-</strong>
                        </div>
                    </div>
                </div>
                <div class="hero-price-box">
                    <div class="hero-price-label">Estimated Total Cost</div>
                    <div class="hero-price-value" id="hero-total-price">$0.0000</div>
                    <div class="hero-savings-tag" id="hero-savings-tag">⚡ Lowest cost route for your payload</div>
                </div>
            </div>
        </section>

        <!-- Stats Overview Row -->
        <section class="stats-grid">
            <div class="stat-card">
                <div class="stat-title">Cheapest Option</div>
                <div class="stat-value" id="stat-cheapest">$0.0000</div>
                <div class="stat-sub" id="stat-cheapest-name">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Average Cost</div>
                <div class="stat-value" id="stat-avg">$0.0000</div>
                <div class="stat-sub">Across matching models</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Max Cost Option</div>
                <div class="stat-value" id="stat-max">$0.0000</div>
                <div class="stat-sub" id="stat-max-name">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Max Savings %</div>
                <div class="stat-value" style="color: #34d399;" id="stat-savings">0.0%</div>
                <div class="stat-sub">vs Most Expensive Model</div>
            </div>
        </section>

        <!-- Calculator Panel -->
        <section class="calculator-card">
            <div class="calc-header">
                <div class="calc-title">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary-light)" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2"></rect><line x1="8" y1="6" x2="16" y2="6"></line><line x1="16" y1="14" x2="16" y2="18"></line><path d="M16 10h.01"></path><path d="M12 10h.01"></path><path d="M8 10h.01"></path><path d="M12 14h.01"></path><path d="M8 14h.01"></path><path d="M12 18h.01"></path><path d="M8 18h.01"></path></svg>
                    Token Calculator & Filters
                </div>
                <div class="preset-buttons">
                    <span style="font-size: 0.78rem; color: var(--text-dim); align-self: center; font-weight: 600;">Workloads:</span>
                    <button class="preset-btn active" onclick="applyPreset(100000, 20000, this)">100k In / 20k Out</button>
                    <button class="preset-btn" onclick="applyPreset(10000, 2000, this)">Short Chat (10k/2k)</button>
                    <button class="preset-btn" onclick="applyPreset(500000, 50000, this)">RAG / Code (500k/50k)</button>
                    <button class="preset-btn" onclick="applyPreset(1000000, 100000, this)">Deep LLM (1M/100k)</button>
                </div>
            </div>
            
            <div class="calc-grid">
                <div class="input-group">
                    <div class="input-label">
                        <span>Expected Input Tokens</span>
                        <span id="input-tokens-formatted" style="color: var(--primary-light);">100,000</span>
                    </div>
                    <input type="number" id="input-tokens-input" class="form-control" value="100000" min="0" step="1000">
                </div>
                
                <div class="input-group">
                    <div class="input-label">
                        <span>Expected Output Tokens</span>
                        <span id="output-tokens-formatted" style="color: var(--primary-light);">20,000</span>
                    </div>
                    <input type="number" id="output-tokens-input" class="form-control" value="20000" min="0" step="1000">
                </div>

                <div class="input-group">
                    <div class="input-label">Min Context Window</div>
                    <select id="context-filter" class="form-control">
                        <option value="0">Any Window</option>
                        <option value="8000">8K+ Tokens</option>
                        <option value="32000">32K+ Tokens</option>
                        <option value="128000">128K+ Tokens</option>
                        <option value="256000">256K+ Tokens</option>
                        <option value="1000000">1M+ Tokens</option>
                    </select>
                </div>

                <div class="input-group">
                    <div class="input-label">Search Model / Provider</div>
                    <div class="search-wrapper">
                        <svg class="search-icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                        <input type="text" id="search-input" class="form-control search-control" placeholder="Search e.g. OpenAI, Claude, Flash...">
                    </div>
                </div>
            </div>
        </section>

        <!-- Top 5-8 Comparison Chart -->
        <section class="chart-card">
            <div class="chart-header">
                <div class="chart-title">Cheapest Models Comparison</div>
                <div class="chart-controls">
                    <button class="toggle-btn active" id="btn-top-5" onclick="setChartTopLimit(5)">Top 5</button>
                    <button class="toggle-btn" id="btn-top-8" onclick="setChartTopLimit(8)">Top 8</button>
                </div>
            </div>
            <div class="bar-chart-list" id="bar-chart-container">
                <!-- Bar elements inserted via JS -->
            </div>
        </section>

        <!-- Sortable Models Table -->
        <section class="table-card">
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th style="width: 70px;" onclick="sortTable('cost')">Rank <span class="sort-icon" id="sort-cost">▲</span></th>
                            <th onclick="sortTable('name')">Model Name <span class="sort-icon" id="sort-name"></span></th>
                            <th onclick="sortTable('provider')">Provider <span class="sort-icon" id="sort-provider"></span></th>
                            <th onclick="sortTable('context')">Context Window <span class="sort-icon" id="sort-context"></span></th>
                            <th onclick="sortTable('input_price')">Input / 1M <span class="sort-icon" id="sort-input_price"></span></th>
                            <th onclick="sortTable('output_price')">Output / 1M <span class="sort-icon" id="sort-output_price"></span></th>
                            <th style="text-align: right;" onclick="sortTable('cost')">Estimated Total Cost <span class="sort-icon" id="sort-cost-2"></span></th>
                        </tr>
                    </thead>
                    <tbody id="models-table-body">
                        <!-- Rows injected via JS -->
                    </tbody>
                </table>
            </div>

            <div id="empty-state-container" style="display: none;">
                <div class="empty-state">
                    <div class="empty-icon">
                        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg>
                    </div>
                    <div class="empty-title">No matching models found</div>
                    <div class="empty-desc">Try loosening your search query or minimum context window filter.</div>
                    <button class="reset-btn" onclick="resetFilters()">Reset All Filters</button>
                </div>
            </div>
        </section>
    </div>

    <!-- Inline Raw JSON Data -->
    <script id="models-data" type="application/json">
{json_embed}
    </script>

    <!-- Application Script -->
    <script>
        // Store parsed model data
        const RAW_MODELS = JSON.parse(document.getElementById('models-data').textContent);
        
        let chartTopLimit = 5;
        let currentSort = {{ key: 'cost', asc: true }};
        let debounceTimer = null;

        // Current Animated Counter Values
        let currentAnimatedValues = {{
            hero: 0,
            cheapest: 0,
            avg: 0,
            max: 0,
            savings: 0
        }};

        // Helper to format currency
        function formatCurrency(val) {{
            if (val === 0) return "$0.0000";
            if (val < 0.001) return "$" + val.toFixed(5);
            if (val < 0.01) return "$" + val.toFixed(4);
            if (val < 1) return "$" + val.toFixed(4);
            return "$" + val.toLocaleString(undefined, {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
        }}

        // Format raw token numbers
        function formatTokenCount(num) {{
            return num.toLocaleString();
        }}

        // Helper for Provider Badge HTML
        function getProviderBadgeHTML(providerId) {{
            const p = (providerId || 'default').toLowerCase();
            let badgeClass = 'badge-default';
            
            if (p.includes('openai')) badgeClass = 'badge-openai';
            else if (p.includes('anthropic')) badgeClass = 'badge-anthropic';
            else if (p.includes('google')) badgeClass = 'badge-google';
            else if (p.includes('deepseek')) badgeClass = 'badge-deepseek';
            else if (p.includes('qwen')) badgeClass = 'badge-qwen';
            else if (p.includes('meta')) badgeClass = 'badge-meta';
            else if (p.includes('mistral')) badgeClass = 'badge-mistralai';
            else if (p.includes('nvidia')) badgeClass = 'badge-nvidia';

            return `<span class="provider-badge ${{badgeClass}}">${{providerId}}</span>`;
        }}

        // Calculate Cost for single model
        function calculateCost(model, inputTokens, outputTokens) {{
            const inputCost = (inputTokens / 1000000) * model.input_price;
            const outputCost = (outputTokens / 1000000) * model.output_price;
            return inputCost + outputCost;
        }}

        // Smooth Counter Animation Function
        function animateNumber(elementId, startVal, endVal, isPercent = false, duration = 600) {{
            const elem = document.getElementById(elementId);
            if (!elem) return;

            const startTime = performance.now();

            function update(now) {{
                const elapsed = now - startTime;
                const progress = Math.min(elapsed / duration, 1);
                // Ease out quad
                const easeProgress = progress * (2 - progress);
                const currentVal = startVal + (endVal - startVal) * easeProgress;

                if (isPercent) {{
                    elem.textContent = currentVal.toFixed(1) + "%";
                }} else {{
                    elem.textContent = formatCurrency(currentVal);
                }}

                if (progress < 1) {{
                    requestAnimationFrame(update);
                }} else {{
                    // Update state store
                    currentAnimatedValues[elementId] = endVal;
                }}
            }}

            requestAnimationFrame(update);
        }}

        // Update all UI elements
        function updateDashboard() {{
            const inputTokens = parseFloat(document.getElementById('input-tokens-input').value) || 0;
            const outputTokens = parseFloat(document.getElementById('output-tokens-input').value) || 0;
            const minContext = parseInt(document.getElementById('context-filter').value) || 0;
            const searchQuery = document.getElementById('search-input').value.toLowerCase().trim();

            // Update token formatted text labels
            document.getElementById('input-tokens-formatted').textContent = formatTokenCount(inputTokens);
            document.getElementById('output-tokens-formatted').textContent = formatTokenCount(outputTokens);

            // Filter models
            let filtered = RAW_MODELS.filter(m => {{
                if (m.context_tokens < minContext) return false;
                if (searchQuery) {{
                    const mName = (m.model_name || '').toLowerCase();
                    const mProv = (m.model_id || '').toLowerCase();
                    if (!mName.includes(searchQuery) && !mProv.includes(searchQuery)) return false;
                }}
                return true;
            }});

            // Compute total cost for each model
            filtered.forEach(m => {{
                m.computedCost = calculateCost(m, inputTokens, outputTokens);
            }});

            // Sort models
            filtered.sort((a, b) => {{
                let valA, valB;
                if (currentSort.key === 'cost') {{ valA = a.computedCost; valB = b.computedCost; }}
                else if (currentSort.key === 'name') {{ valA = a.model_name; valB = b.model_name; }}
                else if (currentSort.key === 'provider') {{ valA = a.model_id; valB = b.model_id; }}
                else if (currentSort.key === 'context') {{ valA = a.context_tokens; valB = b.context_tokens; }}
                else if (currentSort.key === 'input_price') {{ valA = a.input_price; valB = b.input_price; }}
                else if (currentSort.key === 'output_price') {{ valA = a.output_price; valB = b.output_price; }}

                if (valA < valB) return currentSort.asc ? -1 : 1;
                if (valA > valB) return currentSort.asc ? 1 : -1;
                return 0;
            }});

            // Update badge count
            document.getElementById('model-count-badge').textContent = `${{filtered.length}} Models Active`;

            if (filtered.length === 0) {{
                document.getElementById('hero-winner-card').style.display = 'none';
                document.querySelector('.stats-grid').style.display = 'none';
                document.querySelector('.chart-card').style.display = 'none';
                document.querySelector('table').style.display = 'none';
                document.getElementById('empty-state-container').style.display = 'block';
                return;
            }}

            document.getElementById('hero-winner-card').style.display = 'block';
            document.querySelector('.stats-grid').style.display = 'grid';
            document.querySelector('.chart-card').style.display = 'block';
            document.querySelector('table').style.display = 'table';
            document.getElementById('empty-state-container').style.display = 'none';

            // Find absolute cheapest model among filtered
            const cheapestModel = [...filtered].sort((a, b) => a.computedCost - b.computedCost)[0];
            const maxModel = [...filtered].sort((a, b) => b.computedCost - a.computedCost)[0];
            
            const totalCostSum = filtered.reduce((acc, m) => acc + m.computedCost, 0);
            const avgCost = totalCostSum / filtered.length;

            const savingsPct = maxModel.computedCost > 0 ? 
                ((maxModel.computedCost - cheapestModel.computedCost) / maxModel.computedCost) * 100 : 0;

            // Update Hero Card
            document.getElementById('hero-model-name').textContent = cheapestModel.model_name;
            document.getElementById('hero-provider-badge').innerHTML = getProviderBadgeHTML(cheapestModel.model_id);
            document.getElementById('hero-context').textContent = cheapestModel.context_length;
            document.getElementById('hero-input-price').textContent = `$${{cheapestModel.input_price}} / 1M`;
            document.getElementById('hero-output-price').textContent = `$${{cheapestModel.output_price}} / 1M`;

            animateNumber('hero-total-price', currentAnimatedValues.hero || 0, cheapestModel.computedCost);
            currentAnimatedValues.hero = cheapestModel.computedCost;

            // Update Stats
            animateNumber('stat-cheapest', currentAnimatedValues.cheapest || 0, cheapestModel.computedCost);
            currentAnimatedValues.cheapest = cheapestModel.computedCost;
            document.getElementById('stat-cheapest-name').textContent = cheapestModel.model_name;

            animateNumber('stat-avg', currentAnimatedValues.avg || 0, avgCost);
            currentAnimatedValues.avg = avgCost;

            animateNumber('stat-max', currentAnimatedValues.max || 0, maxModel.computedCost);
            currentAnimatedValues.max = maxModel.computedCost;
            document.getElementById('stat-max-name').textContent = maxModel.model_name;

            animateNumber('stat-savings', currentAnimatedValues.savings || 0, savingsPct, true);
            currentAnimatedValues.savings = savingsPct;

            // Update Top Comparison Chart (sorted by cost)
            renderChart(filtered);

            // Update Table
            renderTable(filtered);
        }}

        // Render Bar Chart
        function renderChart(models) {{
            const container = document.getElementById('bar-chart-container');
            container.innerHTML = '';

            const topModels = [...models].sort((a, b) => a.computedCost - b.computedCost).slice(0, chartTopLimit);
            const maxCostInTop = Math.max(...topModels.map(m => m.computedCost), 0.000001);

            topModels.forEach((m, idx) => {{
                const pct = (m.computedCost / maxCostInTop) * 100;
                const isRank1 = idx === 0;

                const item = document.createElement('div');
                item.className = 'chart-item';
                item.innerHTML = `
                    <div class="chart-model-info">
                        ${{getProviderBadgeHTML(m.model_id)}}
                        <span class="chart-model-name" title="${{m.model_name}}">${{m.model_name}}</span>
                    </div>
                    <div class="bar-track">
                        <div class="bar-fill ${{isRank1 ? 'rank-1' : ''}}" style="width: 0%"></div>
                    </div>
                    <div class="chart-cost">${{formatCurrency(m.computedCost)}}</div>
                `;

                container.appendChild(item);

                // Trigger width animation in next frame
                setTimeout(() => {{
                    const barFill = item.querySelector('.bar-fill');
                    if (barFill) barFill.style.width = Math.max(pct, 2) + '%';
                }}, 50);
            }});
        }}

        // Render Sortable Table
        function renderTable(models) {{
            const tbody = document.getElementById('models-table-body');
            tbody.innerHTML = '';

            models.forEach((m, idx) => {{
                const row = document.createElement('tr');
                row.className = `table-row fade-in ${{idx === 0 && currentSort.key === 'cost' && currentSort.asc ? 'rank-1-row' : ''}}`;
                
                row.innerHTML = `
                    <td>
                        <span class="rank-badge">${{idx + 1}}</span>
                    </td>
                    <td>
                        <div class="model-cell">
                            <a href="${{m.product_page_url}}" target="_blank" class="model-link">${{m.model_name}}</a>
                        </div>
                    </td>
                    <td>${{getProviderBadgeHTML(m.model_id)}}</td>
                    <td><strong style="color: var(--text-main);">${{m.context_length}}</strong></td>
                    <td class="price-val">$${{m.input_price.toFixed(4)}}</td>
                    <td class="price-val">$${{m.output_price.toFixed(4)}}</td>
                    <td style="text-align: right;" class="total-cost-val">${{formatCurrency(m.computedCost)}}</td>
                `;

                tbody.appendChild(row);
            }});
        }}

        // Sort table handler
        function sortTable(key) {{
            if (currentSort.key === key) {{
                currentSort.asc = !currentSort.asc;
            }} else {{
                currentSort.key = key;
                currentSort.asc = true;
            }}

            // Update UI sort icons
            document.querySelectorAll('th').forEach(th => th.classList.remove('active-sort'));
            document.querySelectorAll('.sort-icon').forEach(span => span.textContent = '');

            const targetTh = document.getElementById(`sort-${{key}}`) || document.getElementById(`sort-${{key}}-2`);
            if (targetTh) {{
                targetTh.parentElement.classList.add('active-sort');
                targetTh.textContent = currentSort.asc ? '▲' : '▼';
            }}

            updateDashboard();
        }}

        // Chart Top Limit toggle
        function setChartTopLimit(limit) {{
            chartTopLimit = limit;
            document.getElementById('btn-top-5').classList.toggle('active', limit === 5);
            document.getElementById('btn-top-8').classList.toggle('active', limit === 8);
            updateDashboard();
        }}

        // Preset workload handlers
        function applyPreset(inputVal, outputVal, btnElem) {{
            document.getElementById('input-tokens-input').value = inputVal;
            document.getElementById('output-tokens-input').value = outputVal;

            document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
            if (btnElem) btnElem.classList.add('active');

            updateDashboard();
        }}

        // Reset Filters
        function resetFilters() {{
            document.getElementById('input-tokens-input').value = 100000;
            document.getElementById('output-tokens-input').value = 20000;
            document.getElementById('context-filter').value = 0;
            document.getElementById('search-input').value = '';
            currentSort = {{ key: 'cost', asc: true }};
            updateDashboard();
        }}

        // Debounced Event Listener setup
        function setupEventListeners() {{
            const inputs = ['input-tokens-input', 'output-tokens-input', 'search-input'];
            
            inputs.forEach(id => {{
                document.getElementById(id).addEventListener('input', () => {{
                    clearTimeout(debounceTimer);
                    debounceTimer = setTimeout(updateDashboard, 150);
                }});
            }});

            document.getElementById('context-filter').addEventListener('change', updateDashboard);
        }}

        // Initialize on load
        window.addEventListener('DOMContentLoaded', () => {{
            setupEventListeners();
            updateDashboard();
        }});
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Successfully generated index.html!")
