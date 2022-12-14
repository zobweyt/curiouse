from django.urls import reverse_lazy

EDITORJS_VERSION = '2.26.2'

EDITORJS_DEFAULT_PLUGINS = (
    '@editorjs/paragraph',
    '@editorjs/header',
    '@editorjs/list',
    '@editorjs/quote',
    '@editorjs/image',
    '@editorjs/underline',
    '@editorjs/inline-code',
)

EDITORJS_DEFAULT_CONFIG_TOOLS = {
    'paragraph': {
        'class': 'Paragraph',
        'shortcut': 'CMD+SHIFT+A',
    },
    'Header': {
        'class': 'Header',
        'inlineToolbar': False,
        'shortcut': 'CMD+SHIFT+H',
        'config': {
            'placeholder': 'Enter a header',
            'levels': [1, 2, 3],
        },
    },
    'List': {
        'class': 'List',
        'inlineToolbar': True,
        'shortcut': 'CMD+SHIFT+L',
    },
    'Quote': {
        'class': 'Quote',
        'inlineToolbar': True,
        'shortcut': 'CMD+SHIFT+Q',
        'config': {
            'quotePlaceholder': 'Enter the quote',
            'captionPlaceholder': 'Quote by',
        },
    },
    'Image': {
        'class': 'ImageTool',
        'shortcut': 'CMD+SHIFT+U',
        "config": {
            "endpoints": {
                "byFile": reverse_lazy('editorjs_image_upload'),
                "byUrl": reverse_lazy('editorjs_image_by_url')
            }
        },
    },
    'Underline': {
        'class': 'Underline',
        'shortcut': 'CMD+U',
    },
    'InlineCode': {
        'class': 'InlineCode',
        'shortcut': 'CMD+SHIFT+M',
    },
}

EDITORJS_CONFIG_OVERRIDE = {
    'inlineToolbar': ('bold', 'italic', 'Underline', 'InlineCode', 'link'),
    'minHeight': 256,
    'i18n': {
        'messages': {
            'toolNames': {
                'InlineCode': 'Monospace',
                'Strikethrough': 'Cross',
            },
        },
    },
}
