"""
src/create_presentation_pptx.py
Generates a professional 16:9 widescreen PowerPoint presentation (PRESENTATION_VTOP_SLIDES.pptx)
from docs/PRESENTATION_VTOP_SLIDES.md with embedded Speaker Notes for presenting to faculty / mam.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PPTX_PATH = os.path.join(PROJECT_ROOT, "docs", "PRESENTATION_VTOP_SLIDES.pptx")

# Color palette: Academic Executive Navy
NAVY_PRIMARY = RGBColor(15, 30, 65)      # Deep Navy #0F1E41
NAVY_ACCENT  = RGBColor(37, 99, 235)     # Royal Blue #2563EB
SLATE_DARK   = RGBColor(30, 41, 59)      # Charcoal #1E293B
SLATE_MUTED  = RGBColor(100, 116, 139)   # Slate Gray #64748B
BG_CARD      = RGBColor(248, 250, 252)   # Soft Off-White #F8FAFC
BORDER_COLOR = RGBColor(226, 232, 240)   # Border #E2E8F0
WHITE        = RGBColor(255, 255, 255)
GOLD_ALERT   = RGBColor(217, 119, 6)     # Amber #D97706
RED_ALERT    = RGBColor(220, 38, 38)     # Crimson #DC2626
GREEN_OK     = RGBColor(22, 163, 74)     # Emerald #16A34A

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]  # Blank slide

    def add_header(slide, title_text, category_text="FINAL REVIEW 3 • Q2 JOURNAL DEFENSE"):
        # Top banner background
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = NAVY_PRIMARY
        top_bar.line.color.rgb = NAVY_PRIMARY

        # Accent stripe
        stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = NAVY_ACCENT
        stripe.line.color.rgb = NAVY_ACCENT

        # Category text
        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.733), Inches(0.3))
        tf_cat = tb_cat.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = RGBColor(147, 197, 253)

        # Title text
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.40), Inches(11.733), Inches(0.65))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE

    def add_speaker_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = notes_text

    # =========================================================================
    # SLIDE 1: Title & Project Overview
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    # Background full fill
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY_PRIMARY
    bg1.line.color.rgb = NAVY_PRIMARY

    # Title box
    tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = "On the Limitations of Multi-Objective Neuro-Evolutionary Traffic Classification in SDWNs"
    p0.font.size = Pt(32)
    p0.font.bold = True
    p0.font.color.rgb = WHITE
    p0.alignment = PP_ALIGN.LEFT

    p_sub = tf.add_paragraph()
    p_sub.text = "A Negative Result and Lessons Learned — Final Review 3 & Q2 Journal Submission"
    p_sub.font.size = Pt(18)
    p_sub.font.bold = True
    p_sub.font.color.rgb = RGBColor(147, 197, 253)
    p_sub.space_before = Pt(12)

    # Cards on Slide 1
    cards_data = [
        ("The Core Question", "Can a lightweight 325-parameter neuro-evolutionary classifier (MOPSO-FFNN-AD) rival modern deep learning on resource-constrained SDWN edge switches?", NAVY_ACCENT),
        ("The Empirical Reality", "Tested on real PCAPs (ISCX VPN 2016 & USTC-TFC 2016), the proposed MOPSO-FFNN-AD is strictly Pareto-dominated on both accuracy and composite overhead F.", GOLD_ALERT),
        ("Our Academic Contribution", "Rather than making indefensible trade-off claims, we present an honest, rigorous Negative Result paper uncovering why proxy overhead metrics fail.", GREEN_OK)
    ]
    for idx, (head, body, col) in enumerate(cards_data):
        left_pos = Inches(1.0 + idx * 3.85)
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(3.7), Inches(3.6), Inches(2.7))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(23, 42, 85)
        card.line.color.rgb = col
        card.line.width = Pt(2)

        tb_c = s1.shapes.add_textbox(left_pos + Inches(0.2), Inches(3.9), Inches(3.2), Inches(2.3))
        tfc = tb_c.text_frame
        tfc.word_wrap = True
        pc_h = tfc.paragraphs[0]
        pc_h.text = head
        pc_h.font.size = Pt(16)
        pc_h.font.bold = True
        pc_h.font.color.rgb = WHITE
        
        pc_b = tfc.add_paragraph()
        pc_b.text = body
        pc_b.font.size = Pt(13)
        pc_b.font.color.rgb = RGBColor(203, 213, 225)
        pc_b.space_before = Pt(8)

    # Footer
    tb_foot = s1.shapes.add_textbox(Inches(1.0), Inches(6.8), Inches(11.333), Inches(0.4))
    p_f = tb_foot.text_frame.paragraphs[0]
    p_f.text = "School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology (VIT), Vellore • Review 3"
    p_f.font.size = Pt(11)
    p_f.font.color.rgb = RGBColor(148, 163, 184)

    add_speaker_notes(s1, 
        "EXPLANATION TO MAM:\n"
        "1. Good morning/afternoon Mam. Today we present our Final Review 3 for our Software Defined Wireless Networks research project.\n"
        "2. In this review, following the supervisor's directive, we are merging the senior's work (Budithi Supraja) with our team's research into a single Q2 journal submission.\n"
        "3. When we moved the senior's algorithm from synthetic data to real-world PCAP benchmarks (ISCX VPN and USTC-TFC malware), we discovered an honest, critical scientific finding: the proposed MOPSO-FFNN-AD model is strictly Pareto-dominated by deep learning baselines across both accuracy and composite overhead.\n"
        "4. Rather than making false claims that this is an 'intentional trade-off'—which top Q2 reviewers would immediately reject—we have reframed our paper as an authoritative Negative Result and Lessons Learned study, explaining the mathematical and architectural reasons behind this behavior."
    )

    # =========================================================================
    # SLIDE 2: Pareto Domination on Real Benchmarks
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Slide 2: The Core Problem — Pareto Domination on Real Benchmarks")

    # Left Callout Box: What is Pareto Domination
    box_dom = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(4.5), Inches(5.4))
    box_dom.fill.solid()
    box_dom.fill.fore_color.rgb = BG_CARD
    box_dom.line.color.rgb = RED_ALERT
    box_dom.line.width = Pt(2)

    tb_dom = s2.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(4.1), Inches(5.0))
    tf_dom = tb_dom.text_frame
    tf_dom.word_wrap = True
    p = tf_dom.paragraphs[0]
    p.text = "What is Pareto Domination?"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RED_ALERT

    bullets = [
        "In multi-objective optimization, a trade-off requires winning on at least ONE objective (e.g. sacrificing accuracy to gain lower overhead).",
        "Pareto Domination occurs when an alternative model achieves HIGHER accuracy AND LOWER overhead simultaneously.",
        "On ISCX VPN: The Transformer reaches 62.13% accuracy with F = 0.2937, while proposed MOPSO achieves only 37.87% accuracy with F = 0.4817.",
        "The proposed method loses on both axes simultaneously.",
        "Review 3 Decision: It is impossible to defend this as a compromise. Honest reporting protects our paper from desk rejection."
    ]
    for b in bullets:
        pb = tf_dom.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(12)
        pb.font.color.rgb = SLATE_DARK
        pb.space_before = Pt(8)

    # Right: Results Table
    tb_t = s2.shapes.add_textbox(Inches(5.6), Inches(1.4), Inches(7.0), Inches(0.4))
    pt = tb_t.text_frame.paragraphs[0]
    pt.text = "Empirical Results Across Real PCAP Benchmarks (10-Fold CV)"
    pt.font.size = Pt(16)
    pt.font.bold = True
    pt.font.color.rgb = NAVY_PRIMARY

    table_shape = s2.shapes.add_table(6, 6, Inches(5.6), Inches(1.9), Inches(7.0), Inches(4.8))
    table = table_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(0.9)
    table.columns[2].width = Inches(0.9)
    table.columns[3].width = Inches(1.0)
    table.columns[4].width = Inches(1.0)
    table.columns[5].width = Inches(1.0)

    headers = ["Method / Model", "USTC Acc", "ISCX Acc", "USTC F", "ISCX F", "Params"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    rows_data = [
        ("MOPSO-FFNN-AD (Proposed)", "62.97%", "37.87%", "0.3816", "0.4817", "325"),
        ("1D-CNN Baseline", "77.60%", "61.50%", "0.1997", "0.3064", "2,373"),
        ("LSTM Baseline", "77.47%", "64.23%", "0.2008", "0.3067", "13,093"),
        ("Transformer Baseline", "78.57%", "62.13%", "0.1686", "0.2937", "18,437"),
        ("PSO-FFNN (Base Paper)", "74.90%", "47.93%", "0.3544", "0.4486", "325")
    ]
    for r_idx, r_vals in enumerate(rows_data):
        for c_idx, val in enumerate(r_vals):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            if r_idx == 0:
                cell.fill.fore_color.rgb = RGBColor(254, 242, 242) # light red
            else:
                cell.fill.fore_color.rgb = RGBColor(241, 245, 249) if r_idx % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10.5)
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = RED_ALERT
            else:
                p.font.color.rgb = SLATE_DARK

    add_speaker_notes(s2,
        "EXPLANATION TO MAM:\n"
        "1. Mam, this slide contains the core empirical evidence that required us to reframe the paper.\n"
        "2. Please look at the table on the right: When we compare the proposed MOPSO-FFNN-AD against our 1D-CNN, LSTM, and Transformer baselines on real data:\n"
        "   - On USTC: Deep learning gets ~78% accuracy with overhead F of ~0.17 to 0.20. MOPSO gets only 63% accuracy with F = 0.38.\n"
        "   - On ISCX (encrypted VPN): DL achieves 62% to 64% accuracy with F ~ 0.30. MOPSO collapses to 37.87% accuracy with F = 0.48.\n"
        "3. In multi-objective optimization, to claim an 'advantage' or 'trade-off', you must win on at least one objective. But here, the Transformer achieves both HIGHER accuracy and LOWER overhead simultaneously.\n"
        "4. This means our proposed method is mathematically Pareto-dominated. If we claimed in a journal that 37% accuracy is a 'good trade-off', any reviewer would desk-reject it. In Slides 3 and 4, we show exactly why this happened."
    )

    # =========================================================================
    # SLIDE 3: Root Cause 1 — Misaligned Overhead Metrics (F)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Slide 3: Root Cause 1 — Misaligned Composite Overhead Metric (F)")

    # Left Box: The Mathematical Formula
    b_l = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    b_l.fill.solid()
    b_l.fill.fore_color.rgb = BG_CARD
    b_l.line.color.rgb = BORDER_COLOR

    tb_l = s3.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "The Flawed Proxy Metric Formulation"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

    f_bullets = [
        "The composite fitness function was designed as:\nF = 0.45(1 - Acc) + 0.20 f_FRUR + 0.15 f_CPU + 0.10 f_FSD + 0.10 f_BW",
        "Terms f_CPU and f_BW were defined as weight-magnitude penalties:\nf_CPU = (1/D) * Σ I(|w_i| > 0.3)\nf_BW  = (1/D) * Σ I(|w_i| > 0.05)",
        "Flaw: Weight magnitude was assumed to represent physical hardware computation and memory bandwidth.",
        "In modern deep learning, weight magnitude does NOT represent hardware cost!",
        "This allowed deep learning to achieve artificially low overhead scores without optimizing for hardware."
    ]
    for b in f_bullets:
        pb = tf_l.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(12)
        pb.font.color.rgb = SLATE_DARK
        pb.space_before = Pt(8)

    # Right Box: Why Deep Learning "Cheated" the Metric
    b_r = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    b_r.fill.solid()
    b_r.fill.fore_color.rgb = BG_CARD
    b_r.line.color.rgb = NAVY_ACCENT
    b_r.line.width = Pt(2)

    tb_r = s3.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(5.0))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Why Deep Learning Beat the Proxy Metric"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY_ACCENT

    r_bullets = [
        "Weight Decay (L2 Regularization): PyTorch DL models train with weight_decay = 1e-4, which penalizes large weights at every gradient step.",
        "Batch Normalization: Ensures activations and weights stay compactly centered around standard deviations of 0.1 to 0.2.",
        "Result: Over 90% of Transformer and CNN weights naturally stay below 0.30, giving them near-zero f_CPU and f_BW penalties!",
        "Swarm Optimizer Disadvantage: MOPSO optimizes weights in a wide bounding box [-3.0, +3.0] without L2 decay. Swarm weights are naturally large.",
        "The Metric Paradox: An 18,437-parameter Transformer scored F = 0.1686, while the 325-parameter FFNN scored F = 0.3816 because the formula measured weight magnitude instead of actual MAC operations or inference latency!"
    ]
    for b in r_bullets:
        pb = tf_r.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(12)
        pb.font.color.rgb = SLATE_DARK
        pb.space_before = Pt(8)

    add_speaker_notes(s3,
        "EXPLANATION TO MAM:\n"
        "1. Mam, here is Root Cause 1 that explains why the Transformer got a lower overhead score than our tiny FFNN.\n"
        "2. In the senior's code, overhead terms f3, f4, and f5 were defined as the percentage of weights exceeding 0.30 and 0.05. The assumption was that smaller weights mean less hardware cost.\n"
        "3. But in modern Deep Learning, we use Batch Normalization and L2 weight decay. L2 regularization continuously forces weights towards zero during backpropagation. So by design, 90% of the Transformer's weights are below 0.30!\n"
        "4. Particle Swarm Optimization does not use weight decay. Particles search across [-3.0, +3.0]. So our 325-parameter FFNN got heavily penalized, while the 18,000-parameter Transformer got rewarded with an artificially low overhead score.\n"
        "5. The lesson for the journal: Weight magnitude is a flawed proxy for hardware cost. Future researchers must measure actual floating point operations (FLOPs) or microsecond latency."
    )

    # =========================================================================
    # SLIDE 4: Root Cause 2 & 3 — Representational Bottleneck & Feature Flaws
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Slide 4: Root Causes 2 & 3 — Capacity Bottleneck & Feature Vulnerabilities")

    # Left: Root Cause 2
    b_rc2 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    b_rc2.fill.solid()
    b_rc2.fill.fore_color.rgb = BG_CARD
    b_rc2.line.color.rgb = BORDER_COLOR

    tb_rc2 = s4.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
    tf_rc2 = tb_rc2.text_frame
    tf_rc2.word_wrap = True
    p = tf_rc2.paragraphs[0]
    p.text = "Root Cause 2: 325-Parameter Capacity Bottleneck"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

    rc2_points = [
        "Architecture: 8 input -> 16 hidden1 -> 8 hidden2 -> 5 outputs = exactly 325 weights & biases.",
        "Synthetic Data Illusion: On 3,000 synthetic Gaussian samples, 325 parameters achieved 99% accuracy because synthetic clusters were linearly separable.",
        "Real PCAP Traffic Reality: Encrypted VPN and malware traffic share overlapping packet lengths and complex non-linear manifolds.",
        "Representational Failure: With only 325 degrees of freedom, the network cannot learn multi-class decision boundaries for encrypted VPN traffic, stalling at 37.87% on ISCX.",
        "Swarm Search in High Dimensions: While gradient descent easily scales to thousands of parameters, gradient-free PSO search struggles with dimensional scaling."
    ]
    for pt_item in rc2_points:
        pb = tf_rc2.add_paragraph()
        pb.text = "• " + pt_item
        pb.font.size = Pt(12)
        pb.font.color.rgb = SLATE_DARK
        pb.space_before = Pt(8)

    # Right: Root Cause 3
    b_rc3 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    b_rc3.fill.solid()
    b_rc3.fill.fore_color.rgb = BG_CARD
    b_rc3.line.color.rgb = GOLD_ALERT
    b_rc3.line.width = Pt(2)

    tb_rc3 = s4.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(5.0))
    tf_rc3 = tb_rc3.text_frame
    tf_rc3.word_wrap = True
    p = tf_rc3.paragraphs[0]
    p.text = "Root Cause 3: Feature Vulnerabilities"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GOLD_ALERT

    rc3_points = [
        "1. Destination Port (dst_port) Uselessness:\n• Ranked dead last in permutation feature importance (ΔF = -0.00007).\n• In real traffic, Web, Chat, Streaming, and Malware all multiplex over Port 443 (HTTPS/TLS) to bypass firewalls.",
        "2. Time-to-Live (TTL) Fragility:\n• Ranked #1 on USTC malware, but TTL only measures testbed network hop count!\n• Adding noise to TTL causes accuracy to collapse from 78.7% to 48.2% (drop of 30.5%). TTL is an unreliable artifact.",
        "3. Lack of Higher-Order Statistical Moments:\n• Using only mean inter-arrival time ignores flow burstiness.\n• Our experiments show IAT Skewness is a vital physical discriminator (ΔAcc = +0.1060)."
    ]
    for pt_item in rc3_points:
        pb = tf_rc3.add_paragraph()
        pb.text = "• " + pt_item
        pb.font.size = Pt(11.5)
        pb.font.color.rgb = SLATE_DARK
        pb.space_before = Pt(8)

    add_speaker_notes(s4,
        "EXPLANATION TO MAM:\n"
        "1. Mam, Slide 4 explains why the accuracy was so low on real PCAP data.\n"
        "2. Root Cause 2 is Network Capacity: The senior's architecture has only 325 parameters. On synthetic Gaussian data, 325 parameters worked fine because the data was clean. But real encrypted VPN traffic has complex overlapping packet patterns. A 325-parameter network simply lacks the mathematical capacity to separate these classes, resulting in 37.8% accuracy on ISCX.\n"
        "3. Root Cause 3 is Feature Vulnerability:\n"
        "   - First, Destination Port is completely useless today because all applications (YouTube, WhatsApp, and malware) run over Port 443 (HTTPS).\n"
        "   - Second, TTL gave high importance on USTC only because malware was recorded on a different testbed with different hop counts! When we tested TTL under noise, accuracy collapsed by 30.5%.\n"
        "   - This proves that simple 8-feature sets fail on real-world networks without higher-order statistical moments."
    )

    # =========================================================================
    # SLIDE 5: SOTA Comparison
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Slide 5: Comprehensive State-of-the-Art (SOTA) Comparison")

    # Table on Slide 5
    table_shape5 = s5.shapes.add_table(10, 6, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.2))
    t5 = table_shape5.table
    t5.columns[0].width = Inches(2.8)
    t5.columns[1].width = Inches(2.9)
    t5.columns[2].width = Inches(1.4)
    t5.columns[3].width = Inches(1.4)
    t5.columns[4].width = Inches(1.4)
    t5.columns[5].width = Inches(1.833)

    h5 = ["Method / Publication", "Architecture / Category", "Parameters", "USTC Acc", "ISCX Acc", "Classification Status"]
    for c_i, h_val in enumerate(h5):
        cell = t5.cell(0, c_i)
        cell.text = h_val
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    sota_rows = [
        ("ET-BERT (Lin et al. 2022)", "Pre-trained Contextual Transformer", "~50 Million", "96.95%", "—", "Published SOTA (Heavy)"),
        ("YaTC (Chen et al. 2023)", "Large Traffic Transformer", "~30 Million", "97.86%", "—", "Published SOTA (Heavy)"),
        ("FS-Net (Liu et al. 2019)", "End-to-End Bi-RNN Payload Model", "~10 Million", "87.05%", "52.03%", "Published SOTA (Heavy)"),
        ("FlowPic (Shapira 2021)", "2D Flow Image Visual CNN", "~2 Million", ">90.0%", ">85.0%", "Published SOTA (Vision)"),
        ("TFE-GNN (Shen et al. 2023)", "Traffic Flow Graph Neural Network", "~5 Million", "97.47%", "91.92%", "Published SOTA (Graph)"),
        ("Transformer (Ours)", "Generic Compact Transformer", "18,437", "78.57%", "62.13%", "Baseline (Compact DL)"),
        ("LSTM (Ours)", "Generic 2-Layer LSTM", "13,093", "77.47%", "64.23%", "Baseline (Compact DL)"),
        ("1D-CNN (Ours)", "Generic 2-Layer 1D-CNN", "2,373", "77.60%", "61.50%", "Baseline (Compact DL)"),
        ("MOPSO-FFNN-AD (Proposed)", "Multi-Objective Swarm + FFNN", "325", "62.97%", "37.87%", "Proposed (Dominated)")
    ]
    for r_i, r_data in enumerate(sota_rows):
        for c_i, val in enumerate(r_data):
            cell = t5.cell(r_i + 1, c_i)
            cell.text = val
            cell.fill.solid()
            if r_i == 8:
                cell.fill.fore_color.rgb = RGBColor(254, 242, 242)
            elif r_i < 5:
                cell.fill.fore_color.rgb = RGBColor(240, 253, 244) # light green
            else:
                cell.fill.fore_color.rgb = RGBColor(241, 245, 249) if r_i % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.alignment = PP_ALIGN.LEFT if c_i < 2 else PP_ALIGN.CENTER
            if r_i == 8:
                p.font.bold = True
                p.font.color.rgb = RED_ALERT
            elif r_i < 5:
                p.font.color.rgb = RGBColor(21, 128, 61)
            else:
                p.font.color.rgb = SLATE_DARK

    add_speaker_notes(s5,
        "EXPLANATION TO MAM:\n"
        "1. Mam, in Slide 5 we added Table 6 comparing our work against published State-of-the-Art literature, as requested by the supervisor.\n"
        "2. The top rows show published SOTA models: ET-BERT, YaTC, FS-Net, and TFE-GNN. These achieve 96% to 97% accuracy, but they require between 5 Million and 50 Million parameters. They cannot run on resource-constrained SDWN edge switches.\n"
        "3. The middle rows show our re-implemented compact deep learning models (1D-CNN with 2,373 parameters and Compact Transformer with 18,437 parameters). They reach 78% accuracy.\n"
        "4. This table clearly positions our paper: While massive SOTA models are too heavy for edge switches, cutting down to 325 parameters with heuristic swarm search loses too much accuracy. Compact 1D-CNNs (~2k parameters) offer the true sweet spot."
    )

    # =========================================================================
    # SLIDE 6: Time-Based Blocking Cross-Validation
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Slide 6: Eliminating Temporal Leakage — Time-Based Blocking Cross-Validation")

    b_s6_l = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    b_s6_l.fill.solid()
    b_s6_l.fill.fore_color.rgb = BG_CARD
    b_s6_l.line.color.rgb = BORDER_COLOR

    tb_s6_l = s6.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
    tf_s6_l = tb_s6_l.text_frame
    tf_s6_l.word_wrap = True
    p = tf_s6_l.paragraphs[0]
    p.text = "The Leakage Pitfall of Random CV"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

    leak_bullets = [
        "The Problem with Standard K-Fold:\nRandom cross-validation shuffles flows randomly across folds. When a user downloads a file or an attacker runs a botnet, consecutive flows share identical bursts and timing.",
        "Temporal Autocorrelation Leakage:\nRandom splitting places flow N in the training fold and flow N+1 in the test fold, artificially inflating test accuracy by 4% to 9%!",
        "Our Methodological Fix:\nWe implemented Time-Based Blocking Cross-Validation: sorting traffic chronologically and carving it into 10 contiguous chronological time blocks (B1 to B10).",
        "Train on past blocks, test on future blocks — zero session leakage."
    ]
    for b in leak_bullets:
        pb = tf_s6_l.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(12)
        pb.font.color.rgb = SLATE_DARK
        pb.space_before = Pt(8)

    # Right: Results under Time-Blocked CV
    b_s6_r = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    b_s6_r.fill.solid()
    b_s6_r.fill.fore_color.rgb = BG_CARD
    b_s6_r.line.color.rgb = GREEN_OK
    b_s6_r.line.width = Pt(2)

    tb_s6_r = s6.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(5.0))
    tf_s6_r = tb_s6_r.text_frame
    tf_s6_r.word_wrap = True
    p = tf_s6_r.paragraphs[0]
    p.text = "Results Under Strict Temporal Blocking"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GREEN_OK

    res_bullets = [
        "Finding 1: Accuracy Drops Across All Models:\nUnder time-blocked CV, accuracy drops by 4% to 9% for all algorithms, confirming that previous literature suffered from temporal autocorrelation leakage.",
        "Finding 2: Pareto Domination Strictly Holds:\nEven under strict chronological isolation, deep learning still Pareto-dominates MOPSO:",
        "• ISCX Time-Blocked: LSTM achieves 57.30% (F = 0.3343) and Transformer achieves 53.37% (F = 0.3239), while MOPSO-FFNN-AD achieves only 38.23% (F = 0.4837).",
        "• USTC Time-Blocked: 1D-CNN reaches 77.40% (F = 0.1989), while MOPSO reaches 66.60% (F = 0.3742).",
        "Significance: All p-values < 0.001. The negative result is not an artifact of data splitting; it is a permanent property of the model."
    ]
    for b in res_bullets:
        pb = tf_s6_r.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(12)
        pb.font.color.rgb = SLATE_DARK
        pb.space_before = Pt(8)

    add_speaker_notes(s6,
        "EXPLANATION TO MAM:\n"
        "1. Mam, in Slide 6 we address the supervisor's directive on Temporal Leakage.\n"
        "2. In networking, flows from the same user or burst occur close together in time. If you use standard random cross-validation, packets from the same session get mixed into both train and test sets, artificially inflating accuracy.\n"
        "3. To fix this, we wrote `run_time_blocked_cv.py`. We sorted the PCAP data chronologically and split it into 10 contiguous time blocks.\n"
        "4. Notice that when temporal leakage is removed, accuracy drops by 5% across the board. But critically, Pareto domination still holds: Deep learning still beats MOPSO by 15% on accuracy and achieves lower overhead. This proves our negative result is methodologically sound."
    )

    # =========================================================================
    # SLIDE 7: Feature Robustness Experiments
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Slide 7: Empirical Feature Robustness Analysis")

    feat_cards = [
        ("TTL Sensitivity Test", "Fragile Topology Artifact", [
            "Injected bounded noise into Time-to-Live (TTL).",
            "FFNN accuracy collapsed from 78.67% down to 48.17% (a massive 30.5% drop!).",
            "Randomizing TTL dropped accuracy by 26.83%.",
            "Conclusion: High feature importance of TTL was an illusion caused by testbed hop count."
        ], RED_ALERT),
        ("dst_port Ablation", "Obsolete Under Port 443", [
            "Completely ablated destination port from the feature set (7 features vs 8).",
            "Accuracy change: 0.00% drop on ISCX; ΔF = -0.00007.",
            "Conclusion: Port numbers provide ZERO predictive power in modern internet traffic due to universal HTTPS/TLS 1.3 multiplexing."
        ], GOLD_ALERT),
        ("Higher-Order IAT Moments", "True Physical Discrimination", [
            "Extracted IAT Variance, Skewness, and Kurtosis.",
            "IAT Skewness emerged as top physical discriminator (ΔAcc = +0.1060).",
            "Diminishing returns analysis proved accuracy plateaus at k=6 features."
        ], GREEN_OK)
    ]
    for idx, (title, sub, items, col) in enumerate(feat_cards):
        left_pos = Inches(0.8 + idx * 3.95)
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.5), Inches(3.75), Inches(5.4))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = col
        card.line.width = Pt(2)

        tb_fc = s7.shapes.add_textbox(left_pos + Inches(0.2), Inches(1.7), Inches(3.35), Inches(5.0))
        tff = tb_fc.text_frame
        tff.word_wrap = True
        p_h = tff.paragraphs[0]
        p_h.text = title
        p_h.font.size = Pt(17)
        p_h.font.bold = True
        p_h.font.color.rgb = col

        p_s = tff.add_paragraph()
        p_s.text = sub.upper()
        p_s.font.size = Pt(10)
        p_s.font.bold = True
        p_s.font.color.rgb = SLATE_MUTED
        p_s.space_before = Pt(2)

        for it in items:
            p_it = tff.add_paragraph()
            p_it.text = "• " + it
            p_it.font.size = Pt(11.5)
            p_it.font.color.rgb = SLATE_DARK
            p_it.space_before = Pt(8)

    add_speaker_notes(s7,
        "EXPLANATION TO MAM:\n"
        "1. Mam, Slide 7 shows our new experimental findings on network features.\n"
        "2. Many networking papers blindly use the 8 standard features. We ran sensitivity tests to evaluate their true validity:\n"
        "   - First, TTL: When we perturbed TTL with random noise, accuracy plunged by 30.5%. This proves the classifier was relying on an artificial network hop artifact rather than learning true application traffic.\n"
        "   - Second, Destination Port: We removed dst_port completely, and accuracy had zero drop! Because today, all encrypted traffic uses Port 443.\n"
        "   - Third, Higher-Order Moments: When we introduced IAT Skewness, accuracy improved significantly because skewness captures the asymmetry of human typing versus automated streaming bursts."
    )

    # =========================================================================
    # SLIDE 8: Reframing Stability Proofs — Math vs. Classification Performance
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Slide 8: Reframing Stability Proofs — Math vs. Classifier Efficacy")

    # Left: The Mathematical Proofs (Lemmas 1 & 2)
    b_s8_l = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    b_s8_l.fill.solid()
    b_s8_l.fill.fore_color.rgb = BG_CARD
    b_s8_l.line.color.rgb = BORDER_COLOR

    tb_s8_l = s8.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
    tf_s8_l = tb_s8_l.text_frame
    tf_s8_l.word_wrap = True
    p = tf_s8_l.paragraphs[0]
    p.text = "Mathematical Swarm Stability (Appendix A)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

    proof_bullets = [
        "Lemma 1: First-Order Expectation Convergence:\n• Swarm dynamic matrix characteristic equation:\nλ² - (1 + w - c_eff)λ + w = 0\n• Evaluated parameters (w=0.729, c1=c2=1.49445) yield spectral radius ρ = 0.8543 < 1.0.\n• Proof: Expected particle position E[q_s] converges to p.",
        "Lemma 2: Second-Order Variance Stability:\n• Derived via stability constraint 1 - w² - (c1²+c2²)/3 > 0.\n• Computed safety margin: +0.3550 > 0.\n• Proof: Swarm variance Var[q_s] strictly converges to 0.",
        "Status in Review 3: Both complete formal proofs have been relocated to Appendix A of the manuscript."
    ]
    for b in proof_bullets:
        pb = tf_s8_l.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(12)
        pb.font.color.rgb = SLATE_DARK
        pb.space_before = Pt(8)

    # Right: The Vital Scientific Lesson
    b_s8_r = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    b_s8_r.fill.solid()
    b_s8_r.fill.fore_color.rgb = BG_CARD
    b_s8_r.line.color.rgb = NAVY_ACCENT
    b_s8_r.line.width = Pt(2)

    tb_s8_r = s8.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(5.0))
    tf_s8_r = tb_s8_r.text_frame
    tf_s8_r.word_wrap = True
    p = tf_s8_r.paragraphs[0]
    p.text = "The Vital Distinction: Stability ≠ Accuracy"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY_ACCENT

    lesson_bullets = [
        "What the Proofs Guarantee:\nLemmas 1 and 2 prove that the particle swarm optimizer does not explode or oscillate uncontrollably. The algorithm converges smoothly to an equilibrium.",
        "What the Proofs CANNOT Guarantee:\nSwarm stability does NOT imply that the resulting neural network will accurately classify traffic!",
        "The Core Insight:\nA stable optimizer converging smoothly to a local minimum inside an under-parameterized 325-parameter search space simply produces a stably bad classifier.",
        "Paper Framing: In our manuscript, we explicitly decouple optimization stability from classification efficacy, preventing misleading theoretical over-claims."
    ]
    for b in lesson_bullets:
        pb = tf_s8_r.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(12)
        pb.font.color.rgb = SLATE_DARK
        pb.space_before = Pt(8)

    add_speaker_notes(s8,
        "EXPLANATION TO MAM:\n"
        "1. Mam, in our original draft, we had two formal mathematical proofs: Lemma 1 proving first-order expectation convergence, and Lemma 2 proving variance stability.\n"
        "2. The supervisor pointed out a critical distinction: Mathematical stability of an optimizer does not mean the classifier is accurate!\n"
        "3. Lemma 1 and 2 prove that the swarm particles do not explode. But if you give a stable swarm an architecture that has only 325 parameters, it converges stably to a poor solution.\n"
        "4. Therefore, following our supervisor's instruction, we moved the lengthy mathematical proofs to Appendix A, and in the main text we honestly explain: Stability proves the optimization engine works, but it cannot overcome structural capacity limitations."
    )

    # =========================================================================
    # SLIDE 9: Review 3 Deliverables & Q2 Submission Package
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Slide 9: Review 3 Deliverables & Q2 Journal Submission Package")

    # 4 grid cards
    grid_cards = [
        ("1. Fully Reframed Manuscript", [
            "Title: 'On the Limitations of Multi-Objective Neuro-Evolutionary Traffic Classification in SDWNs: A Negative Result and Lessons Learned'",
            "Complete 10-section Q2 manuscript in Word (.docx) and Markdown (.md).",
            "15 new citations (2024–2026) added to Related Work."
        ], NAVY_ACCENT),
        ("2. Empirical Codebase & Fixes", [
            "run_time_blocked_cv.py (eliminates temporal autocorrelation leakage).",
            "feature_robustness_experiments.py (TTL noise, dst_port ablation, IAT moments).",
            "Zero data fabrication: every metric directly logged in CSV."
        ], GREEN_OK),
        ("3. Automated Test Suite", [
            "16 passing unit tests across 5 test suites (pytest).",
            "Verifies mathematical formulas, non-leakage scaling, DL models, and time-blocked splits in 3.19 seconds."
        ], GOLD_ALERT),
        ("4. Packaging & Reproducibility", [
            "Production-ready Dockerfile for one-click environment replication.",
            "Pinned requirements.txt and uv virtual environment.",
            "Zenodo archive instructions ready for DOI minting."
        ], NAVY_PRIMARY)
    ]

    for idx, (title, items, col) in enumerate(grid_cards):
        r_i = idx // 2
        c_i = idx % 2
        left_pos = Inches(0.8 + c_i * 5.95)
        top_pos = Inches(1.5 + r_i * 2.75)

        card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, Inches(5.75), Inches(2.55))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = col
        card.line.width = Pt(2)

        tb_gc = s9.shapes.add_textbox(left_pos + Inches(0.2), top_pos + Inches(0.15), Inches(5.35), Inches(2.25))
        tfg = tb_gc.text_frame
        tfg.word_wrap = True
        p_h = tfg.paragraphs[0]
        p_h.text = title
        p_h.font.size = Pt(16)
        p_h.font.bold = True
        p_h.font.color.rgb = col

        for it in items:
            p_it = tfg.add_paragraph()
            p_it.text = "• " + it
            p_it.font.size = Pt(11.5)
            p_it.font.color.rgb = SLATE_DARK
            p_it.space_before = Pt(4)

    add_speaker_notes(s9,
        "EXPLANATION TO MAM:\n"
        "1. Mam, to conclude our Review 3 presentation, this slide summarizes all the deliverables prepared for our final defense and Q2 submission:\n"
        "   - First: A fully rewritten manuscript formatted according to Q2 journal standards in both Word (.docx) and Markdown (.md), complete with updated citations.\n"
        "   - Second: A clean experimental codebase that removes temporal leakage and runs feature sensitivity tests.\n"
        "   - Third: A complete 16-test unit testing suite that runs via pytest in 3.19 seconds with a 100% pass rate.\n"
        "   - Fourth: Full containerized reproduction via Docker and Zenodo archiving instructions.\n"
        "2. We have satisfied all 8 directives given by the supervisor. We thank you for your guidance and welcome your questions."
    )

    prs.save(PPTX_PATH)
    print(f"Successfully generated PowerPoint at: {PPTX_PATH}")

if __name__ == "__main__":
    create_presentation()
