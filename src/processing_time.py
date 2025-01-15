import time
import streamlit as st
import numpy as np
from datetime import datetime

class ProcessingTimeTracker:
    """Tracks and manages processing times for different operations"""
    
    def __init__(self):
        if 'processing_times' not in st.session_state:
            st.session_state.processing_times = {
                'single': [],
                'batch': [],
                'url': []
            }
            st.session_state.processing_stats = {
                'total_processed': 0,
                'session_start': datetime.now(),
                'failures': 0
            }
    
    def start_operation(self):
        """Start timing an operation"""
        return time.time()
    
    def end_operation(self, start_time, category):
        """End timing an operation and record its duration"""
        duration = time.time() - start_time
        st.session_state.processing_times[category].append(duration)
        st.session_state.processing_stats['total_processed'] += 1
        return duration
    
    def get_stats(self, category):
        """Calculate statistics for a specific category"""
        times = st.session_state.processing_times[category]
        if not times:
            return {
                'avg': 0,
                'min': 0,
                'max': 0,
                'total': 0,
                'count': 0
            }
        
        return {
            'avg': np.mean(times),
            'min': np.min(times),
            'max': np.max(times),
            'total': np.sum(times),
            'count': len(times)
        }
    
    def record_failure(self):
        """Record a processing failure"""
        st.session_state.processing_stats['failures'] += 1
    
    def display_metrics(self, category):
        """Display processing metrics in Streamlit"""
        stats = self.get_stats(category)
        session_duration = (datetime.now() - st.session_state.processing_stats['session_start']).total_seconds()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Time", f"{stats['avg']:.2f}s", f"{stats['count']} processed")
        col2.metric("Fastest", f"{stats['min']:.2f}s", f"Slowest: {stats['max']:.2f}s")
        col3.metric("Success Rate", 
                   f"{((stats['count'] - st.session_state.processing_stats['failures']) / max(stats['count'], 1) * 100):.1f}%",
                   f"{stats['count']} total")
    
    def display_batch_progress(self, current, total, current_time):
        """Display batch processing progress and estimates"""
        if current > 0:
            avg_time_per_item = current_time / current
            remaining_items = total - current
            estimated_remaining = avg_time_per_item * remaining_items
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Progress", f"{(current/total*100):.1f}%", f"{current}/{total} items")
            with col2:
                st.metric("Est. Remaining", f"{estimated_remaining:.1f}s", f"{avg_time_per_item:.2f}s per item")
