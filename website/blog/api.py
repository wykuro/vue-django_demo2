from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from blog.models import Userinfo, Article
from django.contrib.auth.models import User, Group, Permission, ContentType
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password, make_password
import base64
import os
import datetime
import requests
import json

hostUrl = 'http://127.0.0.1:9000/'


@api_view(['POST'])
def dweb_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.filter(username=username)
    if user:
        checkPwd = check_password(password, user[0].password)
        if checkPwd:
            userinfo = Userinfo.objects.get_or_create(belong=user[0])
            userinfo = Userinfo.objects.get(belong=user[0])
            token = Token.objects.get_or_create(user=user[0])
            token = Token.objects.get(user=user[0])
        else:
            return Response('pwderr')
    else:
        return Response("none")
    userinfo_data = {
        'token': token.key,
        'nickName': userinfo.nickName,
        'headImg': userinfo.headImg,
    }
    return Response(userinfo_data)


@api_view(['GET'])
def article_data(request):
    article_id = request.GET['id']
    article = Article.objects.get(id=article_id)
    article_data = {
        'title': article.title,
        "cover": article.cover,
        "describe": article.describe,
        "content": article.content,
        "nickName": article.belong.username,
        "pre_id": 0,
        "next_id": 0
    }
    pre_data = Article.objects.filter(id__lt=article_id).last()
    if pre_data:
        article_data["pre_id"] = pre_data.id
    next_data = Article.objects.filter(id__gt=article_id).first()
    if next_data:
        article_data["next_id"] = next_data.id
    return Response(article_data)


@api_view(['POST'])
def dweb_register(request):
    username = request.POST['username']
    password = request.POST['password']
    password2 = request.POST['password2']
    user = User.objects.filter(username=username)
    if user:
        return Response("repeat")
    else:
        new_password = make_password(password, username)
        newUser = User(username=username, password=new_password)
        newUser.save()
    token = Token.objects.get_or_create(user=newUser)
    token = Token.objects.get(user=newUser)
    userinfo = Userinfo.objects.get_or_create(belong=newUser)
    userinfo = Userinfo.objects.get(belong=newUser)
    userinfo_data = {
        'token': token.key,
        'nickName': userinfo.nickName,
        'headImg': userinfo.headImg,
    }
    return Response(userinfo_data)


@api_view(['POST'])
def dweb_autoLogin(request):
    token = request.POST['token']
    user_token = Token.objects.filter(key=token)
    if user_token:
        userinfo = Userinfo.objects.get(belong=user_token[0].user)
        userinfo_data = {
            'token': token,
            'nickName': userinfo.nickName,
            'headImg': userinfo.headImg,
        }
        return Response(userinfo_data)
    else:
        return Response("token timeout")


@api_view(['POST'])
def dweb_Logout(request):
    token = request.POST['token']
    print(token)
    user_token = Token.objects.get(key=token)
    user_token.delete()
    return Response('logout')


@api_view(['POST'])
def add_article(request):
    title = request.POST['title']
    describe = request.POST['describe']
    cover = request.POST['cover']
    content = request.POST['content']
    token = request.POST['token']
    user_token = Token.objects.filter(key=token)
    if len(user_token) == 0:
        return Response('nologin')
    if len(title) == 0:
        return Response('notitle')
    new_article = Article(title=title)
    new_article.save()
    soup = BeautifulSoup(content, 'html.parser')  # 解析富文本html文档
    imgList = soup.find_all('img')
    for img in range(0, len(imgList)):
        src = imgList[img]['src']
        if 'http://' in src or 'https://' in src:
            image = requests.get(src)
            image_data = Image.open(BytesIO(image.content))
            image_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '-' + str(new_article.id) + '-' + str(img)
            image_data.save('upload/' + image_name + '.png')
            new_src = hostUrl + 'upload/' + image_name + ".png"
            content = content.replace(src, new_src)
            if cover == src:
                cover = new_src
        else:
            image_data = base64.b64decode(src.split(',')[1])
            image_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '-' + str(new_article.id) + '-' \
                         + str(img) + '.' + src.split(',')[0].split('/')[1].split(';')[0]
            image_url = os.path.join('upload', image_name).replace('\\', '/')
            with open(image_url, 'wb') as f:
                f.write(image_data)
            new_src = hostUrl + image_url
            content = content.replace(src, new_src)
            if cover == src:
                cover = new_src
    new_article.content = content
    new_article.belong = user_token[0].user
    new_article.cover = cover
    new_article.describe = describe

    new_article.save()
    return Response("ok")


