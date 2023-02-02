from django.core.management.base import BaseCommand
from django.contrib.staticfiles.finders import get_finders
from django_sass import compile_sass

from pathlib import Path
import os


class Command(BaseCommand):
    help = 'Build SCSS files into CSS ones.'

    def handle(self, *args, **kwargs):
        scss_files = []
        ignore_patterns = ['node_modules', '_*.scss', 'core']

        for finder in get_finders():
            for path, storage in finder.list(ignore_patterns):
                if path.endswith('.scss'):
                    fullpath = finder.find(path)
                    scss_files.append(fullpath)

        for scss_file in scss_files:
            path = Path(scss_file)
            css_file = os.path.join(path.parent.parent, f'dist\\css\\{path.stem}.min.css')

            compile_sass(
                inpath=scss_file,
                outpath=css_file,
                output_style='compressed',
                precision=8,
            )
