from django.shortcuts import render, render_to_response, redirect, get_object_or_404
# Create your views here.
from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django import forms
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from allauth.account.decorators import verified_email_required ,login_required
from project.models import *

#@login_required
#def authenticated_users_only_view(request):
#    print('test')

#@verified_email_required
#def verified_users_only_view(request):
#    print('test')

def about(request):
    return render(request, 'about.html')

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    type = forms.ModelChoiceField(queryset=userType.objects.all(), required=False)
    
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.type = self.cleaned_data['type']
        user.save()

def archive(request):
    reports = report.objects.all().order_by('-timestamp')
    return render_to_response('archive.html', RequestContext(request), Context({'reports': reports}))

def example_post(request):
    return render(request, 'example_post.html')

def post_result(request):
    b = report(title=request.GET['device_id'],
               content=request.GET['content'],
               timestamp=request.GET['timestamp'])
    b.save()
    return redirect('/')

def manage(request):
    if request.user.is_authenticated:
        return render(request, 'manage.html')
    else:
        return redirect('/')

def upload(request):
    if request.user.is_authenticated:
        stations = station.objects.all()
        selected = int(request.GET.get('select_station', '-1'))
        devices = ''
        if selected != '':
            devices = device.objects.filter(station=selected)
            dtypes = ""
            for d in devices:
                dtypes += "'" + str(d.deviceType.unit) + "',"
            dtypes = dtypes[:-1]
        context = {'stations':stations, 'devices':devices, 'dtypes':dtypes}
        return render(request, 'upload.html', context)
    else:
        return redirect('/')

def upload_result(request):
    if request.user.is_authenticated:
        if request.GET.get('station', '')!='':
            s = request.GET.get('station', '')
            c = request.GET.get('report', '')
            d = device.objects.filter(name = request.GET.get('device','')).first()
            t = request.GET.get('timestamp', '1970-01-01 00:00:00')
            r = report(
            device = d,
            content = c,
            reading_time = t,
            timestamp = datetime.now()
            )
            r.save()
            return redirect('/project/manage/upload_result/')
        return render(request, 'upload_result.html')
    else:
        return redirect('/')

def manage_stations(request):
    if request.user.is_authenticated:
        rs = request.GET.get('remove_station','')
        rd = request.GET.get('remove_device','')
        ast = request.GET.get('station_name','')
        ad = request.GET.get('device_name','')
        if rs != '':
            station.objects.filter(pk = int(rs)).delete()
            return redirect('/project/manage/stations/')
        if rd != '':
            device.objects.filter(name = rd).delete()
            return redirect('/project/manage/stations/')
        if ast != '':
            ns = station(
                name = ast,
                #operator = UserProfile.objects.filter(user_id=request.user.id).first(),
                operator = request.user.profile,
                latitude = request.GET.get('station_lat', ''),
                longtitude = request.GET.get('station_long', ''),
                status = status.objects.filter(id='1').first()
                )
            #ns.save()
            ns.save(userobj=request.user)
            return redirect('/project/manage/stations/')
        if ad != '':
            nd = device(
                name = ad,
                station = station.objects.filter(name=request.GET.get('device_station', '')).first(),
                deviceType = deviceType.objects.filter(device_type=request.GET.get('devicetype', '')).first(),
                last_reading_time = '',
                status = status.objects.filter(id='1').first()
                )
            #nd.save()
            nd.save(userobj=request.user)
            return redirect('/project/manage/stations/')
        stations = station.objects.filter(operator=request.user.id)
        #devices = device.objects.none()
        devices = device.objects.all()
        types = deviceType.objects.all()
        #for s in stations:
        #    devices = devices | device.objects.filter(station=s.pk)
        context = {'stations':stations, 'devices':devices, 'types':types}
        return render(request, 'manage_stations.html', context)
    else:
        return redirect('/')
def manage_stations_result(request):
    return render(request, 'manage_stations.html')#, context)



