# -*- coding: utf-8 -*-
"""
Data types provided by plugin

Register data types via the "aiida.data" entry point in setup.json.
"""

# You can directly use or subclass aiida.orm.data.Data
# or any other data type listed under 'verdi data'
from voluptuous import Schema, Optional, Required, All, Any
from aiida.orm import Dict

# A subset of diff's command line options
cmdline_options = {
    Required('c', default='confout.gro'): str,
    Required('e', default='energy.edr'): str,
    Required('g', default='md.log'): str,
    Required('o', default='trajectory.trr'): str,
    Optional('cpo'): str,
    Optional('v'): str
}

class MdrunParameters(Dict):  # pylint: disable=too-many-ancestors
    """
    Command line options for diff.

    This class represents a python dictionary used to
    pass command line options to the executable.
    """

    # "voluptuous" schema  to add automatic validation
    schema = Schema(cmdline_options)


    # pylint: disable=redefined-builtin
    def __init__(self, dict=None, **kwargs):
        """
        Constructor for the data class

        Usage: ``MdrunParameters(dict{'ignore-case': True})``

        :param parameters_dict: dictionary with commandline parameters
        :param type parameters_dict: dict

        """
        dict = self.validate(dict)
        super().__init__(dict=dict, **kwargs)

    def validate(self, parameters_dict):  # pylint: disable=no-self-use
        """Validate command line options.

        Uses the voluptuous package for validation. Find out about allowed keys using::

            print(MdrunParameters).schema.schema

        :param parameters_dict: dictionary with commandline parameters
        :param type parameters_dict: dict
        :returns: validated dictionary
        """
        return MdrunParameters.schema(parameters_dict)

    def cmdline_params(self, tprfile):
        """Synthesize command line parameters.

        e.g. [ '--ignore-case', 'filename1', 'filename2']

        :param pdbfile: Name of input pdb file
        :param type pdbfile: str

        """
        parameters = []

        parameters.append('mdrun')
        parameters.extend(['-s', tprfile])

        parm_dict = self.get_dict()

        for k in parm_dict.keys():

            parameters.extend(['-' + k, parm_dict[k]])

        return [str(p) for p in parameters]

    def __str__(self):
        """String representation of node.

        Append values of dictionary to usual representation. E.g.::

            uuid: b416cbee-24e8-47a8-8c11-6d668770158b (pk: 590)
            {'ignore-case': True}

        """
        string = super().__str__()
        string += '\n' + str(self.get_dict())
        return string
