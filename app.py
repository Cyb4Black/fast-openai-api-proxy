from typing import Dict, Optional

import requests
from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse

from auth import can_request
from models import get_model_data

app = FastAPI()


async def handle_request(request: Request, api_path: str):
    token = request.headers.get('Authorization').split("Bearer ")[1] if 'Authorization' in request.headers else None
    body = await request.json()
    model = body.get('model')
    stream = body.get('stream', False)
    stream_options = body.get('stream_options', {})

    # Retrieve model data including the target model name
    model_data = get_model_data(model, api_path)
    if not model_data:
        raise HTTPException(status_code=404, detail="Model not supported for this API")
    if not can_request(model, token):
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Replace the model name in the request body with the target model name
    body['model'] = model_data['target_model_name']

    target_url = model_data['target_base_url'] + '/' + api_path

    # Forward the request to the target URL
    response = requests.post(target_url, json=body, headers={"Authorization": f"Bearer {token}"},
                             stream=stream)
    return response, stream, stream_options


async def handle_file_upload(request: Request, api_path: str, file: UploadFile, data: Dict[str, Optional[str]]):
    token = request.headers.get('Authorization').split("Bearer ")[1] if 'Authorization' in request.headers else None
    model = data['model']

    if not can_request(model, token):
        raise HTTPException(status_code=403, detail="Unauthorized")

    model_data = get_model_data(model, api_path)
    if not model_data:
        raise HTTPException(status_code=404, detail="Model not supported for this API")

    # Update model name to target model name for backend compatibility
    data['model'] = model_data['target_model_name']

    # Read file contents
    file_content = await file.read()

    # Prepare the form data to be sent, converting all non-file data to strings
    form_data = {key: (None, str(value)) for key, value in data.items() if value is not None}
    form_data['file'] = (file.filename, file_content, file.content_type)

    target_url = model_data['target_base_url'] + '/' + api_path

    response = requests.post(target_url, files=form_data, headers={"Authorization": f"Bearer {token}"})
    return response


def process_response(response, response_format):
    if response.status_code == 200:
        if response_format == 'json':
            return response.json()
        else:
            return StreamingResponse(response.iter_content(), media_type=response.headers.get('Content-Type'))
    else:
        return JSONResponse(status_code=response.status_code, content={"message": "Failed to process request"})


# Define endpoints using the helper function for all required APIs
@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    response, stream, stream_options = await handle_request(request, "v1/chat/completions")
    if stream:
        return StreamingResponse(response.iter_content(**stream_options))
    else:
        return response.json()


@app.post("/v1/completions")
async def completions(request: Request):
    response, stream, stream_options = await handle_request(request, "v1/completions")
    return response.json()


@app.post("/v1/embeddings")
async def embeddings(request: Request):
    response, stream, _ = await handle_request(request, "v1/embeddings")
    return response.json()


# Additional endpoints for audio, images, models, and moderation will follow the same pattern

# Define additional routes for audio services
@app.post("/v1/audio/speech")
async def audio_speech(request: Request):
    # Using the helper function to handle request forwarding and response handling
    response, stream, stream_options = await handle_request(request, "v1/audio/speech")

    # Check response status and content type before parsing
    if response.status_code == 200:
        # As it's an audio file content, it will likely not be JSON but a binary stream
        content_type = response.headers.get('Content-Type', '')

        # Streaming the audio content directly if it's a binary type (assuming mp3 or similar)
        if 'audio/' in content_type:
            return StreamingResponse(response.iter_content(**stream_options), media_type=content_type)
        else:
            return JSONResponse(status_code=415, content={"message": "Unsupported Media Type"})
    else:
        # Log error or return a JSON message in case of failure
        return JSONResponse(status_code=response.status_code, content={"message": "Failed to generate audio"})


@app.post("/v1/audio/transcriptions")
async def audio_transcription(
    request: Request,
    file: UploadFile = File(...),
    model: str = Form(...),
    language: Optional[str] = Form(None),
    prompt: Optional[str] = Form(None),
    response_format: Optional[str] = Form('json'),
    temperature: Optional[float] = Form(0),
    timestamp_granularities: Optional[list] = Form(None)
):
    data = {
        'model': model,
        'language': language,
        'prompt': prompt,
        'response_format': response_format,
        'temperature': temperature,
        'timestamp_granularities': ','.join(timestamp_granularities) if timestamp_granularities else None
    }
    response = await handle_file_upload(request, "v1/audio/transcriptions", file, data)
    return process_response(response, response_format)


@app.post("/v1/audio/translations")
async def audio_translation(
    request: Request,
    file: UploadFile = File(...),
    model: str = Form(...),
    prompt: Optional[str] = Form(None),
    response_format: Optional[str] = Form('json'),
    temperature: Optional[float] = Form(0)
):
    data = {
        'model': model,
        'prompt': prompt,
        'response_format': response_format,
        'temperature': temperature
    }
    response = await handle_file_upload(request, "v1/audio/translations", file, data)
    return process_response(response, response_format)


# Define routes for image services
@app.post("/v1/images/generations")
async def images_generations(request: Request):
    response, stream, _ = await handle_request(request, "v1/images/generations")
    return response.json()


@app.post("/v1/images/edits")
async def images_edits(request: Request):
    response, stream, _ = await handle_request(request, "v1/images/edits")
    return response.json()


@app.post("/v1/images/variations")
async def images_variations(request: Request):
    response, stream, _ = await handle_request(request, "v1/images/variations")
    return response.json()


# Route for model details
@app.get("/v1/models")
async def models_details(request: Request):
    response, stream, _ = await handle_request(request, "v1/models")
    return response.json()


# Route for content moderation
@app.post("/v1/moderations")
async def moderations(request: Request):
    response, stream, _ = await handle_request(request, "v1/moderations")
    return response.json()
