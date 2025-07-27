from pydub import AudioSegment

def bass_boost(audio: AudioSegment, boost_db: int = 25, cutoff_freq: int = 100) -> AudioSegment:
    """
    Enhances bass by applying a low-pass filter and boosting low frequencies.
    
    Parameters:
        audio (AudioSegment): The input audio segment.
        boost_db (int): The amount of bass boost in decibels (default: 10).
        cutoff_freq (int): The low-pass filter cutoff frequency in Hz (default: 150).
    
    Returns:
        AudioSegment: The audio with bass boost applied.
    """
    bass = audio.low_pass_filter(cutoff_freq)  # Apply a low-pass filter
    boosted = bass + boost_db  # Increase bass volume
    return audio.overlay(boosted)  # Mix with original audio
