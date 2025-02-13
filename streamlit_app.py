import streamlit as st
from deep_translator import GoogleTranslator
import json
from typing import Dict, List

# Initialize session state for history
if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []

def translate_text(text: str, from_lang: str, to_lang: str) -> str:
    """Translate text using Google Translator"""
    try:
        translator = GoogleTranslator(source=from_lang, target=to_lang)
        return translator.translate(text)
    except Exception as e:
        return f"Translation Error: {str(e)}"

def save_to_history(word: str, translation: str):
    """Save translation to history"""
    if word and translation:
        st.session_state.translation_history.append({
            'word': word,
            'translation': translation
        })

def export_history() -> Dict[str, List[Dict[str, str]]]:
    """Export translation history as dictionary"""
    return {'history': st.session_state.translation_history}

# Page configuration
st.set_page_config(
    page_title="Spanish-English Dictionary",
    page_icon="📚",
    layout="wide"
)

# Main title
st.title("📚 Spanish-English Dictionary")

# Create two columns for the main layout
col1, col2 = st.columns([2, 1])

with col1:
    # Input section
    st.subheader("Translate")
    
    # Language selection
    direction = st.radio(
        "Translation Direction:",
        ("Spanish to English", "English to Spanish"),
        horizontal=True
    )
    
    # Set source and target languages based on selection
    if direction == "Spanish to English":
        from_lang, to_lang = 'es', 'en'
        placeholder_text = "Enter Spanish text..."
    else:
        from_lang, to_lang = 'en', 'es'
        placeholder_text = "Enter English text..."
    
    # Text input
    input_text = st.text_area(
        "Enter text to translate:",
        height=100,
        placeholder=placeholder_text
    )
    
    # Translate button
    if st.button("Translate", type="primary"):
        if input_text:
            translation = translate_text(input_text, from_lang, to_lang)
            st.success("Translation:")
            st.write(translation)
            
            # Save to history
            save_to_history(input_text, translation)
        else:
            st.warning("Please enter some text to translate.")

with col2:
    # History section
    st.subheader("Translation History")
    
    if st.session_state.translation_history:
        for item in reversed(st.session_state.translation_history[-5:]):  # Show last 5 translations
            with st.expander(f"{item['word'][:30]}..."):
                st.write(f"Translation: {item['translation']}")
        
        # Export history button
        if st.button("Export History"):
            history_data = export_history()
            st.download_button(
                label="Download History",
                data=json.dumps(history_data, indent=2),
                file_name="translation_history.json",
                mime="application/json"
            )
        
        # Clear history button
        if st.button("Clear History"):
            st.session_state.translation_history = []
            st.experimental_rerun()
    else:
        st.info("No translation history yet.")

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ for Nubi dubi do"
)
