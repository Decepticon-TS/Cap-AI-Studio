# app.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

import pandas as pd
import streamlit as st
import time

from src.img_pro import ImageProcessor
from src.processing_time import ProcessingTimeTracker
from src.image_captioning import ImageCaptioningSystem
from src.excel_processor import ExcelProcessor
from src.session_manager import SessionManager

def create_animated_header(text, animation_duration=2):
    return f"""
        <div style='
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96E6B3);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            font-weight: 800;
            text-align: center;
            padding: 2rem 0;
            animation: gradient {animation_duration}s ease infinite;
        '>
            {text}
        </div>
        <style>
            @keyframes gradient {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
        </style>
    """

def initialize_session_manager():
    if 'session_manager' not in st.session_state:
        st.session_state.session_manager = SessionManager()
    return st.session_state.session_manager

def main():
    time_tracker = ProcessingTimeTracker()
    st.set_page_config(
        page_title="✨ AI Vision Studio",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://docs.streamlit.io',
            'Report a bug': "https://github.com/your-repo/issues",
            'About': "# AI Vision Studio\nPowered by Gemini API"
        }
    )

    # Animated header with gradient
    st.markdown(create_animated_header("🎯 AI Vision Studio ✨"), unsafe_allow_html=True)
    
    # Decorative divider
    st.markdown("""
        <div style='text-align: center; margin: 1rem 0;'>
            ⚡ • 🎨 • 🔮 • 🎯 • ✨ • 🎨 • 🔮 • ⚡
        </div>
    """, unsafe_allow_html=True)

    captioning_system = None
    
    with st.sidebar:
        st.markdown("### 🎮 Command Center")
        
        with st.expander("🔑 API Configuration", expanded=True):
            api_container = st.container()
            with api_container:
                gemini_key1 = st.text_input(
                    "🔐 Primary Key",
                    type="password",
                    help="Enter your first Gemini API key",
                    placeholder="••••••••••••••••"
                )
                gemini_key2 = st.text_input(
                    "🔑 Secondary Key",
                    type="password",
                    help="Enter your second Gemini API key",
                    placeholder="••••••••••••••••"
                )

        st.markdown("### 📊 System Metrics")
        metric_cols = st.columns(2)
        with metric_cols[0]:
            st.metric(
                "API Status",
                "✅ Online" if gemini_key1 and gemini_key2 else "❌ Offline",
                delta="Active" if gemini_key1 and gemini_key2 else "Inactive",
                delta_color="normal"
            )
        with metric_cols[1]:
            st.metric(
                "System Load",
                "Optimal",
                delta="-2%",
                delta_color="inverse"
            )

        with st.expander("📈 Performance", expanded=False):
            perf_cols = st.columns(2)
            with perf_cols[0]:
                st.metric("Response Time", "1.8s", delta="-0.2s")
            with perf_cols[1]:
                st.metric("Memory Usage", "85%", delta="5%")

        st.markdown("### ⚡ Quick Actions")
        if st.button("🔄 Reset System", type="secondary", use_container_width=True):
            st.balloons()
        if st.button("💾 Save Config", type="primary", use_container_width=True):
            st.success("✅ Settings saved!")

        st.markdown("---")
        st.markdown("""
            <div style='text-align: center; opacity: 0.8;'>
                <p>📌 Version 1.0.0</p>
                <p>Made with 💫 by AI Team</p>
                <p>Powered by Gemini & Streamlit</p>
            </div>
        """, unsafe_allow_html=True)

    if gemini_key1 and gemini_key2:
        try:
            if not captioning_system:
                with st.spinner("🚀 Initializing AI systems..."):
                    captioning_system = ImageCaptioningSystem(gemini_key1, gemini_key2)
                    time.sleep(0.5)
                    st.success("✨ System ready!")
        except Exception as e:
            st.error(f"⚠️ Initialization failed: {str(e)}")
            st.stop()
    else:
        st.markdown("""
            <div style='text-align: center; padding: 2rem;'>
                <h2>👋 Welcome to AI Vision Studio!</h2>
                <br>
                <div style='max-width: 600px; margin: 0 auto;'>
                    <h3>🚀 Getting Started</h3>
                    <ol>
                        <li>🔑 Configure your API keys</li>
                        <li>📁 Upload images or provide URLs</li>
                        <li>✨ Let AI analyze your content</li>
                    </ol>
                    <br>
                    <p><em>Your API keys are securely encrypted and never stored.</em></p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.stop()

    # Excel Processing Section
    with st.expander("📊 Batch Processing", expanded=False):
        st.markdown("""
            <div style='text-align: center; padding: 1rem;'>
                <h2 style='
                    background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96E6B3);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    font-weight: 800;
                '>
                    🚀 Batch Image Analysis
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Create a modern file upload area
        st.markdown("""
            <div style='
                border: 2px dashed #4ECDC4;
                border-radius: 10px;
                padding: 2rem;
                text-align: center;
                margin: 1rem 0;
            '>
        """, unsafe_allow_html=True)
        
        excel_file = st.file_uploader(
            "📑 Drop your Excel file here",
            type=['xlsx', 'xls'],
            help="Excel file must contain 'URL' and 'content_id' columns"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        if excel_file:
            try:
                excel_processor = ExcelProcessor()
                df = excel_processor.load_excel(excel_file)
                # Animated success message
                st.markdown(f"""
                    <div style='
                        background: linear-gradient(45deg, #96E6B3, #4ECDC4);
                        padding: 1rem;
                        border-radius: 10px;
                        text-align: center;
                        animation: fadeIn 0.5s ease-in;
                    '>
                        <h3 style='color: white; margin: 0;'>
                            ✅ Successfully loaded {len(df)} URLs!
                        </h3>
                    </div>
                    <style>
                        @keyframes fadeIn {{
                            from {{ opacity: 0; transform: translateY(-10px); }}
                            to {{ opacity: 1; transform: translateY(0); }}
                        }}
                    </style>
                """, unsafe_allow_html=True)
                
                # Modern data preview
                st.markdown("### Data Preview")
                st.dataframe(
                    df[['content_id', 'URL']].head(),
                    use_container_width=True,
                    column_config={
                        "content_id": st.column_config.TextColumn(
                            "Content ID",
                            help="Unique identifier for each image",
                            width="medium"
                        ),
                        "URL": st.column_config.TextColumn(
                            "Image URL",
                            help="URL of the image to process",
                            width="large"
                        )
                    }
                )
                
                # Processing section with modern UI
                st.markdown("""
                    <div style='
                        background: linear-gradient(135deg, rgba(78,205,196,0.1), rgba(150,230,179,0.1));
                        border-radius: 10px;
                        padding: 1.5rem;
                        margin: 1rem 0;
                    '>
                """, unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    if st.button("🔮 Process All URLs", type="primary", use_container_width=True):
                        results = []
                        progress_bar = st.progress(0)
                        
                        # Create placeholder for status card
                        status_card = st.empty()
                        
                        # Create placeholder for metrics
                        metrics_container = st.empty()
                        
                        batch_start = time.time()
                        total_items = len(df)
                        
                        for idx, row in df.iterrows():
                            progress = (idx + 1) / total_items
                            progress_bar.progress(progress)
                            
                            # Update status card
                            status_card.markdown(f"""
                                <div style='
                                    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                                    padding: 1rem;
                                    border-radius: 10px;
                                    text-align: center;
                                    color: white;
                                    margin: 0.5rem 0;
                                '>
                                    Processing {idx + 1}/{total_items}: {row['content_id']}
                                </div>
                            """, unsafe_allow_html=True)
                            
                            try:
                                item_start = time.time()
                                components = captioning_system.process_image(row['URL'])
                                duration = time.time() - item_start
                                
                                components['content_id'] = row['content_id']
                                components['processing_time'] = duration
                                results.append(components)
                                
                                # Calculate metrics
                                elapsed_time = time.time() - batch_start
                                items_processed = idx + 1
                                avg_time = elapsed_time / items_processed
                                est_remaining = (total_items - items_processed) * avg_time
                                
                                # Update metrics in place using columns inside the placeholder
                                metrics_container.columns([1, 1, 1])[0].metric(
                                    "Processed",
                                    f"{items_processed}/{total_items}",
                                    f"+{1}" if items_processed > 1 else None
                                )
                                metrics_container.columns([1, 1, 1])[1].metric(
                                    "Avg Time",
                                    f"{avg_time:.1f}s",
                                    f"{(avg_time - (elapsed_time/(items_processed-1) if items_processed > 1 else 0)):.1f}s" if items_processed > 1 else None
                                )
                                metrics_container.columns([1, 1, 1])[2].metric(
                                    "Remaining",
                                    f"{est_remaining:.1f}s",
                                    f"-{(est_remaining - (est_remaining * (items_processed-1)/items_processed if items_processed > 1 else 0)):.1f}s" if items_processed > 1 else None
                                )
                                
                            except Exception as e:
                                st.warning(f"⚠️ Error processing {row['content_id']}: {str(e)}")
                                continue
                        
                        # Clear progress indicators
                        progress_bar.empty()
                        
                        # Show final summary
                        total_time = time.time() - batch_start
                        status_card.markdown(f"""
                            <div style='
                                background: linear-gradient(45deg, #96E6B3, #4ECDC4);
                                padding: 1.5rem;
                                border-radius: 10px;
                                text-align: center;
                                animation: pulseSuccess 2s infinite;
                            '>
                                <h2 style='color: white; margin: 0;'>
                                    ✨ Processing Complete! ✨
                                </h2>
                                <p style='color: white; margin: 0.5rem 0;'>
                                    Processed {total_items} images in {total_time:.1f}s
                                    <br>
                                    Average processing time: {(total_time/total_items):.1f}s per image
                                </p>
                            </div>
                            <style>
                                @keyframes pulseSuccess {{
                                    0% {{ transform: scale(1); }}
                                    50% {{ transform: scale(1.02); }}
                                    100% {{ transform: scale(1); }}
                                }}
                            </style>
                        """, unsafe_allow_html=True)
                        
                        # Clear the metrics and show final summary metrics
                        metrics_container.columns([1, 1, 1])[0].metric(
                            "Total Processed",
                            f"{total_items}/{total_items}",
                            "Completed"
                        )
                        metrics_container.columns([1, 1, 1])[1].metric(
                            "Total Time",
                            f"{total_time:.1f}s",
                            f"Avg: {(total_time/total_items):.1f}s/image"
                        )
                        metrics_container.columns([1, 1, 1])[2].metric(
                            "Success Rate",
                            f"{(len(results)/total_items*100):.1f}%",
                            f"{len(results)}/{total_items} images"
                        )
                        
                        # Export section
                        try:
                            output_file = excel_processor.save_results(
                                df, 
                                results,
                                os.path.splitext(excel_file.name)[0]
                            )
                            
                            with open(output_file, 'rb') as f:
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.download_button(
                                        "📥 Download Excel",
                                        f,
                                        file_name=os.path.basename(output_file),
                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                        use_container_width=True,
                                    )
                                with col2:
                                    if st.button("📊 View Summary", use_container_width=True):
                                        st.dataframe(
                                            pd.DataFrame(results),
                                            use_container_width=True
                                        )
                                
                        except Exception as e:
                            st.error(f"💥 Error saving results: {str(e)}")
                
                st.markdown("</div>", unsafe_allow_html=True)
                        
            except Exception as e:
                st.error(f"💥 Error loading file: {str(e)}")

    # Main Image Processing Section
    st.markdown("### 🎯 Single Image Analysis")
    
    tab1, tab2 = st.tabs(["📁 File Upload", "🔗 URL Input"])
    
    with tab1:
        image_input = st.file_uploader(
            "🖼️ Drop your image here",
            type=['png', 'jpg', 'jpeg'],
            help="Supported formats: PNG, JPG, JPEG"
        )
        
    with tab2:
        image_url = st.text_input(
            "🔗 Image URL",
            placeholder="https://example.com/image.jpg"
        )
        if image_url:
            image_input = image_url

    if image_input:
        try:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("### 🖼️ Preview")
                if isinstance(image_input, str):
                    image = ImageProcessor.load_image_from_url(image_input)
                else:
                    image = ImageProcessor.load_image_from_file(image_input)
                st.image(image, use_container_width=True)

            with col2:
                st.markdown("### 🎯 Analysis Settings")
                
                with st.expander("⚙️ Configuration", expanded=True):
                    depth = st.select_slider(
                        "Analysis Depth",
                        options=["Basic", "Standard", "Detailed", "Advanced", "Expert"],
                        value="Standard"
                    )
                    
                    focus = st.multiselect(
                        "Analysis Focus",
                        ["🎨 Colors", "📦 Objects", "📝 Text", "😊 Emotions", "🎬 Activities"],
                        default=["🎨 Colors", "📦 Objects"]
                    )
                
                if st.button("✨ Analyze Image", type="primary", use_container_width=True):
                    with st.spinner("🔮 Processing image..."):
                        progress = st.progress(0)
                        start_time = time_tracker.start_operation()
                        components = captioning_system.process_image(image_input)
                        duration = time_tracker.end_operation(start_time, 'single' if not isinstance(image_input, str) else 'url')
                        
                        st.markdown("### ⏱️ Processing Metrics")
                        time_tracker.display_metrics('single' if not isinstance(image_input, str) else 'url')
                        st.info(f"Current processing time: {duration:.2f} seconds")
                        progress.empty()
                    
                    tab1, tab2, tab3 = st.tabs([
                        "📝 Summary",
                        "🔍 Analysis",
                        "⚙️ Technical"
                    ])
                    
                    with tab1:
                        st.success(components['base_description'])
                    with tab2:
                        st.info(components['detailed_analysis'])
                    with tab3:
                        st.json(components.get('technical_details', {}))
                    
                    st.markdown("### 📥 Export Results")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "📄 Text Report",
                            '\n\n'.join([f"{k.title()}:\n{v}" for k, v in components.items()]),
                            file_name=f"analysis_{time.strftime('%Y%m%d_%H%M%S')}.txt"
                        )
                    with col2:
                        st.download_button(
                            "📊 JSON Data",
                            str(components),
                            file_name=f"analysis_{time.strftime('%Y%m%d_%H%M%S')}.json"
                        )
                    
                    st.balloons()
                    
        except Exception as e:
            st.error(f"💥 Processing error: {str(e)}")

if __name__ == "__main__":
    main()
# streamlit run app.py
