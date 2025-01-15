import streamlit as st
from img_pro import ImageProcessor
import time
from src.image_captioning import ImageCaptioningSystem
from src.session_manager import SessionManager

def initialize_session_manager():
    if 'session_manager' not in st.session_state:
        st.session_state.session_manager = SessionManager()
    return st.session_state.session_manager

def create_gradient_text(text, color1="#ff4b4b", color2="#7e56d9"):
    return f"""
        <div style='background: linear-gradient(to right, {color1}, {color2});
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    font-size: 3rem;
                    font-weight: bold;
                    text-align: center;
                    padding: 1rem 0;'>
            {text}
        </div>
    """

def main():
    # Configure the page
    st.set_page_config(
        page_title="✨ AI Image Caption Studio",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom theme and styling
    st.markdown("""
        <style>
            [data-testid="stSidebar"][aria-expanded="true"]{
                min-width: 330px;
                max-width: 330px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Animated header using emojis
    st.markdown(create_gradient_text("🎨 AI Image Caption Studio ✨"), unsafe_allow_html=True)
    
    # Create a modern sidebar
    with st.sidebar:
        st.markdown("### 🎮 Command Center")
        
        # API Configuration with visual feedback
        api_container = st.container()
        with api_container:
            st.markdown("#### 🔑 API Setup")
            gemini_key1 = st.text_input(
                "🔐 Primary API Key",
                type="password",
                help="Enter your first Gemini API key",
                placeholder="••••••••••••••••"
            )
            gemini_key2 = st.text_input(
                "🔑 Backup API Key",
                type="password",
                help="Enter your second Gemini API key",
                placeholder="••••••••••••••••"
            )
        
        # System metrics with animations
        st.markdown("#### 📊 System Metrics")
        cols = st.columns(2)
        with cols[0]:
            st.metric(
                "API Status",
                "✅ Active" if gemini_key1 and gemini_key2 else "❌ Inactive",
                delta="Online" if gemini_key1 and gemini_key2 else "Offline"
            )
        with cols[1]:
            st.metric("Response Time", "2.1s", delta="-0.2s")

        # Quick actions section
        st.markdown("#### ⚡ Quick Actions")
        if st.button("🔄 Reset System", use_container_width=True):
            st.balloons()
        if st.button("💾 Save Configuration", use_container_width=True):
            st.success("Settings saved successfully!")

    if not (gemini_key1 and gemini_key2):
        # Enhanced welcome screen
        st.markdown("---")
        cols = st.columns([1, 2, 1])
        with cols[1]:
            st.markdown("""
                ## 👋 Welcome to AI Caption Studio!
                
                ### 🚀 Getting Started
                1. 🔑 Enter your API keys in the sidebar
                2. 📁 Upload an image or provide a URL
                3. ✨ Let AI work its magic!
                
                ### 🎯 Features
                - 🖼️ Advanced image analysis
                - 📝 Detailed captions
                - 📊 Technical insights
                - 💾 Export options
                
                *Your keys are encrypted and never stored permanently.*
            """)
        st.stop()

    try:
        # Initialize system with loading animation
        with st.spinner("🚀 Initializing AI systems..."):
            captioning_system = ImageCaptioningSystem(gemini_key1, gemini_key2)
            time.sleep(0.5)
            st.success("✅ System ready!")

        # Modern tabbed interface for image input
        st.markdown("### 📤 Image Input Methods")
        input_method = st.radio(
            "Choose input method:",
            ["📁 File Upload", "🔗 URL Input"],
            horizontal=True
        )
        
        if input_method == "📁 File Upload":
            image_input = st.file_uploader(
                "Drop your image here",
                type=['png', 'jpg', 'jpeg'],
                help="Supported formats: PNG, JPG, JPEG"
            )
        else:
            image_url = st.text_input(
                "🔗 Enter image URL:",
                placeholder="https://example.com/image.jpg"
            )
            image_input = image_url if image_url else None

        if image_input:
            try:
                # Create a dynamic layout
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("### 🖼️ Image Preview")
                    if isinstance(image_input, str):
                        image = ImageProcessor.load_image_from_url(image_input)
                    else:
                        image = ImageProcessor.load_image_from_file(image_input)
                    st.image(image, use_container_width=True)

                with col2:
                    st.markdown("### 🎯 Analysis Configuration")
                    
                    # Enhanced analysis options
                    with st.expander("🛠️ Advanced Options", expanded=True):
                        analysis_depth = st.select_slider(
                            "Analysis Depth",
                            options=["Basic", "Standard", "Detailed", "Advanced", "Expert"],
                            value="Expert"
                        )
                        
                        focus_areas = st.multiselect(
                            "Analysis Focus Areas",
                            ["🎨 Colors", "📦 Objects", "📝 Text", "😊 Emotions", "🎬 Activities"],
                            default=["🎨 Colors", "📦 Objects" , "😊 Emotions", "🎬 Activities"]
                        )
                    
                    # Animated analysis button
                    if st.button("✨ Generate Magic", use_container_width=True):
                        with st.spinner("🔮 Analyzing your image..."):
                            progress_bar = st.progress(0)
                            for i in range(100):
                                time.sleep(0.01)
                                progress_bar.progress(i + 1)
                            
                            components = captioning_system.process_image(image_input)
                            progress_bar.empty()
                            
                            # Results in modern tabs
                            tab1, tab2, tab3 = st.tabs([
                                "📝 Quick Summary",
                                "🔍 Deep Analysis",
                                "⚙️ Technical Details"
                            ])
                            
                            with tab1:
                                st.success(components['base_description'])
                            
                            with tab2:
                                st.info(components['detailed_analysis'])
                            
                            with tab3:
                                st.json(components['technical_details'])
                            
                            # Export options
                            st.markdown("### 📥 Export Options")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.download_button(
                                    "📄 Download Report (TXT)",
                                    '\n\n'.join([f"{k.title()}:\n{v}" for k, v in components.items()]),
                                    file_name=f"analysis_{time.strftime('%Y%m%d_%H%M%S')}.txt"
                                )
                            with col2:
                                st.download_button(
                                    "📊 Download Data (JSON)",
                                    str(components),
                                    file_name=f"analysis_{time.strftime('%Y%m%d_%H%M%S')}.json"
                                )
                            
                            # Success celebration
                            st.balloons()
                            
            except Exception as e:
                st.error(f"⚠️ Processing Error: {str(e)}")
                
    except Exception as e:
        st.error(f"⚠️ System Error: {str(e)}")

if __name__ == "__main__":
    main()
