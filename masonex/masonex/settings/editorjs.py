EDITORJS_CONFIG = {
    'plugins': [
        '@editorjs/paragraph',
        '@editorjs/underline',
        'editorjs-strikethrough',
        '@editorjs/inline-code',
        '@editorjs/header',
        '@editorjs/list',
        '@editorjs/quote',
        '@editorjs/image',
    ],
    'tools': {
        'Header': {
            'class': 'Header',
            'inlineToolbar': False,
            'shortcut': 'CMD+SHIFT+H',
            'config': {
                'levels': [2, 3, 4],
                'defaultLevel': 2,
            }
        },
        'Quote': {
            'class': 'Quote',
            'inlineToolbar': True,
            'shortcut': 'CMD+SHIFT+O',
            'config': {
                'quotePlaceholder': 'Enter the quote',
                'captionPlaceholder': 'Quote by',
            },
        },
        'List': {
            'class': 'List',
            'inlineToolbar': True,
            'shortcut': 'CMD+SHIFT+L',
        },
        'Underline': {
            'class': 'Underline',
            'shortcut': 'CMD+U',
        },
        'strikethrough': {
            'class': 'Strikethrough',
            'shortcut': 'CMD+SHIFT+X',
        },
        'InlineCode': {
            'class': 'InlineCode',
            'shortcut': 'CMD+SHIFT+M',
        },
    },
    'inlineToolbar': ('bold', 'italic', 'Underline', 'strikethrough', 'InlineCode', 'link'),
    'minHeight': 156,
    'i18n': {
        'messages': {
            'toolNames': {
                'InlineCode': 'Monospace',
                'Strikethrough': 'Cross',
            },
        },
    },
}
