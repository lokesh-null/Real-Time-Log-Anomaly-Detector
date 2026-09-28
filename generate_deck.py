import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Base directory for images
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMG_OVERVIEW = os.path.join(BASE_DIR, "WhatsApp Image 2026-09-28 at 16.25.01.jpeg")
IMG_LIVE_CHART = os.path.join(BASE_DIR, "WhatsApp Image 2026-09-28 at 16.25.01 (1).jpeg")
IMG_ALERTS = os.path.join(BASE_DIR, "WhatsApp Image 2026-09-28 at 16.25.01 (2).jpeg")
IMG_CONSOLE = os.path.join(BASE_DIR, "WhatsApp Image 2026-09-28 at 16.25.01 (3).jpeg")
IMG_HEALTH = os.path.join(BASE_DIR, "WhatsApp Image 2026-09-28 at 16.25.01 (4).jpeg")

# Color Palette Constants
BG_DARK = RGBColor(10, 14, 29)          # Deep Cyber Obsidian #0A0E1D
BG_CARD = RGBColor(18, 25, 48)          # Glassmorphic Card #121930
BG_CARD_LIGHT = RGBColor(26, 36, 68)    # Lighter Container #1A2444
BG_CARD_ACCENT = RGBColor(15, 23, 42)   # Slate Navy #0F172A

CYAN = RGBColor(44, 182, 125)           # Electric Emerald/Cyan #2CB67D
CYAN_BRIGHT = RGBColor(56, 189, 248)    # Neon Sky Blue #38BDF8
NEON_BLUE = RGBColor(59, 130, 246)      # Royal Blue #3B82F6
PURPLE = RGBColor(168, 85, 247)         # Violet/Purple #A855F7
ALERT_RED = RGBColor(239, 68, 68)       # Crimson Alert #EF4444
ALERT_RED_BG = RGBColor(69, 10, 10)     # Dark Red Fill #450A0A
WARNING_AMBER = RGBColor(245, 158, 11)  # Amber Warning #F59E0B
TEXT_WHITE = RGBColor(248, 250, 252)    # Crisp Off-White #F8FAFC
TEXT_MUTED = RGBColor(148, 163, 184)    # Cool Gray #94A3B8
TEXT_DARK = RGBColor(15, 23, 42)        # Dark Slate for light badges
BORDER_SUBTLE = RGBColor(38, 51, 86)    # Border Outline #263356
BORDER_CYAN = RGBColor(56, 189, 248)    # Accent Border #38BDF8
BORDER_EMERALD = RGBColor(44, 182, 125) # Emerald Border #2CB67D
BORDER_RED = RGBColor(239, 68, 68)      # Red Border #EF4444
BORDER_PURPLE = RGBColor(168, 85, 247)  # Purple Border #A855F7
CREAM_ACCENT = RGBColor(252, 241, 208)  # Warm Cream #FCF1D0

FONT_MAIN = "Segoe UI"
FONT_CODE = "Consolas"

