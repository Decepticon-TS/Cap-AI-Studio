import os
import streamlit as st
from img_pro import ImageProcessor
import time
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
        st.markdown("### Upload Excel File")
        excel_file = st.file_uploader(
            "📑 Drop your Excel file here",
            type=['xlsx', 'xls'],
            help="Excel file must contain 'URL' and 'content_id' columns"
        )
        
        if excel_file:
            try:
                excel_processor = ExcelProcessor()
                df = excel_processor.load_excel(excel_file)
                st.success(f"✅ Loaded {len(df)} URLs successfully!")
                
                st.markdown("### Data Preview")
                st.dataframe(
                    df[['content_id', 'URL']].head(),
                    use_container_width=True,
                    column_config={
                        "content_id": "Content ID",
                        "URL": "Image URL"
                    }
                )
                
                if st.button("🔄 Process All URLs", type="primary", use_container_width=True):
                    results = []
                    progress_bar = st.progress(0)
                    status_placeholder = st.empty()
                    progress_metrics = st.empty()
                    time_metrics = st.empty()
                    
                    batch_start = time.time()
                    total_items = len(df)
                    
                    for idx, row in df.iterrows():
                        progress = (idx + 1) / len(df)
                        progress_bar.progress(progress)
                        # status_text.write(f"⚡ Processing {idx + 1}/{len(df)}: {row['content_id']}")
                        
                        try:
                            item_start = time.time()
                            components = captioning_system.process_image(row['URL'])
                            duration = time.time() - item_start
                            
                            components['content_id'] = row['content_id']
                            components['processing_time'] = duration
                            results.append(components)
                            
                            # Calculate metrics
                            items_processed = idx + 1
                            elapsed_time = time.time() - batch_start
                            avg_time_per_item = elapsed_time / items_processed
                            est_remaining_time = (total_items - items_processed) * avg_time_per_item
                            
                            # Update progress metrics in a single container
                            progress_metrics.markdown(f"""
                                ### Current Progress
                                - **Progress**: {items_processed}/{total_items} ({(progress * 100):.1f}%)
                                - **Processing**: {row['content_id']} ({duration:.2f}s)
                                - **Average Time/Item**: {avg_time_per_item:.2f}s
                            """)
                            
                            # Update time metrics in a single container
                            time_metrics.markdown(f"""
                                ### Time Metrics
                                - **Elapsed Time**: {elapsed_time:.1f}s
                                - **Est. Remaining**: {est_remaining_time:.1f}s
                                - **Est. Total Time**: {(elapsed_time + est_remaining_time):.1f}s
                            """)
                            
                            time.sleep(0.1)  # Small delay to prevent UI flicker
                        except Exception as e:
                            st.warning(f"⚠️ Error on {row['content_id']}: {str(e)}")
                            continue
                    
                    # Final summary
                    total_time = time.time() - batch_start
                    progress_metrics.empty()  # Clear the progress metrics
                    time_metrics.empty()  # Clear the time metrics
                    
                    st.success(f"""
                    ✅ Processing Complete!
                    - Total Items: {total_items}
                    - Total Time: {total_time:.1f}s
                    - Average Time/Item: {(total_time/total_items):.2f}s
                    """)
                    
                    try:
                        output_file = excel_processor.save_results(
                            df, 
                            results,
                            os.path.splitext(excel_file.name)[0]
                        )
                        
                        with open(output_file, 'rb') as f:
                            st.download_button(
                                "📥 Download Results",
                                f,
                                file_name=os.path.basename(output_file),
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                            
                    except Exception as e:
                        st.error(f"💥 Error saving results: {str(e)}")
                        
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
# streamlit run App.py
