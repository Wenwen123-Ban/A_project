import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.models import Course, UserProfile
from .utils import parse_json_body, require_auth, unauth


@csrf_exempt
def api_courses(request):
    if request.method == 'GET':
        level = request.GET.get('level')
        qs = Course.objects.filter(is_active=True)
        if level:
            qs = qs.filter(school_level=level)
        courses = list(qs.values('id', 'name', 'school_level'))
        return JsonResponse({'courses': courses})

    elif request.method == 'POST':
        user = require_auth(request)
        if not user or not user.is_staff:
            return unauth()
        
        data = parse_json_body(request)
        name = data.get('name', '').strip()
        level = data.get('school_level', '').strip()
        
        if not name or not level:
            return JsonResponse({'success': False, 'message': 'Name and level required'}, status=400)
            
        if Course.objects.filter(name=name, school_level=level).exists():
            return JsonResponse({'success': False, 'message': 'Course already exists'}, status=400)
            
        course = Course.objects.create(name=name, school_level=level, added_by=user.school_id)
        return JsonResponse({'success': True, 'id': course.id, 'name': course.name, 'school_level': course.school_level})

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def api_course_detail(request, course_id):
    user = require_auth(request)
    if not user or not user.is_staff:
        return unauth()

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Not found'}, status=404)

    if request.method == 'PUT':
        data = parse_json_body(request)
        new_name = data.get('name', '').strip()
        if new_name:
            if Course.objects.filter(name=new_name, school_level=course.school_level).exclude(id=course.id).exists():
                return JsonResponse({'success': False, 'message': 'Course name already exists for this level'}, status=400)
            course.name = new_name
            course.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'message': 'Name required'}, status=400)

    elif request.method == 'DELETE':
        count = UserProfile.objects.filter(course=course.name).count()
        
        data = parse_json_body(request) if request.body else {}
        force = request.GET.get('force') == 'true' or data.get('force') == True
        
        if count > 0 and not force:
            return JsonResponse({'safe': False, 'count': count})
            
        if count > 0 and force:
            UserProfile.objects.filter(course=course.name).update(course='N/A')
            
        course.delete()
        return JsonResponse({'deleted': True})

    return JsonResponse({'error': 'Method not allowed'}, status=405)