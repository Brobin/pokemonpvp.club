from markdownx.utils import markdownify as _markdownify


def markdownify(text):
    return _markdownify(text).replace(
        '<table>', '<table class="table table-striped table-hover">'
    ).replace(
        '<pre>', '<pre class="prettyprint">'
    )
