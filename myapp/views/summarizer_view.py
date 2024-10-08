import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import openai
from django.conf import settings
import os
from myapp.models import GeneratedImage, Bookmark
import uuid
from django.http import HttpResponse 

openai.api_key = settings.OPENAI_API_KEY

def summarizer_view(request):
    summarized_text = None
    generated_image = None
    error_message = None
    similar_image = None

    if request.method == 'POST':
        if 'url' in request.POST:
            # URLが送信された場合、要約を生成
            url = request.POST.get('url')
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                # urlからテキストを抽出
                soup = BeautifulSoup(response.content, 'html.parser')
                for script in soup(["script", "style"]):
                    script.decompose()

                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)

                max_chars = 4000
                if len(text) > max_chars:
                    text = text[:max_chars]

                prompt = (
                    "あなたはテキストマイニングのスペシャリストです。以下制約を守り、webサイトの内容を要約してください。\n"
                    "#制約\n"
                    "- 要約は日本語で記述すること\n"
                    "- 人物を想起させるワードは使わないこと\n"
                    "- マークアップ言語は使わないこと\n"
                    "- 要約文を基にロゴ画像を作成する前提で、文章を要約すること\n"
                    "#webサイトの内容\n"
                    f"{text}"
                )

                # call Open AI API
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.7,
                )

                summarized_text = response.choices[0].message.content.strip()

            except requests.exceptions.RequestException:
                error_message = "不正なURLです"

        elif 'generate_image' in request.POST:
            summarized_text = request.POST.get('summary')
            try:
                # call Stable Diffusion API
                image_relative_path = generate_image_from_prompt(summarized_text)
                generated_image = post_generated_image(request, summarized_text, image_relative_path)
            except Exception as e:
                print("Error processing image to video:", str(e))
                return HttpResponse(f"Error processing image to video: {str(e)}", status=500)
        elif 'generate_similar_image' in request.POST:
            summarized_text = request.POST.get('summary')
            original_image_path = request.POST.get('original_image_path')
            additional_text = request.POST.get('additional_text', '')
            try:
                # call Stable Diffusion API
                similar_image_relative_path = generate_similar_image(
                    additional_text,
                    original_image_path
                )
                similar_image = post_generated_image(request, summarized_text, similar_image_relative_path)
            except Exception as e:
                print("Error generating similar image:", str(e))
                return HttpResponse(f"Error generating similar image: {str(e)}", status=500)
    else:
        image_id = request.GET.get('image_id')
        if image_id:
            try:
                image = GeneratedImage.objects.get(id=image_id)
                generated_image = image
                similar_image = image
                summarized_text = image.summary_text
            except GeneratedImage.DoesNotExist:
                error_message = "指定された画像が見つかりませんでした。"
    if similar_image is None:
        return render(request, 'summarizer.html', {
            'summary': summarized_text,
            'generated_image': generated_image,
            'error_message': error_message
        })
    else:
        return render(request, 'summarizer.html', {
            'summary': summarized_text,
            'similar_image': similar_image,
            'error_message': error_message
        })

@login_required
def bookmark_image_view(request, image_id):
    try:
        image = GeneratedImage.objects.get(id=image_id)
        Bookmark.objects.get_or_create(user=request.user, image=image)
        return redirect('summarizer')
    except GeneratedImage.DoesNotExist:
        return redirect('summarizer')
    
def generate_image_from_prompt(summarized_text):
    api_endpoint = f'{settings.STABLE_DIFFUSION_API_ENDPOINT}/generate/core'

    # stable diffusionは英語のみ対応なので、要約された日本語テキストを英語に翻訳
    en_summarized_text = translate(summarized_text)
    prompt = (
        "high quality icon, simple illustration, favicon image \n"
        "Generated from the following website summary \n"
        "#### Summary \n"
        f"{en_summarized_text}"
    )

    image_relative_path = run_stable_diffusion_api(prompt, api_endpoint)
    return image_relative_path
    
def generate_similar_image(additional_text, original_image_path):
    api_endpoint = f'{settings.STABLE_DIFFUSION_API_ENDPOINT}/control/style'

    en_additional_text = translate(additional_text) if additional_text else ''
    
    prompt = (
        "Create a similar icon image based on the following prompt and image.\n"
        "#### Requirements \n"
        "- illustration style \n"
        "- transparent_background \n"
        "#### Prompt \n"
        f"{en_additional_text}"
    )

    image_path = os.path.join(settings.MEDIA_ROOT, original_image_path)
    image_relative_path = run_stable_diffusion_api(prompt, api_endpoint, image_path=image_path)

    return image_relative_path

def translate(text, source_language='Japanese', target_language='English'):
    prompt = f"Translate the following text from {source_language} to {target_language}:\n\n{text}"
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0,
    )
    return response.choices[0].message.content.strip()

def post_generated_image(request, summarized_text, image_relative_path):
    if request.user.is_authenticated:
        generated_image = GeneratedImage.objects.create(
            user=request.user,
            summary_text=summarized_text,
            image=image_relative_path
        )
    else:
        generated_image = GeneratedImage.objects.create(
            user=None,
            summary_text=summarized_text,
            image=image_relative_path
        )
    return generated_image

def run_stable_diffusion_api(prompt, api_endpoint, image_path=None):
    api_key = settings.STABLE_DIFFUSION_API_KEY

    headers = {
        "authorization": f"Bearer {api_key}",
        "accept": "image/*"
    }
    data = {
        "prompt": prompt,
        "negative_prompt": "real, nsfw, text, EasyNegative, human icons, circle",
        "output_format": "webp",
    }
    files = {}
    
    if image_path:
        with open(image_path, 'rb') as img_file:
            files = {"image": img_file}        
            response = requests.post(
                api_endpoint,
                headers=headers,
                data=data,
                files=files,
            )
    else:
        files = {"none": ''}        
        response = requests.post(
            api_endpoint,
            headers=headers,
            data=data,
            files=files,
        )
    
    if response.status_code == 200:
        image_data = response.content
        image_filename = f"{uuid.uuid4()}.png"
        image_save_path = os.path.join(settings.MEDIA_ROOT, 'generated_images', image_filename)
        os.makedirs(os.path.dirname(image_save_path), exist_ok=True)
        with open(image_save_path, 'wb') as f:
            f.write(image_data)
        return f'generated_images/{image_filename}'
    else:
        error_message = response.json().get('message', 'Unknown error')
        raise Exception(f"Error generating image: {response.status_code} - {error_message}")