@login_required
def view_following(request):
	# Get the stations followed by the user
	followed = station.objects.filter(following__user_id=request.user.id, following__status=1)
	latest_reports = dict()
	for f in followed:
		reportList = []
		dev = device.objects.filter(station=f.id)
		for d in dev:
			try:
				reportList.append(report.objects.filter(device_id = d.id).latest('reading_time'))

			except:
				print('exeception')
		latest_reports[str(f.id)] = reportList
	
	context = {'followed':followed, 'latest_reports':latest_reports }
	return render(request, 'following.html', context)


def station_details(request, id_str):
	s_id = int(id_str)
	crrnt_station = get_object_or_404(station, id=s_id)
	# XXX This could be handled more elegantly, but for now just throw 404
	station_devices = device.objects.filter(station__id=s_id)
	context = {'station':crrnt_station, 'devices':station_devices}
	return render(request, "station_details.html", context)

def device_details(request, id_str):
	d_id = int(id_str)

	crrnt_device = get_object_or_404(device, id=d_id)

	device_reports = report.objects.filter(device__id=d_id)[:10]
	context = {'device':crrnt_device, 'reports':device_reports}
	return render(request, "device_details.html", context)


def download_device_reports(request, device_id):
	dev = get_object_or_404(device, id=device_id)
	headerStr = "Station: "+dev.station.name+"\r\nDevice Name: "+ dev.name+"\r\nDevice Type: "+dev.deviceType.device_type+"\r\nUnits: "+dev.deviceType.unit+"\r\n"
	response = HttpResponse(headerStr, content_type="text")
	reports = report.objects.filter(device__id=int(device_id))
	for r in reports:
		response.write(str(r.content) + "," + str(r.reading_time)+";\r\n")
	response['Content-Disposition'] = 'attachment; filename=\"device_history.csv\"'
	return response


def stations(request):
	stations = station.objects.all().order_by('name')
	station_map = dict()
	station_map['stations'] = stations
	for s in stations:
		station_dtl = dict()
		station_dtl['followed'] = True if s.following_set.filter(user_id=request.user.id,status=1).count() != 0 else False
		station_dtl['devices'] = device.objects.filter(station_id=s.id)
		station_map[str(s.id)] = station_dtl
	context = {'station_map':station_map }
	return render(request, "base_stations.html", context)


@login_required
def follow_unfollow(request, station_id):
	try:
		m = following.objects.get(user_id=request.user.id, station_id=station_id)
		if m.status.id == 1:
			m.status = status.objects.get(id=0)
		else:
			m.status = status.objects.get(id=1)
	except:
		m = following(user=request.user.profile,
			   station=station.objects.get(id=station_id),
			   status=status.objects.get(id=1))
	m.save(userobj=request.user)
	return redirect(request.META.get('HTTP_REFERER'))

def submit_search_query(request, searchMode):
	searchStr = request.POST['searchThisSpecificName']
	return redirect(reverse('project-search-result', args=(searchMode,searchStr)))

def show_search_results(request, searchMode, searchStr):
	results = dict()
	searchStations = False
	searchDevices = False
	if ((searchMode == 'all') or (searchMode == 'stations')):
		station_map = dict()
		stations = station.objects.filter(Q(name__icontains=searchStr)|Q(operator__user__username=searchStr)).order_by('name')
		station_map['stations'] = stations
		for s in stations:
			station_dtl = dict()
			station_dtl['followed'] = True if s.following_set.filter(user_id=request.user.id,status=1).count() != 0 else False
			station_dtl['devices'] = device.objects.filter(station_id=s.id)
			station_map[str(s.id)] = station_dtl
		results['station_map'] = station_map
		searchStations = (stations.count() > 0)
	if ((searchMode == 'all') or (searchMode == 'devices')):
		devices = device.objects.filter(Q(name__icontains=searchStr)|Q(station__name__icontains=searchStr)).order_by('last_reading_time')
		results['devices'] = devices
		searchDevices = (devices.count() > 0)

	context={'showStations':searchStations, 'showDevices':searchDevices, 'results':results}
	return render(request, "search.html", context)
