from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "category", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation"
        self.helper.label_class = "fw-bold"
        self.helper.field_class = "mb-3"

        self.helper.layout = Layout(
            Field("title", css_class="form-control", placeholder="Enter article title"),
            Field("content", css_class="form-control", rows="6", placeholder="Write your article here..."),
            Field("category", css_class="form-select"),
            Field("image", css_class="form-control"),
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Write your comment...", "class": "form-control"}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field("content", css_class="form-control"),
            # No Submit() here – the template or JS will handle buttons
        )


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 2, "placeholder": "Write a reply...", "class": "form-control"}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field("content", css_class="form-control"),
            # No Submit() – JavaScript will control it
        )
