# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from daterange_filter.filter import DateRangeFilterBaseForm
from widgets import DatePickerWidget

FILTER_PREFIX = 'drf__'


class DateRangeExForm(forms.Form):

    def __init__(self, request, *args, **kwargs):
        field_name = kwargs.pop('field_name')
        self.request = request
        super(DateRangeExForm, self).__init__(*args, **kwargs)

        self.fields['%s%s__gte' % (FILTER_PREFIX, field_name)] = forms.DateField(
            label='',
            widget=DatePickerWidget(
                attrs={
                    'class': 'date',
                    'placeholder': 'Desde el día'
                },
                format="%m/%d/%Y"
            ),
            input_formats = ('%Y/%m/%d', '%d/%m/%Y', '%m/%d/%Y'),
            localize=True,
            required=False
        )

        self.fields['%s%s__lte' % (FILTER_PREFIX, field_name)] = forms.DateField(
            label='',
            widget=DatePickerWidget(
                attrs={
                    'class': 'date',
                    'placeholder': 'Hasta el día',
                },
                format="%m/%d/%Y"
            ),
            input_formats = ('%Y/%m/%d', '%d/%m/%Y', '%m/%d/%Y'),
            localize=True,
            required=False,
        )
    # end def
# end class
