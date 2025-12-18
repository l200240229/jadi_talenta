from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework import status
from .serializers import PublicProfileSerializer
from rest_framework.permissions import AllowAny
from django.db.models import Q
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def profile_me(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            "nama": request.user.username,
            "prodi": "",
            "angkatan": "",
            "bio": "",
            "kontak_email": request.user.email or "",
        }
    )

    if request.method == "GET":
        return Response(ProfileSerializer(profile).data)

    if request.method == "PATCH":
        serializer = ProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        update_is_active(profile)
        return Response(serializer.data)
    

def update_is_active(profile):
    has_photo = bool(profile.foto)
    has_skill = profile.skills.exists()
    has_exp = profile.experiences.exists()

    profile.is_active = all([has_photo, has_skill, has_exp])
    profile.save(update_fields=["is_active"])

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_my_profile(request):
    request.user.delete()
    return Response(
        {"detail": "User berhasil dihapus"},
        status=status.HTTP_204_NO_CONTENT
    )

    
@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_profile_list(request):
    profiles = Profile.objects.select_related("user").all()

    data = []
    for p in profiles:
        data.append({
            "id":p.id,
            "username":p.user.username,
            "kontak_email":p.user.kontak_email,
            "nama":p.nama,
            "prodi":p.prodi,
            "is_active":p.is_active,
        })

    return Response(data)

@api_view(["PATCH"])
@permission_classes([IsAdminUser])
def admin_toggle_profile(request, profile_id):
    try:
        profile = Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
        return Response(
            {"detail": "Profile tidak ditemukan"},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    profile.is_active = not profile.is_active
    profile.save(update_fields=["is_active"])

    return Response({
        "id": profile.id,
        "is_active": profile.is_active
    })
    
@api_view(["GET"])
@permission_classes([AllowAny])
def public_talent_list(request):
    search = request.GET.get("search", "")
    skill = request.GET.get("skill", "")
    prodi = request.GET.get("prodi", "")

    profiles = Profile.objects.filter(is_active=True)

    if search:
        profiles = profiles.filter(
            Q(nama__icontains=search) |
            Q(prodi__icontains=search) |
            Q(user__username__icontains=search)
        )

    if prodi:
        profiles = profiles.filter(prodi__icontains=prodi)

    if skill:
        profiles = profiles.filter(
            skills__nama_skill__icontains=skill
        ).distinct()

    serializer = PublicProfileSerializer(profiles, many=True, context={"request": request})
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([AllowAny])
def public_talent_detail(request, username):
    try:
        profile = Profile.objects.get(
            user__username=username,
            is_active=True
        )
    except Profile.DoesNotExist:
        return Response(
            {"detail": "Talenta tidak ditemukan"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = PublicProfileSerializer(profile, context={"request": request})
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([AllowAny])
def public_talent_latest(request):
    profiles = Profile.objects.filter(is_active=True).order_by("-id")[:5]
    serializer = PublicProfileSerializer(profiles, many=True, context={"request": request})
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_cv(request):
    profile = Profile.objects.get(user=request.user)

    data = PublicProfileSerializer(
        profile,
        context={"request": request}
    ).data

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    BLUE = (0.23, 0.51, 0.96)
    GRAY = (0.45, 0.45, 0.45)

    x = 50
    y = height - 50

    # ================= HEADER =================
    p.setFillColorRGB(*BLUE)
    p.rect(0, height - 140, width, 140, fill=1)

    if data.get("foto"):
        try:
            p.drawImage(
                profile.foto.path,
                x,
                height - 120,
                width=80,
                height=80,
                mask="auto"
            )
        except:
            pass

    p.setFillColorRGB(1, 1, 1)
    p.setFont("Helvetica-Bold", 18)
    p.drawString(x + 100, y, data["nama"])

    p.setFont("Helvetica", 11)
    p.drawString(
        x + 100,
        y - 22,
        f"{data['prodi']} · Angkatan {data['angkatan']}"
    )

    p.setFont("Helvetica", 10)
    p.drawString(
        x + 100,
        y - 40,
        "Universitas Muhammadiyah Surakarta"
    )

    # ================= CONTENT =================
    y = height - 180
    p.setFillColorRGB(0, 0, 0)

    # ---- TENTANG SAYA
    y = draw_section_title(p, x, y, "Tentang Saya", width)
    p.setFont("Helvetica", 10)
    text = p.beginText(x, y)
    for line in (data["bio"] or "Belum ada bio").split("\n"):
        text.textLine(line)
    p.drawText(text)
    y -= 40

    # ---- PENGALAMAN
    y = draw_section_title(p, x, y, "Pengalaman", width)

    if data["experiences"]:
        for exp in data["experiences"]:
            p.setFont("Helvetica-Bold", 11)
            p.drawString(x, y, f"{exp['judul']} ({exp['tahun_mulai']})")
            y -= 14

            p.setFont("Helvetica", 10)
            p.setFillColorRGB(*GRAY)
            p.drawString(x + 12, y, exp["deskripsi"])
            p.setFillColorRGB(0, 0, 0)
            y -= 22
    else:
        p.setFont("Helvetica", 10)
        p.drawString(x, y, "Belum ada pengalaman")
        y -= 20

    # ---- SKILL (chip-style)
    y = draw_section_title(p, x, y, "Skill", width)

    p.setFont("Helvetica", 10)
    chip_x = x
    chip_y = y

    for skill in data["skills"]:
        text_width = p.stringWidth(skill["nama_skill"], "Helvetica", 10) + 10
        p.roundRect(chip_x, chip_y - 12, text_width, 16, 6, stroke=1, fill=0)
        p.drawString(chip_x + 5, chip_y - 8, skill["nama_skill"])
        chip_x += text_width + 8

        if chip_x > width - 120:
            chip_x = x
            chip_y -= 22

    if not data["skills"]:
        p.drawString(x, y, "Belum ada skill")

    y = chip_y - 30

    # ---- KONTAK
    y = draw_section_title(p, x, y, "Kontak", width)
    p.setFont("Helvetica", 10)

    if data.get("kontak_email"):
        p.drawString(x, y, f"Email: {data['kontak_email']}")
        y -= 14
    if data.get("kontak_wa"):
        p.drawString(x, y, f"WhatsApp: {data['kontak_wa']}")
        y -= 14
    if data.get("instagram"):
        p.drawString(x, y, f"Instagram: @{data['instagram']}")

    # ================= FINAL =================
    p.showPage()
    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="CV.pdf"'
    return response

def draw_section_title(p, x, y, title, width):
    p.setFont("Helvetica-Bold", 14)
    p.drawString(x, y, title)
    y -= 6
    p.line(x, y, width - x, y)
    return y - 14
