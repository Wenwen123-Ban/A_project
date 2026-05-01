import hashlib, os, random, smtplib
from datetime import timedelta
from email.mime.text import MIMEText
from django.core import signing
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from core.models import OtpRequest, ProblemReport, UserProfile
from .utils import parse_json_body


def _send_email(subject, body, to_email):
    user = os.getenv('LBAS_GMAIL_USER', '')
    pwd = os.getenv('LBAS_GMAIL_APP_PASSWORD', '')
    if not user or not pwd:
        return False
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = to_email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls(); server.login(user, pwd); server.send_message(msg)
    return True

@csrf_exempt
def request_otp(request):
    data = parse_json_body(request)
    school_id = str(data.get('school_id','')).strip().lower(); email = str(data.get('email','')).strip().lower()
    if not school_id or not email: return JsonResponse({'error':'school_id and email required'}, status=400)
    if not UserProfile.objects.filter(school_id=school_id, email=email).exists(): return JsonResponse({'error':'Account not found'}, status=404)
    now = timezone.now()
    lock = OtpRequest.objects.filter(school_id=school_id, lockout_until__gt=now).order_by('-lockout_until').first()
    if lock: return JsonResponse({'error':'locked','lockout_until':lock.lockout_until.isoformat()}, status=429)
    valid = OtpRequest.objects.filter(school_id=school_id, used=False, created_at__gte=now-timedelta(hours=24)).exists()
    if valid: return JsonResponse({'error':'OTP already requested in last 24h'}, status=429)
    otp = f"{random.randint(0,999999):06d}"
    OtpRequest.objects.create(school_id=school_id, otp_hash=hashlib.sha256(otp.encode()).hexdigest(), expires_at=now+timedelta(minutes=15))
    _send_email('Your LBAS Verification Code', f'Your OTP is {otp}. It expires in 15 minutes. Contact library desk for help.', email)
    return JsonResponse({'sent': True})

@csrf_exempt
def verify_otp(request):
    data = parse_json_body(request)
    school_id = str(data.get('school_id','')).strip().lower(); otp = str(data.get('otp','')).strip()
    req = OtpRequest.objects.filter(school_id=school_id, used=False).order_by('-created_at').first()
    if not req: return JsonResponse({'error':'No OTP request found'}, status=404)
    now = timezone.now()
    if req.expires_at < now: return JsonResponse({'error':'OTP expired'}, status=400)
    if hashlib.sha256(otp.encode()).hexdigest() != req.otp_hash:
        req.lockout_until = now + timedelta(hours=24); req.save(update_fields=['lockout_until'])
        admin_mail = os.getenv('LBAS_GMAIL_USER', '')
        if admin_mail: _send_email(f'LBAS OTP FAILURE: {school_id}', 'Invalid OTP attempt locked for 24h.', admin_mail)
        return JsonResponse({'error':'Invalid OTP. Account locked 24h.'}, status=403)
    req.used = True; req.save(update_fields=['used'])
    token = signing.dumps({'school_id': school_id, 'purpose':'reset'})
    return JsonResponse({'verified': True, 'token': token})

@csrf_exempt
def reset_password(request):
    data = parse_json_body(request)
    token = data.get('token',''); pwd = str(data.get('new_password','')).strip()
    if not token or not pwd: return JsonResponse({'error':'token and new_password required'}, status=400)
    try:
        payload = signing.loads(token, max_age=600)
    except Exception:
        return JsonResponse({'error':'Invalid or expired token'}, status=400)
    school_id = payload.get('school_id','')
    u = UserProfile.objects.filter(school_id=school_id).first()
    if not u: return JsonResponse({'error':'User not found'}, status=404)
    u.password = pwd  # TODO: hash password before storing
    u.save(update_fields=['password'])
    return JsonResponse({'reset': True})

@csrf_exempt
def report_problem(request):
    data = parse_json_body(request)
    school_id = str(data.get('school_id','')).strip().lower(); message = str(data.get('message','')).strip()
    if not school_id or not message: return JsonResponse({'error':'school_id and message required'}, status=400)
    now = timezone.now()
    if ProblemReport.objects.filter(school_id=school_id, created_at__gte=now-timedelta(hours=24)).exists():
        return JsonResponse({'error':'You have already submitted a report today. Please wait 24 hours.'}, status=429)
    ProblemReport.objects.create(school_id=school_id, message=message)
    admin_mail = os.getenv('LBAS_GMAIL_USER', '')
    if admin_mail: _send_email(f'LBAS Problem Report: {school_id}', message, admin_mail)
    return JsonResponse({'submitted': True})
