from django import forms

class ParamForm(forms.Form):
   is_nb_addr = forms.CharField(max_length = 50, label='IS neighbor Address', required=False)
   #is_pref = forms.CharField(max_length = 200, label='IS prefix', widget=forms.TextInput(attrs={'size':100}))
   #is_es_nx_hop = forms.CharField(max_length = 50, label='ES next-hop of IS')
   #is_vnh_label = forms.CharField(max_length = 50, label='VNH label of IS')
   dr_nb_addr = forms.CharField(max_length = 50, label='DR neighbor address', required=False)
   #dr_pref = forms.CharField(max_length=50, label='DR prefix')
   #dr_es_nx_hop = forms.CharField(max_length=50, label='ES next-hop of DR')
   #dr_vnh_label = forms.CharField(max_length=50, label='VNH label of DR')
   #dr_sr_addr = forms.CharField(max_length=50, label='DR source address')
   #dr_dt_addr = forms.CharField(max_length=50, label='DR destination address')
   es_nb_addr = forms.CharField(max_length=50, label='ES neighbor address', required=False)

class CollectForm(forms.Form):
   hostname = forms.CharField(max_length = 100, label='Hostname', widget=forms.TextInput(attrs={'size':50}))
   username = forms.CharField(max_length = 100, label='Username', widget=forms.TextInput(attrs={'size':50}))
   password = forms.CharField(max_length = 100, label='Password', widget=forms.TextInput(attrs={'size':50}))
   command = forms.CharField(max_length = 200, label='Command', widget=forms.TextInput(attrs={'size':80}))
