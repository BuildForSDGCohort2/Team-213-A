from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import models

from django.utils import timezone

from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from .managers import EventManager

auth_user_model = getattr(settings, "AUTH_USER_MODEL", "auth.User")


class Event(models.Model):
    """
    Event model
    """
    REPEAT_CHOICES = (
        ('NEVER', _('Never')),
        ('DAILY', _('Every Day')),
        ('WEEKDAY', _('Every Weekday')),
        ('WEEKLY', _('Every Week')),
        ('BIWEEKLY', _('Every 2 Weeks')),
        ('MONTHLY', _('Every Month')),
        ('YEARLY', _('Every Year')),
    )

    start_date = models.DateTimeField(verbose_name=_("start date: yyyy-mm-dd h:m"))
    end_date = models.DateTimeField(_("end date: yyyy-mm-dd h:m"))
    all_day = models.BooleanField(_("all day"), default=False)
    repeat = models.CharField(
        _("repeat"), max_length=15, choices=REPEAT_CHOICES, default='NEVER'
    )
    end_repeat = models.DateField(_("end repeat"), null=True, blank=True)
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"))
    thumbnail = models.ImageField(_("thumbnail"), upload_to="images/", blank=True)
    location = models.ManyToManyField(
        'Location', verbose_name=_('locations'), blank=True,
    )
    objects = EventManager()
    created_by = models.ForeignKey(
        auth_user_model, verbose_name=_("created by"), related_name='events',blank=True, null=True, on_delete=models.CASCADE)
    categories = models.ManyToManyField(
        'Category', verbose_name=_('Categories'), blank=True
    )

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self._last_popover_html = None
        self.title_extra = ''

    def get_l_start_date(self):
        """Localized start date."""
        return timezone.localtime(self.start_date)

    @cached_property
    def l_start_date(self):
        """

        :return:
        """
        return self.get_l_start_date()

    def get_l_end_date(self):
        """Localized end date."""
        return timezone.localtime(self.end_date)

    @cached_property
    def l_end_date(self):
        """

        :return:
        """
        return self.get_l_end_date()

    def is_happening(self, now):
        """Return True if the event is happening 'now', False if not."""
        start = self.l_start_date
        end = self.l_end_date
        happening = False
        # check that the event has started and 'now' is btwn start & end:
        if (now >= start) and (start.time() <= now.time() <= end.time()):
            if self.repeats('WEEKDAY'):
                if not now.weekday() > 4:  # must be weekday
                    happening = True
            elif self.repeats('DAILY') or self.repeats('NEVER'):
                happening = True
            elif self.repeats('MONTHLY'):
                if start.day <= now.day <= end.day:
                    happening = True
            elif self.repeats('YEARLY'):
                if (start.month <= now.month <= end.month) and \
                        (start.day <= now.day <= end.day):
                    happening = True
            else:
                repeat = {'WEEKLY': 7, 'BIWEEKLY': 14}
                while end <= now:
                    start += datetime.timedelta(days=repeat[self.repeat])
                    end += datetime.timedelta(days=repeat[self.repeat])
                if start <= now <= end:
                    happening = True
        return happening

    def repeats(self, repeat):
        """

        :param repeat:
        :return:
        """
        return self.repeat == repeat

    def is_chunk(self):
        """

        :return:
        """
        return self.l_start_date.day != self.l_end_date.day

    def starts_same_month_as(self, month):
        """

        :param month:
        :return:
        """
        return self.l_start_date.month == month

    def ends_same_month_as(self, month):
        """

        :param month:
        :return:
        """
        return self.l_end_date.month == month

    def starts_same_year_month_as(self, year, month):
        """

        :param year:
        :param month:
        :return:
        """
        return self.l_start_date.year == year and \
               self.l_start_date.month == month

    def starts_same_month_not_year_as(self, month, year):
        """

        :param month:
        :param year:
        :return:
        """
        return self.l_start_date.year != year and \
               self.l_start_date.month == month

    def starts_ends_same_month(self):
        """

        :return:
        """
        return self.l_start_date.month == self.l_end_date.month

    def starts_ends_yr_mo(self, year, month):
        """

        :param year:
        :param month:
        :return:
        """
        yr = self.l_start_date.year == year or self.l_end_date.year == year
        mo = self.l_start_date.month == month or self.l_end_date.month == month
        return yr and mo

    def get_start_end_diff(self):
        """Return the difference between start and end dates."""
        s = self.l_start_date
        e = self.l_end_date
        start = datetime.date(s.year, s.month, s.day)
        end = datetime.date(e.year, e.month, e.day)
        diff = start - end
        return abs(diff.days)

    @cached_property
    def start_end_diff(self):
        """

        :return:
        """
        return self.get_start_end_diff()

    def clean(self):
        """
        :return
        """
        self.clean_start_end_dates()
        self.clean_repeat()

    def clean_start_end_dates(self):
        """
        :return
        """
        if self.start_date and self.end_date:
            if self.l_start_date > self.l_end_date:
                raise ValidationError(
                    "The event's start date must be before the end date."
                )
            elif (self.l_end_date - self.l_start_date) > datetime.timedelta(7):
                raise ValidationError(
                    "Only events spanning 7 days or less are supported."
                )

    def clean_repeat(self):
        """
    :return
        """
        if self.repeats('NEVER') and self.end_repeat:
            # events not scheduled to repeat should't have an end repeat date
            self.end_repeat = None

        if self.repeats('DAILY') or self.repeats('WEEKDAY'):
            if self.is_chunk():
                raise ValidationError(
                    "Repeating every day or every weekday is not supported \
                    for events that start and end on different days."
                )

    def get_absolute_url(self):
        """

        :return:
        """
        return reverse('calendar:detail', args=[str(self.id)])

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')


class Location(models.Model):
    name_location = models.CharField(_('Name'), max_length=255)
    region = models.CharField(
        _('Region'), max_length=63, blank=True)
    city = models.CharField(
        _('City / Town'), max_length=63, blank=True)
    country = models.CharField(_('Country'), max_length=127, blank=True)

    def __str__(self):
        return self.name_location


class Category(models.Model):
    title = models.CharField(_('title'), max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'
