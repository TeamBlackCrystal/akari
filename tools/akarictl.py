import argparse
import os
from string import capwords

from templates import (
    INPUT_DATA_CLASS_NAME_TEMPLATE,
    INPUT_DATA_TEMPLATE,
    INTERACTOR_CLASS_NAME,
    INTERACTOR_TEMPLATE,
    REPOSITORY_CLASS_NAME_TEMPLATE,
    REPOSITORY_TEMPLATE,
    USE_CASE_CLASS_NAME_TEMPLATE,
    USE_CASE_TEMPLATE,
)
from mipac.utils.format import str_lower

# from templates import TEMPLATES

parser = argparse.ArgumentParser()
parser.add_argument('--method')
parser.add_argument('--model')
parser.add_argument('--generate', '-g', action=argparse.BooleanOptionalAction)
args = parser.parse_args()


def create_python_path(path: str) -> str:
    return path.replace('/', '.').replace('...src', 'src')


class Generater:
    def __init__(self, method: str, model: str) -> None:
        self.method = method
        self.model = model
        self._split_name = args.model.split('/')
        print('/'.join(self._split_name[:-1]))
        self.path = '/'.join(self._split_name[:-1]) + '/'
        self.name = self._split_name[-1]

    def exists_or_make(self, path: str):

        if os.path.exists(f'../src/{path}/{self.path[:-1]}') is False:
            os.makedirs(f'../src/{path}/{self.path[:-1]}')
            with open(
                f'../src/{path}/{self.path}__init__.py', mode='w', encoding='utf-8'
            ) as f:
                f.close()
            return f'../src/{path}/{self.path[:-1]}'
        return f'../src/{path}/{self.path[:-1]}'

    def create_file(self, path: str, content: str | None = None):
        if os.path.exists(path) is False:
            with open(path, encoding='utf-8', mode='w') as f:
                if content:
                    f.write(content)

    def generate_domain(self):
        path = f'domain/models/{self._split_name[-1]}'
        create_path = self.exists_or_make(str_lower(path))
        domain_path = f'{create_path}{str_lower(self.name)}_if'
        repository_class_name = REPOSITORY_CLASS_NAME_TEMPLATE.format(
            self.name.capitalize()
        )
        content = REPOSITORY_TEMPLATE.format(repository_class_name)
        self.create_file(f'{domain_path}.py', content)
        return {
            'import_path': f'{create_python_path(domain_path)}',
            'class_name': repository_class_name,
        }

    def generate_input_data(self, path):
        input_data_path = (
            f'{path}{str_lower(self.name)}_{str_lower(self.method)}_input_if'
        )
        input_data_class_name = INPUT_DATA_CLASS_NAME_TEMPLATE.format(
            self.name.capitalize(), self.method.capitalize()
        )
        input_data_template = INPUT_DATA_TEMPLATE.format(input_data_class_name)
        self.create_file(f'{input_data_path}.py', input_data_template)

        return {
            'import_path': f'{create_python_path(input_data_path)}',
            'class_name': input_data_class_name,
        }

    def generate_usecase(self, path: str):

        input_data = self.generate_input_data(path)

        use_case_class_name = USE_CASE_CLASS_NAME_TEMPLATE.format(
            f'{self.name.capitalize()}{self.method.capitalize()}'
        )
        usecase_template = USE_CASE_TEMPLATE.format(
            input_data['import_path'], input_data['class_name'], use_case_class_name
        )
        usecase_path = f'{path}{str_lower(self.name)}_{str_lower(self.method)}_use_case'
        self.create_file(f'{usecase_path}.py', usecase_template)
        return {
            'import_path': create_python_path(usecase_path),
            'class_name': use_case_class_name,
            'input_data': input_data,
        }

    def generate_interactor(self):
        path = f'interactor/{self._split_name[-1]}/{self.method}'
        create_path = self.exists_or_make(str_lower(path))
        interactor_path = (
            f'{create_path}{str_lower(self.name)}_{str_lower(self.method)}'
        )

        domain = self.generate_domain()
        usecase = self.generate_usecase(create_path)

        interactor_class_name = INTERACTOR_CLASS_NAME.format(f'{self.name.capitalize()}{self.method.capitalize()}')

        interactor_template = INTERACTOR_TEMPLATE.format(
            domain['import_path'], # TODO 無罪
            domain['class_name'], # TODO 無罪
            usecase['input_data']['import_path'], # TODO 無罪
            usecase['input_data']['class_name'], # TODO 無罪
            usecase['import_path'], # TODO 無罪
            usecase['class_name'],
            interactor_class_name,
            str_lower(domain['class_name']).replace('_i_f_', ''),
        )
        self.create_file(f'{interactor_path}.py', interactor_template)


if args.generate:
    generator = Generater(args.method, args.model)
    generator.generate_interactor()

