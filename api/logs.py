from django.http import JsonResponse
from core.models import AuditLog
from .utils import require_admin, unauth

def api_logs(request):
    if not require_admin(request):
        return unauth()
    page = max(1, int(request.GET.get('page', '1') or '1'))
    per = 30
    qs = AuditLog.objects.all().order_by('-timestamp')
    total = qs.count()
    start = (page-1)*per
    rows = list(qs[start:start+per].values('timestamp','actor_id','action','target_type','target_id','detail'))
    return JsonResponse({'results': rows, 'page': page, 'pages': (total+per-1)//per, 'total': total})