def create_deck(output_path="Log_Sentinel_Deck_With_Images.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, tag_text, title_text, slide_num=None):
        add_slide_background(slide)
        
        # Subtle top glowing bar
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.04))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = CYAN_BRIGHT
        top_bar.line.fill.background()

        # Tag pill
        tag_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.55), Inches(3.2), Inches(0.32))
        tag_box.fill.solid()
        tag_box.fill.fore_color.rgb = BG_CARD_LIGHT
        tag_box.line.color.rgb = BORDER_CYAN
        tag_box.line.width = Pt(1)
        tf_tag = tag_box.text_frame
        tf_tag.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_tag.margin_top = Inches(0.02)
        tf_tag.margin_bottom = Inches(0.02)
        tf_tag.margin_left = Inches(0.1)
        tf_tag.margin_right = Inches(0.1)
        p_tag = tf_tag.paragraphs[0]
        p_tag.alignment = PP_ALIGN.CENTER
        r_tag = p_tag.add_run()
        r_tag.text = tag_text.upper()
        r_tag.font.name = FONT_MAIN
        r_tag.font.size = Pt(9.5)
        r_tag.font.bold = True
        r_tag.font.color.rgb = CYAN_BRIGHT

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(11.733), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = Inches(0)
        tf_title.margin_top = Inches(0)
        p_title = tf_title.paragraphs[0]
        r_title = p_title.add_run()
        r_title.text = title_text
        r_title.font.name = FONT_MAIN
        r_title.font.size = Pt(22)
        r_title.font.bold = True
        r_title.font.color.rgb = TEXT_WHITE

        # Footer
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.35))
        tf_foot = footer_box.text_frame
        tf_foot.margin_left = Inches(0)
        tf_foot.margin_top = Inches(0)
        p_foot = tf_foot.paragraphs[0]
        
        r_foot_left = p_foot.add_run()
        r_foot_left.text = "LOG SENTINEL  //  ACENTRA HACKATHON 2026  //  THE LIABILITIES"
        r_foot_left.font.name = FONT_MAIN
        r_foot_left.font.size = Pt(9)
        r_foot_left.font.color.rgb = TEXT_MUTED

        if slide_num:
            r_foot_num = p_foot.add_run()
            r_foot_num.text = f"                                                                                                              SLIDE {slide_num:02d} / 12"
            r_foot_num.font.name = FONT_MAIN
            r_foot_num.font.size = Pt(9)
            r_foot_num.font.bold = True
            r_foot_num.font.color.rgb = CYAN_BRIGHT

    def add_image_card(slide, img_path, left, top, width, height, border_color, caption=None):
        # Card container with glowing border
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD_LIGHT
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        # Inset image slightly inside the card container
        img_left = left + Inches(0.08)
        img_top = top + Inches(0.08)
        img_w = width - Inches(0.16)
        img_h = height - Inches(0.38 if caption else 0.16)

        if os.path.exists(img_path):
            slide.shapes.add_picture(img_path, img_left, img_top, img_w, img_h)

        if caption:
            c_box = slide.shapes.add_textbox(left, top + height - Inches(0.32), width, Inches(0.28))
            tf_c = c_box.text_frame
            tf_c.margin_left = Inches(0.1)
            tf_c.margin_top = Inches(0)
            p_c = tf_c.paragraphs[0]
            p_c.alignment = PP_ALIGN.CENTER
            r_c = p_c.add_run()
            r_c.text = caption
            r_c.font.name = FONT_MAIN
            r_c.font.size = Pt(8.5)
            r_c.font.bold = True
            r_c.font.color.rgb = border_color

    # ==========================================
    # SLIDE 1: Title Slide (Hero)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    add_slide_background(s1)

    glow_bg = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.6), Inches(11.733), Inches(6.3))
    glow_bg.fill.solid()
    glow_bg.fill.fore_color.rgb = BG_CARD
    glow_bg.line.color.rgb = BORDER_SUBTLE
    glow_bg.line.width = Pt(1.5)

    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(1.0), Inches(4.8), Inches(0.36))
    pill.fill.solid()
    pill.fill.fore_color.rgb = BG_CARD_LIGHT
    pill.line.color.rgb = CYAN_BRIGHT
    pill.line.width = Pt(1)
    tf_pill = pill.text_frame
    tf_pill.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_p = tf_pill.paragraphs[0]
    p_p.alignment = PP_ALIGN.CENTER
    r_p = p_p.add_run()
    r_p.text = "ACENTRA HACKATHON 2026  •  CLOUD OBSERVABILITY / AI-OPS"
    r_p.font.name = FONT_MAIN
    r_p.font.size = Pt(10)
    r_p.font.bold = True
    r_p.font.color.rgb = CYAN_BRIGHT

    t_box = s1.shapes.add_textbox(Inches(1.3), Inches(1.45), Inches(10.7), Inches(1.2))
    tf_t = t_box.text_frame
    p_t = tf_t.paragraphs[0]
    r_t = p_t.add_run()
    r_t.text = "LOG SENTINEL"
    r_t.font.name = FONT_MAIN
    r_t.font.size = Pt(44)
    r_t.font.bold = True
    r_t.font.color.rgb = TEXT_WHITE

    sub_box = s1.shapes.add_textbox(Inches(1.3), Inches(2.55), Inches(10.7), Inches(0.6))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    r_sub = p_sub.add_run()
    r_sub.text = "Sub-Second Statistical Log Anomaly Detection & Real-Time Incident Response Engine"
    r_sub.font.name = FONT_MAIN
    r_sub.font.size = Pt(16)
    r_sub.font.bold = True
    r_sub.font.color.rgb = CYAN_BRIGHT

    feats = [
        ("⚡ < 100ms Latency", "Non-blocking async tailing"),
        ("🧠 Dynamic Z-Score", "Self-adapting rolling baseline"),
        ("🔄 Self-Healing Engine", "Zero-human incident recovery"),
        ("🌐 Production NGINX", "Tested with real microservices")
    ]
    for i, (title, desc) in enumerate(feats):
        x = Inches(1.3 + i * 2.7)
        c_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(3.25), Inches(2.55), Inches(0.95))
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = BG_CARD_LIGHT
        c_box.line.color.rgb = BORDER_CYAN
        c_box.line.width = Pt(1)
        tf_c = c_box.text_frame
        tf_c.margin_left = Inches(0.12)
        tf_c.margin_right = Inches(0.12)
        tf_c.margin_top = Inches(0.1)
        
        p1 = tf_c.paragraphs[0]
        r1 = p1.add_run()
        r1.text = title
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.color.rgb = TEXT_WHITE
        
        p2 = tf_c.add_paragraph()
        r2 = p2.add_run()
        r2.text = desc
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_MUTED

    team_bg = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(4.45), Inches(10.733), Inches(2.0))
    team_bg.fill.solid()
    team_bg.fill.fore_color.rgb = BG_CARD_ACCENT
    team_bg.line.color.rgb = BORDER_PURPLE
    team_bg.line.width = Pt(1)
    
    t_lbl = s1.shapes.add_textbox(Inches(1.5), Inches(4.55), Inches(4.0), Inches(0.3))
    tf_tl = t_lbl.text_frame
    p_tl = tf_tl.paragraphs[0]
    r_tl = p_tl.add_run()
    r_tl.text = "ENGINEERED BY TEAM : THE LIABILITIES"
    r_tl.font.name = FONT_MAIN
    r_tl.font.size = Pt(10)
    r_tl.font.bold = True
    r_tl.font.color.rgb = PURPLE

    members = [
        ("Lokesh R", "System Architect & Integration Lead", "Architecture & Real E-Commerce Services"),
        ("Jashwanth B", "Anomaly Engine & Statistical Models", "Z-Score Engine, Sliding Window & Hysteresis"),
        ("Harish Neralla", "Observability UI & Dashboard", "React/Vite Glassmorphism & Recharts Telemetry"),
        ("Tejeshwar Senthilkumar", "AWS SNS Pipeline & Simulation", "Async Cloud Dispatcher & Chaos Blaster")
    ]

    for i, (name, role, task) in enumerate(members):
        x = Inches(1.5 + i * 2.58)
        m_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(4.9), Inches(2.45), Inches(1.35))
        m_box.fill.solid()
        m_box.fill.fore_color.rgb = BG_CARD_LIGHT
        m_box.line.color.rgb = BORDER_SUBTLE
        m_box.line.width = Pt(1)
        tf_m = m_box.text_frame
        tf_m.margin_left = Inches(0.1)
        tf_m.margin_right = Inches(0.1)
        tf_m.margin_top = Inches(0.08)

        p1 = tf_m.paragraphs[0]
        r1 = p1.add_run()
        r1.text = name
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.color.rgb = TEXT_WHITE

        p2 = tf_m.add_paragraph()
        r2 = p2.add_run()
        r2.text = role
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(9)
        r2.font.bold = True
        r2.font.color.rgb = CYAN_BRIGHT

        p3 = tf_m.add_paragraph()
        r3 = p3.add_run()
        r3.text = task
        r3.font.name = FONT_MAIN
        r3.font.size = Pt(8)
        r3.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 2: The Problem (Observability Lag)
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "01 // THE CHALLENGE", "The Problem: Observability Lag in High-Throughput Modern Systems", 2)

    top_ctx = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(0.75))
    top_ctx.fill.solid()
    top_ctx.fill.fore_color.rgb = BG_CARD
    top_ctx.line.color.rgb = BORDER_RED
    top_ctx.line.width = Pt(1)
    tf_ctx = top_ctx.text_frame
    tf_ctx.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_ctx.margin_left = Inches(0.2)
    p_ctx = tf_ctx.paragraphs[0]
    r_ctx1 = p_ctx.add_run()
    r_ctx1.text = "THE INDUSTRY DILEMMA: "
    r_ctx1.font.name = FONT_MAIN
    r_ctx1.font.size = Pt(11)
    r_ctx1.font.bold = True
    r_ctx1.font.color.rgb = ALERT_RED

    r_ctx2 = p_ctx.add_run()
    r_ctx2.text = "In high-traffic systems (E-Commerce, FinTech, SaaS), every minute of downtime costs thousands of dollars. Traditional observability stacks fail during flash crashes."
    r_ctx2.font.name = FONT_MAIN
    r_ctx2.font.size = Pt(11)
    r_ctx2.font.color.rgb = TEXT_WHITE

    cards_data = [
        ("01. High MTTD (Alert Lag)", ALERT_RED, BORDER_RED, [
            ("Batch Polling Delays:", "Traditional log analyzers (ELK / CloudWatch) run batch queries on 1 to 5 minute cron intervals."),
            ("Blind Spot During Outages:", "By the time an alert fires 3 minutes later, hundreds of shopping carts are abandoned and thousands of dollars lost."),
            ("Slow Incident Discovery:", "Mean Time To Detect (MTTD) remains in minutes instead of sub-seconds.")
        ]),
        ("02. Alert Fatigue & False Alarms", WARNING_AMBER, WARNING_AMBER, [
            ("Static Thresholds Fail:", "Rigid rules (e.g. 'errors > 50') trigger false alarms during legitimate traffic peaks or miss errors in low-volume hours."),
            ("Alert Desensitization:", "On-call engineers get overwhelmed by false positives and begin ignoring critical warnings."),
            ("No Statistical Context:", "Lack of rolling variance and baseline normalization.")
        ]),
        ("03. Heavy Ingestion Overhead", PURPLE, BORDER_PURPLE, [
            ("Cloud Transport Latency:", "Shipping terabytes of raw logs across the internet introduces network buffer delays."),
            ("Extreme Egress Costs:", "Massive cloud bills simply to ship raw unparsed text logs to third-party SaaS platforms."),
            ("Single Point of Failure:", "If external logging ingestion stalls, production teams are completely blind.")
        ])
    ]

    for i, (ctitle, accent_col, border_col, bullets) in enumerate(cards_data):
        x = Inches(0.8 + i * 4.0)
        c_shape = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.55), Inches(3.75), Inches(3.3))
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = BG_CARD
        c_shape.line.color.rgb = border_col
        c_shape.line.width = Pt(1.5)
        tf = c_shape.text_frame
        tf.margin_left = Inches(0.18)
        tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.18)

        p_t = tf.paragraphs[0]
        r_t = p_t.add_run()
        r_t.text = ctitle
        r_t.font.name = FONT_MAIN
        r_t.font.size = Pt(13)
        r_t.font.bold = True
        r_t.font.color.rgb = accent_col

        p_div = tf.add_paragraph()
        p_div.space_after = Pt(6)

        for b_title, b_desc in bullets:
            p_b = tf.add_paragraph()
            p_b.space_after = Pt(6)
            
            rb1 = p_b.add_run()
            rb1.text = f"• {b_title} "
            rb1.font.name = FONT_MAIN
            rb1.font.size = Pt(9.5)
            rb1.font.bold = True
            rb1.font.color.rgb = TEXT_WHITE

            rb2 = p_b.add_run()
            rb2.text = b_desc
            rb2.font.name = FONT_MAIN
            rb2.font.size = Pt(9.5)
            rb2.font.color.rgb = TEXT_MUTED

    q_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.7))
    q_box.fill.solid()
    q_box.fill.fore_color.rgb = BG_CARD_LIGHT
    q_box.line.color.rgb = CYAN_BRIGHT
    q_box.line.width = Pt(1)
    tf_q = q_box.text_frame
    tf_q.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_q.margin_left = Inches(0.2)
    p_q = tf_q.paragraphs[0]
    rq1 = p_q.add_run()
    rq1.text = "THE CORE QUESTION: "
    rq1.font.name = FONT_MAIN
    rq1.font.size = Pt(11)
    rq1.font.bold = True
    rq1.font.color.rgb = CYAN_BRIGHT

    rq2 = p_q.add_run()
    rq2.text = "How can engineering teams detect payment gateway outages (504s) and database deadlocks within 1 second of occurrence without expensive cloud telemetry?"
    rq2.font.name = FONT_MAIN
    rq2.font.size = Pt(11)
    rq2.font.italic = True
    rq2.font.color.rgb = TEXT_WHITE

    # ==========================================
    # SLIDE 3: The Solution (Log Sentinel)
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "02 // THE SOLUTION", "Log Sentinel: Local-First Streaming Statistical Observability", 3)

    sol_banner = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(0.7))
    sol_banner.fill.solid()
    sol_banner.fill.fore_color.rgb = BG_CARD
    sol_banner.line.color.rgb = BORDER_CYAN
    sol_banner.line.width = Pt(1)
    tf_sb = sol_banner.text_frame
    tf_sb.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_sb.margin_left = Inches(0.2)
    p_sb = tf_sb.paragraphs[0]
    r_sb1 = p_sb.add_run()
    r_sb1.text = "WHAT IS LOG SENTINEL? "
    r_sb1.font.name = FONT_MAIN
    r_sb1.font.size = Pt(11)
    r_sb1.font.bold = True
    r_sb1.font.color.rgb = CYAN_BRIGHT
    
    r_sb2 = p_sb.add_run()
    r_sb2.text = "A lightweight, streaming observability engine that performs continuous sliding-window statistical anomaly detection on live production server logs."
    r_sb2.font.name = FONT_MAIN
    r_sb2.font.size = Pt(11)
    r_sb2.font.color.rgb = TEXT_WHITE

    sol_pillars = [
        ("⚡ Sub-Second Latency (< 100ms)", CYAN_BRIGHT, BORDER_CYAN, [
            ("Non-Blocking File Tailer:", "Directly tails local server access logs as OS disk writes occur."),
            ("Zero Cloud Transport Delay:", "Detects spikes at the ingestion point before forwarding."),
            ("Sub-15ms Detection:", "Instantaneous evaluation of every new log batch.")
        ]),
        ("🧠 Dynamic Z-Score Baseline", CYAN, BORDER_EMERALD, [
            ("Self-Adapting Statistical Baseline:", "Continuously updates rolling mean and standard deviation."),
            ("Suppresses False Alarms:", "Adapts to natural traffic dips (nighttime) and normal busy spikes."),
            ("Dynamic Sensitivity:", "Triggers based on relative deviation (sigma) rather than arbitrary magic numbers.")
        ]),
        ("🔄 Self-Healing State Machine", PURPLE, BORDER_PURPLE, [
            ("Automated Lifecycle:", "Tracks NORMAL → WARNING → HIGH → CRITICAL → RECOVERY."),
            ("Zero-Human Reset:", "Automatically returns to NORMAL once clean traffic flushes the rolling buffer."),
            ("Hysteresis Protection:", "Enforces sustained recovery before resetting alerts to avoid flap cycles.")
        ]),
        ("🌐 Live Real-World Validation", WARNING_AMBER, WARNING_AMBER, [
            ("Real Production NGINX (Port 8080):", "Captures genuine Combined Log Format requests."),
            ("CloudMart E-Commerce Service (5001):", "Real microservice with products, orders, and payment endpoints."),
            ("Live Chaos Fault Injection:", "Simulates real Stripe 504 timeouts & DB crashes on demand.")
        ])
    ]

    for i, (stitle, scolor, sborder, sbullets) in enumerate(sol_pillars):
        row = i // 2
        col = i % 2
        x = Inches(0.8 + col * 6.0)
        y = Inches(2.45 + row * 2.25)
        
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.733), Inches(2.1))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = sborder
        card.line.width = Pt(1.5)
        tf = card.text_frame
        tf.margin_left = Inches(0.18)
        tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.14)

        p_t = tf.paragraphs[0]
        r_t = p_t.add_run()
        r_t.text = stitle
        r_t.font.name = FONT_MAIN
        r_t.font.size = Pt(12.5)
        r_t.font.bold = True
        r_t.font.color.rgb = scolor

        for btitle, bdesc in sbullets:
            p_b = tf.add_paragraph()
            p_b.space_before = Pt(3)
            rb1 = p_b.add_run()
            rb1.text = f"• {btitle} "
            rb1.font.name = FONT_MAIN
            rb1.font.size = Pt(9.5)
            rb1.font.bold = True
            rb1.font.color.rgb = TEXT_WHITE

            rb2 = p_b.add_run()
            rb2.text = bdesc
            rb2.font.name = FONT_MAIN
            rb2.font.size = Pt(9)
            rb2.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 4: System Architecture & End-to-End Pipeline
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "03 // SYSTEM ARCHITECTURE", "End-to-End Real-Time Ingestion & Alerting Pipeline", 4)

    pipeline_steps = [
        ("1. Traffic Source", "Real Users &\nChaos Blaster", "HTTP Requests\n(200 / 502 / 504)", BG_CARD_LIGHT, CYAN_BRIGHT),
        ("2. NGINX Proxy", "Port 8080\nReverse Proxy", "Writes Combined\nLog Format", BG_CARD_LIGHT, CYAN_BRIGHT),
        ("3. Async Tailer", "FastAPI Port 8000\nBackground Task", "Non-blocking\nShared File Read", BG_CARD_LIGHT, NEON_BLUE),
        ("4. Anomaly Engine", "Z-Score & Rolling\nSliding Window", "Calculates Error Rate\n& Sigma Deviation", BG_CARD_LIGHT, PURPLE),
    ]

    for i, (step_title, step_tech, step_detail, bg_c, border_c) in enumerate(pipeline_steps):
        x = Inches(0.8 + i * 2.5)
        box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.65), Inches(2.2), Inches(2.5))
        box.fill.solid()
        box.fill.fore_color.rgb = BG_CARD
        box.line.color.rgb = border_c
        box.line.width = Pt(1.5)
        tf = box.text_frame
        tf.margin_left = Inches(0.12)
        tf.margin_right = Inches(0.12)
        tf.margin_top = Inches(0.12)

        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = step_title
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.color.rgb = border_c

        p2 = tf.add_paragraph()
        p2.space_before = Pt(8)
        r2 = p2.add_run()
        r2.text = step_tech
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(10)
        r2.font.bold = True
        r2.font.color.rgb = TEXT_WHITE

        p3 = tf.add_paragraph()
        p3.space_before = Pt(8)
        r3 = p3.add_run()
        r3.text = step_detail
        r3.font.name = FONT_MAIN
        r3.font.size = Pt(8.5)
        r3.font.color.rgb = TEXT_MUTED

        if i < 3:
            arrow = s4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(3.05 + i * 2.5), Inches(2.75), Inches(0.2), Inches(0.3))
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = CYAN_BRIGHT
            arrow.line.fill.background()

    arr_a = s4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(10.55), Inches(2.1), Inches(0.2), Inches(0.25))
    arr_a.fill.solid()
    arr_a.fill.fore_color.rgb = CYAN_BRIGHT
    arr_a.line.fill.background()

    box_5a = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.8), Inches(1.65), Inches(1.733), Inches(1.18))
    box_5a.fill.solid()
    box_5a.fill.fore_color.rgb = BG_CARD
    box_5a.line.color.rgb = CYAN_BRIGHT
    box_5a.line.width = Pt(1.5)
    tf_5a = box_5a.text_frame
    tf_5a.margin_left = Inches(0.1)
    tf_5a.margin_top = Inches(0.08)
    p_5a = tf_5a.paragraphs[0]
    r_5a1 = p_5a.add_run()
    r_5a1.text = "5A. WebSocket /ws\n"
    r_5a1.font.name = FONT_MAIN
    r_5a1.font.size = Pt(9.5)
    r_5a1.font.bold = True
    r_5a1.font.color.rgb = CYAN_BRIGHT
    r_5a2 = p_5a.add_run()
    r_5a2.text = "React Dashboard\n(Port 5173 - Sub-100ms)"
    r_5a2.font.name = FONT_MAIN
    r_5a2.font.size = Pt(8.5)
    r_5a2.font.color.rgb = TEXT_WHITE

    arr_b = s4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(10.55), Inches(3.5), Inches(0.2), Inches(0.25))
    arr_b.fill.solid()
    arr_b.fill.fore_color.rgb = ALERT_RED
    arr_b.line.fill.background()

    box_5b = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.8), Inches(2.97), Inches(1.733), Inches(1.18))
    box_5b.fill.solid()
    box_5b.fill.fore_color.rgb = BG_CARD
    box_5b.line.color.rgb = ALERT_RED
    box_5b.line.width = Pt(1.5)
    tf_5b = box_5b.text_frame
    tf_5b.margin_left = Inches(0.1)
    tf_5b.margin_top = Inches(0.08)
    p_5b = tf_5b.paragraphs[0]
    r_5b1 = p_5b.add_run()
    r_5b1.text = "5B. AWS SNS Push\n"
    r_5b1.font.name = FONT_MAIN
    r_5b1.font.size = Pt(9.5)
    r_5b1.font.bold = True
    r_5b1.font.color.rgb = ALERT_RED
    r_5b2 = p_5b.add_run()
    r_5b2.text = "Cloud Alerting\n(Thread Pool Isolated)"
    r_5b2.font.name = FONT_MAIN
    r_5b2.font.size = Pt(8.5)
    r_5b2.font.color.rgb = TEXT_WHITE

    c1 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.35), Inches(5.733), Inches(2.35))
    c1.fill.solid()
    c1.fill.fore_color.rgb = BG_CARD
    c1.line.color.rgb = BORDER_CYAN
    c1.line.width = Pt(1)
    tf_c1 = c1.text_frame
    tf_c1.margin_left = Inches(0.18)
    tf_c1.margin_right = Inches(0.18)
    tf_c1.margin_top = Inches(0.14)
    p1 = tf_c1.paragraphs[0]
    r1 = p1.add_run()
    r1.text = "⚡ High-Throughput Async Non-Blocking File Tailer"
    r1.font.name = FONT_MAIN
    r1.font.size = Pt(11.5)
    r1.font.bold = True
    r1.font.color.rgb = CYAN_BRIGHT

    bullets_c1 = [
        ("Lock-Free Shared File Stream:", "Tails logs directly via Windows-compliant shared read handles without interfering with NGINX write locks."),
        ("Zero Busy-Waiting:", "Uses asynchronous polling with backoff yielding to conserve 99% CPU during idle traffic."),
        ("Universal Ingestion API:", "Also exposes POST /api/v1/logs for direct OpenTelemetry / FluentBit push ingestion.")
    ]
    for btitle, bdesc in bullets_c1:
        pb = tf_c1.add_paragraph()
        pb.space_before = Pt(3)
        rb1 = pb.add_run()
        rb1.text = f"• {btitle} "
        rb1.font.name = FONT_MAIN
        rb1.font.size = Pt(9)
        rb1.font.bold = True
        rb1.font.color.rgb = TEXT_WHITE
        rb2 = pb.add_run()
        rb2.text = bdesc
        rb2.font.name = FONT_MAIN
        rb2.font.size = Pt(8.5)
        rb2.font.color.rgb = TEXT_MUTED

    c2 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.35), Inches(5.733), Inches(2.35))
    c2.fill.solid()
    c2.fill.fore_color.rgb = BG_CARD
    c2.line.color.rgb = BORDER_RED
    c2.line.width = Pt(1)
    tf_c2 = c2.text_frame
    tf_c2.margin_left = Inches(0.18)
    tf_c2.margin_right = Inches(0.18)
    tf_c2.margin_top = Inches(0.14)
    p2 = tf_c2.paragraphs[0]
    r2 = p2.add_run()
    r2.text = "🛡️ Thread-Isolated Cloud Dispatcher (Zero Block)"
    r2.font.name = FONT_MAIN
    r2.font.size = Pt(11.5)
    r2.font.bold = True
    r2.font.color.rgb = ALERT_RED

    bullets_c2 = [
        ("asyncio.to_thread Isolation:", "AWS Boto3 API calls run on separate background thread workers; cloud latency NEVER blocks the real-time event loop."),
        ("Sub-100ms WebSocket Sync:", "WebSocket broadcaster streams raw telemetry directly into React UI without waiting for SNS responses."),
        ("Zero-Crash Cloud Fallback:", "If AWS credentials are missing, system auto-activates zero-crash AWS Simulator Mode.")
    ]
    for btitle, bdesc in bullets_c2:
        pb = tf_c2.add_paragraph()
        pb.space_before = Pt(3)
        rb1 = pb.add_run()
        rb1.text = f"• {btitle} "
        rb1.font.name = FONT_MAIN
        rb1.font.size = Pt(9)
        rb1.font.bold = True
        rb1.font.color.rgb = TEXT_WHITE
        rb2 = pb.add_run()
        rb2.text = bdesc
        rb2.font.name = FONT_MAIN
        rb2.font.size = Pt(8.5)
        rb2.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 5: Statistical Anomaly Engine (Deep Dive + IMAGE 2: Live Chart)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "04 // STATISTICAL ENGINE", "Mathematical Formulation & Live Telemetry Verification", 5)

    # Left Column: Math & Formulations
    math_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
    math_card.fill.solid()
    math_card.fill.fore_color.rgb = BG_CARD
    math_card.line.color.rgb = BORDER_CYAN
    math_card.line.width = Pt(1.5)
    tf_m = math_card.text_frame
    tf_m.margin_left = Inches(0.18)
    tf_m.margin_right = Inches(0.18)
    tf_m.margin_top = Inches(0.14)

    p_mt = tf_m.paragraphs[0]
    r_mt = p_mt.add_run()
    r_mt.text = "Sliding Window & Statistical Z-Score Formulation"
    r_mt.font.name = FONT_MAIN
    r_mt.font.size = Pt(12)
    r_mt.font.bold = True
    r_mt.font.color.rgb = CYAN_BRIGHT

    p_f1_lbl = tf_m.add_paragraph()
    p_f1_lbl.space_before = Pt(6)
    r = p_f1_lbl.add_run()
    r.text = "1. Instantaneous Window Error Rate:"
    r.font.name = FONT_MAIN
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = TEXT_WHITE

    p_f1 = tf_m.add_paragraph()
    p_f1.space_before = Pt(2)
    r_f1 = p_f1.add_run()
    r_f1.text = "    Error Rate (R_t) = Errors in Window / Total Logs in Window"
    r_f1.font.name = FONT_CODE
    r_f1.font.size = Pt(9)
    r_f1.font.bold = True
    r_f1.font.color.rgb = CREAM_ACCENT

    p_f2_lbl = tf_m.add_paragraph()
    p_f2_lbl.space_before = Pt(6)
    r = p_f2_lbl.add_run()
    r.text = "2. Statistical Deviation (Z-Score):"
    r.font.name = FONT_MAIN
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = TEXT_WHITE

    p_f2 = tf_m.add_paragraph()
    p_f2.space_before = Pt(2)
    r_f2 = p_f2.add_run()
    r_f2.text = "    Deviation (σ) = (Current Rate - Rolling Baseline) / Standard Dev"
    r_f2.font.name = FONT_CODE
    r_f2.font.size = Pt(9)
    r_f2.font.bold = True
    r_f2.font.color.rgb = CREAM_ACCENT

    p_sf_lbl = tf_m.add_paragraph()
    p_sf_lbl.space_before = Pt(8)
    r = p_sf_lbl.add_run()
    r.text = "Four-Tier Severity & Safeguards:"
    r.font.name = FONT_MAIN
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = TEXT_WHITE

    safeguards = [
        ("🟢 NORMAL (σ < 2):", "Baseline continuously adapts to healthy traffic."),
        ("🟡 WARNING (2 ≤ σ < 3):", "Elevated error rate logged to local buffer."),
        ("🟠 HIGH (σ ≥ 3 or >10%):", "Significant statistical anomaly flagged."),
        ("🚨 CRITICAL (σ ≥ 3 & >15%):", "Severe outage; triggers instant AWS SNS push."),
        ("🛡️ Low-Volume Protection:", "Suppresses noise if window count is < 10 logs.")
    ]
    for stitle, sdesc in safeguards:
        p_s = tf_m.add_paragraph()
        p_s.space_before = Pt(2)
        rs1 = p_s.add_run()
        rs1.text = f"• {stitle} "
        rs1.font.name = FONT_MAIN
        rs1.font.size = Pt(8.5)
        rs1.font.bold = True
        rs1.font.color.rgb = CYAN_BRIGHT
        rs2 = p_s.add_run()
        rs2.text = sdesc
        rs2.font.name = FONT_MAIN
        rs2.font.size = Pt(8.5)
        rs2.font.color.rgb = TEXT_MUTED

    # Right Column: Real Live Chart Screenshot (Image 2)
    add_image_card(
        s5, 
        IMG_LIVE_CHART, 
        Inches(6.6), 
        Inches(1.6), 
        Inches(5.933), 
        Inches(5.1), 
        BORDER_CYAN,
        "LIVE TELEMETRY: 15.1% Error Rate Surge vs 0.3% Dynamic Baseline (9.9σ Peak Deviation)"
    )

    # ==========================================
    # SLIDE 6: Real Target Integration (NGINX & CloudMart)
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "05 // PRODUCTION TARGET", "Battle-Tested with Real NGINX & E-Commerce Microservice", 6)

    r_banner = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(0.65))
    r_banner.fill.solid()
    r_banner.fill.fore_color.rgb = BG_CARD
    r_banner.line.color.rgb = BORDER_CYAN
    r_banner.line.width = Pt(1)
    tf_rb = r_banner.text_frame
    tf_rb.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_rb.margin_left = Inches(0.2)
    p_rb = tf_rb.paragraphs[0]
    r_rb1 = p_rb.add_run()
    r_rb1.text = "NO MOCKED DATA: "
    r_rb1.font.name = FONT_MAIN
    r_rb1.font.size = Pt(11)
    r_rb1.font.bold = True
    r_rb1.font.color.rgb = CYAN_BRIGHT
    r_rb2 = p_rb.add_run()
    r_rb2.text = "Log Sentinel runs against a genuine local multi-service architecture with real TCP networking and disk I/O."
    r_rb2.font.name = FONT_MAIN
    r_rb2.font.size = Pt(11)
    r_rb2.font.color.rgb = TEXT_WHITE

    targets = [
        ("Official NGINX Web Server (Port 8080)", CYAN_BRIGHT, BORDER_CYAN, [
            ("Standard Reverse Proxy:", "Listens on port 8080 and proxies traffic to backend microservices."),
            ("Combined Log Format:", "Emits production standard access logs with client IP, timestamp, method, status code, and latency."),
            ("Direct Disk Writing:", "Writes to logs/app.log concurrently while Sentinel tails without locking.")
        ]),
        ("CloudMart E-Commerce API (Port 5001)", CYAN, BORDER_EMERALD, [
            ("Standalone Microservice:", "Production-ready FastAPI service modeling modern e-commerce operations."),
            ("Real Business Endpoints:", "Serves /api/products, /api/orders, /api/payments, and /api/auth."),
            ("Realistic Latencies:", "Simulates realistic database query latency (~4ms to 120ms).")
        ]),
        ("Universal Ingestion API (POST /api/v1/logs)", PURPLE, BORDER_PURPLE, [
            ("OTel / FluentBit Ready:", "Accepts batch and single JSON log payloads from any modern collector."),
            ("Multi-Source Support:", "Can ingest Kubernetes pod logs, Docker stdout, and syslog streams simultaneously."),
            ("Stateless Ingestion:", "Parses and routes logs to the anomaly pipeline in < 1ms per event.")
        ]),
        ("Chaos Injection Engine", ALERT_RED, BORDER_RED, [
            ("One-Click Outage Trigger:", "Simulates catastrophic infrastructure failures on demand during live demos."),
            ("Stripe 504 Gateway Timeout:", "Emulates 3rd-party payment provider outage during peak shopping."),
            ("PostgreSQL Deadlock (500):", "Simulates database connection pool exhaustion and transaction lockups.")
        ])
    ]

    for i, (ttitle, tcolor, tborder, tbullets) in enumerate(targets):
        row = i // 2
        col = i % 2
        x = Inches(0.8 + col * 6.0)
        y = Inches(2.4 + row * 2.3)
        
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.733), Inches(2.15))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = tborder
        card.line.width = Pt(1.5)
        tf = card.text_frame
        tf.margin_left = Inches(0.18)
        tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.14)

        p_t = tf.paragraphs[0]
        r_t = p_t.add_run()
        r_t.text = ttitle
        r_t.font.name = FONT_MAIN
        r_t.font.size = Pt(12)
        r_t.font.bold = True
        r_t.font.color.rgb = tcolor

        for btitle, bdesc in tbullets:
            p_b = tf.add_paragraph()
            p_b.space_before = Pt(3)
            rb1 = p_b.add_run()
            rb1.text = f"• {btitle} "
            rb1.font.name = FONT_MAIN
            rb1.font.size = Pt(9.5)
            rb1.font.bold = True
            rb1.font.color.rgb = TEXT_WHITE

            rb2 = p_b.add_run()
            rb2.text = bdesc
            rb2.font.name = FONT_MAIN
            rb2.font.size = Pt(9)
            rb2.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 7: Live Frontend Observability Dashboard (IMAGE 1: Overview Dashboard)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "06 // FRONTEND OBSERVABILITY", "Real-Time React + Vite Glassmorphic Dashboard", 7)

    # Left Column: Features & Highlights
    dash_card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.1))
    dash_card.fill.solid()
    dash_card.fill.fore_color.rgb = BG_CARD
    dash_card.line.color.rgb = BORDER_CYAN
    dash_card.line.width = Pt(1.5)
    tf_dc = dash_card.text_frame
    tf_dc.margin_left = Inches(0.18)
    tf_dc.margin_right = Inches(0.18)
    tf_dc.margin_top = Inches(0.14)

    p_dct = tf_dc.paragraphs[0]
    r_dct = p_dct.add_run()
    r_dct.text = "Observability UI Modules"
    r_dct.font.name = FONT_MAIN
    r_dct.font.size = Pt(12.5)
    r_dct.font.bold = True
    r_dct.font.color.rgb = CYAN_BRIGHT

    dash_items = [
        ("🎮 Live Chaos Controller:", "One-click triggers for Normal Traffic, Stripe 504 Timeout, DB Deadlock, and Recovery."),
        ("📈 Dual-Line Area Chart:", "80-point rolling history displaying Error Rate area vs Baseline dashed line at 60 FPS."),
        ("📋 Real-Time Alert Feed:", "Timestamped incident audit trail with root-cause identification (`psycopg2.operationalerror`)."),
        ("⚡ Sub-100ms WebSocket Sync:", "Instant push synchronization between FastAPI backend and React frontend."),
        ("🛍️ Interactive Storefront Tab:", "Embedded store allowing judges to click 'Buy Now' to generate live TCP access logs.")
    ]

    for btitle, bdesc in dash_items:
        pb = tf_dc.add_paragraph()
        pb.space_before = Pt(6)
        rb1 = pb.add_run()
        rb1.text = f"• {btitle} "
        rb1.font.name = FONT_MAIN
        rb1.font.size = Pt(9)
        rb1.font.bold = True
        rb1.font.color.rgb = TEXT_WHITE
        rb2 = pb.add_run()
        rb2.text = bdesc
        rb2.font.name = FONT_MAIN
        rb2.font.size = Pt(8.5)
        rb2.font.color.rgb = TEXT_MUTED

    # Right Column: Actual Overview Dashboard Screenshot (Image 1)
    add_image_card(
        s7,
        IMG_OVERVIEW,
        Inches(5.8),
        Inches(1.6),
        Inches(6.733),
        Inches(5.1),
        BORDER_CYAN,
        "PRODUCTION UI: Real-Time Overview Dashboard (Rate: 15.1% | Baseline: 0.3% | Deviation: 9.9σ | Status: HIGH)"
    )

    # ==========================================
    # SLIDE 8: Enterprise Alerting & AWS SNS (IMAGE 3: Alerts History)
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "07 // ENTERPRISE ALERTING", "Asynchronous AWS SNS Cloud Notification Pipeline", 8)

    # Left Column: Alerting Architecture
    c_left8 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.1))
    c_left8.fill.solid()
    c_left8.fill.fore_color.rgb = BG_CARD
    c_left8.line.color.rgb = BORDER_RED
    c_left8.line.width = Pt(1.5)
    tf_l8 = c_left8.text_frame
    tf_l8.margin_left = Inches(0.18)
    tf_l8.margin_right = Inches(0.18)
    tf_l8.margin_top = Inches(0.14)

    p_lt8 = tf_l8.paragraphs[0]
    r_lt8 = p_lt8.add_run()
    r_lt8.text = "Enterprise Alerting Architecture"
    r_lt8.font.name = FONT_MAIN
    r_lt8.font.size = Pt(12)
    r_lt8.font.bold = True
    r_lt8.font.color.rgb = ALERT_RED

    l8_items = [
        ("Multi-Tier Notification Fan-Out:", "HIGH and CRITICAL anomalies trigger instant AWS SNS push notifications fanning out to Email, SMS, Slack, and PagerDuty."),
        ("Thread Pool Isolation (`asyncio.to_thread`):", "AWS Boto3 API calls run on background worker threads — AWS network latency NEVER blocks log tailing or WebSocket broadcasts."),
        ("Zero-Crash AWS Simulator Fallback:", "If AWS credentials are missing, system auto-activates zero-crash Simulator Mode with full JSON audit logs."),
        ("Automated Root-Cause Correlation:", "Alert payload flags exact culprit service and exception (`[order-service] psycopg2.operationalerror`).")
    ]
    for btitle, bdesc in l8_items:
        pb = tf_l8.add_paragraph()
        pb.space_before = Pt(6)
        rb1 = pb.add_run()
        rb1.text = f"• {btitle} "
        rb1.font.name = FONT_MAIN
        rb1.font.size = Pt(9)
        rb1.font.bold = True
        rb1.font.color.rgb = TEXT_WHITE
        rb2 = pb.add_run()
        rb2.text = bdesc
        rb2.font.name = FONT_MAIN
        rb2.font.size = Pt(8.5)
        rb2.font.color.rgb = TEXT_MUTED

    # Right Column: Actual Alerts Audit History Screenshot (Image 3)
    add_image_card(
        s8,
        IMG_ALERTS,
        Inches(5.8),
        Inches(1.6),
        Inches(6.733),
        Inches(5.1),
        BORDER_RED,
        "INCIDENT AUDIT TRAIL: 40 Live Anomaly Alerts with Exact Root Cause & Statistical Scores"
    )

    # ==========================================
    # SLIDE 9: Live Demo Walkthrough (IMAGE 5: System Health & State Machine)
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "08 // LIVE DEMO FLOW", "The Winning Live Demo Walkthrough (The 4-Minute Story)", 9)

    # Left Column: 4 Acts Breakdown
    acts_card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.1))
    acts_card.fill.solid()
    acts_card.fill.fore_color.rgb = BG_CARD
    acts_card.line.color.rgb = BORDER_PURPLE
    acts_card.line.width = Pt(1.5)
    tf_ac = acts_card.text_frame
    tf_ac.margin_left = Inches(0.18)
    tf_ac.margin_right = Inches(0.18)
    tf_ac.margin_top = Inches(0.14)

    p_act = tf_ac.paragraphs[0]
    r_act = p_act.add_run()
    r_act.text = "4-Minute Live Narrative"
    r_act.font.name = FONT_MAIN
    r_act.font.size = Pt(12)
    r_act.font.bold = True
    r_act.font.color.rgb = PURPLE

    act_list = [
        ("🟢 ACT 1: Normal Traffic (0:00 - 1:00)", "Shoppers browse CloudMart; NGINX returns 200 OK (latency ~4ms). Dashboard baseline flatlines at 0.0%."),
        ("🚨 ACT 2: Black Friday Outage (1:00 - 2:15)", "Stripe 504 timeout injected; in <500ms error rate surges to 80% and Sentinel transitions to HIGH/CRITICAL."),
        ("🔄 ACT 3: Self-Healing Recovery (2:15 - 3:15)", "Traffic recovers; clean logs flush the rolling window. System smoothly resets to NORMAL automatically."),
        ("💳 ACT 4: Judge Interaction (3:15 - 4:00)", "Judge clicks 'Buy Now' on embedded store; live TCP request registers on NGINX and flashes on dashboard.")
    ]
    for atitle, adesc in act_list:
        pb = tf_ac.add_paragraph()
        pb.space_before = Pt(6)
        rb1 = pb.add_run()
        rb1.text = f"{atitle}\n"
        rb1.font.name = FONT_MAIN
        rb1.font.size = Pt(9)
        rb1.font.bold = True
        rb1.font.color.rgb = CYAN_BRIGHT
        rb2 = pb.add_run()
        rb2.text = adesc
        rb2.font.name = FONT_MAIN
        rb2.font.size = Pt(8.5)
        rb2.font.color.rgb = TEXT_MUTED

    # Right Column: Actual System Health & State Transitions Screenshot (Image 5)
    add_image_card(
        s9,
        IMG_HEALTH,
        Inches(5.8),
        Inches(1.6),
        Inches(6.733),
        Inches(5.1),
        BORDER_PURPLE,
        "STATE MACHINE TELEMETRY: Automatic Transitions from WARNING (16:20:34) to HIGH (16:20:37) & Uptime Tracking"
    )

    # ==========================================
    # SLIDE 10: Technical Specifications & Verification (IMAGE 4: Log Console)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "09 // QUALITY ASSURANCE", "Benchmarked Performance & 100% Test Coverage", 10)

    # Left Column: Performance Metrics & Verification
    qa_col = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.1))
    qa_col.fill.solid()
    qa_col.fill.fore_color.rgb = BG_CARD
    qa_col.line.color.rgb = BORDER_CYAN
    qa_col.line.width = Pt(1.5)
    tf_qac = qa_col.text_frame
    tf_qac.margin_left = Inches(0.18)
    tf_qac.margin_right = Inches(0.18)
    tf_qac.margin_top = Inches(0.14)

    p_qt = tf_qac.paragraphs[0]
    r_qt = p_qt.add_run()
    r_qt.text = "Benchmarked Performance & QA"
    r_qt.font.name = FONT_MAIN
    r_qt.font.size = Pt(12)
    r_qt.font.bold = True
    r_qt.font.color.rgb = CYAN_BRIGHT

    stats = [
        ("⚡ < 15ms Latency:", "From disk write to anomaly calculation."),
        ("🚀 Sub-100ms Sync:", "Real-time WebSocket frame rate."),
        ("🧪 100% Passing Tests:", "10 comprehensive Pytest detector test cases."),
        ("🔒 Shared File Concurrency:", "Tested high-rate simultaneous write and read on Windows OS.")
    ]
    for stitle, sdesc in stats:
        pb = tf_qac.add_paragraph()
        pb.space_before = Pt(6)
        rb1 = pb.add_run()
        rb1.text = f"{stitle} "
        rb1.font.name = FONT_MAIN
        rb1.font.size = Pt(9.5)
        rb1.font.bold = True
        rb1.font.color.rgb = TEXT_WHITE
        rb2 = pb.add_run()
        rb2.text = sdesc
        rb2.font.name = FONT_MAIN
        rb2.font.size = Pt(8.5)
        rb2.font.color.rgb = TEXT_MUTED

    pb_more = tf_qac.add_paragraph()
    pb_more.space_before = Pt(8)
    r_m = pb_more.add_run()
    r_m.text = "✔ Automated Flap Damping Safeguards\n✔ Thread Isolation Under Simulated Network Drops\n✔ Zero-Error Production Vite Build"
    r_m.font.name = FONT_MAIN
    r_m.font.size = Pt(8.5)
    r_m.font.color.rgb = CYAN_BRIGHT

    # Right Column: Actual Log Console Streaming Screenshot (Image 4)
    add_image_card(
        s10,
        IMG_CONSOLE,
        Inches(5.8),
        Inches(1.6),
        Inches(6.733),
        Inches(5.1),
        BORDER_CYAN,
        "REAL STREAMING LOG CONSOLE: 312 Events Processed | 200 Entries Buffer | Real-Time Root Cause Stacks"
    )

    # ==========================================
    # SLIDE 11: Business Impact & Future Roadmap
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "10 // IMPACT & ROADMAP", "Enterprise Business Value & Next-Gen Capabilities", 11)

    b_card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.733), Inches(5.1))
    b_card.fill.solid()
    b_card.fill.fore_color.rgb = BG_CARD
    b_card.line.color.rgb = BORDER_EMERALD
    b_card.line.width = Pt(1.5)
    tf_b = b_card.text_frame
    tf_b.margin_left = Inches(0.18)
    tf_b.margin_right = Inches(0.18)
    tf_b.margin_top = Inches(0.16)

    p_bt = tf_b.paragraphs[0]
    r_bt = p_bt.add_run()
    r_bt.text = "Measurable Business Impact"
    r_bt.font.name = FONT_MAIN
    r_bt.font.size = Pt(12.5)
    r_bt.font.bold = True
    r_bt.font.color.rgb = CYAN

    b_items = [
        ("📉 MTTD Reduced from Minutes to < 100ms:", "Enables immediate automatic failovers and saves thousands of dollars in lost transactions during payment outages."),
        ("🛡️ Revenue Protection During Checkout Outages:", "Detects Stripe 504 and payment gateway failures before customers bounce to competitors."),
        ("🛑 Eliminates On-Call Alert Fatigue:", "Dynamic rolling Z-Score baseline suppresses noisy false alarms caused by expected traffic fluctuations."),
        ("💰 90% Cost Reduction vs Cloud Ingestion:", "Eliminates massive cloud logging egress and storage bills by performing statistical detection at the source.")
    ]
    for btitle, bdesc in b_items:
        pb = tf_b.add_paragraph()
        pb.space_before = Pt(8)
        rb1 = pb.add_run()
        rb1.text = f"• {btitle}\n   "
        rb1.font.name = FONT_MAIN
        rb1.font.size = Pt(9.5)
        rb1.font.bold = True
        rb1.font.color.rgb = TEXT_WHITE
        rb2 = pb.add_run()
        rb2.text = bdesc
        rb2.font.name = FONT_MAIN
        rb2.font.size = Pt(9)
        rb2.font.color.rgb = TEXT_MUTED

    r_card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.1))
    r_card.fill.solid()
    r_card.fill.fore_color.rgb = BG_CARD
    r_card.line.color.rgb = BORDER_PURPLE
    r_card.line.width = Pt(1.5)
    tf_r = r_card.text_frame
    tf_r.margin_left = Inches(0.18)
    tf_r.margin_right = Inches(0.18)
    tf_r.margin_top = Inches(0.16)

    p_rt = tf_r.paragraphs[0]
    r_rt = p_rt.add_run()
    r_rt.text = "Future Technical Roadmap"
    r_rt.font.name = FONT_MAIN
    r_rt.font.size = Pt(12.5)
    r_rt.font.bold = True
    r_rt.font.color.rgb = PURPLE

    r_items = [
        ("Horizon 1: 🛰️ Distributed Ingestion Scale:", "Integrate Apache Kafka and Redis Streams clustering to scale log ingestion to 1,000,000+ logs/second across distributed server farms."),
        ("Horizon 2: 🤖 AI-Powered Root Cause Explanations:", "Attach an LLM agent to inspect anomalous stack traces and auto-generate pull request bug fixes and rollback suggestions in real time."),
        ("Horizon 3: ☸️ Kubernetes Operator & Auto-Remediation:", "Trigger automated pod restarts, circuit breaker tripwires, and traffic rerouting upon CRITICAL anomaly detection.")
    ]
    for btitle, bdesc in r_items:
        pb = tf_r.add_paragraph()
        pb.space_before = Pt(8)
        rb1 = pb.add_run()
        rb1.text = f"• {btitle}\n   "
        rb1.font.name = FONT_MAIN
        rb1.font.size = Pt(9.5)
        rb1.font.bold = True
        rb1.font.color.rgb = TEXT_WHITE
        rb2 = pb.add_run()
        rb2.text = bdesc
        rb2.font.name = FONT_MAIN
        rb2.font.size = Pt(9)
        rb2.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 12: Conclusion & Q&A
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    add_slide_background(s12)

    glow_bg12 = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.6), Inches(11.733), Inches(6.3))
    glow_bg12.fill.solid()
    glow_bg12.fill.fore_color.rgb = BG_CARD
    glow_bg12.line.color.rgb = BORDER_CYAN
    glow_bg12.line.width = Pt(1.5)

    pill12 = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(0.95), Inches(3.8), Inches(0.35))
    pill12.fill.solid()
    pill12.fill.fore_color.rgb = BG_CARD_LIGHT
    pill12.line.color.rgb = CYAN_BRIGHT
    pill12.line.width = Pt(1)
    tf_p12 = pill12.text_frame
    tf_p12.vertical_anchor = MSO_ANCHOR.MIDDLE
    p12 = tf_p12.paragraphs[0]
    p12.alignment = PP_ALIGN.CENTER
    r12 = p12.add_run()
    r12.text = "CONCLUSION  •  SUMMARY & LIVE ACCESS"
    r12.font.name = FONT_MAIN
    r12.font.size = Pt(10)
    r12.font.bold = True
    r12.font.color.rgb = CYAN_BRIGHT

    t_box12 = s12.shapes.add_textbox(Inches(1.3), Inches(1.35), Inches(10.7), Inches(0.8))
    tf_t12 = t_box12.text_frame
    p_t12 = tf_t12.paragraphs[0]
    r_t12 = p_t12.add_run()
    r_t12.text = "LOG SENTINEL"
    r_t12.font.name = FONT_MAIN
    r_t12.font.size = Pt(36)
    r_t12.font.bold = True
    r_t12.font.color.rgb = TEXT_WHITE

    q_box12 = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(2.2), Inches(10.733), Inches(0.85))
    q_box12.fill.solid()
    q_box12.fill.fore_color.rgb = BG_CARD_LIGHT
    q_box12.line.color.rgb = BORDER_EMERALD
    q_box12.line.width = Pt(1)
    tf_qb12 = q_box12.text_frame
    tf_qb12.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_qb12.margin_left = Inches(0.2)
    p_qb12 = tf_qb12.paragraphs[0]
    r_q1 = p_qb12.add_run()
    r_q1.text = "“ Log Sentinel bridges the gap between raw server logs and instantaneous incident response with statistical precision and zero cloud overhead. ”"
    r_q1.font.name = FONT_MAIN
    r_q1.font.size = Pt(12)
    r_q1.font.bold = True
    r_q1.font.italic = True
    r_q1.font.color.rgb = TEXT_WHITE

    endpoints = [
        ("React Observability UI", "http://localhost:5173/", "Live Dark Glassmorphic Dashboard"),
        ("NGINX Web Server", "http://127.0.0.1:8080/", "Production Reverse Proxy"),
        ("CloudMart Microservice", "http://127.0.0.1:5001/", "Standalone E-Commerce API"),
        ("Backend & API Docs", "http://127.0.0.1:8000/docs", "FastAPI Engine & Swagger Docs")
    ]

    for i, (svc, url, sdesc) in enumerate(endpoints):
        x = Inches(1.3 + i * 2.7)
        e_box = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(3.2), Inches(2.55), Inches(1.35))
        e_box.fill.solid()
        e_box.fill.fore_color.rgb = BG_CARD_LIGHT
        e_box.line.color.rgb = BORDER_CYAN
        e_box.line.width = Pt(1)
        tf_e = e_box.text_frame
        tf_e.margin_left = Inches(0.12)
        tf_e.margin_right = Inches(0.12)
        tf_e.margin_top = Inches(0.1)

        p1 = tf_e.paragraphs[0]
        r1 = p1.add_run()
        r1.text = svc
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(10.5)
        r1.font.bold = True
        r1.font.color.rgb = TEXT_WHITE

        p2 = tf_e.add_paragraph()
        p2.space_before = Pt(3)
        r2 = p2.add_run()
        r2.text = url
        r2.font.name = FONT_CODE
        r2.font.size = Pt(8.5)
        r2.font.bold = True
        r2.font.color.rgb = CYAN_BRIGHT

        p3 = tf_e.add_paragraph()
        p3.space_before = Pt(3)
        r3 = p3.add_run()
        r3.text = sdesc
        r3.font.name = FONT_MAIN
        r3.font.size = Pt(8)
        r3.font.color.rgb = TEXT_MUTED

    ty_banner = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(4.75), Inches(10.733), Inches(1.8))
    ty_banner.fill.solid()
    ty_banner.fill.fore_color.rgb = BG_CARD_ACCENT
    ty_banner.line.color.rgb = BORDER_PURPLE
    ty_banner.line.width = Pt(1.5)
    tf_ty = ty_banner.text_frame
    tf_ty.margin_left = Inches(0.2)
    tf_ty.margin_top = Inches(0.15)

    p_ty1 = tf_ty.paragraphs[0]
    p_ty1.alignment = PP_ALIGN.CENTER
    r_ty1 = p_ty1.add_run()
    r_ty1.text = "THANK YOU!"
    r_ty1.font.name = FONT_MAIN
    r_ty1.font.size = Pt(24)
    r_ty1.font.bold = True
    r_ty1.font.color.rgb = TEXT_WHITE

    p_ty2 = tf_ty.add_paragraph()
    p_ty2.alignment = PP_ALIGN.CENTER
    p_ty2.space_before = Pt(4)
    r_ty2 = p_ty2.add_run()
    r_ty2.text = "We welcome your questions and invite you to test live chaos injection on the dashboard."
    r_ty2.font.name = FONT_MAIN
    r_ty2.font.size = Pt(12)
    r_ty2.font.bold = True
    r_ty2.font.color.rgb = CYAN_BRIGHT

    p_ty3 = tf_ty.add_paragraph()
    p_ty3.alignment = PP_ALIGN.CENTER
    p_ty3.space_before = Pt(6)
    r_ty3 = p_ty3.add_run()
    r_ty3.text = "Team The Liabilities: Lokesh R  •  Jashwanth B  •  Harish Neralla  •  Tejeshwar Senthilkumar"
    r_ty3.font.name = FONT_MAIN
    r_ty3.font.size = Pt(9.5)
    r_ty3.font.color.rgb = TEXT_MUTED

    # Try saving to primary and fallback
    try:
        prs.save(output_path)
        print(f"Presentation successfully created at: {output_path}")
    except Exception as e:
        fallback = "Log_Sentinel_Presentation_With_Screenshots.pptx"
        prs.save(fallback)
        print(f"Primary save locked ({e}). Saved to: {fallback}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "Log_Sentinel_Deck_With_Images.pptx"
    create_deck(out)
