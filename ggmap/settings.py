import yaml
import os
import sys

FP_SETTINGS = os.path.join(os.environ['HOME'], '.ggmaprc')

DEFAULTS = {'condaenv_qiime1': {'default': 'qiime_env',
                                'variable_name': 'QIIME_ENV'},
            'condaenv_qiime2': {'default': 'qiime2-2019.1',
                                'variable_name': 'QIIME2_ENV'},
            'condaenv_picrust': {'default': 'picrust',
                                 'variable_name': 'PICRUST_ENV'},
            # since condas init magic, activating an environment failes if
            # .bashrc is not read, which is the case when executing a
            # subprocess from python :-(
            'dir_conda': {'default': '%s/miniconda3/' % os.environ['HOME'],
                          'variable_name': 'DIR_CONDA'},
            # set a default for using a grid when submitting a job.
            # this is useful for people working on local hardware without a
            # grid infrastructure. Thus, typing fct(..., use_grid=False, ...)
            # is no longer necessary.
            'use_grid': {'default': True,
                         'variable_name': 'USE_GRID'},
            'fp_reference_phylogeny': {'default': None,
                                       'variable_name': 'FILE_REFERENCE_TREE'},
            'fp_reference_taxonomy': {
                'default': ('/projects/emp/03-otus/reference/'
                            '97_otu_taxonomy.txt'),
                'variable_name': 'FILE_REFERENCE_TAXONOMY'},
            'fp_binary_time': {'default': '/usr/bin/time',
                               'variable_name': 'EXEC_TIME'},
            'list_ranks': {'default': ['Kingdom', 'Phylum', 'Class', 'Order',
                                       'Family', 'Genus', 'Species'],
                           'variable_name': 'RANKS'},
            }


# stolen from https://stackoverflow.com/questions/13034496/
# using-global-variables-between-files
def init(err=sys.stderr):
    # load settings from file
    if os.path.exists(FP_SETTINGS):
        err.write('ggmap is custome code from Stefan Janssen, '
                  'download at https://github.com/sjanssen2/ggmap\n')
        err.write("Reading settings file '%s'\n" % FP_SETTINGS)
        with open(FP_SETTINGS, 'r') as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
    else:
        config = dict()

    # if variable is not set in settings file, fall back to default
    for field in DEFAULTS.keys():
        if field not in config:
            config[field] = DEFAULTS[field]['default']

    # set global variables to values from config file or fall back to defaults
    global QIIME_ENV
    QIIME_ENV = config['condaenv_qiime1']
    global QIIME2_ENV
    QIIME2_ENV = config['condaenv_qiime2']
    global PICRUST_ENV
    PICRUST_ENV = config['condaenv_picrust']
    global FILE_REFERENCE_TREE
    FILE_REFERENCE_TREE = config['fp_reference_phylogeny']
    global FILE_REFERENCE_TAXONOMY
    FILE_REFERENCE_TAXONOMY = config['fp_reference_taxonomy']
    global EXEC_TIME
    EXEC_TIME = config['fp_binary_time']
    global RANKS
    RANKS = config['list_ranks']
    global DIR_CONDA
    DIR_CONDA = config['dir_conda']
    global USE_GRID
    USE_GRID = config['use_grid']

    # if settings file does not exist, create one with current values as a
    # primer for user edits
    if not os.path.exists(FP_SETTINGS):
        with open(FP_SETTINGS, 'w') as f:
            yaml.dump(config, f)
        err.write('New config file "%s" created.' % FP_SETTINGS)