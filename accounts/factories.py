import factory
from factory.django import DjangoModelFactory
from faker import Faker
from .models import CustomUser, Profile

fake = Faker()

class CustomUserFactory(DjangoModelFactory):
    """
    Factory for generating CustomUser instances.
    """
    class Meta:
        model = CustomUser

    email = factory.LazyAttribute(lambda _: fake.email())
    username = factory.LazyAttribute(lambda _: fake.user_name())
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    date_of_birth = factory.LazyAttribute(lambda _: fake.date_of_birth())
    is_active = True
    is_admin = False
    date_joined = factory.LazyAttribute(lambda _: fake.date_time_this_decade())

class ProfileFactory(DjangoModelFactory):
    """
    Factory for generating Profile instances.
    """
    class Meta:
        model = Profile
        # accounts.signals.create_or_update_user_profile already creates a
        # Profile when the SubFactory below creates a new CustomUser, so a
        # plain create() here would violate Profile.user's unique
        # constraint. get_or_create fetches that row and updates it with
        # the fields below instead of inserting a duplicate.
        django_get_or_create = ("user",)

    user = factory.SubFactory(CustomUserFactory)
    profile_image = None
    bio = factory.LazyAttribute(lambda _: fake.paragraph(nb_sentences=3))
    # Profile.phone_number is max_length=15; Faker's default phone_number()
    # provider can exceed that (extensions, formatting), so truncate.
    phone_number = factory.LazyAttribute(lambda _: fake.phone_number()[:15])
    website = factory.LazyAttribute(lambda _: fake.url())
    address = factory.LazyAttribute(lambda _: fake.address())
    date_of_birth = None
