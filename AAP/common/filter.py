from django_filters import FilterSet
from .models import Pet


class PetOwnerFilter(FilterSet):
    class Meta:
        model = Pet
        fields = ['owner', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = kwargs['request']
        if request.user.is_authenticated:
            username = request.user.username
            my_choices = username
            self.filters['account'].extra.update({'choices': my_choices})
