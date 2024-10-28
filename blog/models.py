from django.db import models
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField  
from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from meta.models import ModelMeta  
from datetime import datetime
from django.utils import timezone

class Author(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="author_profile",
        verbose_name=_("User"),
    )
    bio = models.TextField(_("Bio"), blank=True, null=True)
    profile_image = models.ImageField(
        _("Profile Image"),
        upload_to="author_images/",
        blank=True,
        null=True,
        help_text=_("Upload an image for the author's profile."),
    )
    website = models.URLField(_("Website"), blank=True, null=True)
    twitter_handle = models.CharField(
        _("Twitter Handle"),
        max_length=15,  # Limiting to 15 characters to match Twitter's username limit
        blank=True,
        null=True,
        help_text=_("Enter the Twitter handle without the '@' symbol."),
    )
    tags = TaggableManager(
        _("Tags"),
        help_text=_("Add relevant skills or interests to categorize authors."),
        blank=True,
    )

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def __str__(self):
        return self.get_full_name() or str(self.user)

    def get_full_name(self):
        """Returns the author's full name if available, otherwise their username."""
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return full_name if full_name else self.user.username

    def get_short_name(self):
        """Returns the author's first name, or username if first name is unavailable."""
        return self.user.first_name or self.user.username

    @property
    def twitter_url(self):
        """Returns the full Twitter profile URL if a handle is provided."""
        if self.twitter_handle:
            return f"https://twitter.com/{self.twitter_handle}"
        return None


class Article(ModelMeta, models.Model):
    title = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True, blank=True, editable=False)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="articles",
        verbose_name=_("Author"),
    )
    content = HTMLField(_("Content"))
    tags = TaggableManager(_("Tags"), help_text=_("Tags for categorizing articles"))
    publish_at = models.DateTimeField(_("Publish Date"), null=True, blank=True)
    is_published = models.BooleanField(_("Published"), default=False)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    _metadata = {
        "title": "title",
        "description": "get_description",
        "keywords": "get_keywords",
        "og_type": "article",
    }

    class Meta:
        ordering = ["-publish_at"]
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    def get_description(self):
        """Return a shortened excerpt of the content for SEO description."""
        return self.content[:160]

    def get_keywords(self):
        """Generate SEO keywords based on assigned tags."""
        return ", ".join(tag.name for tag in self.tags.all())

    def save(self, *args, **kwargs):
        """Generate slug if not provided and update published date if publishing."""
        if not self.slug:
            self.slug = slugify(self.title)
        # Automatically set publish_at if publishing and not already set
        if self.is_published and not self.publish_at:
            self.publish_at = datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(
        "Article",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Article"),
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Author"),
    )
    content = models.TextField(_("Content"), max_length=500)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        """Return a concise representation of the comment's author and a preview of the content."""
        return f"{self.author.first_name} {self.author.last_name} - {self.content[:20]}"

    def is_recent(self):
        """Return True if the comment was posted within the last day."""
        return (timezone.now() - self.created_at).days < 1


class Reaction(models.Model):
    LIKE = "like"
    DISLIKE = "dislike"
    HEART = "heart"
    LAUGH = "laugh"
    SAD = "sad"

    REACTION_CHOICES = [
        (LIKE, _("Like")),
        (DISLIKE, _("Dislike")),
        (HEART, _("Heart")),
        (LAUGH, _("Laugh")),
        (SAD, _("Sad")),
    ]

    article = models.ForeignKey(
        "Article",
        on_delete=models.CASCADE,
        related_name="reactions",
        verbose_name=_("Article"),
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="reactions",
        verbose_name=_("User"),
    )
    reaction_type = models.CharField(
        _("Reaction Type"),
        max_length=10,
        choices=REACTION_CHOICES,
        help_text=_("Type of reaction, e.g., Like, Dislike, etc."),
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        unique_together = ("article", "user", "reaction_type")
        verbose_name = _("Reaction")
        verbose_name_plural = _("Reactions")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} reacted with '{self.reaction_type}' to {self.article.title}"
