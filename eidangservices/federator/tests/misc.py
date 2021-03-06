# -*- coding: utf-8 -*-
"""
Federator misc related test facilities.
"""

import copy
import io
import unittest

from lxml import etree

from eidangservices import settings
from eidangservices.federator.server.misc import elements_equal


# -----------------------------------------------------------------------------
class ElementsEqualTestCase(unittest.TestCase):

    def setUp(self):
        self.ifd = io.BytesIO(b'<?xml version="1.0" encoding="UTF-8"?><FDSNStationXML xmlns="http://www.fdsn.org/xml/station/1" schemaVersion="1.0"><Source>EIDA</Source><Created>2018-07-31T11:02:19.176617</Created><Network xmlns="http://www.fdsn.org/xml/station/1" code="Z3" startDate="2015-01-01T00:00:00" endDate="2020-07-01T00:00:00" restrictedStatus="closed"><Description>AlpArray Seismic Network (AASN) temporary component</Description></Network><Network xmlns="http://www.fdsn.org/xml/station/1" code="Z3" startDate="2005-06-05T00:00:00" endDate="2007-04-30T00:00:00" restrictedStatus="open"><Description>Egelados project, RUB Bochum, Germany</Description></Network><Network xmlns="http://www.fdsn.org/xml/station/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:resif="http://www.fdsn.org/xml/station/1/resif" code="Z3" alternateCode="ALPARRAY" startDate="2015-07-01T00:00:00.000000" endDate="2020-07-31T00:00:00.000000" restrictedStatus="closed"><Comment><Value>DOI:http://dx.doi.org/10.12686/alparray/z3_2015</Value><BeginEffectiveTime>2015-07-01T00:00:00.000000</BeginEffectiveTime><EndEffectiveTime>2020-07-31T00:00:00.000000</EndEffectiveTime><Author><Name>Resif Information System</Name><Agency>R&#233;seau Sismologique et g&#233;od&#233;sique Fran&#231;ais (RESIF)</Agency><Email>sismob@resif.fr</Email></Author></Comment><Description>AlpArray backbone temporary stations</Description><SelectedNumberStations>306</SelectedNumberStations><TotalNumberStations>68</TotalNumberStations></Network><Network xmlns="http://www.fdsn.org/xml/station/1" code="Z3" startDate="1980-01-01T00:00:00" restrictedStatus="closed"><Description>AlpArray DSEBRA</Description></Network></FDSNStationXML>') # noqa

    def test_equal(self):
        t = etree.parse(self.ifd).getroot()
        t[:] = sorted(t, key=lambda c: c.tag)
        t_other = copy.deepcopy(t)

        self.assertTrue(elements_equal(t, t_other))

    def test_unequal(self):
        t = etree.parse(self.ifd).getroot()
        t[:] = sorted(t, key=lambda c: c.tag)
        t_other = copy.deepcopy(t)
        # remove a single child element (here the first one)
        t_other[:] = t[1:]

        self.assertFalse(elements_equal(t, t_other))

    def test_equal_with_exclude_recursive(self):
        t = etree.parse(self.ifd).getroot()
        t[:] = sorted(t, key=lambda c: c.tag)
        t_other = copy.deepcopy(t)
        # manipulate a single child element
        t_other[1][0].text = 'FOO'

        self.assertTrue(
            elements_equal(
                t, t_other,
                exclude_tags=['{}{}'.format(ns, 'Description') for ns in
                              settings.STATIONXML_NAMESPACES],
                recursive=True))

    def test_unequal_with_exclude_nonrecursive(self):
        t = etree.parse(self.ifd).getroot()
        t[:] = sorted(t, key=lambda c: c.tag)
        t_other = copy.deepcopy(t)
        # manipulate a single child element
        t_other[1][0].text = 'FOO'

        self.assertFalse(
            elements_equal(
                t, t_other,
                exclude_tags=['{}{}'.format(ns, 'Description') for ns in
                              settings.STATIONXML_NAMESPACES],
                recursive=False))


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
