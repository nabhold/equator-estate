from django.contrib import admin
from .models import Article, Comment, Reaction

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_published", "publish_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "author__username", "tags__name")
    list_filter = ("is_published", "tags", "publish_at")
    date_hierarchy = "publish_at"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "content", "created_at")
    search_fields = ("author__username", "content")
    list_filter = ("created_at",)
    date_hierarchy = "created_at"

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ("user", "reaction_type", "article")
    search_fields = ("user__username", "reaction_type", "article__title")
    list_filter = ("reaction_type", "article")
 

 