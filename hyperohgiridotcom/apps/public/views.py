from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from hyperohgiridotcom.apps.accounts.models import Post, Comment, Zabuton, UserProfile, User
from .forms import PostForm, CommentForm, ContactForm
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db.models import F
from django.core.mail import send_mail





def index(request):
        print(request.user)
        most_commented_post = Post.objects.order_by('-total_comments').first()

        if most_commented_post:
            posts = Post.objects.prefetch_related(
                Prefetch('comments', queryset=Comment.objects.all(), to_attr='comments_list')
            ).exclude(id=most_commented_post.id).order_by('-created_at')    
        else:
            posts = Post.objects.all().order_by('-created_at')  
        
        
        comments = Comment.objects.filter(post=most_commented_post) if most_commented_post else []
        alert_over_like_comment_id = request.GET.get('alert_over_like_comment_id', None)
        alert_over_comment_comment_id = request.GET.get('alert_over_comment_comment_id', None)
    

        return render(request, 'index.html', {
             'most_commented_post':most_commented_post,
             'posts':posts, 
             'comments':comments,
             'alert_over_like_comment_id':alert_over_like_comment_id,
             'alert_over_comment_comment_id':alert_over_comment_comment_id
             })
def ranking(request):
    zabuton_rank_user = UserProfile.objects.all().order_by('-total_zabutons_received')
    post_rank = Post.objects.all().order_by('-total_comments')
    return render(request, 'ranking.html', {'zabuton_rank_user':zabuton_rank_user, 'post_rank':post_rank})

def post_detail(request, post_id):
     post = get_object_or_404(Post, id=post_id)
    
   
     comments = post.comments.all()
     return render(request, 'post_detail.html', {'post':post, 'comments':comments})

def about(request):
        return render(request, 'about.html') 

def contact(request):
        if request.method == 'POST':
             contact_form = ContactForm(request.POST)
             if contact_form.is_valid():
                  user_email = contact_form.cleaned_data['email']
                  contact_content = contact_form.cleaned_data['content']
                  send_contact_email(user_email, contact_content)
                  messages.success(request, "お問い合せメールを送信しました。")
             else:
                  messages.error(request, "メールの送信に失敗しました。メールアドレスをお確かめください。")
             return redirect('public:contact')
        return render(request, 'contact.html')

def send_contact_email(user_email, contact_content):
    subject ='[ハイパーオーギリドットコム] ユーザー様からのお問い合わせ。'
    message = f'お問い合わせ内容: {contact_content}' 
    to_email = 'pinestudio0224@gmail.com'
    send_mail(subject, message, user_email, [to_email])

@login_required
def post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('public:index')
    else:
        post_form = PostForm()

    return render(request, 'post.html', {'post_form': post_form})

@login_required
def comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if Comment.objects.filter(user=request.user, post=post).exists():
         comment_instance = Comment.objects.get(user=request.user, post=post)
         return redirect(reverse('public:index') + f'?alert_over_comment_comment_id={comment_instance.id}')
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()

            Post.objects.filter(id=post.id).update(total_comments=F('total_comments')+1)
            return redirect('public:index')
            
            
    else:
        comment_form = CommentForm()
    
    return render(request, 'comment.html', {'comment_form': comment_form, 'post': post})


def over_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    num_zabutons = comment.num_zabutons
    content = comment.content
    return render(request, 'over_comment.html', {'num_zabutons':num_zabutons, 'content':content})

def over_like(request, comment_id):
     return render(request, 'over_like.html', {'comment_id':comment_id})

@login_required
def like_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    post = comment.post
    if Zabuton.objects.filter(user=request.user, comment__post=post).exists():
          return redirect(reverse('public:index') + f'?alert_over_like_comment_id={comment.id}')
     
    comment.num_zabutons += 1
    comment.save()

    Zabuton.objects.create(user=request.user, comment=comment)
    UserProfile.objects.filter(user=comment.user).update(total_zabutons_received=F('total_zabutons_received')+1)
    return redirect('public:index')





def user_info(request, user_id):
     user_instance = User.objects.get(id=user_id)
     return render(request, 'userInfo.html', {'user':user_instance})

def start_page(request):
     return render(request, 'startPage.html')

