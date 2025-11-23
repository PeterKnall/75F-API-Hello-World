from unittest import TestCase
import Tools.TextTools as TextTools


class TestTextTools(TestCase):

##########

    def test_remove_building_equip_text___with_hyphen(self):
        test_string = "Canal Place-buildingEquip"
        expected_string = "Canal Place"
        self.assertEqual(expected_string, TextTools.TextTools.remove_building_equip_text(test_string))

    def test_remove_building_equip_text___without_hyphen(self):
        test_string = "Canal Place buildingEquip"
        expected_string = "Canal Place buildingEquip"
        self.assertEqual(expected_string, TextTools.TextTools.remove_building_equip_text(test_string))

    def test_remove_building_equip_text___with_None(self):
        test_string = None
        self.assertRaises(Exception, TextTools.TextTools.remove_building_equip_text, test_string)

##########

    def test_remove_type_information_text___normal(self):
        test_string = "r:2f279255-a859-4a2d-974e-1dfcb5f0c627"
        expected_string = "2f279255-a859-4a2d-974e-1dfcb5f0c627"
        self.assertEqual(expected_string, TextTools.TextTools.remove_type_information_text(test_string))

    def test_remove_type_information_text___with_colon_not_second_character(self):
        test_string = "rr:2f279255-a859-4a2d-974e-1dfcb5f0c62"
        self.assertRaises(Exception, TextTools.TextTools.remove_type_information_text, test_string)

    def test_remove_type_information_text___with_None(self):
        test_string = None
        self.assertRaises(Exception, TextTools.TextTools.remove_type_information_text, test_string)

    def test_remove_type_information_text___only_2_characters(self):
        test_string = "r:"
        self.assertRaises(Exception, TextTools.TextTools.remove_type_information_text, test_string)

    def test_remove_type_information_text___with_37_characters(self):
        test_string = "r:2f279255-a859-4a2d-974e-1dfcb5f0c62"
        self.assertRaises(Exception, TextTools.TextTools.remove_type_information_text, test_string)

    def test_remove_type_information_text___with_39_characters(self):
        test_string = "r:2f279255-a859-4a2d-974e-1dfcb5f0c627x"
        self.assertRaises(Exception, TextTools.TextTools.remove_type_information_text, test_string)

##########

    def test_get_float_from_string___float_value_only(self):
        test_string = "123.4"
        expected_value = 123.4
        self.assertEqual(expected_value, TextTools.TextTools.get_float_from_string(test_string))

    def test_get_float_from_string___float_value_with_text(self):
        test_string = "abc123.4def"
        expected_value = 123.4
        self.assertEqual(expected_value, TextTools.TextTools.get_float_from_string(test_string))

    def test_get_float_from_string___float_value_no_float_value(self):
        test_string = "abc def"
        expected_value = -998
        self.assertEqual(expected_value, TextTools.TextTools.get_float_from_string(test_string))

    def test_get_float_from_string___float_value_with_text_and_exponent(self):
        test_string = "abc 123.4E127 def"
        expected_value = 123.4E127
        self.assertEqual(expected_value, TextTools.TextTools.get_float_from_string(test_string))

    def test_get_float_from_string___with_None(self):
        test_string = None
        self.assertRaises(Exception, TextTools.TextTools.get_float_from_string, test_string)

##########

    def test_get_query_string___with_empty_tag_list(self):
        string1 = "siteId"
        string2 = "<site_id>"
        string3 = "domainName"
        string4 = []
        pass


    def test_get_query_string___first_argument_is_None(self):
        string1 = None
        string2 = "don't care"
        string3 = "don't care"
        string4 = "don't care"
        self.assertRaises(Exception, TextTools.TextTools.get_query_string, string1, string2, string3, string4)

    def test_get_query_string___second_argument_is_None(self):
        string1 = "don't care"
        string2 = None
        string3 = "don't care"
        string4 = "don't care"
        self.assertRaises(Exception, TextTools.TextTools.get_query_string, string1, string2, string3, string4)

    def test_get_query_string___third_argument_is_None(self):
        string1 = "don't care"
        string2 = "don't care"
        string3 = None
        string4 = "don't care"
        self.assertRaises(Exception, TextTools.TextTools.get_query_string, string1, string2, string3, string4)

    def test_get_query_string___fourth_argument_is_None(self):
        string1 = "don't care"
        string2 = "don't care"
        string3 = "don't care"
        string4 = None
        self.assertRaises(Exception, TextTools.TextTools.get_query_string, string1, string2, string3, string4)