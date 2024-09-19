import datetime

from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from myapp.models import *


def public(request):
    a=Category.objects.all()
    b=Book.objects.all()
    return render(request,'publicindex.html',{'data':a,'data1':b})


def login(request):
    if 'submit' in request.POST:
        username = request.POST['username']
        password = request.POST['password']

        a=Login.objects.filter(username=username,password=password)
        if a.exists():
            b = Login.objects.get(username=username, password=password)
            request.session['lid']=b.id
            if b.type=='admin':
                return HttpResponse('''<script>window.location='/adminhome'</script>''')
            elif b.type == 'user':

                return HttpResponse('''<script>window.location='/user_home'</script>''')
            else:
                return HttpResponse('''<script>alert("Invalid ");window.location='/'</script>''')
        else:
            return HttpResponse('''<script>alert("Invalid ");window.location='/'</script>''')
    return  render(request,'login.html')

from django.utils.dateformat import format

def admin_home(request):


    a=Book.objects.all()
    book=a.count()
    request.session['book'] = book

    u=User.objects.all()
    user=u.count()
    request.session['user']=user

    c=Category.objects.all()
    cat=c.count()
    request.session['cat']=cat



    com=Complaints.objects.filter(reply='pending')
    complaint=com.count()
    request.session['complaint']=complaint

    book_data = (
        Book.objects.values('adddate')
            .annotate(count=Count('id'))
            .order_by('adddate')
    )

    labels = [str(item['adddate']) for item in book_data]  # Convert to string
    data = [item['count'] for item in book_data]

    request.session['lab'] = labels
    request.session['data'] = data

    user_data = (
        User.objects.values('registerationdate')  # Assuming 'registration_date' is the field for user registration
            .annotate(count=Count('id'))
            .order_by('registerationdate')
    )
    user_labels = [str(item['registerationdate']) for item in user_data]  # Convert to string
    user_data_values = [item['count'] for item in user_data]
    request.session['user_lab'] = user_labels
    request.session['user_data'] = user_data_values

    return render(request,'admin/adminhome.html',{'data':a,'complaint':complaint,'book':book,'user':user,'cat':cat})




def admin_add_category(request):
    if 'submit' in request.POST:
        category=request.POST['category']
        var=Category()
        var.category=category
        var.save()
        return HttpResponse('''<script>window.location='/admin_add_category'</script>''')

    return render(request,'admin/add category.html')


def admin_add_books(request):
    c=Category.objects.all()
    if 'submit' in request.POST:
        CATEGORY=request.POST['category']
        title=request.POST['title']
        price=request.POST['price']
        quantity=request.POST['quantity']
        isbn=request.POST['isbn']
        author=request.POST['author']
        publish_year=request.POST['publish_year']
        language=request.POST['language']
        publisher=request.POST['publisher']
        description=request.POST['description']
        image=request.FILES['image']

        fs = FileSystemStorage()
        date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.jpg'
        fs.save(date, image)
        path = fs.url(date)

        b=Book()
        b.CATEGORY=Category.objects.get(id=CATEGORY)
        b.image=path
        b.title=title
        b.isbn=isbn
        b.price=float(price)
        b.quantity=quantity
        b.adddate=datetime.datetime.now().date().today().year
        b.author=author
        b.publish_year=publish_year
        b.language=language
        b.publisher=publisher
        b.description=description


        b.save()
        return HttpResponse('''<script>alert(" successfully ");window.location='/admin_add_books'</script>''')


    return render(request,'admin/add  books.html',{'data':c,"d":datetime.datetime.now().strftime("%Y-%m-%d")})



def admin_view_books(request):
    a=Book.objects.all()
    return render(request,'admin/admin_view_books.html',{'data':a})



def admin_view_user(request):
    a=User.objects.all()
    return render(request,'admin/view_users.html',{'data':a})


def blockuser(request,id):
    ob=Login.objects.get(id=id)
    ob.type='block'
    ob.save()
    return redirect('/admin_view_user')


def unblockuser(request,id):
    ob = Login.objects.get(id=id)
    ob.type = 'user'
    ob.save()

    return redirect('/admin_view_user')


def admin_edit_books(request,id):
    a=Book.objects.get(id=id)
    a1=Category.objects.all()

    return render(request,'admin/edit  books.html',{'data':a,'data1':a1})

def admin_edit_books_post(request):
    CATEGORY = request.POST['category']
    title = request.POST['title']
    price = request.POST['price']
    quantity = request.POST['quantity']
    isbn = request.POST['isbn']
    author = request.POST['author']
    publish_year = request.POST['publish_year']
    language = request.POST['language']
    publisher = request.POST['publisher']
    description = request.POST['description']
    id = request.POST['id']

    b = Book.objects.get(id=id)
    if 'image' in request.FILES:
        image = request.FILES['image']

        fs = FileSystemStorage()
        date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.jpg'
        path=fs.save(date, image)
        # path = fs.url(date)
    b.image = path

    b.CATEGORY = Category.objects.get(id=CATEGORY)
    b.title = title
    b.price = float(price)
    b.quantity = quantity
    b.isbn = isbn
    b.author = author
    b.publish_year = publish_year
    b.language = language
    b.publisher = publisher
    b.description = description

    b.save()
    return HttpResponse('''<script>window.location='/admin_view_books'</script>''')


def admin_delete_book(request,id):
    var=Book.objects.get(id=id)
    var.delete()

    return HttpResponse('''<script>window.location='/admin_view_books'</script>''')

def userreg(request):
    if 'submit' in request.POST:
        fname=request.POST['fname']

        gender=request.POST['gender']
        password=request.POST['password']
        confirmpassword=request.POST['confirmpassword']
        lastname=request.POST['lastname']
        email=request.POST['email']
        phone=request.POST['phone']
        path = "user1.jpg"
        if 'image' in request.FILES:
            image = request.FILES['image']

            fs=FileSystemStorage()
            date=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jpg'
            fs.save(date,image)
            path=fs.url(date)


        a=Login.objects.filter(username=email)



        if password==confirmpassword:
            l = Login()
            l.username = email
            l.password = confirmpassword
            l.type='user'
            l.save()


            u=User()
            u.LOGIN=l
            u.fname=fname
            u.lname=lastname
            u.gender=gender
            u.email=email
            u.phonenumber=phone
            u.phonenumber=phone
            u.registerationdate=datetime.datetime.now().date().today().year
            u.image=path
            u.save()
            return HttpResponse('''<script>window.location='/'</script>''')
        else:
            return HttpResponse('''<script>alert("Password cant match ");window.location='/userreg'</script>''')

    return render(request,'registerindex.html')



def user_home(request):
    a=Book.objects.all()
    b=Category.objects.all()
    return render(request,'user/userindex.html',{'data':a,'data1':b})