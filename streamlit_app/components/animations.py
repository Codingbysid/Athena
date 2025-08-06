"""
🎨 Advanced Animations and Interactive Elements
Special effects and animations for Athena Streamlit App
"""

import streamlit as st
import time
import random

def add_floating_particles():
    """Add floating particle animation background"""
    particles_html = """
    <style>
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
        pointer-events: none;
    }
    
    .particle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: #667eea;
        border-radius: 50%;
        opacity: 0.7;
        animation: float 6s infinite ease-in-out;
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px) translateX(0px);
            opacity: 0.7;
        }
        50% {
            transform: translateY(-100px) translateX(50px);
            opacity: 0.3;
        }
    }
    
    .particle:nth-child(1) { left: 10%; animation-delay: 0s; animation-duration: 6s; }
    .particle:nth-child(2) { left: 20%; animation-delay: 1s; animation-duration: 8s; }
    .particle:nth-child(3) { left: 30%; animation-delay: 2s; animation-duration: 7s; }
    .particle:nth-child(4) { left: 40%; animation-delay: 0.5s; animation-duration: 9s; }
    .particle:nth-child(5) { left: 50%; animation-delay: 1.5s; animation-duration: 6s; }
    .particle:nth-child(6) { left: 60%; animation-delay: 3s; animation-duration: 8s; }
    .particle:nth-child(7) { left: 70%; animation-delay: 2.5s; animation-duration: 7s; }
    .particle:nth-child(8) { left: 80%; animation-delay: 0.8s; animation-duration: 9s; }
    .particle:nth-child(9) { left: 90%; animation-delay: 1.8s; animation-duration: 6s; }
    .particle:nth-child(10) { left: 95%; animation-delay: 2.8s; animation-duration: 8s; }
    </style>
    
    <div class="particles">
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
    </div>
    """
    
    st.markdown(particles_html, unsafe_allow_html=True)

def create_countdown_timer(target_value, duration=2):
    """Create animated countdown to a target value"""
    placeholder = st.empty()
    
    steps = 20
    step_size = target_value / steps
    step_duration = duration / steps
    
    for i in range(steps + 1):
        current_value = int(step_size * i)
        placeholder.markdown(f"<h2 style='text-align: center; color: #667eea;'>{current_value}</h2>", 
                           unsafe_allow_html=True)
        time.sleep(step_duration)
    
    return target_value

def add_glowing_border(element_class="glow-element"):
    """Add glowing border animation to elements"""
    glow_css = f"""
    <style>
    .{element_class} {{
        border: 2px solid #667eea;
        border-radius: 15px;
        position: relative;
        overflow: hidden;
    }}
    
    .{element_class}::before {{
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #667eea, #764ba2, #667eea, #764ba2);
        background-size: 400% 400%;
        border-radius: 15px;
        z-index: -1;
        animation: glowing 4s ease-in-out infinite;
    }}
    
    @keyframes glowing {{
        0%, 100% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
    }}
    </style>
    """
    
    st.markdown(glow_css, unsafe_allow_html=True)

def create_pulsing_icon(icon, color="#667eea", size="2rem"):
    """Create a pulsing icon animation"""
    pulsing_html = f"""
    <div style="text-align: center; font-size: {size}; color: {color}; 
                animation: pulse 2s infinite ease-in-out;">
        {icon}
    </div>
    <style>
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); opacity: 1; }}
        50% {{ transform: scale(1.1); opacity: 0.7; }}
    }}
    </style>
    """
    
    return pulsing_html

def create_loading_spinner(text="Processing..."):
    """Create an animated loading spinner"""
    spinner_html = f"""
    <div style="display: flex; align-items: center; justify-content: center; margin: 2rem 0;">
        <div class="spinner"></div>
        <span style="margin-left: 1rem; color: #667eea; font-weight: 500;">{text}</span>
    </div>
    
    <style>
    .spinner {{
        width: 40px;
        height: 40px;
        border: 4px solid #e2e8f0;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    </style>
    """
    
    return spinner_html

def add_scroll_animations():
    """Add scroll-triggered animations"""
    scroll_js = """
    <script>
    // Add intersection observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'slideInUp 0.6s ease-out forwards';
            }
        });
    }, observerOptions);
    
    // Observe all chart containers and cards
    document.querySelectorAll('.chart-container, .feature-card, .metric-card').forEach(el => {
        observer.observe(el);
    });
    </script>
    
    <style>
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
    """
    
    st.markdown(scroll_js, unsafe_allow_html=True)

def create_progress_ring(percentage, size=100, stroke_width=8):
    """Create an animated circular progress ring"""
    radius = (size - stroke_width) / 2
    circumference = 2 * 3.14159 * radius
    offset = circumference - (percentage / 100) * circumference
    
    progress_ring = f"""
    <div style="display: flex; justify-content: center; margin: 1rem 0;">
        <svg width="{size}" height="{size}" style="transform: rotate(-90deg);">
            <circle
                cx="{size/2}"
                cy="{size/2}"
                r="{radius}"
                stroke="#e2e8f0"
                stroke-width="{stroke_width}"
                fill="none"
            />
            <circle
                cx="{size/2}"
                cy="{size/2}"
                r="{radius}"
                stroke="url(#gradient)"
                stroke-width="{stroke_width}"
                fill="none"
                stroke-dasharray="{circumference}"
                stroke-dashoffset="{offset}"
                stroke-linecap="round"
                style="animation: progressRing 2s ease-out forwards;"
            />
            <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
                </linearGradient>
            </defs>
        </svg>
        <div style="position: absolute; margin-top: {size/2-10}px; font-weight: bold; font-size: 1.2rem; color: #667eea;">
            {percentage}%
        </div>
    </div>
    
    <style>
    @keyframes progressRing {{
        from {{
            stroke-dashoffset: {circumference};
        }}
        to {{
            stroke-dashoffset: {offset};
        }}
    }}
    </style>
    """
    
    return progress_ring

