# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.core.urlresolvers import reverse

from data_collector.models import DataPoint, Alert

class StatusView(TemplateView):
    template_name = 'status.html'

    def get_context_data(self, **kwargs):
        ctx = super(StatusView, self).get_context_data(**kwargs)

        nodes_and_data_types = DataPoint.objects.all().values_list('node_name',
                                                                   'data_type').distinct()
        status_data_dict = dict()
        for node_and_data_type_pair in nodes_and_data_types:
            node_name = node_and_data_type_pair[0]
            data_type = node_and_data_type_pair[1]

            data_point_map = status_data_dict.setdefault(node_name, dict())
            data_point_map[data_type] = DataPoint.objects.filter(
                node_name=node_name, data_type=data_type
            ).latest('datetime')

        ctx['status_data_dict'] = status_data_dict
        return ctx

class AlertListView(ListView):
    template_name = 'alerts_list.html'
    model = Alert

class NewAlertView(CreateView):
    template_name = 'create_or_update_alert.html'
    model = Alert
    fields = [
        'data_type', 'min_value', 'max_value', 'node_name', 'is_active'
    ]

    def get_success_url(self):
        return reverse('alerts-list')

class EditAlertView(UpdateView):
    template_name = 'create_or_update_alert.html'
    model = Alert
    fields = [
        'data_type', 'min_value', 'max_value', 'node_name', 'is_active'
    ]

    def get_success_url(self):
        return reverse('alerts-list')
