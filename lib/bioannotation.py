'''
Warning: this module requires Python 3.2 or higher

It's also in an initial development phase, so either don't use it or be tolerant of
API changes.
'''

import re

class FunctionalAnnotation:
    """
    While recognizing that an enormous variety of attributes could go here in
    describing the functional annotation of a BioThing, I'm starting with those
    we most often encounter and need to be available in common output formats.

    Also, there's a place for having attributes like this abstracted, stored in
    ontologies, etc.  We've done all that before.  For now I'm going to try
    and hopefully enjoy the utility of having the most direct properties always
    directly available.
    """
    def __init__( self, product_name=None, gene_symbol=None, go_annotations=None, ec_numbers=None ):
        self.product_name     = product_name
        self.gene_symbol      = gene_symbol
        self.go_annotations   = go_annotations
        self.ec_numbers       = ec_numbers

        if self.go_annotations is None:
            self.go_annotations = list()

        if self.ec_numbers is None:
            self.ec_numbers = list()

    def add_go_annotation( self, go ):
        """
        Note to self: Modify this to allow passing GOAnnotation object or string.
        Right now it expects an GOAnnotation object
        """
        self.go_annotations.append( go )
        
    def add_ec_number( self, ec_num ):
        """
        Note to self: Modify this to allow passing ECAnnotation object or string.
        Right now it expects an ECAnnotation object
        """
        self.ec_numbers.append( ec_num )
        
class GOAnnotation:
    """
    A functional annotation can have an infinite number of associated GO Annotations

    Details here:
    http://www.geneontology.org/GO.evidence.shtml

    Yes, the 'with_from' attribute name is awkward, but 'with/from' isn't legal and
    both 'with' and 'from' are python reserved words.

    The go_id attribute here is just the numeric portion without "GO" or "GO:" or
    anything else attached (allowing the developer to define it as required.)
    """
    def __init__( self, go_id=None, ev_code=None, with_from=None ):
        self.go_id        = go_id
        self.ev_code      = ev_code
        self.with_from    = with_from

        ## process any GO ID passed to only contain the numeric portion
        go_pattern = re.compile('(\d+)')
        m = go_pattern.search(self.go_id)

        if m:
            self.go_id = m.group(1)
        else:
            raise Exception("ERROR: failed to extract numeric portion of ID from new GOAnnotation")


class ECAnnotation:
    """
    A functional annotation can have an infinite number of associated EC Annotations

    Details here:
    http://www.chem.qmul.ac.uk/iubmb/enzyme/

    While the official terms for the levels are 'class', 'subclass' etc. we have to use
    different keys for the attributes since those conflict with reserved keywords in
    both python and other frameworks.

    class1 = 1          = Oxidoreductases
    class2 = 1.10       = Acting on diphenols and related substances as donors
    class3 = 1.10.3     = With oxygen as acceptor
    number = 1.10.3.2   = laccase

    Currently does not have an index of EC terms to provide other attributes which will
    be added in the future, such as:

    accepted_name = laccase
    reaction = 4 benzenediol + O2 = 4 benzosemiquinone + 2 H2O
    systematic_name = benzenediol:oxygen oxidoreductase
    CAS_registry_number = 80498-15-3
    """
    def __init__( self, number=None ):
        self.number = number
        self.class1 = None
        self.class2 = None
        self.class3 = None

        re_pattern = re.compile('(((([0-9\-]+)\.[0-9\-]+)\.[0-9\-]+)\.[a-z0-9\-]+)')
        m = re_pattern.search(self.number)

        if m:
            self.class1 = m.group(4)
            self.class2 = m.group(3)
            self.class3 = m.group(2)
            self.number = m.group(1)
        else:
            raise Exception("ERROR: Attempt to add an EC number ({0}) in unrecognized format.  Expected N.N.N.N (where N can be 0-9 or a dash)".format(self.number))
        