def create_typewriter_effect(text, speed=50):
    """Create typewriter effect with cursor"""
    typewriter_html = f"""
    <div class="typewriter-container">
        <span class="typewriter-text"></span>
        <span class="cursor">|</span>
    </div>
    
    <style>
    .typewriter-container {{
        font-size: 1.2rem;
        color: #64748b;
        text-align: center;
        margin: 2rem 0;
    }}
    
    .cursor {{
        animation: blink 1s infinite;
        color: #667eea;
        font-weight: bold;
    }}
    
    @keyframes blink {{
        0%, 50% {{ opacity: 1; }}
        51%, 100% {{ opacity: 0; }}
    }}
    </style>
    
    <script>
    (function() {{
        const text = "{text}";
        const speed = {speed};
        const typewriterElement = document.querySelector('.typewriter-text');
        let i = 0;
        
        function typeWriter() {{
            if (i < text.length) {{
                typewriterElement.innerHTML += text.charAt(i);
                i++;
                setTimeout(typeWriter, speed);
            }}
        }}
        
        typeWriter();
    }})();
    </script>
    """
    
    return typewriter_html

def add_hover_effects():
    """Add advanced hover effects to interactive elements"""
    hover_css = """
    <style>
    /* Enhanced button hover effects */
    .stButton > button {
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    /* Card hover effects */
    .feature-card, .metric-card, .chart-container {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .feature-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.3);
    }
    
    .chart-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
    }
    
    /* Ripple effect on click */
    .ripple {
        position: relative;
        overflow: hidden;
    }
    
    .ripple::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(102, 126, 234, 0.3);
        transform: translate(-50%, -50%);
        animation: ripple 0.6s ease-out;
    }
    
    @keyframes ripple {
        to {
            width: 300px;
            height: 300px;
            opacity: 0;
        }
    }
    </style>
    """
    
    st.markdown(hover_css, unsafe_allow_html=True)

def create_success_animation(message="Success!", duration=3):
    """Create success animation with confetti effect"""
    success_html = f"""
    <div class="success-container">
        <div class="success-checkmark">
            <div class="check-icon">
                <span class="icon-line line-tip"></span>
                <span class="icon-line line-long"></span>
                <div class="icon-circle"></div>
                <div class="icon-fix"></div>
            </div>
        </div>
        <h3 style="text-align: center; color: #10b981; margin-top: 1rem;">{message}</h3>
    </div>
    
    <style>
    .success-container {{
        text-align: center;
        padding: 2rem;
        animation: successPop 0.6s ease-out;
    }}
    
    .success-checkmark {{
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: inline-block;
        stroke-width: 2;
        stroke: #10b981;
        stroke-miterlimit: 10;
        box-shadow: inset 0px 0px 0px #10b981;
        animation: checkmarkFill 0.4s ease-in-out 0.4s forwards, checkmarkScale 0.3s ease-in-out 0.9s both;
    }}
    
    .check-icon {{
        width: 80px;
        height: 80px;
        position: relative;
        border-radius: 50%;
        box-sizing: border-box;
        border: 2px solid #10b981;
    }}
    
    .icon-line {{
        height: 2px;
        background: #10b981;
        display: block;
        border-radius: 2px;
        position: absolute;
        z-index: 10;
    }}
    
    .line-tip {{
        top: 46px;
        left: 14px;
        width: 25px;
        transform: rotate(45deg);
        animation: checkmarkIconTip 0.75s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
    }}
    
    .line-long {{
        top: 38px;
        right: 8px;
        width: 47px;
        transform: rotate(-45deg);
        animation: checkmarkIconLong 0.75s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
    }}
    
    @keyframes successPop {{
        0% {{ transform: scale(0); opacity: 0; }}
        50% {{ transform: scale(1.1); }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    
    @keyframes checkmarkFill {{
        100% {{ box-shadow: inset 0px 0px 0px 30px #10b981; }}
    }}
    
    @keyframes checkmarkScale {{
        0%, 100% {{ transform: none; }}
        50% {{ transform: scale3d(1.1, 1.1, 1); }}
    }}
    
    @keyframes checkmarkIconTip {{
        0% {{ width: 0; left: 1px; top: 19px; }}
        54% {{ width: 0; left: 1px; top: 19px; }}
        70% {{ width: 50px; left: -8px; top: 37px; }}
        84% {{ width: 17px; left: 21px; top: 48px; }}
        100% {{ width: 25px; left: 14px; top: 45px; }}
    }}
    
    @keyframes checkmarkIconLong {{
        0% {{ width: 0; right: 46px; top: 54px; }}
        65% {{ width: 0; right: 46px; top: 54px; }}
        84% {{ width: 55px; right: 0px; top: 35px; }}
        100% {{ width: 47px; right: 8px; top: 38px; }}
    }}
    </style>
    """
    
    return success_html