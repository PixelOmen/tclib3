from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name='tclib3',
    version='1.0.0',
    description='A timecode utility library.',
    author='Eman',
    author_email='pixelomen@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Media Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=['src'],
    python_requires='>=3.10, <4',
    install_requires=[],
    include_package_data=True,
)