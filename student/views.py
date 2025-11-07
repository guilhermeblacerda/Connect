from django.shortcuts import render,redirect,get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.db.models import Count,Q
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from barcode import Code128
from barcode.writer import ImageWriter
import json,io,datetime
from PIL import Image
from .models import *

def home_page(request):
    return render(request,"student/home.html")

def login_page(request):
    context = {}

    if request.method == 'POST':
        name = request.POST.get('username')
        passw = request.POST.get('password')

        user = authenticate(request, username=name, password=passw)

        if user is not None:
            login(request, user)

            return redirect ('home')
        else:
            context['error'] = 'Nome de usuario ou senha incorretos'
 
    return render(request, "student/login.html", context)

def register_page(request):
    context = {}

    if request.method == "POST":
        name = request.POST.get('username')
        email = request.POST.get('email')
        passw = request.POST.get('password')

        if not name or not email or not passw:
            context['error'] = 'Preencha todos os campos'
            
            return render(request, 'student/register.html',context)
        
        if User.objects.filter(username=name).exists():
            context['error'] = 'Usuario ja existe'

            return render(request, 'student/register.html',context)
        
        user = User.objects.create_user(username=name,email=email,password=passw)
        return redirect('login')

    return render(request, 'student/register.html',context)

def logout_page(request):
    logout(request)
    return(redirect('login'))


def absence_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    faltas = Falta.objects.filter(aluno__user=request.user).order_by('-data')
    total = faltas.count()
    return render(request, 'student/absence.html',{'faltas': faltas, 'total': total})

def score_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    aluno = Aluno.objects.filter(user=request.user).first()

    if aluno:
        materias = aluno.materias.all()
        avaliacoes = Avaliacao.objects.filter(aluno__user=request.user).order_by('-data')
        medias = aluno.medias.all()

        return render(request, 'student/score.html',{'materias': materias,'avaliacoes': avaliacoes,'aluno':aluno,'medias':medias})

    return render(request, 'student/score.html')

def calendar_page(request):
    if not request.user.is_authenticated:
        return redirect('login')

    aluno = Aluno.objects.filter(user=request.user).first()

    if aluno:
        materias = aluno.materias.all()

        eventos = []    

        for materia in materias:
            eventos.append({
                "title":materia.nome,
                "daysOfWeek": materia.get_dias(),
            })

        return render(request,'student/calendar.html',{'materias': materias,'eventos': json.dumps(eventos)})

    return render(request,'student/calendar.html')

def chat_page(request,usuario_id=None):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    mensagens = []
    destinatario = None

    if user.is_staff:
        usuarios = User.objects.exclude(is_staff=True)
        usuarios = usuarios.annotate(
            toRead = Count('mensagens_enviadas',filter=Q(mensagens_enviadas__destinatario=user,mensagens_enviadas__lida=False))
        )
    else:
        usuarios = None
        usuario_id = User.objects.get(username="stackadmin").id

    if usuario_id:
        destinatario = User.objects.get(id=usuario_id)

        Mensagem.objects.filter(
            remetente__in=[user,destinatario],
            destinatario__in=[user, destinatario]
        ).update(lida=True)

        mensagens = Mensagem.objects.filter(
            remetente__in=[user,destinatario],
            destinatario__in=[user, destinatario]
        ).order_by('data_envio','id')

    if request.method == 'POST':
        documentos = request.POST.get("documentos")
        dispensa = request.POST.get("dispensa")
        texto = request.POST.get('mensagem')

        if destinatario:
            if documentos:
                Mensagem.objects.create(remetente=user,destinatario=destinatario,texto=documentos)
            elif dispensa:
                Mensagem.objects.create(remetente=user,destinatario=destinatario,texto=dispensa)
            elif texto:
                Mensagem.objects.create(remetente=user,destinatario=destinatario,texto=texto) 
            
            return redirect('chat', usuario_id=destinatario.id)
        
    return render(request,'student/chat.html', {'mensagens': mensagens,'destinatario':destinatario, 'usuarios':usuarios})

def GoToBoletos(request,boletoId=None):
    if not request.user.is_authenticated:
        return redirect('login')
    
    usuario = request.user
    BoletosDoUsuario = usuario.boletos.all()
    context = {'usuario': usuario,'boletos':BoletosDoUsuario}

    if boletoId:
        boleto = usuario.boletos.filter(id=boletoId).first()

    return render(request,'student/boletos.html',context)

def gerar_boleto_pdf(request, boleto_id):
    boleto = get_object_or_404(Boleto, id=boleto_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="boleto_{boleto.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, height - 60, "BANCO ESCOLAR 999-9")
    p.setFont("Helvetica", 12)
    p.drawString(width - 220, height - 40, "Data do documento:")
    p.drawString(width - 200, height - 60, datetime.date.today().strftime("%d/%m/%Y"))

    linha_digitavel = "23793.38127 60000.000123 45000.789654 1 23450000020000"
    p.setFont("Courier-Bold", 13)
    p.drawString(50, height - 90, linha_digitavel)

    p.setStrokeColor(colors.black)
    p.line(50, height - 100, width - 50, height - 100)

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 130, "Beneficiário:")
    p.setFont("Helvetica", 11)
    p.drawString(150, height - 130, "ESCOLA MODELO LTDA")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 150, "Pagador:")
    p.setFont("Helvetica", 11)
    p.drawString(150, height - 150, f"{boleto.usuario.username}")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 170, "Data processamento:")
    p.setFont("Helvetica", 11)
    p.drawString(200, height - 170, boleto.atualizadoEm.strftime("%d/%m/%Y"))

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 190, "Valor:")
    p.setFont("Helvetica", 11)
    p.drawString(150, height - 190, f"R$ {boleto.valor:.2f}")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 210, "Vencimento:")
    p.setFont("Helvetica", 11)
    p.drawString(150, height - 210, boleto.dataDeVencimento.strftime("%d/%m/%Y"))

    p.setStrokeColor(colors.gray)
    p.rect(45, height - 240, width - 90, 100, stroke=1, fill=0)

    barcode_value = "12345678901234567890123456789012345678901234"

    buffer = io.BytesIO()
    options = {"write_text": False}
    Code128(barcode_value, writer=ImageWriter()).write(buffer, options)
    buffer.seek(0)

    barcode_img = Image.open(buffer)

    orig_width, orig_height = barcode_img.size

    target_width = 420
    target_height = 90
    scale = min(1,target_width/orig_width,target_height / orig_height)

    display_width = orig_width * scale
    display_height = orig_height * scale

    p.drawInlineImage(barcode_img, 50, 100, width=display_width, height=display_height)

    p.line(50, 80, width - 50, 80)
    p.setFont("Helvetica", 8)
    p.drawString(50, 65, "Documento demonstrativo - sem valor legal")

    p.showPage()
    p.save()

    return response

# Create your views here.