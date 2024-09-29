models = {
    'llama-3.2-vision': {'apis_supported': ['v1/chat/completions'], 'target_base_url': 'http://llama-32-vision-service.example.com', 'target_model_name': 'llama-3.2-vision'},
    'llama-3.2-vision-instruct': {'apis_supported': ['v1/chat/completions'], 'target_base_url': 'http://llama-32-vision-service.example.com', 'target_model_name': 'llama-3.2-vision'},
    'llama-3.2-vi-inst': {'apis_supported': ['v1/chat/completions'], 'target_base_url': 'http://llama-32-vision-service.example.com', 'target_model_name': 'llama-3.2-vision'},
    'llama-31-70b': {'apis_supported': ['v1/chat/completions', 'v1/completions'], 'target_base_url': 'https://llama-31-70b.example.com', 'target_model_name': 'llama-31-70b'},
    'llama-3.1-70b': {'apis_supported': ['v1/chat/completions', 'v1/completions'], 'target_base_url': 'https://llama-31-70b.example.com', 'target_model_name': 'llama-3.1-70b'},
    'llama-3-8b': {'apis_supported': ['v1/chat/completions', 'v1/completions'], 'target_base_url': 'https://llama-3-8b.example.com', 'target_model_name': 'llama-3-8b'},
    'chat-large': {'apis_supported': ['v1/chat/completions', 'v1/completions'], 'target_base_url': 'https://chat-large.example.com', 'target_model_name': 'chat-large'},
    'chat-default': {'apis_supported': ['v1/chat/completions', 'v1/completions'], 'target_base_url': 'https://chat-default.example.com', 'target_model_name': 'chat-default'},
    'chat-mts': {'apis_supported': ['v1/chat/completions', 'v1/completions'], 'target_base_url': 'https://chat-mts.example.com', 'target_model_name': 'chat-mts'},
    'chat-lts': {'apis_supported': ['v1/chat/completions', 'v1/completions'], 'target_base_url': 'https://chat-lts.example.com', 'target_model_name': 'lts-mts'},
    'phi-35-vision': {'apis_supported': ['v1/chat/completions'], 'target_base_url': 'https://phi-35-vision.example.com', 'target_model_name': 'phi-35-vision'},
    'phi-3.5-vision': {'apis_supported': ['v1/chat/completions'], 'target_base_url': 'https://phi-3.5-vision.example.com', 'target_model_name': 'phi-3.5-vision'},
    'xtts-v2': {'apis_supported': ['v1/audio/speech'], 'target_base_url': 'https://xtts-v2.example.com', 'target_model_name': 'tts-1-hd'},
    'whisper-3-large': {'apis_supported': ['v1/audio/transcriptions', 'v1/audio/translations'], 'target_base_url': 'https://whisper-3-large.example.com', 'target_model_name': 'whisper-1'},
    'dall-e-3': {'apis_supported': ['v1/images/generations'], 'target_base_url': 'https://dall-e-3.example.com', 'target_model_name': 'flux.1-dev'},
    'flux.1-dev': {'apis_supported': ['v1/images/generations'], 'target_base_url': 'https://flux-1-dev.example.com', 'target_model_name': 'flux.1-dev'},
    'bge-m3': {'apis_supported': ['v1/embeddings'], 'target_base_url': 'https://bge-m3.example.com', 'target_model_name': 'tei'},
}

def get_model_data(model, api_path):
    model_info = models.get(model)
    if model_info and api_path in model_info['apis_supported']:
        return model_info
    return None