@api_view(["GET"])
def article_list(request):
    page = request.GET['page']
    pageSize = request.GET['pageSize']
    print(page)
    articles = Article.objects.all()
    total = len(articles)
    paginator = Paginator(articles, pageSize)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    print(articles)
    articles_data = []
    for a in articles:
        a_item = {
            'title': a.title,
            'cover': a.cover,
            'nickName': "",
            'id': a.id,
        }
        article_user = a.belong
        userinfo = Userinfo.objects.filter(belong=article_user)
        if userinfo[0].nickName:
            a_item['nickName'] = userinfo[0].nickName
        else:
            a_item['nickName'] = article_user.username
        articles_data.append(a_item)
    return Response({'data': articles_data, 'total': total})


@api_view(['DELETE'])
def del_article(request):
    article_id = request.POST['id']
    token = request.POST['token']
    print(article_id)
    user_token = Token.objects.filter(key=token)
    if len(user_token) == 0:
        return Response('nologin')
    user = user_token[0].user
    user_perm = user.has_perm('blog.delete_article')
    print(user_perm)
    if user_perm == False:
        return Response('noperm')
    article = Article.objects.get(id=article_id)
    article.delete()
    return Response('ok')


@api_view(['POST'])
def dweb_checkperm(request):
    token = request.POST['token']
    content_type = request.POST['contentType']
    permissions = json.loads(request.POST['permissions'])
    user_token = Token.objects.filter(key=token)
    if user_token:
        user = user_token[0].user
        for p in permissions:
            app_str = content_type.split('_')[0]
            model_str = content_type.split('_')[1]
            perm_str = app_str + '.' + p + '_' + model_str
            print(perm_str)
            check = user.has_perm(perm_str)
            print(check)
            if (check == False):
                return Response('noperm')
    else:
        return Response('nologin')

    return Response("ok")


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def dweb_group(request):
    if request.method == "POST":
        token = request.POST['token']
        permList = [
            'auth.add_user',
            'auth.delete_user',
            'auth.change_user',
            'auth.view_user'
        ]
        checkUser = userLoginAndPerm(token, permList)
        if checkUser != 'perm_pass':
            return Response(checkUser)
        group_name = request.POST['group']
        userlist_name = json.loads(request.POST['userlist'])
        group = Group.objects.get(name=group_name)
        for username in userlist_name:
            user = User.objects.get(username=username)
            group.user_set.add(user)
        return Response("ok")

    if request.method == "GET":
        groups = Group.objects.all()
        groups_data = []
        for g in groups:
            g_item = {
                "name": g.name
            }
            groups_data.append(g_item)
        return Response(groups_data)
    if request.method == 'DELETE':
        token = request.POST['token']
        name = request.POST['name']
        permList = [
            'auth.add_user',
            'auth.delete_user',
            'auth.change_user',
            'auth.view_user'
        ]
        checkUser = userLoginAndPerm(token, permList)
        if checkUser != 'perm_pass':
            return Response(checkUser)
        group = Group.objects.get(name=name)
        group.delete()
        return Response('ok')
    if request.method == 'PUT':
        token = request.POST['token']
        new_name = request.POST['new_group']
        perm_list = json.loads(request.POST['perm_list'])
        permList = [
            'auth.add_user',
            'auth.delete_user',
            'auth.change_user',
            'auth.view_user'
        ]
        checkUser = userLoginAndPerm(token, permList)
        if checkUser != 'perm_pass':
            return Response(checkUser)
        new_group = Group.objects.filter(name=new_name)
        if new_group:
            return Response('samename')
        new_group = Group.objects.create(name=new_name)
        for perm in perm_list:
            app_str = perm['content_type'].split('_')[0]
            model_str = perm['content_type'].split('_')[1]
            contentType = ContentType.objects.get(app_label=app_str, model=model_str)
            for method in perm['perm_methods']:
                codename = method + '_' + model_str
                permission = Permission.objects.get(content_type=contentType, codename=codename)
                new_group.permissions.add(permission)
    return Response("ok")


@api_view(['GET'])
def dweb_userlist(request):
    user_list = User.objects.all()
    user_list_data = []
    for user in user_list:
        user_item = {
            "name": user.username
        }
        user_list_data.append(user_item)
    return Response(user_list_data)


def userLoginAndPerm(token, permlist):
    user_token = Token.objects.filter(key=token)
    if user_token:
        user = user_token[0].user
        for perm_str in permlist:
            perm_user = user.has_perm(perm_str)
            if perm_user:
                return 'perm_pass'
            else:
                return 'noperm'
    else:
        return 'nologin'
