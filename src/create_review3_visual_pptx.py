"""
src/create_review3_visual_pptx.py
Builds a clean, human, professional 16:9 PowerPoint presentation
(PRESENTATION_REVIEW3_VTOP.pptx) avoiding AI slop.
Features:
- Clean minimalist academic styling (plenty of white space, no cluttered badge blocks)
- Clear, punchy human headlines
- Exactly 3 concise, high-signal bullet points per slide (with bold lead-ins)
- Prominent high-res benchmark figure placement
- 1-sentence bottom takeaway pill
- Natural, conversational first-person speaker notes
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PPTX_OUTPUTS = [
    os.path.join(PROJECT_ROOT, "PRESENTATION_REVIEW3_VTOP.pptx"),
    os.path.join(PROJECT_ROOT, "results_review3", "PRESENTATION_VTOP_SLIDES.pptx"),
    os.path.join(PROJECT_ROOT, "docs", "PRESENTATION_VTOP_SLIDES.pptx")
]
IMG_DIR = os.path.join(PROJECT_ROOT, "results_review3")

# Modern Minimalist Palette (Crisp White / Slate / Subtle Blue Accent)
COLOR_BG          = RGBColor(255, 255, 255)  # Pure White
COLOR_TEXT_MAIN   = RGBColor(15, 23, 42)     # Slate-900 #0F172A
COLOR_TEXT_MUTED  = RGBColor(100, 116, 139)  # Slate-500 #64748B
COLOR_ACCENT_BLUE = RGBColor(37, 99, 235)    # Blue-600 #2563EB
COLOR_CARD_BG     = RGBColor(248, 250, 252)  # Slate-50 #F8FAFC
COLOR_BORDER      = RGBColor(226, 232, 240)  # Slate-200 #E2E8F0
COLOR_PILL_BG     = RGBColor(239, 246, 255)  # Light Blue-50 #EFF6FF
COLOR_PILL_TEXT   = RGBColor(29, 78, 216)    # Blue-700 #1D4ED8
COLOR_ALERT_RED   = RGBColor(185, 28, 28)    # Red-700 #B91C1C

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_clean_header(slide, slide_num, title, subtitle):
        # Category / Slide counter
        tb_meta = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.25))
        tf_meta = tb_meta.text_frame
        p_m = tf_meta.paragraphs[0]
        p_m.text = f"SLIDE {slide_num:02d} • REVIEW 3 & Q2 JOURNAL DEFENSE"
        p_m.font.size = Pt(9.5)
        p_m.font.bold = True
        p_m.font.color.rgb = COLOR_ACCENT_BLUE

        # Main Title
        tb_t = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.7), Inches(0.55))
        tf_t = tb_t.text_frame
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(21)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_TEXT_MAIN

        # Subtitle
        tb_s = slide.shapes.add_textbox(Inches(0.8), Inches(1.15), Inches(11.7), Inches(0.35))
        tf_s = tb_s.text_frame
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle
        p_s.font.size = Pt(11)
        p_s.font.color.rgb = COLOR_TEXT_MUTED

        # Hairline divider
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.48), Inches(11.733), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_BORDER
        line.line.color.rgb = COLOR_BORDER

    def add_notes(slide, notes_text):
        slide.notes_slide.notes_text_frame.text = notes_text

    def create_content_slide(slide_num, title, subtitle, img_filename, bullets, takeaway_text, speaker_script):
        slide = prs.slides.add_slide(blank_layout)
        add_clean_header(slide, slide_num, title, subtitle)

        # Left Column Card (Clean, spacious text)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.65), Inches(4.7), Inches(5.35))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_BG
        card.line.color.rgb = COLOR_BORDER
        card.line.width = Pt(1)

        tb_bullets = slide.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.3), Inches(3.8))
        tf_b = tb_bullets.text_frame
        tf_b.word_wrap = True

        for i, (heading, text) in enumerate(bullets):
            p = tf_b.paragraphs[0] if i == 0 else tf_b.add_paragraph()
            p.text = f"{heading}: "
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = COLOR_TEXT_MAIN
            if i > 0:
                p.space_before = Pt(12)

            run = p.add_run()
            run.text = text
            run.font.bold = False
            run.font.size = Pt(11.5)
            run.font.color.rgb = RGBColor(51, 65, 85)

        # Bottom Takeaway Pill
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(5.85), Inches(4.3), Inches(0.95))
        pill.fill.solid()
        pill.fill.fore_color.rgb = COLOR_PILL_BG
        pill.line.color.rgb = RGBColor(191, 219, 254)
        pill.line.width = Pt(1)

        tb_pill = slide.shapes.add_textbox(Inches(1.1), Inches(5.92), Inches(4.1), Inches(0.8))
        tf_p = tb_pill.text_frame
        tf_p.word_wrap = True
        p_p = tf_p.paragraphs[0]
        p_p.text = "TAKEAWAY: "
        p_p.font.size = Pt(9.5)
        p_p.font.bold = True
        p_p.font.color.rgb = COLOR_PILL_TEXT

        run_p = p_p.add_run()
        run_p.text = takeaway_text
        run_p.font.bold = False
        run_p.font.size = Pt(10)
        run_p.font.color.rgb = RGBColor(30, 58, 138)

        # Right Column: Prominent Benchmark Figure
        img_path = os.path.join(IMG_DIR, img_filename)
        if os.path.exists(img_path):
            slide.shapes.add_picture(img_path, Inches(5.7), Inches(1.65), Inches(6.8), Inches(5.35))

        add_notes(slide, speaker_script)
        return slide

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide (Clean, uncluttered, human)
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)

    # Accent top strip
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_ACCENT_BLUE
    top_bar.line.color.rgb = COLOR_ACCENT_BLUE

    # Title box
    tb_title = s1.shapes.add_textbox(Inches(1.0), Inches(1.4), Inches(11.333), Inches(2.2))
    tft = tb_title.text_frame
    tft.word_wrap = True

    p_badge = tft.paragraphs[0]
    p_badge.text = "SDWN TRAFFIC CLASSIFICATION RESEARCH • REVIEW 3 DEFENSE"
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = COLOR_ACCENT_BLUE

    p_m = tft.add_paragraph()
    p_m.text = "Limits of Neuro-Evolutionary Traffic Classification in SDWNs"
    p_m.font.size = Pt(28)
    p_m.font.bold = True
    p_m.font.color.rgb = COLOR_TEXT_MAIN
    p_m.space_before = Pt(8)

    p_s = tft.add_paragraph()
    p_s.text = "A Rigorous Empirical Negative Result, Real-PCAP Benchmarks & Lessons Learned"
    p_s.font.size = Pt(15)
    p_s.font.color.rgb = COLOR_TEXT_MUTED
    p_s.space_before = Pt(6)

    # 3 System Comparison Cards
    sys_cards = [
        ("System A (Base Paper)", "Pradhan et al. (IET 2022)", "Single-objective PSO-FFNN. Optimized accuracy only, tested only on historical tables."),
        ("System B (Senior Baseline)", "Budithi Supraja (2024)", "Bi-objective MOPSO-FFNN-AD with drift detection. Tested strictly on synthetic Gaussian data."),
        ("System C (Our Work)", "Q2 Journal Submission", "Real PCAP evaluation (ISCX & USTC), DL baselines, time-blocked CV, and an honest negative result.")
    ]

    for idx, (title_sc, author_sc, desc_sc) in enumerate(sys_cards):
        left_sc = Inches(1.0 + idx * 3.9)
        card_sc = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_sc, Inches(4.0), Inches(3.6), Inches(2.5))
        card_sc.fill.solid()
        card_sc.fill.fore_color.rgb = COLOR_CARD_BG
        card_sc.line.color.rgb = COLOR_ACCENT_BLUE if idx == 2 else COLOR_BORDER
        card_sc.line.width = Pt(1.5 if idx == 2 else 1)

        tb_sc = s1.shapes.add_textbox(left_sc + Inches(0.2), Inches(4.15), Inches(3.2), Inches(2.2))
        tf_sc = tb_sc.text_frame
        tf_sc.word_wrap = True

        p1 = tf_sc.paragraphs[0]
        p1.text = title_sc
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_ACCENT_BLUE if idx == 2 else COLOR_TEXT_MAIN

        p2 = tf_sc.add_paragraph()
        p2.text = author_sc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_TEXT_MUTED
        p2.space_before = Pt(2)

        p3 = tf_sc.add_paragraph()
        p3.text = desc_sc
        p3.font.size = Pt(10)
        p3.font.color.rgb = RGBColor(71, 85, 105)
        p3.space_before = Pt(8)

    add_notes(s1,
        "HOW TO INTRODUCE YOURSELF & PROJECT:\n"
        "Good morning, Mam and Sir. Today we present our Review 3 defense for our paper merging our senior's research into a Q2 journal submission.\n"
        "Rather than defending inflated numbers from synthetic data, we did the hard engineering: we evaluated the method on real packet captures.\n"
        "Our contribution is an honest, mathematically rigorous negative result. We show why a 325-parameter evolutionary network is Pareto-dominated by deep learning on real traffic, uncover temporal data leakage, and share practical design lessons for SDWN edge intelligence."
    )

    # -------------------------------------------------------------
    # SLIDE 2: Figure 1 - Pareto Domination
    # -------------------------------------------------------------
    create_content_slide(
        slide_num=2,
        title="MOPSO is Strictly Pareto-Dominated by Deep Learning",
        subtitle="Real PCAPs show our proposed method loses on both accuracy and overhead simultaneously.",
        img_filename="01_core_finding_pareto_domination.png",
        bullets=[
            ("The Trade-off Myth", "Prior work claimed MOPSO achieved an intentional trade-off between accuracy and hardware cost. On real traffic, this trade-off does not exist."),
            ("The Real Numbers", "On USTC malware, Transformer hits 78.6% with overhead F=0.17, while MOPSO gets 63.0% with F=0.38. On ISCX encrypted traffic, LSTM gets 64.2% while MOPSO collapses to 37.9%."),
            ("The Negative Result", "To claim a trade-off, a method must win on at least one metric. Deep learning dominates on both axes. Reporting this honestly makes our paper credible for publication.")
        ],
        takeaway_text="Deep learning achieves higher accuracy (+15% to +26%) AND lower overhead F (-0.19 to -0.21). MOPSO is strictly dominated.",
        speaker_script=(
            "WHAT TO SAY IN 45 SECONDS:\n"
            "Mam, this first graph is our core finding. In multi-objective optimization, a trade-off requires winning on at least one axis—like lower overhead or higher speed.\n"
            "As you can see in Figure 1, the ideal region is the top-left: high accuracy, low overhead F.\n"
            "Standard deep learning models—CNN, LSTM, and Transformer—occupy that ideal region. They achieved 77% to 78% accuracy with overhead F under 0.20.\n"
            "Our proposed MOPSO had 63% accuracy and a higher overhead of 0.38. So it loses on both axes simultaneously. That is Pareto domination, not a trade-off.\n"
            "Publishing this as an honest negative result explains why the formula failed, which is exactly what Q2 reviewers want to see."
        )
    )

    # -------------------------------------------------------------
    # SLIDE 3: Figure 2 - Synthetic Illusion vs Real PCAPs
    # -------------------------------------------------------------
    create_content_slide(
        slide_num=3,
        title="The 'Synthetic Benchmark Illusion' vs. Real Network Traffic",
        subtitle="Why the senior's 94.3% claim collapsed the moment real packets were introduced.",
        img_filename="02_synthetic_illusion_vs_real_pcap.png",
        bullets=[
            ("The Senior's Claim", "Senior reported 94.33% accuracy. However, this was tested strictly on synthetic Gaussian clusters where classes were artificially separated."),
            ("The Real PCAP Reality", "When evaluated on real PCAP captures, MOPSO dropped by 31.4% on malware (USTC), and collapsed by 56.5% on encrypted traffic (ISCX, 37.87%)."),
            ("Capacity Bottleneck", "Real encrypted flows have complex, non-linear timing distributions. A tiny 325-parameter network simply lacks the representational capacity to separate them.")
        ],
        takeaway_text="Synthetic Gaussian clusters create a false sense of success. Real encrypted packets reveal true model capacity limits.",
        speaker_script=(
            "WHAT TO SAY IN 45 SECONDS:\n"
            "Why did our senior get 94.3% accuracy? Because it was tested only on synthetic data—clean, artificial Gaussian clusters.\n"
            "Figure 2 shows what happened the moment we piped real network packet captures into the system.\n"
            "On USTC malware, MOPSO fell to 63%. On ISCX encrypted VPN traffic, it collapsed to 37.8%.\n"
            "Meanwhile, standard 1D-CNN and LSTM models maintained 61% to 78% accuracy on the exact same real packets.\n"
            "This proved that synthetic datasets are an illusion in network research. 325 parameters is simply too small to partition encrypted traffic."
        )
    )

    # -------------------------------------------------------------
    # SLIDE 4: Figure 3 - SOTA vs Edge Switch Limits
    # -------------------------------------------------------------
    create_content_slide(
        slide_num=4,
        title="SOTA Traffic Classifiers vs. SDWN Edge Hardware Limits",
        subtitle="Balancing multi-million parameter accuracy against switch TCAM/SRAM constraints.",
        img_filename="03_sota_benchmarks_and_edge_constraints.png",
        bullets=[
            ("The Giant Models", "Published SOTA models like ET-BERT (50M params) and YaTC (30M params) achieve 97%+ accuracy, but require server-grade GPUs."),
            ("The Switch Bottleneck", "SDWN edge switches have strict TCAM and SRAM memory limits. They cannot store or execute models exceeding roughly 10,000 parameters."),
            ("The Practical Sweet Spot", "MOPSO easily fits the switch (325 params) but loses too much accuracy. A compact 1D-CNN (~2,300 params) hits the practical sweet spot: fits edge memory and reaches 77.6% accuracy.")
        ],
        takeaway_text="ET-BERT cannot run at line rate on an edge switch. A 2,300-parameter 1D-CNN is the true sweet spot for edge intelligence.",
        speaker_script=(
            "WHAT TO SAY IN 45 SECONDS:\n"
            "Faculty often ask: why not just use ET-BERT or YaTC if they get 97% accuracy?\n"
            "Figure 3 plots model accuracy against parameter count on a logarithmic scale.\n"
            "ET-BERT has 50 million parameters and requires a GPU server. But OpenFlow edge switches have limited TCAM memory—they can't store more than 10,000 parameters.\n"
            "Our goal was to test whether a compact 325-parameter model could run directly on the switch.\n"
            "Our conclusion: while it fits into memory, it loses too much accuracy. The best trade-off for edge intelligence is actually a compact 1D-CNN with 2,300 parameters."
        )
    )

    # -------------------------------------------------------------
    # SLIDE 5: Figure 4 - Temporal Autocorrelation Leakage
    # -------------------------------------------------------------
    create_content_slide(
        slide_num=5,
        title="Fixing Temporal Leakage: Time-Blocked Cross Validation",
        subtitle="Standard random CV leaks session patterns; time-blocked CV sets an honest benchmark.",
        img_filename="04_temporal_leakage_random_vs_time_blocked_cv.png",
        bullets=[
            ("The Leakage Flaw", "Standard random 10-fold CV randomly shuffles flows. Packets from the same user session or attack appear in both train and test folds, artificially inflating accuracy."),
            ("Our Chronological Fix", "We sorted 3,000 flows by timestamp into 10 contiguous chronological blocks. Models were trained on past flows and tested strictly on future flows."),
            ("The Verified Result", "Accuracy dropped by 6% to 8% across all models once leakage was removed. Even with zero leakage, deep learning still beats MOPSO by +15%, confirming our negative result is solid.")
        ],
        takeaway_text="Time-blocked CV removes session autocorrelation leakage. Deep learning still dominates MOPSO by +15% to +19%.",
        speaker_script=(
            "WHAT TO SAY IN 45 SECONDS:\n"
            "Next, we audited experimental methodology. Most machine learning papers in networking use random 10-fold cross validation. But that leaks future data.\n"
            "In real life, packets in a network flow occur seconds apart. Random splitting mixes packets from the same session into both training and testing folds, allowing the model to cheat.\n"
            "In Figure 4, we built a Time-Blocked CV pipeline that splits flows chronologically into 10 strict time blocks.\n"
            "As expected, accuracy dropped by 6% to 8% once leakage was eliminated. But deep learning still beats MOPSO by 15% to 19%.\n"
            "This proves our negative result is not an evaluation fluke."
        )
    )

    # -------------------------------------------------------------
    # SLIDE 6: Figure 5 - TTL Perturbation Fragility
    # -------------------------------------------------------------
    create_content_slide(
        slide_num=6,
        title="Feature Fragility: TTL is a Topology Artifact, Not a Signature",
        subtitle="Realistic network jitter exposes why static benchmark rankings cannot be trusted.",
        img_filename="05_ttl_perturbation_fragility.png",
        bullets=[
            ("The False Assumption", "Senior and prior papers ranked Time-To-Live (TTL) as their #1 most important classification feature."),
            ("The Stress Test", "We injected realistic network jitter into TTL values (simulating packet rerouting, multi-path forwarding, and NAT changes)."),
            ("Catastrophic Drop", "Under realistic TTL noise, FFNN accuracy collapsed from 78.7% down to 48.2% (a 30.5% collapse). TTL measures router hops, not application behavior.")
        ],
        takeaway_text="Corrupting TTL degrades accuracy by 30.5%. Classifiers deployed in dynamic SDWN switches must not rely on TTL.",
        speaker_script=(
            "WHAT TO SAY IN 45 SECONDS:\n"
            "Prior literature claimed that TTL—Time-To-Live—is the most important feature for identifying network traffic.\n"
            "We tested that assumption in Figure 5. TTL is just a hop counter. It decrements each time a packet hops through a router. It changes when packets take alternate paths or pass through a NAT.\n"
            "We added realistic noise to the TTL field to simulate route changes. The FFNN accuracy crashed by 30.5%—down to 48%!\n"
            "This proves feature fragility: models that look great on static captures will fail in dynamic wireless networks if they rely on topology artifacts."
        )
    )

    # -------------------------------------------------------------
    # SLIDE 7: Figure 6 - Port 443 vs IAT Moments
    # -------------------------------------------------------------
    create_content_slide(
        slide_num=7,
        title="Destination Port is Obsolete; Timing Burstiness is King",
        subtitle="Port 443 HTTPS multiplexing breaks legacy features; IAT moments provide true signal.",
        img_filename="06_feature_importance_and_iat_moments.png",
        bullets=[
            ("Port 443 Multiplexing", "Legacy networks used port numbers to identify apps. Today, web, VPN, and malware all tunnel through port 443. Removing dst_port changed performance by virtually zero."),
            ("Higher-Order IAT Moments", "We extracted higher-order statistical moments: IAT Skewness (10.6% drop on permutation) and IAT Variance (6.3% drop)."),
            ("Unhideable Fingerprint", "Encryption hides packet payloads, but it cannot hide packet delivery burstiness—how packets clump together over time.")
        ],
        takeaway_text="dst_port has zero utility under port 443 tunneling. IAT Skewness and Variance capture real encrypted burstiness.",
        speaker_script=(
            "WHAT TO SAY IN 45 SECONDS:\n"
            "Similarly, in Figure 6, we analyzed destination ports. In modern networks, destination port is useless because everything tunnels over port 443 using TLS or HTTPS.\n"
            "When we completely removed destination port, it caused virtually zero change in model performance.\n"
            "Instead, our experiments show that higher-order moments—specifically IAT Skewness and IAT Variance—provide the strongest discriminative power.\n"
            "Encryption hides packet payloads, but it cannot hide the physical burstiness of packet delivery."
        )
    )

    # -------------------------------------------------------------
    # SLIDE 8: Figure 7 - Feature Diminishing Returns
    # -------------------------------------------------------------
    create_content_slide(
        slide_num=8,
        title="Why 8 Features? The Saturation Curve",
        subtitle="Justifying our compact feature set against switch TCAM memory overhead.",
        img_filename="07_diminishing_returns_feature_saturation.png",
        bullets=[
            ("The Experiment", "We evaluated models incrementally, starting from 1 feature up to all 8 features, to test for diminishing returns."),
            ("Accuracy Plateau", "Accuracy rises from 35.3% (1 feature) to 41.0% (5 features), and completely plateaus between 5 and 8 features (42.7%)."),
            ("Hardware Memory Cost", "Every additional feature increases neural network weights linearly (213 to 325 parameters). Adding features beyond 8 wastes switch memory for zero gain.")
        ],
        takeaway_text="Accuracy plateaus after 5 features. 8 features captures maximum signal without wasting switch flow table memory.",
        speaker_script=(
            "WHAT TO SAY IN 45 SECONDS:\n"
            "In Figure 7, we answered why our model uses 8 features instead of 3 or 20.\n"
            "We plotted classification accuracy against feature count alongside neural network parameter growth.\n"
            "Notice how accuracy climbs quickly up to 5 features, but then completely plateaus between 5 and 8 features.\n"
            "Because switch memory scales directly with input size, extracting more than 8 features wastes memory without improving classification."
        )
    )

    # -------------------------------------------------------------
    # SLIDE 9: Figure 8 - Swarm Stability vs Accuracy
    # -------------------------------------------------------------
    create_content_slide(
        slide_num=9,
        title="Swarm Stability Does Not Imply Classifier Accuracy",
        subtitle="Reframing Lemmas 1 & 2: Proving the swarm converges, but into a sub-optimal basin.",
        img_filename="08_swarm_stability_vs_classifier_accuracy.png",
        bullets=[
            ("The Proofs are Valid", "We re-derived the mathematical proofs for Lemmas 1 & 2. The swarm spectral radius is 0.8543 < 1.0, proving particle velocities and positions converge stably."),
            ("The Conceptual Trap", "Prior work claimed mathematical stability proved the classifier was effective. But stability only proves particles stop moving—not that the solution is accurate!"),
            ("The Local Minima Trap", "As shown on the right, the swarm stably contracts into a sub-optimal basin of attraction (trapped at 37.8%), because 325 parameters is too small.")
        ],
        takeaway_text="Mathematical swarm stability (ρ = 0.8543 < 1.0) is proven, but numerical stability cannot overcome capacity limits.",
        speaker_script=(
            "WHAT TO SAY IN 45 SECONDS:\n"
            "Finally, Mam and Sir, we evaluated the mathematical stability proofs from the senior's paper.\n"
            "Lemmas 1 and 2 prove that the particle swarm converges. We verified the eigenanalysis: the spectral radius is 0.8543, which is strictly less than 1.0. The math is 100% correct.\n"
            "However, our key scientific insight is that mathematical swarm convergence does NOT imply classifier accuracy.\n"
            "As shown in the right panel, a swarm can contract stably into a poor local minimum because 325 parameters is too small to learn encrypted traffic.\n"
            "That is why we moved the proofs to Appendix A and focused the main paper on the empirical reality."
        )
    )

    # -------------------------------------------------------------
    # SLIDE 10: Deliverables & Conclusion
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_clean_header(s10, 10, "Summary of Review 3 & Q2 Submission Deliverables", "Everything packaged, verified, and reproducible.")

    cards_d = [
        ("1. Full Research Manuscript", "Written for Q2 Journal standards (IEEE/ACM Transactions format).\nAvailable in Word (.docx) and LaTeX (.tex) with 17 tables and 12 figures.\nScrubbed of false trade-off claims; fully reframed as an empirical negative result."),
        ("2. Leakage-Free Codebase", "Built Scapy PCAP streaming pipeline (6,000 balanced real flows).\nTime-Blocked CV and Feature Robustness suites fully reproducible.\nZero data leakage: StandardScaler fit strictly on training splits."),
        ("3. Automated Test Suite", "16 passing unit tests across 5 test suites (pytest).\nVerifies mathematical formulas, non-leakage scaling, DL models, and time-blocked splits in 3.3 seconds (100% pass rate)."),
        ("4. Containerization & Archive", "Production-ready Dockerfile for one-click environment replication.\nClean GitHub repository: https://github.com/rikkumahan/CN_research.git\nPrepared for Zenodo DOI archiving upon paper submission.")
    ]

    for idx, (title_d, text_d) in enumerate(cards_d):
        r_i = idx // 2
        c_i = idx % 2
        left_d = Inches(0.8 + c_i * 5.95)
        top_d = Inches(1.65 + r_i * 2.7)

        card_d = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_d, top_d, Inches(5.75), Inches(2.45))
        card_d.fill.solid()
        card_d.fill.fore_color.rgb = COLOR_CARD_BG
        card_d.line.color.rgb = COLOR_BORDER
        card_d.line.width = Pt(1)

        tb_d = s10.shapes.add_textbox(left_d + Inches(0.2), top_d + Inches(0.15), Inches(5.35), Inches(2.15))
        tf_d = tb_d.text_frame
        tf_d.word_wrap = True

        p_hd = tf_d.paragraphs[0]
        p_hd.text = title_d
        p_hd.font.size = Pt(14)
        p_hd.font.bold = True
        p_hd.font.color.rgb = COLOR_ACCENT_BLUE

        for line in text_d.split("\n"):
            p_ld = tf_d.add_paragraph()
            p_ld.text = "• " + line
            p_ld.font.size = Pt(11)
            p_ld.font.color.rgb = RGBColor(51, 65, 85)
            p_ld.space_before = Pt(4)

    add_notes(s10,
        "WHAT TO SAY (FINAL WRAP-UP):\n"
        "To conclude our Review 3 presentation, we have satisfied all 8 directives from our supervisor:\n"
        "1. Complete research manuscript in both Word (.docx) and LaTeX (.tex) reframing the research as a high-value negative result.\n"
        "2. A clean, leakage-free codebase with streaming PCAP processing.\n"
        "3. A 16-test automated unit testing suite that passes in 3.3 seconds.\n"
        "4. A public GitHub repository with a Dockerfile ready for one-command replication.\n"
        "We thank you for your guidance and welcome any questions from the panel."
    )

    # Save to all target paths
    for path in PPTX_OUTPUTS:
        prs.save(path)
        print(f"[SUCCESS] Saved clean presentation to: {path}")

if __name__ == "__main__":
    build_presentation()
