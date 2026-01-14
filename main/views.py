import os
from openai import OpenAI
from django.shortcuts import render, redirect
from .models import AIPost
from dotenv import load_dotenv

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

load_dotenv() # Load environment variables from .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # log user in after registration
            return redirect('index')
    else:
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form':form})


def index(request):
    generated_post = None
    if request.method == 'POST':

        # check if user is logged in  and only generate if logged in
        if not request.user.is_authenticated:
            return redirect('login')

        topic = request.POST.get('topic')
        tone = request.POST.get('tone')

        # the AI magic prompt
        prompt = f"Write a viral Linkedln post about {topic}. The tone should be {tone}. Include relevant hastags and emojis."

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a world-class social media manager"},
                    {"role": "user", "content": prompt}
                ]
            )

            generated_post = response.choices[0].message.content
        except Exception as e:
            print(f"Error:{e}")
            generated_post = "(Demo Mode): OpenAI Quota exceeded! Once you add credits, your real viral posts will appear hear."

        # save to database
        new_post = AIPost(
            user=request.user,
            topic=topic,
            tone=tone,
            generated_content=generated_post
        )
        new_post.save()
        return render(request, 'main/index.html', {'generated_post': new_post.generated_content})

    return render(request, 'main/index.html')

@login_required
def dashboard(request):
    posts = AIPost.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/dashboard.html', 
    {
        'total_posts':posts.count(),
        'recent_posts':posts[:3]
    })

@login_required
def history(request):
    posts = AIPost.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/history.html', {'posts':posts})
