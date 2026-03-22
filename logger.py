"""
Utility for logging AI prompts and responses to Streamlit session state.
"""
import streamlit as st
from typing import Any, Dict
from datetime import datetime


class PromptLogger:
    """Captures and stores prompt execution details in Streamlit session state."""

    @staticmethod
    def initialize():
        """Initialize session state for prompt logs if not exists."""
        if 'prompt_logs' not in st.session_state:
            st.session_state.prompt_logs = []

    @staticmethod
    def log_interaction(
        system_prompt: str,
        user_prompt: str,
        structured_input: Dict[str, Any],
        raw_output: Any,
        model_name: str = "gemini-1.5-flash"
    ):
        """
        Log a complete AI interaction cycle.

        Args:
            system_prompt: The system instructions sent to the model
            user_prompt: The user/task prompt
            structured_input: The PageMetrics data passed to the model
            raw_output: The raw model response before parsing
            model_name: The AI model used
        """
        PromptLogger.initialize()

        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model": model_name,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "structured_input": structured_input,
            "raw_output": str(raw_output)
        }

        st.session_state.prompt_logs.append(log_entry)

    @staticmethod
    def get_logs():
        """Retrieve all logged interactions."""
        PromptLogger.initialize()
        return st.session_state.prompt_logs

    @staticmethod
    def clear_logs():
        """Clear all logged interactions."""
        st.session_state.prompt_logs = []

    @staticmethod
    def display_logs():
        """Display prompt logs in Streamlit UI."""
        logs = PromptLogger.get_logs()

        if not logs:
            st.info("No prompt logs yet. Run an audit to see the reasoning trace.")
            return

        for idx, log in enumerate(logs, 1):
            with st.expander(f"🔍 Interaction {idx} - {log['timestamp']} ({log['model']})"):
                st.markdown("### 📋 System Prompt")
                st.code(log['system_prompt'], language="text")

                st.markdown("### 💬 User Prompt")
                st.code(log['user_prompt'], language="text")

                st.markdown("### 📊 Structured Input (PageMetrics)")
                st.json(log['structured_input'])

                st.markdown("### 🤖 Raw Model Output")
                st.code(log['raw_output'], language="text")
